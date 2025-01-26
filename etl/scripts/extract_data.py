import pandas as pd
import os

staging_dir = 'data/staging'
os.makedirs(staging_dir, exist_ok=True)

# ---- Extracting Data ----
products = pd.read_csv('data/raw/inventory_data.csv')
sales = pd.read_csv('data/raw/sales_data.csv')
time = pd.read_csv('data/raw/time_data.csv')

customers = pd.read_excel('data/raw/customer_data.xlsx')
shipping = pd.read_excel('data/raw/shipping_data.xlsx')

# ---- Save Raw Data to Staging Area ----

products.to_csv(f'{staging_dir}/products_raw.csv', index=False)
sales.to_csv(f'{staging_dir}/sales_raw.csv', index=False)
time.to_csv(f'{staging_dir}/time_raw.csv', index=False)

customers.to_excel(f'{staging_dir}/customers_raw.xlsx', index=False)
shipping.to_excel(f'{staging_dir}/shipping_raw.xlsx', index=False)

print("Data extraction completed and saved to staging area.")