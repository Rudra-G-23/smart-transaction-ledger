import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# --- Configuration & Seed ---
random.seed(42)
np.random.seed(42)
num_rows = 1000

# --- 1. MERCHANT DATABASE ---
merchants = [
    ["M001", "Starbucks", "Food & Beverage", 300, "low"],
    ["M002", "Amazon", "Shopping", 1500, "medium"],
    ["M003", "Flipkart", "E-commerce", 1200, "medium"],
    ["M004", "Big Bazaar", "Grocery", 800, "low"],
    ["M005", "OLA", "Transport", 200, "low"],
    ["M006", "DMart", "Grocery", 1000, "low"],
    ["M007", "Local Shop", np.nan, 100, "high"],
    ["M008", "Apple", "Electronics", 25000, "medium"],
    ["M009", "Swiggy", "Food & Beverage", 400, "low"],
    ["M010", "Unknown Store", "???", 500, "high"]
]
df_merchants = pd.DataFrame(merchants, columns=['merchant_id', 'merchant_name', 'expected_category', 'avg_transaction_value', 'risk_level'])

# --- 2. USER DATABASE ---
users = []
cities = ["Bhubaneswar", "BBSR", "Bhubaneshwar", "Cuttack", None]
risk_scores = [0.1, 0.2, 0.3, 0.5, "low", "medium", "high", "NA"]

for i in range(1, 51):
    u_id = f"U{str(i).zfill(3)}"
    income = random.choice(["50000-70000", ">100000", "30000", "45000-55000", "70000-90000", "NA"])
    users.append([u_id, income, random.choice(cities), random.choice([10000, 15000, 20000, 25000, 50000, np.nan]), random.choice(risk_scores)])

df_users = pd.DataFrame(users, columns=['user_id', 'income_range', 'city', 'spending_limit', 'risk_score'])

# --- 3. PREVIOUS FRAUD DB ---
fraud_patterns = [
    ["P001", "Big Bazaar", ">5000", 1],
    ["P002", "Amazon", "<50", 0],
    ["P003", "Unknown Store", "any", 1],
    ["P004", "Flipkart", ">10000", 1],
    ["P005", "OLA", ">1000", 0],
    ["P006", "", ">20000", 1]
]
df_fraud = pd.DataFrame(fraud_patterns, columns=['pattern_id', 'merchant', 'amount_range', 'fraud_flag'])

# --- 4. THE MAIN DIRTY TRANSACTIONS (1000 ROWS) ---
txn_data = []
locations = ["Bhubaneswar", "BBSR", "Bhubaneshwar", "Online", "local shop", ""]
categories = ["food", "shopping", "grocery", "transport", "electronics", "other", "Food & Beverage", "refund"]
payment_modes = ["UPI", "Card", "Cash"]

start_date = datetime(2024, 1, 1)

for i in range(1, num_rows + 1):
    m_info = random.choice(merchants)
    u_id = f"U{str(random.randint(1, 20)).zfill(3)}"
    
    # Random Date Formats
    curr_date = start_date + timedelta(days=random.randint(0, 90))
    date_fmt = random.choice(["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"])
    formatted_date = curr_date.strftime(date_fmt)
    
    # Messy Description Logic
    noise = random.choice(["", "!!!", "???", " 0412", "*Order#99", " purchase", " fee"])
    desc = f"{m_info[1]} {noise}".strip()
    
    # Random amounts (including occasional negative for refunds)
    amount = round(random.uniform(10, 30000), 2)
    if random.random() < 0.05: amount = -abs(amount) # 5% are refunds
    
    txn_data.append({
        "transaction_id": f"TXN{str(i).zfill(4)}",
        "user_id": u_id,
        "date": formatted_date,
        "amount": amount,
        "description": desc,
        "merchant_name": m_info[1] if random.random() > 0.1 else "", # 10% missing merchant
        "location": random.choice(locations),
        "payment_mode": random.choice(payment_modes),
        "category": random.choice(categories) if random.random() > 0.05 else "" # 5% missing category
    })

df_transactions = pd.DataFrame(txn_data)

# --- Save to CSVs ---
df_transactions.to_csv("data/raw/finance_transactions.csv", index=False)
df_users.to_csv("data/raw/user_db.csv", index=False)
df_merchants.to_csv("data/raw/merchant_db.csv", index=False)
df_fraud.to_csv("data/raw/fraud_patterns.csv", index=False)

print("Success! 4 Dirty CSVs generated.")
print(df_transactions.head(10))
print(df_users.head(10))
print(df_merchants.head(10))
print(df_fraud.head(10))
