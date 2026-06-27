import pandas as pd
import numpy as np

def calculate_kpis(df: pd.DataFrame):
    """
    Computes key performance indicators for the finance dashboard.
    """
    if df.empty:
        return {
            "total_income": 0.0,
            "total_expense": 0.0,
            "net_savings": 0.0,
            "savings_rate": 0.0,
            "largest_expense_category": "N/A",
            "highest_spending_month": "N/A",
            "total_transactions": 0,
            "avg_monthly_income": 0.0,
            "avg_monthly_expense": 0.0
        }

    # Filter income/expense
    income_df = df[df["Transaction Type"] == "Income"]
    expense_df = df[df["Transaction Type"] == "Expense"]

    total_income = float(income_df["Amount"].sum())
    total_expense = float(expense_df["Amount"].sum())
    net_savings = total_income - total_expense
    
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0.0
    if savings_rate < 0:
        savings_rate = 0.0 # Standardize negative savings rate as 0 or leave negative? Better display as negative or 0. Let's leave negative if net savings is negative, but usually standard is min 0 or showing negative savings rate. Let's allow negative savings rate.

    # Total transactions
    total_transactions = len(df)

    # Largest expense category
    if not expense_df.empty:
        cat_expenses = expense_df.groupby("Category")["Amount"].sum()
        largest_expense_category = cat_expenses.idxmax()
    else:
        largest_expense_category = "N/A"

    # Monthly groupings
    df_temp = df.copy()
    df_temp["Month_Year"] = df_temp["Date"].dt.strftime("%Y-%m")
    
    # Average Monthly Income/Expense
    monthly_income = df_temp[df_temp["Transaction Type"] == "Income"].groupby("Month_Year")["Amount"].sum()
    monthly_expense = df_temp[df_temp["Transaction Type"] == "Expense"].groupby("Month_Year")["Amount"].sum()
    
    # Get total unique months in df
    unique_months = df_temp["Month_Year"].nunique()
    
    avg_monthly_income = float(monthly_income.sum() / unique_months) if unique_months > 0 else 0.0
    avg_monthly_expense = float(monthly_expense.sum() / unique_months) if unique_months > 0 else 0.0

    # Highest spending month
    if not monthly_expense.empty:
        highest_month_raw = monthly_expense.idxmax() # returns "YYYY-MM"
        # Convert YYYY-MM to Month Name YYYY (e.g. "March 2025")
        try:
            highest_month_dt = pd.to_datetime(highest_month_raw + "-01")
            highest_spending_month = highest_month_dt.strftime("%B %Y")
        except Exception:
            highest_spending_month = highest_month_raw
    else:
        highest_spending_month = "N/A"

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "largest_expense_category": largest_expense_category,
        "highest_spending_month": highest_spending_month,
        "total_transactions": total_transactions,
        "avg_monthly_income": avg_monthly_income,
        "avg_monthly_expense": avg_monthly_expense
    }

def get_monthly_summary(df: pd.DataFrame):
    """
    Returns monthly aggregated income, expenses, and savings.
    """
    if df.empty:
        return pd.DataFrame(columns=["Month_Year", "Income", "Expense", "Savings"])

    df_temp = df.copy()
    df_temp["Month_Year"] = df_temp["Date"].dt.to_period("M")
    
    # Pivot table to get month-by-month Income and Expense
    pivot = df_temp.pivot_table(
        index="Month_Year",
        columns="Transaction Type",
        values="Amount",
        aggfunc="sum"
    ).fillna(0.0)

    # Ensure columns exist
    if "Income" not in pivot.columns:
        pivot["Income"] = 0.0
    if "Expense" not in pivot.columns:
        pivot["Expense"] = 0.0

    pivot["Savings"] = pivot["Income"] - pivot["Expense"]
    pivot = pivot.reset_index()
    pivot["Month_Year"] = pivot["Month_Year"].astype(str)
    return pivot

def get_category_spending(df: pd.DataFrame):
    """
    Returns expenses grouped by Category, sorted descending.
    """
    expense_df = df[df["Transaction Type"] == "Expense"]
    if expense_df.empty:
        return pd.DataFrame(columns=["Category", "Amount", "Percentage"])
    
    cat_df = expense_df.groupby("Category")["Amount"].sum().reset_index()
    cat_df = cat_df.sort_values(by="Amount", ascending=False).reset_index(drop=True)
    
    total_expense = cat_df["Amount"].sum()
    cat_df["Percentage"] = (cat_df["Amount"] / total_expense * 100).round(2)
    return cat_df

def get_top_expenses(df: pd.DataFrame, limit=10):
    """
    Returns the top N largest expense transactions.
    """
    expense_df = df[df["Transaction Type"] == "Expense"]
    if expense_df.empty:
        return pd.DataFrame(columns=["Date", "Description", "Category", "Amount"])
    
    top_df = expense_df.sort_values(by="Amount", ascending=False).head(limit)
    return top_df[["Date", "Description", "Category", "Amount"]].reset_index(drop=True)

def get_category_monthly_spending(df: pd.DataFrame):
    """
    Returns category-wise expenses grouped by Month-Year for stacked bar charts.
    """
    expense_df = df[df["Transaction Type"] == "Expense"].copy()
    if expense_df.empty:
        return pd.DataFrame()
    
    expense_df["Month_Year"] = expense_df["Date"].dt.strftime("%Y-%m")
    pivot = expense_df.pivot_table(
        index="Month_Year",
        columns="Category",
        values="Amount",
        aggfunc="sum"
    ).fillna(0.0).reset_index()
    
    return pivot

def get_daily_spending(df: pd.DataFrame):
    """
    Returns daily aggregated expenses.
    """
    expense_df = df[df["Transaction Type"] == "Expense"]
    if expense_df.empty:
        return pd.DataFrame(columns=["Date", "Amount"])
    
    daily = expense_df.groupby("Date")["Amount"].sum().reset_index()
    return daily.sort_values(by="Date").reset_index(drop=True)

def get_correlation_data(df: pd.DataFrame):
    """
    Prepares numeric variables for correlation analysis.
    Columns: Amount, Day of Month, Month, Year, Is_Income (0/1).
    """
    if df.empty:
        return pd.DataFrame()
    
    corr_df = df.copy()
    corr_df["Day"] = corr_df["Date"].dt.day
    corr_df["Month"] = corr_df["Date"].dt.month
    corr_df["Year"] = corr_df["Date"].dt.year
    corr_df["Is_Income"] = (corr_df["Transaction Type"] == "Income").astype(int)
    
    return corr_df[["Amount", "Day", "Month", "Year", "Is_Income"]].corr()
