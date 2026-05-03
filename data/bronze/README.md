# Bronze Datasets
> Few Examples

## Finance Transactions
```csv
transaction_id,user_id,date,amount,description,merchant_name,location,payment_mode,category
TXN0001,U019,11/03/2024,6614.32,Starbucks *Order#99,Starbucks,BBSR,UPI,other
TXN0002,U017,2024/01/31,14567.58,Amazon  purchase,Amazon,local shop,Cash,refund
TXN0003,U007,2024-01-13,12937.22,Local Shop  purchase,Local Shop,,UPI,shopping
TXN0004,U013,2024-02-13,5755.79,Starbucks !!!,Starbucks,BBSR,Card,shopping
TXN0005,U018,2024-01-13,29978.48,Apple  purchase,Apple,BBSR,UPI,refund
```

## Fraud Patterns
```csv
pattern_id,merchant,amount_range,fraud_flag
P001,Big Bazaar,>5000,1
P002,Amazon,<50,0
P003,Unknown Store,any,1
P004,Flipkart,>10000,1
P005,OLA,>1000,0
P006,,>20000,1
```

## Merchant DB
```csv
merchant_id,merchant_name,expected_category,avg_transaction_value,risk_level
M001,Starbucks,Food & Beverage,300,low
M002,Amazon,Shopping,1500,medium
M003,Flipkart,E-commerce,1200,medium
M004,Big Bazaar,Grocery,800,low
M005,OLA,Transport,200,low
M006,DMart,Grocery,1000,low
M007,Local Shop,,100,high
M008,Apple,Electronics,25000,medium
M009,Swiggy,Food & Beverage,400,low
M010,Unknown Store,???,500,high
```

## User DB
```csv
user_id,income_range,city,spending_limit,risk_score
U001,NA,Bhubaneswar,10000.0,low
U002,>100000,BBSR,15000.0,0.2
U003,NA,,10000.0,high
U004,50000-70000,Bhubaneswar,10000.0,0.5
U005,>100000,,50000.0,0.1
U006,70000-90000,BBSR,,high
U007,>100000,Cuttack,50000.0,low
U008,50000-70000,BBSR,,high
U009,30000,Bhubaneshwar,15000.0,0.5
U010,30000,Bhubaneswar,10000.0,high
```