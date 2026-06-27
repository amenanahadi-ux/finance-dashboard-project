import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import plotly.graph_objects as go

# Import modular backend components
from utils.cleaning import clean_transaction_data
from utils.analytics import (
    calculate_kpis, get_monthly_summary, get_category_spending,
    get_top_expenses, get_category_monthly_spending, get_daily_spending,
    get_correlation_data
)
from utils.visualization import (
    plot_income_vs_expense, plot_spending_trend, plot_expenses_by_category,
    plot_expense_distribution, plot_top_expenses, plot_monthly_savings,
    plot_category_monthly_spending, plot_daily_spending, plot_correlation_heatmap,
    COLORS, apply_premium_layout
)
from utils.forecasting import prepare_forecasting_data, train_and_evaluate_models
from utils.insights import generate_financial_insights
from utils.report import generate_pdf_report
from utils.helpers import inject_custom_css, format_currency

# Page Config
st.set_page_config(
    page_title="Personal Finance Analytics Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "df" not in st.session_state:
    st.session_state["df"] = None
if "cleaning_summary" not in st.session_state:
    st.session_state["cleaning_summary"] = None
if "budgets" not in st.session_state:
    st.session_state["budgets"] = {}
if "ml_results" not in st.session_state:
    st.session_state["ml_results"] = None
if "kpis" not in st.session_state:
    st.session_state["kpis"] = None
if "insights" not in st.session_state:
    st.session_state["insights"] = []
if "file_name" not in st.session_state:
    st.session_state["file_name"] = ""

# Inject custom CSS
inject_custom_css()

# Helper function to generate sample data if needed
def check_or_generate_sample_data():
    csv_path = "/Users/amenanahadi/Downloads/fd proj/sample_data/sample_transactions.csv"
    xlsx_path = "/Users/amenanahadi/Downloads/fd proj/sample_data/sample_transactions.xlsx"
    if not os.path.exists(csv_path):
        from sample_data.generate_sample import generate_sample_data
        generate_sample_data(csv_path, xlsx_path)
    return csv_path

def recompute_derived_states():
    """
    Recalculates KPIs, insights, and forecast models based on current st.session_state["df"].
    """
    df = st.session_state["df"]
    if df is not None and not df.empty:
        # Calculate KPIs
        st.session_state["kpis"] = calculate_kpis(df)
        # Generate Insights
        st.session_state["insights"] = generate_financial_insights(df)
        
        # Prepare & Train ML Models
        features_df = prepare_forecasting_data(df)
        if not features_df.empty:
            ml_res = train_and_evaluate_models(features_df)
            st.session_state["ml_results"] = ml_res
        else:
            st.session_state["ml_results"] = {
                "success": False,
                "message": "Insufficient data to train models. Requires at least 4 unique months of transaction data."
            }
            
        # Initialize default budgets for categories if empty
        expense_df = df[df["Transaction Type"] == "Expense"]
        if not expense_df.empty:
            categories = expense_df["Category"].unique()
            for cat in categories:
                if cat not in st.session_state["budgets"]:
                    # Set default budget as 1.2x of the average monthly spend in that category
                    cat_monthly = expense_df[expense_df["Category"] == cat].groupby(expense_df["Date"].dt.to_period("M"))["Amount"].sum()
                    avg_spend = cat_monthly.mean() if not cat_monthly.empty else 0.0
                    # Standardize budget to nearest 500
                    st.session_state["budgets"][cat] = float(max(500, round(avg_spend * 1.2 / 500) * 500))

# Sidebar layout
st.sidebar.markdown("<h2 class='gradient-text'>WealthFlow</h2>", unsafe_allow_html=True)
st.sidebar.caption("Personal Finance Intelligence Dashboard")
st.sidebar.markdown("---")

# Data Info in Sidebar
if st.session_state["df"] is not None:
    st.sidebar.success(f"Loaded: {st.session_state['file_name']}")
    st.sidebar.metric("Transactions Cached", f"{len(st.session_state['df'])}")
    if st.sidebar.button("Clear Dataset", use_container_width=True):
        st.session_state["df"] = None
        st.session_state["cleaning_summary"] = None
        st.session_state["budgets"] = {}
        st.session_state["ml_results"] = None
        st.session_state["kpis"] = None
        st.session_state["insights"] = []
        st.session_state["file_name"] = ""
        st.rerun()
else:
    st.sidebar.info("No transaction data loaded.")
    if st.sidebar.button("💡 Load Sample Dataset", use_container_width=True):
        sample_path = check_or_generate_sample_data()
        raw_df = pd.read_csv(sample_path)
        df_clean, summary = clean_transaction_data(raw_df)
        st.session_state["df"] = df_clean
        st.session_state["cleaning_summary"] = summary
        st.session_state["file_name"] = "sample_transactions.csv"
        recompute_derived_states()
        st.success("Sample dataset loaded successfully!")
        st.rerun()

st.sidebar.markdown("---")

# Navigation Menu
navigation = st.sidebar.radio(
    "Navigate App Pages",
    [
        "📁 Upload Data",
        "📊 Dashboard Overview",
        "📈 Deep Analytics",
        "🎯 Budget Planner",
        "🔮 Expense Forecast",
        "📄 Export Report"
    ]
)

# Render Pages
if navigation == "📁 Upload Data":
    st.markdown("<h1 class='gradient-text'>Upload Financial History</h1>", unsafe_allow_html=True)
    st.markdown("Upload your monthly transactional records in CSV or XLSX format to automatically clean and analyze your finances.")
    
    col_upload, col_sample = st.columns([3, 1])
    
    with col_upload:
        uploaded_file = st.file_uploader(
            "Choose a transaction history CSV or Excel file",
            type=["csv", "xlsx"],
            help="File must contain columns like Date, Description, Category, Amount, Type"
        )
        
        if uploaded_file is not None:
            # Load file
            try:
                if uploaded_file.name.endswith(".csv"):
                    raw_df = pd.read_csv(uploaded_file)
                else:
                    raw_df = pd.read_excel(uploaded_file)
                
                st.session_state["file_name"] = uploaded_file.name
                
                # Perform Data Cleaning
                df_clean, summary = clean_transaction_data(raw_df)
                
                if summary["success"]:
                    st.session_state["df"] = df_clean
                    st.session_state["cleaning_summary"] = summary
                    recompute_derived_states()
                    
                    st.success("File uploaded, cleaned, and compiled successfully!")
                else:
                    st.error("Data Validation Error:")
                    for err in summary["errors"]:
                        st.write(f"- {err}")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

    with col_sample:
        st.markdown("### Test Dataset")
        st.write("Don't have a dataset ready? Generate and load a highly realistic 2-year sample history:")
        if st.button("Generate & Load Sample", type="primary", use_container_width=True):
            sample_path = check_or_generate_sample_data()
            raw_df = pd.read_csv(sample_path)
            df_clean, summary = clean_transaction_data(raw_df)
            st.session_state["df"] = df_clean
            st.session_state["cleaning_summary"] = summary
            st.session_state["file_name"] = "sample_transactions.csv"
            recompute_derived_states()
            st.success("Loaded Sample transactions!")
            st.rerun()

    # If data is loaded, show cleaning report and data preview
    if st.session_state["df"] is not None and st.session_state["cleaning_summary"] is not None:
        summary = st.session_state["cleaning_summary"]
        
        st.markdown("### 🧹 Data Cleaning Report")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Initial Row Count", summary["initial_rows"])
        with col2:
            st.metric("Cleaned Row Count", summary["final_rows"])
        with col3:
            st.metric("Duplicates Removed", summary["duplicates_removed"])
        with col4:
            st.metric("Missing Categories Fixed", summary["missing_categories_filled"])
        with col5:
            st.metric("Invalid Entries Dropped", summary["invalid_amounts_dropped"] + summary["invalid_dates_dropped"])

        st.markdown("### 📋 Cleaned Dataset Preview")
        st.dataframe(st.session_state["df"].head(100), use_container_width=True)

    else:
        st.info("Waiting for data to be uploaded. Use the file uploader or load the sample dataset to proceed.")

elif st.session_state["df"] is None:
    # Fallback page if user navigates without loading data
    st.warning("⚠️ No Dataset Loaded")
    st.info("Please navigate to the **Upload Data** tab to upload a file or generate sample transaction history.")
    
    # Showcase some premium UI layouts
    st.markdown("---")
    st.subheader("Features available in the Dashboard:")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        st.markdown("""
        **📊 Executive Analytics Dashboard**
        - Real-time calculations of Net Position, Savings Rates, and high-level KPIs.
        - Month-over-Month cashflow comparisons.
        """)
    with f_col2:
        st.markdown("""
        **🎯 Flexible Budget Tracking**
        - Define budgets by category and monitor your actual outflows in real-time.
        - Highlight variance and alert overspending.
        """)
    with f_col3:
        st.markdown("""
        **🔮 Machine Learning Forecasts**
        - Linear Regression and Random Forest training.
        - Automatic accuracy evaluation.
        - 1-Month Out Expense Forecast.
        """)

else:
    # All dashboard views expect active dataset
    df = st.session_state["df"]
    kpis = st.session_state["kpis"]
    insights = st.session_state["insights"]
    
    if navigation == "📊 Dashboard Overview":
        st.markdown("<h1 class='gradient-text'>Financial Overview</h1>", unsafe_allow_html=True)
        st.markdown("A bird's eye view of your cash flow, savings rate, and crucial observations.")
        st.markdown("---")

        # 3 Key Metric Blocks
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Cash Inflow</div>
                    <div class="kpi-value">{format_currency(kpis['total_income'])}</div>
                    <div class="kpi-subtitle">Income received in dataset</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        with kpi_col2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Expenses</div>
                    <div class="kpi-value">{format_currency(kpis['total_expense'])}</div>
                    <div class="kpi-subtitle">Combined outflows</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        with kpi_col3:
            net_color = "#2ecc71" if kpis['net_savings'] >= 0 else "#e74c3c"
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Net Savings</div>
                    <div class="kpi-value" style="background: linear-gradient(to right, {net_color}, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{format_currency(kpis['net_savings'])}</div>
                    <div class="kpi-subtitle">Net cash position</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        with kpi_col4:
            rate_color = "#2ecc71" if kpis['savings_rate'] >= 20 else ("#f1c40f" if kpis['savings_rate'] >= 10 else "#e74c3c")
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Savings Rate</div>
                    <div class="kpi-value" style="background: linear-gradient(to right, {rate_color}, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{kpis['savings_rate']:.1f}%</div>
                    <div class="kpi-subtitle">Net savings / Gross income</div>
                </div>
                """, 
                unsafe_allow_html=True
            )

        st.markdown("<br/>", unsafe_allow_html=True)

        # Split: Monthly Trend and Key Insights List
        col_chart, col_insights = st.columns([5, 3])
        
        with col_chart:
            st.markdown("### 📊 Monthly Income vs Expenses")
            monthly_summary = get_monthly_summary(df)
            fig_inc_exp = plot_income_vs_expense(monthly_summary)
            st.plotly_chart(fig_inc_exp, use_container_width=True)

            st.markdown("### 📈 Net Savings Path")
            fig_savings = plot_monthly_savings(monthly_summary)
            st.plotly_chart(fig_savings, use_container_width=True)

        with col_insights:
            st.markdown("### 💡 Financial Observations")
            for ins in insights:
                st.markdown(ins)
            
            # Showcase some average stats
            st.markdown("---")
            st.markdown("### 🧮 Cash Flow Averages")
            st.write(f"- **Avg Monthly Income:** {format_currency(kpis['avg_monthly_income'])}")
            st.write(f"- **Avg Monthly Expenses:** {format_currency(kpis['avg_monthly_expense'])}")
            st.write(f"- **Top Cost Center:** `{kpis['largest_expense_category']}`")
            st.write(f"- **Highest Month:** `{kpis['highest_spending_month']}`")

    elif navigation == "📈 Deep Analytics":
        st.markdown("<h1 class='gradient-text'>Deep-Dive Analytics</h1>", unsafe_allow_html=True)
        st.markdown("Detailed charts exploring Category breakdowns, Spending Trends, and Feature Correlation.")
        st.markdown("---")

        tab_categories, tab_daily, tab_correlation = st.tabs([
            "🛍️ Category Breakdowns",
            "📅 Daily Outflow Trends",
            "🧮 Statistical Correlations"
        ])

        with tab_categories:
            col_cat_bar, col_cat_donut = st.columns(2)
            
            cat_df = get_category_spending(df)
            
            with col_cat_bar:
                st.markdown("### Category Spending totals")
                fig_cat_bar = plot_expenses_by_category(cat_df)
                st.plotly_chart(fig_cat_bar, use_container_width=True)
                
            with col_cat_donut:
                st.markdown("### Expense Share Distribution")
                fig_cat_donut = plot_expense_distribution(cat_df)
                st.plotly_chart(fig_cat_donut, use_container_width=True)

            st.markdown("---")
            st.markdown("### Category spending changes over time")
            cat_monthly = get_category_monthly_spending(df)
            if not cat_monthly.empty:
                fig_cat_monthly = plot_category_monthly_spending(cat_monthly)
                st.plotly_chart(fig_cat_monthly, use_container_width=True)

        with tab_daily:
            col_daily_chart, col_top_exp = st.columns([5, 3])
            
            with col_daily_chart:
                st.markdown("### Daily Expense Trends")
                daily_df = get_daily_spending(df)
                fig_daily = plot_daily_spending(daily_df)
                st.plotly_chart(fig_daily, use_container_width=True)
                
            with col_top_exp:
                st.markdown("### Top 10 Largest Individual Outflows")
                top_exp_df = get_top_expenses(df, 10)
                fig_top = plot_top_expenses(top_exp_df)
                st.plotly_chart(fig_top, use_container_width=True)

        with tab_correlation:
            col_heat, col_notes = st.columns([5, 3])
            
            with col_heat:
                st.markdown("### Correlation Heatmap")
                corr_df = get_correlation_data(df)
                if not corr_df.empty:
                    fig_heat = plot_correlation_heatmap(corr_df)
                    st.plotly_chart(fig_heat, use_container_width=True)
                else:
                    st.info("No numerical variables available to correlate.")
                    
            with col_notes:
                st.markdown("### Understanding the Heatmap")
                st.markdown("""
                This matrix measures the linear relationship between variables:
                - **Amount**: The absolute size of the transaction.
                - **Day**: Day of the month. Useful to identify if higher transactions occur at the start or end of months (e.g. salary deposits vs credit bills).
                - **Month/Year**: Identifies long-term seasonal or annual growths.
                - **Is_Income**: Boolean representing if transaction was positive inflow.
                
                **Key Interpretation Details:**
                - A coefficient of **1.0** indicates perfect positive correlation.
                - A coefficient of **-1.0** indicates perfect negative correlation.
                - A coefficient near **0.0** implies no linear correlation.
                """)

    elif navigation == "🎯 Budget Planner":
        st.markdown("<h1 class='gradient-text'>Budget Tracker & Planner</h1>", unsafe_allow_html=True)
        st.markdown("Set limits on categories and inspect if your outflows align with your goals.")
        st.markdown("---")

        # Layout: Setup budgets in left columns, show tracker in right column
        col_setup, col_tracker = st.columns([1, 2])
        
        expense_df = df[df["Transaction Type"] == "Expense"]
        if expense_df.empty:
            st.info("No expenses found in your dataset. Budgeting applies only to Expense records.")
        else:
            categories = sorted(expense_df["Category"].unique())
            
            with col_setup:
                st.markdown("### ⚙️ Configure Monthly Budgets")
                st.write("Update target spending thresholds for each category:")
                
                # Dynamic inputs
                for cat in categories:
                    current_budget = st.session_state["budgets"].get(cat, 1000.0)
                    st.session_state["budgets"][cat] = st.number_input(
                        f"Budget limit for {cat} (₹)",
                        min_value=0.0,
                        max_value=500000.0,
                        value=float(current_budget),
                        step=500.0
                    )
                    
            with col_tracker:
                st.markdown("### 🎯 Actual Outflows vs Budget Limits")
                
                # Fetch actual spending totals by category
                actual_spending = expense_df.groupby("Category")["Amount"].sum().to_dict()
                
                # Display individual categories
                for cat in categories:
                    limit = st.session_state["budgets"].get(cat, 0.0)
                    actual = actual_spending.get(cat, 0.0)
                    remaining = limit - actual
                    
                    if limit > 0:
                        pct_used = min(1.0, actual / limit)
                        pct_display = (actual / limit * 100)
                        
                        col_lbl, col_val = st.columns([3, 1])
                        with col_lbl:
                            st.write(f"**{cat}**")
                        with col_val:
                            if remaining < 0:
                                st.markdown(f"<span class='status-pill status-over'>Over budget (₹{abs(remaining):,.0f})</span>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<span class='status-pill status-under'>Remaining: ₹{remaining:,.0f}</span>", unsafe_allow_html=True)
                        
                        # Style progress bar dynamically based on percentage used
                        st.progress(pct_used)
                        st.caption(f"Spent: {format_currency(actual)} of {format_currency(limit)} ({pct_display:.1f}% utilized)")
                        st.markdown("<br/>", unsafe_allow_html=True)
                    else:
                        col_lbl, col_val = st.columns([3, 1])
                        with col_lbl:
                            st.write(f"**{cat}**")
                        with col_val:
                            st.markdown("<span class='status-pill status-none'>No Budget Target Set</span>", unsafe_allow_html=True)
                        st.write(f"Spent: {format_currency(actual)}")
                        st.markdown("<br/>", unsafe_allow_html=True)

    elif navigation == "🔮 Expense Forecast":
        st.markdown("<h1 class='gradient-text'>Expense Forecasting & ML Engine</h1>", unsafe_allow_html=True)
        st.markdown("We use historic spending trends to train machine learning models and forecast your total expenses for next month.")
        st.markdown("---")

        ml_results = st.session_state["ml_results"]
        
        if ml_results is not None and ml_results.get("success", False):
            # Display Forecast Card
            next_month = ml_results["next_month"]
            lr_fc = ml_results["lr_forecast"]
            rf_fc = ml_results["rf_forecast"]
            best_model = ml_results["best_model_name"]
            
            best_fc = lr_fc if best_model == "Linear Regression" else rf_fc
            
            fc_col1, fc_col2, fc_col3 = st.columns(3)
            with fc_col1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">Forecast for {next_month}</div>
                        <div class="kpi-value" style="background: linear-gradient(to right, #3498db, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{format_currency(best_fc)}</div>
                        <div class="kpi-subtitle">Based on recommended {best_model} model</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with fc_col2:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">Linear Regression Forecast</div>
                        <div class="kpi-value">{format_currency(lr_fc)}</div>
                        <div class="kpi-subtitle">Linear trend extrapolation</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with fc_col3:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">Random Forest Forecast</div>
                        <div class="kpi-value">{format_currency(rf_fc)}</div>
                        <div class="kpi-subtitle">Non-linear ensemble model</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown("<br/>", unsafe_allow_html=True)
            
            # Forecast Visuals
            st.markdown("### 📊 Historical Actuals vs Model Fit Curves")
            compare_df = ml_results["comparison_df"]
            
            # Create Plotly figure for comparison
            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(
                x=compare_df["Month_Year"],
                y=compare_df["Expense"],
                mode="lines+markers",
                name="Actual Expenses",
                line=dict(color=COLORS["expense"], width=3)
            ))
            fig_fc.add_trace(go.Scatter(
                x=compare_df["Month_Year"],
                y=compare_df["LR_Predicted"],
                mode="lines+markers",
                name="Linear Regression Fit",
                line=dict(color=COLORS["accent1"], width=2, dash="dash")
            ))
            fig_fc.add_trace(go.Scatter(
                x=compare_df["Month_Year"],
                y=compare_df["RF_Predicted"],
                mode="lines+markers",
                name="Random Forest Fit",
                line=dict(color=COLORS["savings"], width=2, dash="dot")
            ))
            
            fig_fc = apply_premium_layout(fig_fc, "Historical Fit Comparison", "Month", "Expense Total (₹)")
            st.plotly_chart(fig_fc, use_container_width=True)

            # Model Evaluation metrics
            st.markdown("### 🧮 Model Evaluation Metrics")
            metrics = ml_results["metrics"]
            
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.markdown("#### 📈 Linear Regression")
                st.write(f"- **Mean Absolute Error (MAE):** {format_currency(metrics['lr']['MAE'])}")
                st.write(f"- **Root Mean Squared Error (RMSE):** {format_currency(metrics['lr']['RMSE'])}")
                st.write(f"- **R² Coefficient of Determination:** `{metrics['lr']['R2']:.4f}`")
            with m_col2:
                st.markdown("#### 🌳 Random Forest Regressor")
                st.write(f"- **Mean Absolute Error (MAE):** {format_currency(metrics['rf']['MAE'])}")
                st.write(f"- **Root Mean Squared Error (RMSE):** {format_currency(metrics['rf']['RMSE'])}")
                st.write(f"- **R² Coefficient of Determination:** `{metrics['rf']['R2']:.4f}`")
                
            st.info(f"💡 **Recommended Model:** `{best_model}` has a lower Mean Absolute Error (MAE) on test evaluation splits, making it the most robust forecasting choice.")
        else:
            fail_msg = ml_results.get("message", "Forecasting requires at least 4 unique months of historical data to perform lag feature engineering.")
            st.warning("⚠️ Forecasting Unavailable")
            st.write(fail_msg)
            st.write("Ensure your transaction history dataset contains a sufficient timeline of monthly entries.")

    elif navigation == "📄 Export Report":
        st.markdown("<h1 class='gradient-text'>Generate PDF Statements</h1>", unsafe_allow_html=True)
        st.markdown("Export a clean, professional summary of your financial metrics, budget performance, and machine learning projections.")
        st.markdown("---")

        col_rep_info, col_rep_btn = st.columns([2, 1])
        
        with col_rep_info:
            st.write("### PDF Summary Contents:")
            st.markdown("""
            - **Executive Summary:** Income, Outflow, Savings Rates, and high-level KPIs.
            - **Observations:** Programmatic financial alerts.
            - **Budget Variance Statement:** Tabulated comparison of actual vs limit amounts.
            - **Machine Learning Projections:** Next month forecast and evaluation metrics.
            """)
            
        with col_rep_btn:
            st.markdown("### Compile & Download")
            report_name = f"WealthFlow_Statement_{datetime.now().strftime('%Y%m%d')}.pdf"
            report_path = f"/Users/amenanahadi/Downloads/fd proj/reports/{report_name}"
            
            # Button triggers generation
            if st.button("Generate Statement", type="primary", use_container_width=True):
                # Prepare ML results dict (handle None case gracefully)
                ml_res_dict = st.session_state["ml_results"] if st.session_state["ml_results"] is not None else {"success": False}
                
                # Generate PDF
                with st.spinner("Compiling statement PDF..."):
                    generate_pdf_report(
                        df=df,
                        kpis=kpis,
                        insights=insights,
                        budgets=st.session_state["budgets"],
                        ml_results=ml_res_dict,
                        output_pdf_path=report_path
                    )
                st.success("Report statement created successfully!")
                
                # Show download button
                with open(report_path, "rb") as f:
                    pdf_bytes = f.read()
                    
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=report_name,
                    mime="application/pdf",
                    use_container_width=True
                )
