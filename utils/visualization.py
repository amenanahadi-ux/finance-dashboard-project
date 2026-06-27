import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Premium Fintech Color Palette
COLORS = {
    "income": "#2ecc71",       # Emerald Green
    "expense": "#e74c3c",      # Coral Red
    "savings": "#3498db",      # Electric Blue
    "accent1": "#9b59b6",      # Amethyst Purple
    "accent2": "#f1c40f",      # Sunflower Yellow
    "accent3": "#1abc9c",      # Turquoise
    "accent4": "#e67e22",      # Carrot Orange
    "background": "rgba(0,0,0,0)",
    "grid": "rgba(128, 128, 128, 0.15)",
    "text": "#555"             # Automatically overridden by theme, but good fallback
}

# Dark-mode responsive text color
TEXT_COLOR = "#FFFFFF" # We can dynamically set or rely on Streamlit's default theme settings.
# Plotly figures styled with template="plotly_white" or "plotly_dark".
# Streamlit allows transparent background, so we can make layout background transparent.

def apply_premium_layout(fig, title_text, x_title="", y_title="", show_legend=True):
    """
    Applies unified premium theme styles to a Plotly figure.
    """
    fig.update_layout(
        title={
            'text': f"<b>{title_text}</b>",
            'y': 0.95,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 18, 'family': "Outfit, sans-serif"}
        },
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["background"],
        font=dict(family="Outfit, sans-serif"),
        hovermode="closest",
        margin=dict(t=80, b=40, l=40, r=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11)
        ) if show_legend else dict(visible=False),
    )
    fig.update_xaxes(
        title=x_title,
        showgrid=False,
        linecolor="rgba(128, 128, 128, 0.2)",
        linewidth=1,
        gridcolor=COLORS["grid"]
    )
    fig.update_yaxes(
        title=y_title,
        showgrid=True,
        gridcolor=COLORS["grid"],
        linecolor="rgba(128, 128, 128, 0.2)",
        linewidth=1
    )
    return fig

def plot_income_vs_expense(df_monthly: pd.DataFrame):
    """
    Creates a grouped bar chart of Monthly Income vs Expenses.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_monthly["Month_Year"],
        y=df_monthly["Income"],
        name="Income",
        marker_color=COLORS["income"],
        hovertemplate="Income: ₹%{y:,.2f}<extra></extra>"
    ))
    
    fig.add_trace(go.Bar(
        x=df_monthly["Month_Year"],
        y=df_monthly["Expense"],
        name="Expense",
        marker_color=COLORS["expense"],
        hovertemplate="Expense: ₹%{y:,.2f}<extra></extra>"
    ))

    fig = apply_premium_layout(fig, "Monthly Income vs Expenses", "Month", "Amount (₹)")
    fig.update_layout(barmode="group")
    return fig

def plot_spending_trend(df_monthly: pd.DataFrame):
    """
    Creates an area chart showing the overall spending trend month-by-month.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_monthly["Month_Year"],
        y=df_monthly["Expense"],
        mode="lines+markers",
        name="Expenses",
        line=dict(color=COLORS["expense"], width=3),
        marker=dict(size=8, symbol="circle"),
        fill="tozeroy",
        fillcolor="rgba(231, 76, 60, 0.1)",
        hovertemplate="Spent: ₹%{y:,.2f}<extra></extra>"
    ))
    
    fig = apply_premium_layout(fig, "Monthly Spending Trend", "Month", "Amount (₹)", show_legend=False)
    return fig

def plot_expenses_by_category(df_category: pd.DataFrame):
    """
    Creates a bar chart of spending by category.
    """
    fig = go.Figure()
    
    # Generate custom colors
    color_scale = [COLORS["expense"], COLORS["savings"], COLORS["accent1"], COLORS["accent2"], 
                   COLORS["accent3"], COLORS["accent4"], "#34495e", "#7f8c8d"]
    
    fig.add_trace(go.Bar(
        x=df_category["Category"],
        y=df_category["Amount"],
        marker_color=color_scale[:len(df_category)],
        hovertemplate="Category: %{x}<br>Spent: ₹%{y:,.2f}<extra></extra>"
    ))
    
    fig = apply_premium_layout(fig, "Expenses by Category", "Category", "Amount (₹)", show_legend=False)
    return fig

