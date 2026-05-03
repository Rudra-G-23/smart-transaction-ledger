import os
import pandas as pd
import numpy as np

SILVER_PATH = r"data/silver"
GOLD_PATH = r"data/gold"

os.makedirs(GOLD_PATH, exist_ok=True)

def apply_amount_rule(amount, rule):
    """Check if amount satisfies fraud rule"""
    if pd.isna(rule):
        return 0
    if '>' in rule:
        return int(amount > float(rule.replace('>', '')))
    elif '<' in rule:
        return int(amount < float(rule.replace('<', '')))
    return 0


def fraud_dataset_features(txn_df, user_df, merchant_df, fraud_df):
    """Create final ML fraud dataset with user, merchant, transaction, and rule features"""

    df = txn_df.merge(user_df, on='user_id', how='left')
    df = df.merge(merchant_df, on='merchant_name', how='left')
    df = df.merge(fraud_df, left_on='merchant_name', right_on='merchant', how='left')

    # Avg spend per user
    user_avg = txn_df.groupby('user_id')['amount'].mean().reset_index()
    user_avg.columns = ['user_id', 'user_avg_spend']

    df = df.merge(user_avg, on='user_id', how='left')

    # Spending limit ratio
    df['spending_limit_ratio'] = df['amount'] / df['spending_limit']

    # Risk score (already cleaned)
    df['user_risk_score'] = df['risk_score_new']

    df['merchant_risk_level'] = df['risk_level_encoded']
    df['avg_transaction_value'] = df['avg_transaction_value']

    # High amount
    df['is_high_amount'] = (df['amount'] > 15000).astype(int)

    # Unusual payment mode 
    # If user's most frequent payment is UPI but current is Cash → unusual
    user_payment_mode = txn_df.groupby('user_id')['payment_mode'] \
                             .agg(lambda x: x.mode()[0] if not x.mode().empty else 'UPI') \
                             .reset_index()
    user_payment_mode.columns = ['user_id', 'preferred_payment']

    df = df.merge(user_payment_mode, on='user_id', how='left')

    df['unusual_payment_mode'] = (df['payment_mode'] != df['preferred_payment']).astype(int)

    # Category mismatch
    df['category_mismatch'] = (df['category'] != df['expected_category']).astype(int)

    df['matches_fraud_pattern'] = df.apply(
        lambda row: apply_amount_rule(row['amount'], row['amount_range']),
        axis=1
    )

    final_cols = [
        'transaction_id',
        'user_id',
        'merchant_name',
        'amount',

        # User features
        'user_avg_spend',
        'user_risk_score',
        'spending_limit_ratio',

        # Merchant features
        'merchant_risk_level',
        'avg_transaction_value',

        # Transaction features
        'is_high_amount',
        'unusual_payment_mode',
        'category_mismatch',

        # Rule features
        'matches_fraud_pattern',

        # Target
        'fraud_flag'
    ]

    df_final = df[final_cols]

    return df_final


def call_fraud_dataset_pipeline():
    """Run silver to gold fraud dataset pipeline"""

    txn_df = pd.read_csv(os.path.join(SILVER_PATH, "finance_transactions_clean.csv"))
    user_df = pd.read_csv(os.path.join(SILVER_PATH, "user_db_clean.csv"))
    merchant_df = pd.read_csv(os.path.join(SILVER_PATH, "merchant_db_clean.csv"))
    fraud_df = pd.read_csv(os.path.join(SILVER_PATH, "fraud_patterns_clean.csv"))

    gold_df = fraud_dataset_features(txn_df, user_df, merchant_df, fraud_df)

    gold_df.to_csv(os.path.join(GOLD_PATH, "gold_fraud_dataset.csv"), index=False)

    return gold_df


if __name__ == "__main__":
    call_fraud_dataset_pipeline()