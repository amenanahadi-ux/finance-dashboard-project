import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(output_csv_path, output_xlsx_path):
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Date range: 24 months (July 2024 to June 2026)
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2026, 6, 30)
    
    current_date = start_date
    records = []

    # Categories & standard descriptions
    categories_config = {
        "Income": [("Salary", 50000, 50000), ("Freelance Project", 3000, 15000), ("Investment Yield", 1000, 5000)],
        "Food": [("Starbucks Coffee", 150, 450), ("McDonald's Meal", 250, 600), ("Local Grocery Store", 1200, 4000), ("UberEats Delivery", 400, 1200), ("Fine Dining", 1500, 5000)],
        "Utilities": [("Electricity Bill", 1500, 3000), ("Water Bill", 300, 800), ("Fiber Internet Bill", 800, 1200), ("Mobile Phone Bill", 400, 900)],
        "Transportation": [("Uber Ride", 100, 500), ("Gas Station", 1500, 3500), ("Metro Card Topup", 200, 600), ("Car Service", 3000, 8000)],
        "Shopping": [("Amazon Purchase", 500, 8000), ("Zara Clothing", 1200, 6000), ("Nike Shoes", 3000, 7000), ("Electronics Store", 5000, 25000)],
        "Entertainment": [("Netflix Monthly Plan", 199, 649), ("Cinema Movie Ticket", 300, 800), ("Spotify Premium", 119, 119), ("Concert Ticket", 2000, 6000), ("Steam Game Purchase", 500, 3000)],
        "Travel": [("Flight Booking", 5000, 18000), ("Hotel Accommodation", 4000, 15000), ("Airbnb Booking", 6000, 20000)],
        "Medical": [("Pharmacy Medicines", 200, 1500), ("Dental Clinic Visit", 1000, 4000), ("Health Checkup Package", 2500, 6000)]
    }

    # Generate daily or periodic transactions
    days_to_generate = (end_date - start_date).days + 1
    
    for day_offset in range(days_to_generate):
        date = start_date + timedelta(days=day_offset)
        year, month = date.year, date.month
        is_first_of_month = (date.day == 1)
        is_weekend = date.weekday() >= 5
        
        # 1. Monthly income
        if is_first_of_month:
            # Regular Salary
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": "Salary Credit",
                "Category": "Income",
                "Amount": 60000.0 if year == 2025 else (65000.0 if year == 2026 else 55000.0), # increasing salary trend
                "Transaction Type": "Income"
            })
            
            # Recurring utility bills on 5th to 10th (simulated by day offset)
            # Add electricity, internet, phone bills
            records.append({
                "Date": (date + timedelta(days=4)).strftime("%Y-%m-%d"),
                "Description": "Fiber Internet Bill",
                "Category": "Utilities",
                "Amount": float(random.randint(800, 1000)),
                "Transaction Type": "Expense"
            })
            records.append({
                "Date": (date + timedelta(days=6)).strftime("%Y-%m-%d"),
                "Description": "Electricity Bill",
                "Category": "Utilities",
                "Amount": float(random.randint(1800, 3200)),
                "Transaction Type": "Expense"
            })
            records.append({
                "Date": (date + timedelta(days=8)).strftime("%Y-%m-%d"),
                "Description": "Mobile Phone Bill",
                "Category": "Utilities",
                "Amount": float(random.randint(400, 600)),
                "Transaction Type": "Expense"
            })
            
            # Monthly subscriptions
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": "Netflix Premium",
                "Category": "Entertainment",
                "Amount": 649.0,
                "Transaction Type": "Expense"
            })
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": "Spotify Family Plan",
                "Category": "Entertainment",
                "Amount": 179.0,
                "Transaction Type": "Expense"
            })

        # 2. Freelance / Investment Income occasionally
        if date.day in [10, 25] and random.random() < 0.3:
            desc, min_val, max_val = random.choice(categories_config["Income"][1:])
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Income",
                "Amount": float(random.randint(min_val, max_val)),
                "Transaction Type": "Income"
            })

        # 3. Daily Expenses (Food, Transport, etc.)
        # Food almost every day
        if random.random() < 0.8:
            desc, min_val, max_val = random.choice(categories_config["Food"])
            # Let's add some inflation effect over months to make forecasting more interesting
            inflation_multiplier = 1.0 + (day_offset / days_to_generate) * 0.15  # Up to 15% increase over 2 years
            amt = float(random.randint(min_val, max_val)) * inflation_multiplier
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Food",
                "Amount": round(amt, 2),
                "Transaction Type": "Expense"
            })
            
        # Transport
        if random.random() < 0.4:
            desc, min_val, max_val = random.choice(categories_config["Transportation"])
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Transportation",
                "Amount": float(random.randint(min_val, max_val)),
                "Transaction Type": "Expense"
            })
            
        # Shopping (mostly weekends or mid-month)
        shopping_prob = 0.5 if is_weekend else 0.15
        # Seasonal: higher shopping probability in December & November
        if month in [11, 12]:
            shopping_prob += 0.15
            
        if random.random() < shopping_prob:
            desc, min_val, max_val = random.choice(categories_config["Shopping"])
            # In Dec, shopping amounts are higher
            val_multiplier = 1.3 if month == 12 else 1.0
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Shopping",
                "Amount": float(random.randint(min_val, max_val)) * val_multiplier,
                "Transaction Type": "Expense"
            })

        # Entertainment
        entertainment_prob = 0.4 if is_weekend else 0.1
        if random.random() < entertainment_prob:
            desc, min_val, max_val = random.choice(categories_config["Entertainment"][1:])
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Entertainment",
                "Amount": float(random.randint(min_val, max_val)),
                "Transaction Type": "Expense"
            })

        # Travel: quarterly or vacation periods (May, December)
        travel_prob = 0.05 if month in [5, 12] else 0.005
        if random.random() < travel_prob:
            desc, min_val, max_val = random.choice(categories_config["Travel"])
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Travel",
                "Amount": float(random.randint(min_val, max_val)),
                "Transaction Type": "Expense"
            })

        # Medical: occasional
        if random.random() < 0.02:
            desc, min_val, max_val = random.choice(categories_config["Medical"])
            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Description": desc,
                "Category": "Medical",
                "Amount": float(random.randint(min_val, max_val)),
                "Transaction Type": "Expense"
            })

    # Create the DataFrame
    df = pd.DataFrame(records)

    # Let's introduce DIRTY DATA elements for testing the cleaning module
    dirty_records = []
    
    # 1. Duplicates (Add 15 duplicate rows)
    duplicate_indices = np.random.choice(df.index, 15, replace=False)
    for idx in duplicate_indices:
        dirty_records.append(df.iloc[idx].to_dict())
        
    # 2. Casing issues and whitespaces in Categories (Add 10 rows)
    casing_issues = [
        {"Date": "2025-05-15", "Description": "Local Groceries", "Category": "food", "Amount": 450.0, "Transaction Type": "Expense"},
        {"Date": "2025-05-16", "Description": "Starbucks Coffee", "Category": "FOOD", "Amount": 150.0, "Transaction Type": "Expense"},
        {"Date": "2025-05-17", "Description": "Amazon Purchase", "Category": "shopping", "Amount": 1200.0, "Transaction Type": "Expense"},
        {"Date": "2025-05-18", "Description": "Zara Shopping", "Category": "  Shopping  ", "Amount": 3400.0, "Transaction Type": "Expense"},
        {"Date": "2025-05-19", "Description": "Uber Auto", "Category": "transportation", "Amount": 120.0, "Transaction Type": "Expense"}
    ]
    dirty_records.extend(casing_issues)

    # 3. Missing Categories (Add 5 rows with None or empty category)
    missing_cats = [
        {"Date": "2025-06-01", "Description": "Miscellaneous Spent", "Category": None, "Amount": 500.0, "Transaction Type": "Expense"},
        {"Date": "2025-06-02", "Description": "Cash withdrawal", "Category": "", "Amount": 2000.0, "Transaction Type": "Expense"}
    ]
    dirty_records.extend(missing_cats)

    # 4. Invalid Amount values (e.g. non-numeric strings or negative expense amount - wait, expenses are positive amounts representing outflow, or we can see text like "150 USD")
    invalid_amounts = [
        {"Date": "2025-06-03", "Description": "Coffee Shop", "Category": "Food", "Amount": "350 INR", "Transaction Type": "Expense"},
        {"Date": "2025-06-04", "Description": "Taxi Service", "Category": "Transportation", "Amount": "invalid_amt", "Transaction Type": "Expense"}
    ]
    dirty_records.extend(invalid_amounts)

    # 5. Invalid Date values
    invalid_dates = [
        {"Date": "2025/13/45", "Description": "Weekend Getaway", "Category": "Travel", "Amount": 4500.0, "Transaction Type": "Expense"},
        {"Date": "Not a Date", "Description": "Movie Night", "Category": "Entertainment", "Amount": 350.0, "Transaction Type": "Expense"}
    ]
    dirty_records.extend(invalid_dates)

    # Append dirty records
    df_dirty = pd.concat([df, pd.DataFrame(dirty_records)], ignore_index=True)

    # Shuffle the dataset to mix dirty records
    df_dirty = df_dirty.sample(frac=1.0, random_state=42).reset_index(drop=True)

    # Save to CSV
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df_dirty.to_csv(output_csv_path, index=False)
    print(f"Generated sample CSV dataset with {len(df_dirty)} rows at {output_csv_path}")

    # Save to Excel
    df_dirty.to_excel(output_xlsx_path, index=False)
    print(f"Generated sample Excel dataset with {len(df_dirty)} rows at {output_xlsx_path}")

if __name__ == "__main__":
    generate_sample_data(
        "/Users/amenanahadi/Downloads/fd proj/sample_data/sample_transactions.csv",
        "/Users/amenanahadi/Downloads/fd proj/sample_data/sample_transactions.xlsx"
    )
