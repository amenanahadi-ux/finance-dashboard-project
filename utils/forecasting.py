import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

def prepare_forecasting_data(df: pd.DataFrame):
    """
    Groups transactions by month, aggregates expenses, and builds features for training.
    """
    expense_df = df[df["Transaction Type"] == "Expense"].copy()
    if expense_df.empty:
        return pd.DataFrame()

    # Aggregate by Month-Year
    expense_df["Month_Start"] = expense_df["Date"].dt.to_period("M").dt.to_timestamp()
    monthly = expense_df.groupby("Month_Start")["Amount"].sum().reset_index()
    monthly = monthly.sort_values(by="Month_Start").reset_index(drop=True)
    monthly.rename(columns={"Amount": "Expense"}, inplace=True)

    # Check data points
    if len(monthly) < 4:
        # Not enough data points to create lag features and train models
        return monthly

    # Feature Engineering
    monthly["Month"] = monthly["Month_Start"].dt.month
    monthly["Year"] = monthly["Month_Start"].dt.year
    
    # Lags
    monthly["Lag_1"] = monthly["Expense"].shift(1)
    monthly["Lag_2"] = monthly["Expense"].shift(2)
    monthly["Lag_3"] = monthly["Expense"].shift(3)
    
    # Rolling Metrics (using previous months to avoid data leakage)
    monthly["Rolling_Mean_3M"] = (monthly["Lag_1"] + monthly["Lag_2"] + monthly["Lag_3"]) / 3.0
    monthly["Expense_Growth"] = (monthly["Lag_1"] - monthly["Lag_2"]) / (monthly["Lag_2"] + 1e-5) # Avoid division by zero

    # Drop NaNs created by shifts
    monthly_features = monthly.dropna().reset_index(drop=True)
    return monthly_features

def train_and_evaluate_models(df_features: pd.DataFrame, models_dir="/Users/amenanahadi/Downloads/fd proj/models"):
    """
    Trains Linear Regression and Random Forest models to predict expenses.
    Evaluates them using a train/test split.
    """
    os.makedirs(models_dir, exist_ok=True)
    
    if len(df_features) < 3:
        return {
            "success": False,
            "message": "Insufficient data to train and evaluate models. At least 6 months of historical data are required to generate lag features."
        }

    # Features and Target
    feature_cols = ["Month", "Year", "Lag_1", "Lag_2", "Rolling_Mean_3M", "Expense_Growth"]
    X = df_features[feature_cols]
    y = df_features["Expense"]

    # Sequential split for time series: train on all except the last month, test on last month
    # If we have larger datasets, say > 12 points, we can test on last 3 months
    test_size = 2 if len(df_features) >= 10 else 1
    
    X_train, X_test = X.iloc[:-test_size], X.iloc[-test_size:]
    y_train, y_test = y.iloc[:-test_size], y.iloc[-test_size:]

    # Model 1: Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred_test = lr_model.predict(X_test)
    lr_pred_train = lr_model.predict(X_train)

    # Model 2: Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred_test = rf_model.predict(X_test)
    rf_pred_train = rf_model.predict(X_train)

    # Evaluate on Test Set
    metrics = {}
    
    # Linear Regression metrics
    lr_mae = mean_absolute_error(y_test, lr_pred_test)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred_test))
    # R2 requires at least 2 points, otherwise it returns NaN or 1.0/0.0. Let's safeguard R2.
    if len(y_test) > 1:
        lr_r2 = r2_score(y_test, lr_pred_test)
        rf_r2 = r2_score(y_test, rf_pred_test)
    else:
        # Calculate pseudo R2 or default to 1 - MAE / Mean(y_test)
        lr_r2 = 1.0 - (lr_mae / (y_test.mean() + 1e-5))
        rf_r2 = 1.0 - (mean_absolute_error(y_test, rf_pred_test) / (y_test.mean() + 1e-5))

    rf_mae = mean_absolute_error(y_test, rf_pred_test)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred_test))

    metrics["lr"] = {"MAE": lr_mae, "RMSE": lr_rmse, "R2": lr_r2}
    metrics["rf"] = {"MAE": rf_mae, "RMSE": rf_rmse, "R2": rf_r2}

    # Decide best model based on MAE (lower is better)
    best_model_name = "Linear Regression" if lr_mae <= rf_mae else "Random Forest"
    best_model = lr_model if lr_mae <= rf_mae else rf_model

    # Save models
    joblib.dump(lr_model, os.path.join(models_dir, "linear_regression.joblib"))
    joblib.dump(rf_model, os.path.join(models_dir, "random_forest.joblib"))

    # Generate predictions on all available features for comparison plotting
    df_compare = df_features.copy()
    
    # Combined prediction arrays
    lr_all_preds = lr_model.predict(X)
    rf_all_preds = rf_model.predict(X)
    
    df_compare["LR_Predicted"] = lr_all_preds
    df_compare["RF_Predicted"] = rf_all_preds
    df_compare["Month_Year"] = df_compare["Month_Start"].dt.strftime("%Y-%m")

    # Forecast for the subsequent month (immediately following the last record)
    last_record = df_features.iloc[-1]
    last_date = last_record["Month_Start"]
    
    # Next month date calculation
    next_month_start = last_date + pd.DateOffset(months=1)
    
    # Predict next month features
    next_month_num = next_month_start.month
    next_month_year = next_month_start.year
    next_lag1 = last_record["Expense"]
    next_lag2 = last_record["Lag_1"]
    next_lag3 = last_record["Lag_2"]
    next_rolling = (next_lag1 + next_lag2 + next_lag3) / 3.0
    next_growth = (next_lag1 - next_lag2) / (next_lag2 + 1e-5)

    next_features = pd.DataFrame([{
        "Month": next_month_num,
        "Year": next_month_year,
        "Lag_1": next_lag1,
        "Lag_2": next_lag2,
        "Rolling_Mean_3M": next_rolling,
        "Expense_Growth": next_growth
    }])

    lr_forecast = lr_model.predict(next_features[feature_cols])[0]
    rf_forecast = rf_model.predict(next_features[feature_cols])[0]

    return {
        "success": True,
        "metrics": metrics,
        "best_model_name": best_model_name,
        "lr_forecast": lr_forecast,
        "rf_forecast": rf_forecast,
        "comparison_df": df_compare,
        "next_month": next_month_start.strftime("%B %Y"),
        "next_month_features": next_features
    }
