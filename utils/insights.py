import pandas as pd
import numpy as np

def generate_financial_insights(df: pd.DataFrame):
    """
    Programmatically generates actionable financial insights from transaction data.
    """
    insights = []
    
    if df.empty:
        return ["No transaction data available to generate insights."]

    expense_df = df[df["Transaction Type"] == "Expense"].copy()
    income_df = df[df["Transaction Type"] == "Income"].copy()

    total_income = income_df["Amount"].sum()
    total_expense = expense_df["Amount"].sum()
    total_savings = total_income - total_expense
    
    # 1. Savings Rate Check
    savings_rate = (total_savings / total_income * 100) if total_income > 0 else 0
    if savings_rate > 30:
        insights.append(f"🌟 **Excellent Savings Rate**: Your total savings rate is **{savings_rate:.1f}%** (₹{total_savings:,.2f}), which indicates outstanding financial health.")
    elif savings_rate > 15:
        insights.append(f"👍 **Healthy Savings Rate**: You are saving **{savings_rate:.1f}%** of your income. You are on track to build a solid emergency fund.")
    elif savings_rate > 0:
        insights.append(f"⚠️ **Low Savings Rate**: Your savings rate is **{savings_rate:.1f}%**, which is below the recommended 20% benchmark. Consider auditing discretionary expenses.")
    else:
        insights.append(f"🚨 **Negative Cash Flow**: Your expenses exceed your income by **₹{abs(total_savings):,.2f}**. You are drawing down on savings or credit.")

    # Group by Month-Year for MoM analysis
    df_temp = df.copy()
    df_temp["Month_Year"] = df_temp["Date"].dt.to_period("M")
    
    monthly_expense = df_temp[df_temp["Transaction Type"] == "Expense"].groupby("Month_Year")["Amount"].sum()
    monthly_income = df_temp[df_temp["Transaction Type"] == "Income"].groupby("Month_Year")["Amount"].sum()
    
    # 2. Month-over-Month Expense Trends
    if len(monthly_expense) >= 2:
        last_month = monthly_expense.index[-1]
        prev_month = monthly_expense.index[-2]
        
        last_val = monthly_expense.loc[last_month]
        prev_val = monthly_expense.loc[prev_month]
        
        diff = last_val - prev_val
        pct_change = (diff / prev_val * 100) if prev_val > 0 else 0
        
        last_month_name = last_month.strftime("%B %Y")
        prev_month_name = prev_month.strftime("%B")
        
        if pct_change > 10:
            insights.append(f"📈 **Expense Spike**: Overall spending in **{last_month_name}** increased by **{pct_change:.1f}%** (₹{diff:,.2f}) compared to {prev_month_name}.")
        elif pct_change < -10:
            insights.append(f"📉 **Spending Drop**: Great job! Overall spending in **{last_month_name}** decreased by **{abs(pct_change):.1f}%** (₹{abs(diff):,2f}) compared to {prev_month_name}.")
        else:
            insights.append(f"⚖️ **Stable Outflows**: Your overall monthly spending remains stable, changing by just **{pct_change:.1f}%** MoM.")

    # 3. Savings Rate Declining Check
    if len(monthly_income) >= 3:
        # Get savings rate for last 3 months
        last_3_months = monthly_income.index[-3:]
        sr_trends = []
        for m in last_3_months:
            inc = monthly_income.get(m, 0)
            exp = monthly_expense.get(m, 0)
            sr = ((inc - exp) / inc * 100) if inc > 0 else 0
            sr_trends.append(sr)
            
        if sr_trends[2] < sr_trends[1] < sr_trends[0]:
            insights.append("📉 **Savings Trend Warning**: Your savings rate has declined consecutively for the last three months. It is recommended to review recurring subscriptions or leisure costs.")

    # 4. Pareto Principle (Largest Categories)
    if not expense_df.empty:
        cat_spending = expense_df.groupby("Category")["Amount"].sum()
        top_cat = cat_spending.idxmax()
        top_cat_amount = cat_spending.max()
        top_cat_pct = (top_cat_amount / total_expense * 100) if total_expense > 0 else 0
        
        if top_cat_pct > 30:
            insights.append(f"🛍️ **Category Concentration**: The **{top_cat}** category constitutes **{top_cat_pct:.1f}%** of your total expenses (₹{top_cat_amount:,.2f}). Focusing budget cuts here will yield the largest savings.")

        # MoM spikes for individual categories
        if len(monthly_expense) >= 2:
            last_month = monthly_expense.index[-1]
            prev_month = monthly_expense.index[-2]
            
            # Category pivot by month
            cat_pivot = df_temp[df_temp["Transaction Type"] == "Expense"].pivot_table(
                index="Month_Year", columns="Category", values="Amount", aggfunc="sum"
            ).fillna(0)
            
            if last_month in cat_pivot.index and prev_month in cat_pivot.index:
                for cat in cat_pivot.columns:
                    l_val = cat_pivot.loc[last_month, cat]
                    p_val = cat_pivot.loc[prev_month, cat]
                    
                    if p_val > 500 and l_val > p_val: # Check only for significant categories
                        cat_pct = ((l_val - p_val) / p_val * 100)
                        if cat_pct >= 20:
                            insights.append(f"⚡ **Category Alert**: Spending in **{cat}** jumped by **{cat_pct:.1f}%** MoM (from ₹{p_val:,.0f} to ₹{l_val:,.0f}).")

    # 5. Outlier/Anomaly Detection (Single Transaction Outliers)
    if not expense_df.empty and len(expense_df) >= 5:
        # Detect large single transactions
        # Define outliers as transactions > mean + 2.5 * std for that category
        outliers = []
        for cat, group in expense_df.groupby("Category"):
            if len(group) >= 3:
                mean_val = group["Amount"].mean()
                std_val = group["Amount"].std()
                # If std is 0, no outlier logic
                if std_val > 0:
                    threshold = mean_val + 2.5 * std_val
                    # Filter matching rows
                    outlier_rows = group[group["Amount"] > threshold]
                    for _, r in outlier_rows.iterrows():
                        outliers.append({
                            "Date": r["Date"].strftime("%Y-%m-%d"),
                            "Category": r["Category"],
                            "Amount": r["Amount"],
                            "Description": r["Description"]
                        })
        
        # Sort outliers and display the top 2
        if outliers:
            outliers_sorted = sorted(outliers, key=lambda x: x["Amount"], reverse=True)
            for out in outliers_sorted[:2]:
                insights.append(f"🔍 **Large Transaction Detected**: A transaction of **₹{out['Amount']:,.2f}** for *'{out['Description']}'* under **{out['Category']}** on **{out['Date']}** was flagged as significantly higher than normal.")

    # 6. Budget Check & Variance (Consistency)
    # Highlight category volatility
    if not expense_df.empty:
        # Pivot category spending monthly
        cat_monthly = df_temp[df_temp["Transaction Type"] == "Expense"].pivot_table(
            index="Month_Year", columns="Category", values="Amount", aggfunc="sum"
        ).fillna(0)
        
        if len(cat_monthly) >= 3:
            # Coefficient of Variation = std / mean
            cv = cat_monthly.std() / (cat_monthly.mean() + 1e-5)
            # Volatile categories (excluding those with negligible spending)
            volatile_cats = cv[cat_monthly.mean() > 500].sort_values(ascending=False)
            stable_cats = cv[cat_monthly.mean() > 500].sort_values(ascending=True)
            
            if not volatile_cats.empty and volatile_cats.iloc[0] > 0.5:
                insights.append(f"🔄 **Volatile Category**: Your spending in **{volatile_cats.index[0]}** fluctuates heavily month-to-month (CV: {volatile_cats.iloc[0]:.2f}). Creating a fixed budget for this category is advised.")
            if not stable_cats.empty and stable_cats.iloc[0] < 0.15:
                insights.append(f"🛡️ **Predictable Category**: Your spending in **{stable_cats.index[0]}** is highly predictable (CV: {stable_cats.iloc[0]:.2f}). This is a fixed expense you can safely build your budget around.")

    return insights
