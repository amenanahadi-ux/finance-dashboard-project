# Personal Finance Analytics Dashboard

> A professional data analytics and machine learning portfolio project built using Python and Streamlit that enables users to upload financial transaction data, analyze spending habits, forecast future expenses, and generate actionable financial insights.

---

# 1. Project Overview

The Personal Finance Analytics Dashboard is an interactive web application that allows users to upload their financial transaction history in CSV or Excel format and automatically generates meaningful insights using data analytics and machine learning.

The project is designed to simulate a real-world business intelligence dashboard while remaining manageable for a second-year engineering student.

The focus is on demonstrating:

* Data Cleaning
* Exploratory Data Analysis (EDA)
* Data Visualization
* Dashboard Development
* Machine Learning
* Time Series Analysis
* Business Analytics
* Software Engineering Best Practices

---

# 2. Objectives

The project should demonstrate the complete data analytics workflow:

Raw Data
→ Cleaning
→ Analysis
→ Visualization
→ Machine Learning
→ Insights
→ Report Generation

Instead of simply predicting values, the dashboard should help users understand their financial behavior.

---

# 3. Target Users

* Students
* Working professionals
* Individuals tracking personal expenses
* Recruiters evaluating software/data analytics skills

---

# 4. Tech Stack

## Programming Language

Python 3.12+

---

## Frontend

Streamlit

---

## Data Processing

* pandas
* numpy

---

## Data Visualization

* Plotly
* matplotlib

---

## Machine Learning

scikit-learn

Algorithms:

* Linear Regression
* Random Forest Regressor

(Optional future enhancement)

* XGBoost

---

## Report Generation

ReportLab

---

## File Handling

openpyxl

---

## Model Saving

joblib

---

## Version Control

Git

GitHub

---

# 5. Project Workflow

```
User Uploads Dataset
        │
        ▼
Data Validation
        │
        ▼
Data Cleaning
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Dashboard & KPIs
        │
        ▼
Machine Learning
        │
        ▼
Forecast
        │
        ▼
Financial Insights
        │
        ▼
PDF Report
```

---

# 6. Folder Structure

```
Personal-Finance-Dashboard/

│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── sample_data/
│
├── reports/
│
├── screenshots/
│
├── assets/
│
├── models/
│
├── utils/
│   ├── cleaning.py
│   ├── analytics.py
│   ├── visualization.py
│   ├── forecasting.py
│   ├── report.py
│   ├── insights.py
│   └── helpers.py
│
└── notebooks/
```

---

# 7. Expected Dataset

Required columns:

| Column           | Type             |
| ---------------- | ---------------- |
| Date             | Date             |
| Description      | String           |
| Category         | String           |
| Amount           | Float            |
| Transaction Type | Income / Expense |

Example:

| Date       | Description | Category  | Amount | Type    |
| ---------- | ----------- | --------- | ------ | ------- |
| 2025-01-05 | Salary      | Income    | 50000  | Income  |
| 2025-01-08 | Starbucks   | Food      | 420    | Expense |
| 2025-01-12 | Uber        | Transport | 180    | Expense |

---

# 8. Features

## Feature 1 — File Upload

Supported formats:

* CSV
* XLSX

Requirements

* Validate uploaded file
* Display preview
* Display row count
* Display column count
* Detect invalid formats

---

## Feature 2 — Data Cleaning

Automatically perform:

### Missing Values

* Detect
* Fill where appropriate
* Display missing value summary

---

### Duplicate Removal

* Remove duplicate transactions

Display:

```
Removed 12 duplicate rows.
```

---

### Date Formatting

Convert all dates into datetime objects.

---

### Numeric Validation

Ensure Amount column contains only valid numeric values.

---

### Category Standardization

Convert

```
food
Food
FOOD
```

into

```
Food
```

---

### Cleaning Report

Display:

* Missing values fixed
* Duplicate rows removed
* Invalid entries corrected

---

# 9. Dashboard KPIs

Display large metric cards for:

## Income

Total Income

---

## Expenses

Total Expenses

---

## Net Savings

Income − Expenses

---

## Savings Rate

(Savings / Income) × 100

---

## Largest Expense Category

Example:

Shopping

---

## Highest Spending Month

Example:

March

---

## Total Transactions

Example:

2,485

---

## Average Monthly Expense

---

## Average Monthly Income

---

# 10. Exploratory Data Analysis

Generate interactive visualizations.

---

## Monthly Income vs Expenses

