# Data Cleaning Process



## 1. Merchant

```mermaid
graph TD
    M_In[Raw Merchant] --> M1[Assume 'store' means 'Local Store']
    M1 --> M2[Fill NaN Category with 'Others']
    M2 --> M3[Encode Risk Level Label]
    M3 --> M_Out[(Clean Merchant Data)]
```

### 1.1.  Merchant Name
Assumptions:
- We don't know store means 
- That is the Local Store
  
### 1.2 expected_category
- Replace NaN value
- Fill nan with Others

### 1.3 risk_level
- Encoded the Label

---

## 2. User DB

```mermaid
graph TD
    U_In[Raw User] --> U1[Use Railway Station Code & FFill for City]
    U1 --> U2[Treat NaN Income as <45k & Map]
    U2 --> U3[Map Risk Score 0.2/0.3/0.5 & BFill]
    U3 --> U4[Fill NaN Spending Limit with Min Value]
    U4 --> U_Out[(Clean User Data)]
```

### 2.1. City
- Used Railway Station Code
- Forward Filling

## 2.2. Income
- Nan value treat as the under 45k.
- Then Category the income group Mapping
  
## 2.3. risk score
- Map the risk score
- Low means 0.2, medium is 0.3 and high is 0.5
- Nan value fill with backward filling

## 2.4. Spending Limit
- Nan value fill with minimum value

---

## 3. Fraud Pattern

```mermaid
graph TD
    F_In[Raw Fraud] --> F1[Fill NaN Merchant with 'Unknown']
    F1 --> F2[Fill Amount Range with '>20000']
    F2 --> F_Out[(Clean Fraud Data)]
```

### 3.1 merchant
- NaN value fill with the Unknown

### 3.1 amount_range
- any that fill with >20000	

---

## 4. Fin Txn DB

```mermaid
graph TD
    T_In[Raw Fin Txn] --> T1[Fix Date Format]
    T1 --> T2[Make Amount Positive & Bin]
    T2 --> T3[Extract Merchant Name from Desc]
    T3 --> T4[Create Refund Feature]
    T4 --> T_Out[(Clean Fin Txn Data)]
```

### 4.1. Date
- Fix the date format

## 4.2. amount 
- Make everything +ve
- Using bins make the category
  
## 4.3. Desc
- From desc extract the Merchant name

## 4.4. category 
- Refund feature creation

---