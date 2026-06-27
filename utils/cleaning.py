import pandas as pd
import numpy as np

def clean_transaction_data(df: pd.DataFrame):
    """
    Validates and cleans raw financial transaction DataFrame.
    Returns:
        tuple: (cleaned_df, cleaning_summary)
    """
    summary = {
        "success": True,
        "initial_rows": len(df),
        "final_rows": 0,
        "duplicates_removed": 0,
        "missing_categories_filled": 0,
        "invalid_amounts_dropped": 0,
        "invalid_dates_dropped": 0,
        "errors": []
    }

    if df.empty:
        summary["success"] = False
        summary["errors"].append("The uploaded file is empty.")
        return df, summary

    # Copy to avoid modifying original
    df_clean = df.copy()

    # Column Mapping (case-insensitive & synonym mapping)
    col_mapping = {}
    date_cols = ['date', 'transaction date']
    desc_cols = ['description', 'desc', 'details', 'particulars']
    cat_cols = ['category', 'cat']
    amt_cols = ['amount', 'val', 'value', 'transaction amount']
    type_cols = ['transaction type', 'type', 'type of transaction']

    # Identify columns
    for col in df_clean.columns:
        col_lower = str(col).strip().lower()
        if col_lower in date_cols:
            col_mapping[col] = "Date"
        elif col_lower in desc_cols:
            col_mapping[col] = "Description"
        elif col_lower in cat_cols:
            col_mapping[col] = "Category"
        elif col_lower in amt_cols:
            col_mapping[col] = "Amount"
        elif col_lower in type_cols:
            col_mapping[col] = "Transaction Type"

    # Rename columns
    df_clean = df_clean.rename(columns=col_mapping)

    # Check for required columns
    required_cols = ["Date", "Description", "Category", "Amount", "Transaction Type"]
    missing_cols = [col for col in required_cols if col not in df_clean.columns]
    
    if missing_cols:
        summary["success"] = False
        summary["errors"].append(f"Missing required columns: {', '.join(missing_cols)}")
        return df_clean, summary

    # Select only required columns
    df_clean = df_clean[required_cols]

    # 1. Clean Dates
    initial_count = len(df_clean)
    # Coerce invalid dates to NaT and drop them
    df_clean["Date"] = pd.to_datetime(df_clean["Date"], errors='coerce')
    df_clean = df_clean.dropna(subset=["Date"])
    summary["invalid_dates_dropped"] = initial_count - len(df_clean)

    # Sort by date
    df_clean = df_clean.sort_values(by="Date").reset_index(drop=True)

    # 2. Clean Amounts
    initial_count = len(df_clean)
    
    def clean_amount_val(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            return float(val)
        # Handle string clean-up (remove currency symbols, commas, spaces)
        val_str = str(val).strip().replace(',', '').replace('$', '').replace('₹', '').replace(' ', '')
        # Remove alphabetical characters if they are at the end (e.g. 150USD)
        # Try to parse
        try:
            return float(val_str)
        except ValueError:
            # Try to extract numbers using regex or basic split
            import re
            match = re.search(r"[-+]?\d*\.\d+|\d+", val_str)
            if match:
                try:
                    return float(match.group())
                except ValueError:
                    return np.nan
            return np.nan

    df_clean["Amount"] = df_clean["Amount"].apply(clean_amount_val)
    df_clean = df_clean.dropna(subset=["Amount"])
    summary["invalid_amounts_dropped"] = initial_count - len(df_clean)
    
    # Standardize negative amounts if any (e.g. make amount positive, type is expense/income)
    # If amount is negative, convert to positive and check if type can be inferred
    def resolve_amount_type(row):
        amt = row["Amount"]
        t_type = str(row["Transaction Type"]).strip().capitalize()
        if amt < 0:
            amt = abs(amt)
            if t_type == "Income":
                t_type = "Expense"
            elif t_type == "Expense":
                t_type = "Income"
        return amt, t_type

    if not df_clean.empty:
        resolved = df_clean.apply(resolve_amount_type, axis=1, result_type='expand')
        df_clean["Amount"] = resolved[0]
        df_clean["Transaction Type"] = resolved[1]

    # 3. Clean Transaction Type
    def standardize_type(val):
        val_str = str(val).strip().lower()
        if val_str in ['income', 'credit', 'inflow', 'deposit', 'earnings']:
            return "Income"
        else:
            # Default to Expense for any other outflow values
            return "Expense"

    df_clean["Transaction Type"] = df_clean["Transaction Type"].apply(standardize_type)

    # 4. Clean Category
    # Fill missing values with 'Other'
    missing_cat_count = df_clean["Category"].isna().sum() + (df_clean["Category"].astype(str).str.strip() == "").sum()
    summary["missing_categories_filled"] = int(missing_cat_count)
    
    df_clean["Category"] = df_clean["Category"].fillna("Other").astype(str).str.strip()
    df_clean.loc[df_clean["Category"] == "", "Category"] = "Other"
    
    # Standardize Category name format: capitalized (e.g., 'food', 'FOOD' -> 'Food')
    df_clean["Category"] = df_clean["Category"].apply(lambda c: c.capitalize())

    # 5. Clean Description
    df_clean["Description"] = df_clean["Description"].fillna("Unknown").astype(str).str.strip()

    # 6. Remove Duplicates
    initial_count = len(df_clean)
    # Reset Date index or string format for exact match if desired, but we can do it on standard columns
    df_clean = df_clean.drop_duplicates(keep='first').reset_index(drop=True)
    summary["duplicates_removed"] = initial_count - len(df_clean)

    summary["final_rows"] = len(df_clean)
    return df_clean, summary
