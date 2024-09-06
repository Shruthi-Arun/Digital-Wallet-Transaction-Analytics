import pandas as pd
import matplotlib.pyplot as plt

file_path = 'digital_wallet_transactions.csv'  
data = pd.read_csv(file_path)


data['transaction_date'] = pd.to_datetime(data['transaction_date'])

# 1. User Spending Patterns
# Group by user_id to calculate total spending, number of transactions, and preferred categories and payment methods
user_spending = data.groupby('user_id').agg(
    total_spent=pd.NamedAgg(column='product_amount', aggfunc='sum'),
    transaction_count=pd.NamedAgg(column='transaction_id', aggfunc='count'),
    avg_transaction_value=pd.NamedAgg(column='product_amount', aggfunc='mean'),
    preferred_category=pd.NamedAgg(column='product_category', aggfunc=lambda x: x.mode()[0]),
    preferred_payment_method=pd.NamedAgg(column='payment_method', aggfunc=lambda x: x.mode()[0])
).reset_index()

# Visualizing top 5 categories in terms of spending
category_spending = data.groupby('product_category')['product_amount'].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(10, 6))
category_spending.plot(kind='bar', color='skyblue')
plt.title('Top 5 Categories by Spending')
plt.ylabel('Total Amount Spent')
plt.xlabel('Product Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualizing top 5 payment methods in terms of usage
payment_method_usage = data['payment_method'].value_counts().head(5)

plt.figure(figsize=(10, 6))
payment_method_usage.plot(kind='bar', color='orange')
plt.title('Top 5 Payment Methods Used')
plt.ylabel('Number of Transactions')
plt.xlabel('Payment Method')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Merchant Performance
# Group by merchant_name to find the number of transactions and total sales
merchant_performance = data.groupby('merchant_name').agg(
    total_sales=pd.NamedAgg(column='product_amount', aggfunc='sum'),
    transaction_count=pd.NamedAgg(column='transaction_id', aggfunc='count')
).reset_index()

# Sort merchants by total sales to identify top-performing merchants
top_merchants = merchant_performance.sort_values(by='total_sales', ascending=False).head(5)

# Visualizing top 5 merchants by total sales
plt.figure(figsize=(10, 6))
plt.bar(top_merchants['merchant_name'], top_merchants['total_sales'], color='green')
plt.title('Top 5 Merchants by Total Sales')
plt.ylabel('Total Sales')
plt.xlabel('Merchant')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Display the first few rows of user spending and merchant performance for insight
print(user_spending.head())
print(merchant_performance.head())