def plot_expense_distribution(df_category: pd.DataFrame):
    """
    Creates a premium donut chart of expense distribution by category.
    """
    color_scale = [COLORS["expense"], COLORS["savings"], COLORS["accent1"], COLORS["accent2"], 
                   COLORS["accent3"], COLORS["accent4"], "#34495e", "#7f8c8d"]
    
    fig = go.Figure(data=[go.Pie(
        labels=df_category["Category"],
        values=df_category["Amount"],
        hole=0.5,
        marker=dict(colors=color_scale),
        textinfo="percent+label",
        hovertemplate="Category: %{label}<br>Spent: ₹%{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )])
    
    fig = apply_premium_layout(fig, "Expense Distribution", show_legend=True)
    # Donut chart margins
    fig.update_layout(margin=dict(t=80, b=20, l=20, r=20))
    return fig

def plot_top_expenses(df_top: pd.DataFrame):
    """
    Creates a horizontal bar chart of the top 10 largest expense items.
    """
    # Sort for horizontal bar (largest on top)
    df_sorted = df_top.sort_values(by="Amount", ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df_sorted["Description"] + " (" + df_sorted["Category"] + ")",
        x=df_sorted["Amount"],
        orientation="h",
        marker_color=COLORS["expense"],
        hovertemplate="Description: %{y}<br>Amount: ₹%{x:,.2f}<extra></extra>"
    ))
    
    fig = apply_premium_layout(fig, "Top 10 Largest Expense Transactions", "Amount (₹)", "", show_legend=False)
    return fig

def plot_monthly_savings(df_monthly: pd.DataFrame):
    """
    Creates a line/bar chart of monthly savings.
    """
    fig = go.Figure()
    
    # Coloring bars dynamically based on positive or negative savings
    colors = [COLORS["income"] if val >= 0 else COLORS["expense"] for val in df_monthly["Savings"]]
    
    fig.add_trace(go.Bar(
        x=df_monthly["Month_Year"],
        y=df_monthly["Savings"],
        marker_color=colors,
        hovertemplate="Savings: ₹%{y:,.2f}<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=df_monthly["Month_Year"],
        y=df_monthly["Savings"],
        mode="lines+markers",
        line=dict(color=COLORS["savings"], width=2),
        hovertemplate="Savings: ₹%{y:,.2f}<extra></extra>",
        name="Savings Trend"
    ))
    
    fig = apply_premium_layout(fig, "Monthly Savings & Net Position", "Month", "Savings (₹)", show_legend=False)
    return fig

def plot_category_monthly_spending(df_cat_monthly: pd.DataFrame):
    """
    Creates a stacked bar chart showing category spending changes over time.
    """
    fig = go.Figure()
    
    categories = [col for col in df_cat_monthly.columns if col != "Month_Year"]
    color_scale = [COLORS["expense"], COLORS["savings"], COLORS["accent1"], COLORS["accent2"], 
                   COLORS["accent3"], COLORS["accent4"], "#34495e", "#7f8c8d"]
    
    for idx, cat in enumerate(categories):
        color = color_scale[idx % len(color_scale)]
        fig.add_trace(go.Bar(
            x=df_cat_monthly["Month_Year"],
            y=df_cat_monthly[cat],
            name=cat,
            marker_color=color,
            hovertemplate=f"Category: {cat}<br>Spent: ₹%{{y:,.2f}}<extra></extra>"
        ))
        
    fig = apply_premium_layout(fig, "Monthly Spending breakdown by Category", "Month", "Amount (₹)")
    fig.update_layout(barmode="stack")
    return fig

def plot_daily_spending(df_daily: pd.DataFrame):
    """
    Creates a scatter and line chart of daily spending.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_daily["Date"],
        y=df_daily["Amount"],
        mode="lines",
        name="Daily Expenses",
        line=dict(color=COLORS["expense"], width=1.5),
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Spent: ₹%{y:,.2f}<extra></extra>"
    ))
    
    # 7-day rolling average to smooth daily spikes
    df_daily["Rolling_Avg"] = df_daily["Amount"].rolling(window=7, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=df_daily["Date"],
        y=df_daily["Rolling_Avg"],
        mode="lines",
        name="7-Day Moving Avg",
        line=dict(color=COLORS["savings"], width=2.5, dash="dash"),
        hovertemplate="Rolling Avg: ₹%{y:,.2f}<extra></extra>"
    ))
    
    fig = apply_premium_layout(fig, "Daily Expenses & Rolling Average", "Date", "Amount (₹)")
    return fig

def plot_correlation_heatmap(df_corr: pd.DataFrame):
    """
    Creates an interactive Plotly heatmap showing feature correlations.
    """
    if df_corr.empty:
        return go.Figure()
        
    fig = go.Figure(data=go.Heatmap(
        z=df_corr.values,
        x=df_corr.columns,
        y=df_corr.index,
        colorscale="RdYlBu",
        zmin=-1,
        zmax=1,
        text=np.round(df_corr.values, 2),
        texttemplate="%{text}",
        hovertemplate="Correlation between %{x} and %{y}: %{z:.2f}<extra></extra>"
    ))
    
    fig = apply_premium_layout(fig, "Correlation Matrix", show_legend=False)
    fig.update_layout(margin=dict(t=80, b=40, l=80, r=40))
    return fig
