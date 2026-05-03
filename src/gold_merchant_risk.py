import os
import pandas as pd
import numpy as np

SILVER_PATH = r"data/silver"
GOLD_PATH = r"data/gold"

os.makedirs(GOLD_PATH, exist_ok=True)

def apply_amount_rule(amount, rule):
    """Check if transaction amount satisfies fraud rule"""
    if pd.isna(rule):
        return 0
    if '>' in rule:
        return int(amount > float(rule.replace('>', '')))
    elif '<' in rule:
        return int(amount < float(rule.replace('<', '')))
    return 0



def merchant_risk_features(txn_df, merchant_df, fraud_df):
    """Create merchant risk features: fraud signals, patterns, scoring"""

    df = txn_df.merge(merchant_df, on='merchant_name', how='left')
    df = df.merge(fraud_df, left_on='merchant_name', right_on='merchant', how='left')

    df['rule_based_flag'] = df.apply(
        lambda row: apply_amount_rule(row['amount'], row['amount_range']),
        axis=1
    )

    df['is_high_value'] = (df['amount'] > 15000).astype(int)

    merchant_agg = df.groupby('merchant_name').agg(

        # Risk Signals
        fraud_transaction_count=('fraud_flag', 'sum'),
        high_value_txn_count=('is_high_value', 'sum'),
        avg_transaction_amount=('amount', 'mean'),

        # Pattern Matching
        rule_based_hits=('rule_based_flag', 'sum'),

        # Volume 
        total_txn=('transaction_id', 'count')

    ).reset_index()

    # Normalize signals
    merchant_agg['fraud_ratio'] = merchant_agg['fraud_transaction_count'] / merchant_agg['total_txn']
    merchant_agg['high_value_ratio'] = merchant_agg['high_value_txn_count'] / merchant_agg['total_txn']
    merchant_agg['rule_hit_ratio'] = merchant_agg['rule_based_hits'] / merchant_agg['total_txn']

    # weighted scoring 
    merchant_agg['merchant_risk_score'] = (
        0.5 * merchant_agg['fraud_ratio'] +
        0.3 * merchant_agg['rule_hit_ratio'] +
        0.2 * merchant_agg['high_value_ratio']
    )

    merchant_agg = merchant_agg.merge(
        merchant_df[['merchant_name', 'risk_level_encoded', 'expected_category']],
        on='merchant_name',
        how='left'
    )

    return merchant_agg



def call_merchant_risk_pipeline():
    """Run silver to gold merchant risk pipeline"""

    txn_df = pd.read_csv(os.path.join(SILVER_PATH, "finance_transactions_clean.csv"))
    merchant_df = pd.read_csv(os.path.join(SILVER_PATH, "merchant_db_clean.csv"))
    fraud_df = pd.read_csv(os.path.join(SILVER_PATH, "fraud_patterns_clean.csv"))

    gold_df = merchant_risk_features(txn_df, merchant_df, fraud_df)

    gold_df.to_csv(os.path.join(GOLD_PATH, "gold_merchant_risk.csv"), index=False)

    return gold_df

if __name__ == "__main__":
    call_merchant_risk_pipeline()