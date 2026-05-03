import os
import pandas as pd
import numpy as np

# ================= PATH =================
BRONZE_PATH = r"data/bronze"
SILVER_PATH = r"data/silver"

os.makedirs(SILVER_PATH, exist_ok=True)


# ================= MERCHANT PIPELINE =================

def merchant_cleaning_features(df):
    """Clean merchant data: name fix, category fill, risk encoding"""
    
    # Fix merchant name
    df['merchant_name'] = df['merchant_name'].replace('Unknown Store', 'Local Shop')

    # Fix expected category
    df['expected_category'] = df['expected_category'].replace({'???': 'Others', 'NaN': 'Others'})
    df['expected_category'] = df['expected_category'].fillna('Others')

    # Encode risk level
    df['risk_level_encoded'] = df['risk_level'].replace({'low': 1, 'medium': 2, 'high': 3})

    return df


def call_merchant_pipeline():
    """Run merchant bronze to silver pipeline"""
    
    df = pd.read_csv(os.path.join(BRONZE_PATH, "merchant_db.csv"))
    
    df = merchant_cleaning_features(df)
    
    df.to_csv(os.path.join(SILVER_PATH, "merchant_db_clean.csv"), index=False)
    
    return df


# ================= USER PIPELINE =================

def user_cleaning_features(df):
    """Clean user data: city normalize, income mapping, risk score, spending fix"""

    #  City normalize
    df['city'] = df['city'].replace({
        "Bhubaneswar": 'BSSR',
        "Bhubaneshwar": 'BSSR',
        'Cuttack': 'CTC'
    })
    df['city'] = df['city'].ffill()

    #  Income mapping
    income_mapping = {
        '>100000': 'Over 100k',
        '70000-90000': '70k - 90k',
        '50000-70000': '50k - 70k',
        '45000-55000': '45k - 55k',
        '30000': 'Under 45k'
    }

    df['income_range_clean'] = df['income_range'].map(income_mapping)
    df['income_range_clean'] = df['income_range_clean'].fillna('Under 45k')

    #  Risk score mapping
    risk_mapping = {
        'low': 0.1,
        'medium': 0.3,
        'high': 0.5
    }

    df['risk_score_new'] = df['risk_score'].map(risk_mapping)
    df['risk_score_new'] = df['risk_score_new'].bfill()

    #  Spending limit fix
    df['spending_limit'] = df['spending_limit'].fillna(df['spending_limit'].min())

    #  Drop old columns
    df = df.drop(columns={'income_range', 'risk_score'})

    return df


def call_user_pipeline():
    """Run user bronze to silver pipeline"""
    
    df = pd.read_csv(os.path.join(BRONZE_PATH, "user_db.csv"))
    
    df = user_cleaning_features(df)
    
    df.to_csv(os.path.join(SILVER_PATH, "user_db_clean.csv"), index=False)
    
    return df


# ================= FRAUD PATTERN PIPELINE =================

def fraud_pattern_cleaning_features(df):
    """Clean fraud pattern data: merchant fill and amount range fix"""

    df['merchant'] = df['merchant'].fillna('Unknown Store')
    df['amount_range'] = df['amount_range'].replace({'any': '>20000'})

    return df


def call_fraud_pattern_pipeline():
    """Run fraud pattern bronze to silver pipeline"""
    
    df = pd.read_csv(os.path.join(BRONZE_PATH, "fraud_patterns.csv"))
    
    df = fraud_pattern_cleaning_features(df)
    
    df.to_csv(os.path.join(SILVER_PATH, "fraud_patterns_clean.csv"), index=False)
    
    return df


# ================= FINANCIAL TRANSACTION PIPELINE =================

def fin_txn_cleaning_features(df):
    """Clean transaction data: date, amount, bins, brand extraction, refund flag"""

    #  Date fix
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed')

    #  Amount fix
    df['amount'] = np.abs(df['amount'])

    bins = [359, 8500, 18000, 23000, 299964]
    labels = ['Low', 'Medium-Low', 'Medium-High', 'High']
    df['user_category_new'] = pd.cut(df['amount'], bins=bins, labels=labels, include_lowest=True)

    #  Brand extraction
    brands = ['Starbucks', 'Amazon', 'Apple', 'Flipkart', 'DMart',
              'Swiggy', 'OLA', 'Big Bazaar', 'Local Shop', 'Unknown Store']

    pattern = '|'.join(brands)
    df['clean_brand'] = df['description'].str.extract(f'({pattern})', expand=False)

    df['merchant_name'] = df['clean_brand'].replace('Unknown Store', 'Local Shop')

    #  Refund flag
    df['is_refund'] = np.where(df['category'] == 'refund', 1, 0)

    #  Drop unused
    df = df.drop(columns={'location', 'description'})

    return df


def call_fin_txn_pipeline():
    """Run financial transaction bronze to silver pipeline"""
    
    df = pd.read_csv(os.path.join(BRONZE_PATH, "finance_transactions.csv"))
    
    df = fin_txn_cleaning_features(df)
    
    df.to_csv(os.path.join(SILVER_PATH, "finance_transactions_clean.csv"), index=False)
    
    return df


# ================= MASTER PIPELINE =================

def run_all_pipelines():
    """Run all bronze to silver pipelines"""

    call_merchant_pipeline()
    call_user_pipeline()
    call_fraud_pattern_pipeline()
    call_fin_txn_pipeline()

    print("All datasets cleaned and saved to SILVER layer")


if __name__ == "__main__":
    run_all_pipelines()