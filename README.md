# WealthFlow: Personal Finance Analytics Dashboard

A professional data analytics and machine learning portfolio project built using Python and Streamlit that enables users to upload financial transaction data, analyze spending habits, forecast future expenses, and generate actionable financial insights.

---

## 🚀 Key Features

- **📁 Automated Data Cleaning & Validation**: Standardizes category casing, strips trailing spaces, converts dates to datetime objects, removes duplicate transactions, coerces amounts to numeric values, and handles missing categories.
- **📊 Executive KPI Overview**: Displays real-time calculations for Total Income, Total Expenses, Net Savings, Savings Rate, Top Cost Centers, and Average Monthly Cashflows.
- **📈 High-Fidelity Visualizations**: Interactive graphs built with custom-styled Plotly templates, including:
  - Monthly Cashflows (Income vs Expenses)
  - Savings Accumulation Trend
  - Category Share Distributions (Donut/Bar)
  - Category Spending changes over time (Stacked Bar)
  - Daily outflow line plots with 7-Day Moving Averages
  - Statistical Correlation Heatmap
- **🎯 Dynamic Budget Planner**: Set category limit thresholds, track actual spending via visual progress bars, and flag budget overruns instantly.
- **🔮 ML Forecasting Engine**: Automatically trains **Linear Regression** and **Random Forest Regressor** models on your historical monthly aggregates, compares testing metrics ($MAE$, $RMSE$, $R^2$), and forecasts next month's total expenses.
- **📄 Downloadable PDF Statement**: A professional financial statement containing compiled KPIs, programmatic insights, budget variance tables, and predictive analysis metrics.

---

## 🛠️ Tech Stack

- **Frontend Application**: [Streamlit](https://streamlit.io/)
- **Data Engineering**: Pandas, Numpy, Openpyxl
- **Interactive Visualizations**: Plotly Express, Plotly Graph Objects, Matplotlib
- **Machine Learning Projections**: Scikit-learn (Linear Regression, Random Forest Regressor)
- **Model Storage**: Joblib
- **Statement Compilation**: ReportLab PDF library

---

## 🏗️ Project Architecture

```
Personal-Finance-Dashboard/
│
├── app.py                      # Main Streamlit frontend interface & page router
├── requirements.txt            # Dependency list
├── LICENSE                     # MIT License terms
├── README.md                   # Documentation
│
├── sample_data/                # Transaction templates & generators
│   ├── generate_sample.py      # Random transaction history generator script
│   ├── sample_transactions.csv  # 24-Month realistic mock history (CSV)
│   └── sample_transactions.xlsx # 24-Month realistic mock history (Excel)
│
├── utils/                      # Modular backend engines
│   ├── cleaning.py             # Data loader, cleaner and validator
│   ├── analytics.py            # Financial aggregates & KPI computations
│   ├── visualization.py        # Customized interactive Plotly charts
│   ├── forecasting.py          # ML data preprocessor, trainer & forecaster
│   ├── insights.py             # Rule-based analytical insights parser
│   ├── report.py               # PDF statement report compiler
│   └── helpers.py              # Typography & CSS themes and helpers
│
├── models/                     # Cache directory for trained models
├── reports/                    # Target folder for generated PDF statements
└── screenshots/                # Application preview assets
```

---

## ⚙️ Installation & Setup

Follow these steps to run WealthFlow locally on your machine:

### 1. Clone & Enter Repository
```bash
git clone https://github.com/yourusername/Personal-Finance-Dashboard.git
cd Personal-Finance-Dashboard
```

### 2. Configure Virtual Environment
We recommend setting up a virtual environment to manage dependencies cleanly:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Package Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Boot up Streamlit Application
```bash
streamlit run app.py
```
The dashboard should load automatically in your default browser at `http://localhost:8501`.

---

## 💡 How to Use

1. **Upload Transaction History**:
   - Navigate to the **Upload Data** tab in the sidebar.
   - Upload your own transaction CSV or Excel worksheet. The file must contain the fields: `Date`, `Description`, `Category`, `Amount`, and `Type` (or equivalents).
   - Alternatively, click the **💡 Load Sample Dataset** button in the sidebar to instant-launch the app using our generated 2-year sample history.
2. **Review Dashboard & Deep Analytics**:
   - Inspect the top metric cards to understand your net savings and savings rate.
   - Use the **Deep Analytics** tab to view category shares, rolling daily averages, and correlation matrices.
3. **Establish Category Budgets**:
   - Go to the **Budget Planner** page.
   - Define custom spending ceilings for each category on the left side, and watch the progress bars update in real-time. Overspent categories will automatically display red alerts.
4. **Train Projections & Download Statements**:
   - Check the **Expense Forecast** tab to inspect the fitted trends of the models.
   - Review $MAE$ and $R^2$ scores to see why WealthFlow selects a specific model for your forecast.
   - Compile a PDF printout in the **Export Report** tab and download your report statement with a single click.

---

## 🔮 Machine Learning Details

WealthFlow uses historical transactional history to group outflows by calendar month. 

### Feature Engineering:
- **Lags**: `Lag_1` (Last month's total expense), `Lag_2` (2 months ago), `Lag_3` (3 months ago).
- **Rolling Metric**: `Rolling_Mean_3M` (Average of the last 3 months).
- **Growth Velocity**: `Expense_Growth` (Rate of change of spending between last month and 2 months ago).

### Models Evaluated:
1. **Ordinary Least Squares (Linear Regression)**: Extrapolates long-term linear directions.
2. **Random Forest Regressor**: Captures non-linear dynamics, seasonality spikes, and volatility variations.

The dashboard split-evaluates models against the most recent month(s), choosing the model with the lowest Mean Absolute Error ($MAE$) to run the future projection.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
