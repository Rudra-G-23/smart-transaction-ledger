# Raw DB Schema
Tool: https://www.drawdb.app/

### 1. User Database (`user_db`)
```sql
CREATE TABLE users (
    user_id VARCHAR(10) PRIMARY KEY,
    income_range VARCHAR(50),
    city VARCHAR(100),
    spending_limit NUMERIC(15, 2), -- Handles 10000.0 and NULL/NaN
    risk_score VARCHAR(20)         -- Handles '0.2', 'low', 'high', 'NA'
);
```

### 2. Merchant Database (`merchant_db`)
```sql
CREATE TABLE merchants (
    merchant_id VARCHAR(10) PRIMARY KEY,
    merchant_name VARCHAR(100),
    expected_category VARCHAR(100),
    avg_transaction_value NUMERIC(15, 2),
    risk_level VARCHAR(20)
);
```

### 3. Finance Transactions (`finance_transactions`)
```sql
CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    user_id VARCHAR(10) REFERENCES users(user_id),
    date VARCHAR(20),               -- Messy date formats stored as text
    amount NUMERIC(15, 2),
    description TEXT,
    merchant_name VARCHAR(100),
    location VARCHAR(100),
    payment_mode VARCHAR(20),
    category VARCHAR(50)
);
```

### 4. Previous Fraud Patterns (`fraud_patterns`)
```sql
CREATE TABLE fraud_patterns (
    pattern_id VARCHAR(10) PRIMARY KEY,
    merchant VARCHAR(100),
    amount_range VARCHAR(50),      -- Handles ">5000", "<50", "any"
    fraud_flag INTEGER             -- 0 or 1
);
```