Line chart

---

## Spending Trend

Line chart

---

## Expenses by Category

Bar chart

---

## Expense Distribution

Pie chart

---

## Top 10 Largest Expenses

Horizontal bar chart

---

## Monthly Savings

Line chart

---

## Category-wise Spending

Stacked bar chart

---

## Daily Spending

Time-series graph

---

## Correlation Heatmap

For numerical variables.

---

# 11. Budget Planner

Allow users to define monthly budgets.

Example:

Food

₹6000

Actual

₹7100

Status

⚠ Over Budget

---

Show

* Budget
* Actual Spending
* Remaining Budget
* Percentage Used

Highlight overspending.

---

# 12. Machine Learning Module

Objective

Predict next month's total expenses.

---

## Data Preparation

Feature Engineering

Examples:

Month

Year

Previous Month Expense

Rolling Average

Expense Growth

---

## Models

Train

### Linear Regression

Evaluate

---

### Random Forest Regressor

Evaluate

---

## Metrics

Display

* MAE
* RMSE
* R² Score

Compare models.

Highlight the better-performing model.

---

## Forecast

Predict

Next Month Expense

Example

```
Expected Expense

₹43,850
```

---

## Visualization

Actual vs Predicted

Line chart

---

# 13. Financial Insights

Automatically generate meaningful insights.

Examples

* Food spending increased 18% compared to last month.
* Shopping accounts for 42% of total expenses.
* Transportation costs decreased.
* Average monthly savings is ₹14,300.
* Highest expense occurred in March.
* Utility bills remain consistent.
* Spending trend is increasing.
* Savings rate has declined over the last three months.

These insights should be generated programmatically without using an AI model.

---

# 14. PDF Report

Generate a downloadable report containing

* Dashboard Summary
* KPIs
* Charts
* Financial Insights
* Model Performance
* Forecast
* Budget Analysis

Include date generated.

---

# 15. User Interface

Sidebar Navigation

* Upload Data
* Dashboard
* Analytics
* Budget
* Forecast
* Reports

---

Main Dashboard

Professional layout

Large KPI cards

Interactive charts

Modern spacing

Responsive design

---

# 16. Error Handling

Handle gracefully:

* Empty dataset
* Missing required columns
* Invalid dates
* Corrupted files
* Non-numeric amounts

Display user-friendly error messages.

---

# 17. Code Quality Requirements

* Follow PEP 8
* Use modular architecture
* Use reusable functions
* Use descriptive variable names
* Include type hints where appropriate
* Handle exceptions
* Keep functions focused on a single responsibility

---

# 18. Future Enhancements

Potential improvements:

* User authentication
* Multiple user accounts
* Cloud database
* Automatic transaction categorization using NLP
* AI-powered financial assistant
* Investment portfolio analysis
* Goal-based savings tracker
* Email monthly reports
* Expense anomaly detection
* Mobile-responsive UI
* Dark mode
* Currency conversion
* OCR receipt scanning

---

# 19. GitHub Deliverables

The repository should include:

* Complete source code
* requirements.txt
* README.md
* Sample dataset
* Screenshots
* Project architecture diagram
* Installation guide
* Usage guide
* License
* Git commit history

---

# 20. Learning Outcomes

By completing this project, the developer should gain practical experience in:

* Python programming
* Data preprocessing
* Exploratory Data Analysis (EDA)
* Interactive dashboard development
* Data visualization
* Machine learning model development
* Model evaluation
* Time-series forecasting fundamentals
* Financial data analysis
* Git and GitHub workflows
* Writing maintainable, modular code
* Documentation and portfolio presentation

---

# 21. Suggested Development Milestones

### Milestone 1

Project setup and repository structure

### Milestone 2

File upload and validation

### Milestone 3

Data cleaning module

### Milestone 4

Dashboard KPIs

### Milestone 5

Interactive visualizations

### Milestone 6

Budget planning module

### Milestone 7

Machine learning forecasting

### Milestone 8

Financial insights engine

### Milestone 9

PDF report generation

### Milestone 10

UI polishing, testing, documentation, and deployment

---

# 22. Expected Outcome

The final application should resemble a lightweight business intelligence platform capable of transforming raw financial transaction data into meaningful visualizations, predictive analytics, and actionable financial insights.

The project should emphasize clean software architecture, intuitive user experience, and practical analytics over unnecessary complexity, making it suitable as a portfolio project for software engineering, data analytics, and machine learning internship applications.
