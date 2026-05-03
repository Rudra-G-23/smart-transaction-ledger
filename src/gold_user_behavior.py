import os
import pandas as pd
import numpy as np

SILVER_PATH = r"data/silver"
GOLD_PATH = r"data/gold"

os.makedirs(GOLD_PATH, exist_ok=True)

def user_behavior_features(txn_df, user_df):
    """Create user behavior features: spending, time, payment, category"""

    df = txn_df.merge(user_df, on='user_id', how='left')

    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date
    df['weekday'] = df['date'].dt.weekday
    df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)

    user_agg = df.groupby('user_id').agg(

        # Spending Behavior
        total_spent=('amount', 'sum'),
        avg_transaction=('amount', 'mean'),
        max_transaction=('amount', 'max'),
        transaction_count=('transaction_id', 'count'),

        # Time Behavior
        active_days=('day', 'nunique'),
        weekend_spending=('amount', lambda x: x[df.loc[x.index, 'is_weekend'] == 1].sum()),

        # Payment Behavior
        upi_count=('payment_mode', lambda x: (x == 'UPI').sum()),
        cash_count=('payment_mode', lambda x: (x == 'Cash').sum()),

        # Category Behavior
        most_used_category=('category', lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'),
        category_diversity=('category', 'nunique')

    ).reset_index()


    # Spending per day
    user_agg['spending_per_day'] = user_agg['total_spent'] / user_agg['active_days']

    # Payment ratios
    user_agg['upi_ratio'] = user_agg['upi_count'] / user_agg['transaction_count']
    user_agg['cash_ratio'] = user_agg['cash_count'] / user_agg['transaction_count']

    # Merge back user info
    user_agg = user_agg.merge(user_df, on='user_id', how='left')

    return user_agg

def call_user_behavior_pipeline():
    """Run silver to gold user behavior pipeline"""

    txn_df = pd.read_csv(os.path.join(SILVER_PATH, "finance_transactions_clean.csv"))
    user_df = pd.read_csv(os.path.join(SILVER_PATH, "user_db_clean.csv"))

    gold_df = user_behavior_features(txn_df, user_df)

    gold_df.to_csv(os.path.join(GOLD_PATH, "gold_user_behavior.csv"), index=False)

    return gold_df

if __name__ == "__main__":
    call_user_behavior_pipeline()