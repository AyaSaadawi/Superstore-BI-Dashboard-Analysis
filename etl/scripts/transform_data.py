import pandas as pd

def clean_data():
        # Load raw data from staging area
        products = pd.read_csv('data/staging/products_raw.csv')
        sales = pd.read_csv('data/staging/sales_raw.csv')
        time = pd.read_csv('data/staging/time_raw.csv')

        customers = pd.read_excel('data/staging/customers_raw.xlsx')
        shipping = pd.read_excel('data/staging/shipping_raw.xlsx')

        # Function to check and handle missing data
        def handle_missing_data(df, name):
            print(f"Missing values in {name}:")
            print(df.isnull().sum())
            
            # Fill missing values based on column type
            for col in df.columns:
                if df[col].dtype == 'object':  
                    mode_value = df[col].mode()[0]  
                    df[col] = df[col].fillna(mode_value)
                elif df[col].dtype in ['int64', 'float64']:  
                    if df[col].skew() > 1:  
                        median_value = df[col].median()
                        df[col] = df[col].fillna(median_value)
                    else:  
                        mean_value = df[col].mean()
                        df[col] = df[col].fillna(mean_value)
            
            print(f"Missing values in {name} after handling:")
            print(df.isnull().sum())
            return df

        # ---- Data Cleaning ----

        # 1--- cleaning customers data
        # Standardize text
        customers['Customer Name'] = customers['Customer Name'].str.title()

        # Handle missing values
        customers = handle_missing_data(customers, 'customers')

        # Trim whitespace
        customers['City'] = customers['City'].str.strip()
        customers['State'] = customers['State'].str.strip()
        customers['Country'] = customers['Country'].str.strip()
        customers['Region'] = customers['Region'].str.strip()

        # Validate 'Segment' column
        valid_segments = ['Consumer', 'Corporate', 'Home Office']
        customers['Segment'] = customers['Segment'].apply(lambda x: x if x in valid_segments else 'Unknown')

        # Standardize 'Country' and 'Region' values
        customers['Country'] = customers['Country'].str.upper()
        customers['Region'] = customers['Region'].str.upper()

        # 2--- cleaning shipping data
        # Convert 'Ship Date' to datetime
        shipping['Ship Date'] = pd.to_datetime(shipping['Ship Date'], format='%d-%m-%Y', errors='coerce')

        # Handle missing values
        shipping = handle_missing_data(shipping, 'shipping')

        # Validate 'Ship Mode' column
        valid_ship_modes = ['First Class', 'Second Class', 'Standard Class', 'Same Day']
        shipping['Ship Mode'] = shipping['Ship Mode'].apply(lambda x: x if x in valid_ship_modes else 'Unknown')

        # Validate 'Delivery Days' (ensure non-negative)
        shipping['Delivery Days'] = pd.to_numeric(shipping['Delivery Days'], errors='coerce')
        shipping['Delivery Days'] = shipping['Delivery Days'].clip(lower=0)

        # Validate 'Shipping Cost' (ensure non-negative)
        shipping['Shipping Cost'] = pd.to_numeric(shipping['Shipping Cost'], errors='coerce')
        shipping['Shipping Cost'] = shipping['Shipping Cost'].clip(lower=0)
        
        
        # 3--- Cleaning products data
        # Handle missing values
        products = handle_missing_data(products, 'products')

        # Standardize text
        products['Product Name'] = products['Product Name'].str.strip().str.title()
        products['Category'] = products['Category'].str.strip().str.title()
        products['Sub-Category'] = products['Sub-Category'].str.strip().str.title()

        # 4--- Cleaning sales data
        # Debug: Inspect raw 'Order Date' values in sales
        print("Unique 'Order Date' values in raw sales data:")
        print(sales['Order Date'].unique())

        # Convert 'Order Date' to datetime
        sales['Order Date'] = pd.to_datetime(sales['Order Date'], format='%d-%m-%Y', errors='coerce')

        # Debug: Inspect rows with missing 'Order Date' after conversion
        missing_order_dates_sales = sales[sales['Order Date'].isnull()]
        print("Rows with missing 'Order Date' in sales after conversion:")
        print(missing_order_dates_sales)

        # Handle missing values
        sales = handle_missing_data(sales, 'sales')

        # Validate numerical columns
        sales['Sales'] = pd.to_numeric(sales['Sales'], errors='coerce')
        sales['Profit'] = pd.to_numeric(sales['Profit'], errors='coerce')
        sales['Quantity'] = pd.to_numeric(sales['Quantity'], errors='coerce')
        sales['Discount'] = pd.to_numeric(sales['Discount'], errors='coerce')

        # Ensure non-negative values
        sales['Sales'] = sales['Sales'].clip(lower=0)
        sales['Profit'] = sales['Profit'].clip(lower=0)
        sales['Quantity'] = sales['Quantity'].clip(lower=0)
        sales['Discount'] = sales['Discount'].clip(lower=0)

        # Validate logical consistency (Profit <= Sales)
        invalid_profit = sales[sales['Profit'] > sales['Sales']]
        if not invalid_profit.empty:
            print("Invalid Profit values found (Profit > Sales):", invalid_profit)

        # 5--- Cleaning time data
        # Debug: Inspect raw 'Order Date' values
        print("Unique 'Order Date' values in raw time data:")
        print(time['Order Date'].unique())

        # Convert 'Order Date' to datetime
        time['Order Date'] = pd.to_datetime(time['Order Date'], format='%d-%m-%Y', errors='coerce')

        # Debug: Inspect rows with missing 'Order Date' after conversion
        missing_order_dates = time[time['Order Date'].isnull()]
        print("Rows with missing 'Order Date' after conversion:")
        print(missing_order_dates)

        # Handle missing values
        time = handle_missing_data(time, 'time')

        # Validate 'order year' and 'order month'
        time['order year'] = pd.to_numeric(time['order year'], errors='coerce')
        time['order month'] = pd.to_numeric(time['order month'], errors='coerce')

        # Ensure 'order month' is between 1 and 12
        time['order month'] = time['order month'].clip(lower=1, upper=12)

        # ---- Save Cleaned Data ----
        customers.to_csv('data/processed/customers_cleaned.csv', index=False)
        shipping.to_csv('data/processed/shipping_cleaned.csv', index=False)
        products.to_csv('data/processed/products_cleaned.csv', index=False)
        sales.to_csv('data/processed/sales_cleaned.csv', index=False)
        time.to_csv('data/processed/time_cleaned.csv', index=False)

        print("Data cleaning completed and saved to processed area.")


def validate_data():
    # Load transformed data
    customer_dim = pd.read_csv('data/transformed/customer_dim.csv')
    product_dim = pd.read_csv('data/transformed/product_dim.csv')
    time_dim = pd.read_csv('data/transformed/time_dim.csv')
    shipping_dim = pd.read_csv('data/transformed/shipping_dim.csv')
    sales_fact = pd.read_csv('data/transformed/sales_fact.csv')

    # Convert 'Order Date' in time_dim to datetime format
    time_dim['Order Date'] = pd.to_datetime(time_dim['Order Date'], format='%Y-%m-%d', errors='coerce')
    sales_fact['Order Date'] = pd.to_datetime(sales_fact['Order Date'], format='%Y-%m-%d', errors='coerce')

    # ---- Data Validation ----

    # 1--- Validate Dimension Tables

    # Check for missing values in dimension tables
    for table_name, table in zip(
        ['Customer_Dim', 'Product_Dim', 'Time_Dim', 'Shipping_Dim'],
        [customer_dim, product_dim, time_dim, shipping_dim]
    ):
        print(f"Missing values in {table_name}:")
        print(table.isnull().sum())
        assert table.isnull().sum().sum() == 0, f"Missing values found in {table_name}"

    # Check for duplicate primary keys in dimension tables
    assert customer_dim['Customer ID'].duplicated().sum() == 0, "Duplicate Customer IDs found in Customer_Dim"
    assert product_dim['Product ID'].duplicated().sum() == 0, "Duplicate Product IDs found in Product_Dim"
    assert time_dim['Order Date'].duplicated().sum() == 0, "Duplicate Order Dates found in Time_Dim"
    assert shipping_dim['Order ID'].duplicated().sum() == 0, "Duplicate Order IDs found in Shipping_Dim"

    # 2--- Validate Fact Table

    # Check for missing values in the fact table
    print("Missing values in Sales_Fact:")
    print(sales_fact.isnull().sum())
    assert sales_fact.isnull().sum().sum() == 0, "Missing values found in Sales_Fact"

    # Check for invalid foreign keys in the fact table
    assert sales_fact['Customer ID'].isin(customer_dim['Customer ID']).all(), "Invalid Customer ID in Sales_Fact"
    assert sales_fact['Product ID'].isin(product_dim['Product ID']).all(), "Invalid Product ID in Sales_Fact"
    assert sales_fact['Order Date'].isin(time_dim['Order Date']).all(), "Invalid Order Date in Sales_Fact"
    assert sales_fact['Order ID'].isin(shipping_dim['Order ID']).all(), "Invalid Order ID in Sales_Fact"

    # Check for negative values in measures
    assert (sales_fact['Sales'] >= 0).all(), "Negative values found in Sales"
    assert (sales_fact['Profit'] >= 0).all(), "Negative values found in Profit"
    assert (sales_fact['Quantity'] >= 0).all(), "Negative values found in Quantity"
    assert (sales_fact['Discount'] >= 0).all(), "Negative values found in Discount"
    assert (sales_fact['Shipping Cost'] >= 0).all(), "Negative values found in Shipping Cost"

    # 3--- Validate Data Types

    # Check data types in dimension tables
    assert customer_dim['Customer ID'].dtype == 'object', "Invalid data type for Customer ID in Customer_Dim"
    assert product_dim['Product ID'].dtype == 'object', "Invalid data type for Product ID in Product_Dim"
    assert pd.api.types.is_datetime64_any_dtype(time_dim['Order Date']), "Invalid data type for Order Date in Time_Dim"
    assert shipping_dim['Order ID'].dtype == 'object', "Invalid data type for Order ID in Shipping_Dim"

    # Check data types in the fact table
    assert pd.api.types.is_numeric_dtype(sales_fact['Sales']), "Invalid data type for Sales in Sales_Fact"
    assert pd.api.types.is_numeric_dtype(sales_fact['Profit']), "Invalid data type for Profit in Sales_Fact"
    assert pd.api.types.is_numeric_dtype(sales_fact['Quantity']), "Invalid data type for Quantity in Sales_Fact"
    assert pd.api.types.is_numeric_dtype(sales_fact['Discount']), "Invalid data type for Discount in Sales_Fact"
    assert pd.api.types.is_numeric_dtype(sales_fact['Shipping Cost']), "Invalid data type for Shipping Cost in Sales_Fact"

    print("Data validation completed. No issues found.")   
    

def transform_data():
    # Load cleaned data
    customers = pd.read_csv('data/processed/customers_cleaned.csv')
    products = pd.read_csv('data/processed/products_cleaned.csv')
    sales = pd.read_csv('data/processed/sales_cleaned.csv')
    shipping = pd.read_csv('data/processed/shipping_cleaned.csv')
    time = pd.read_csv('data/processed/time_cleaned.csv')

    # Clean the 'Order Date' column
    sales['Order Date'] = sales['Order Date'].str.strip()
    time['Order Date'] = time['Order Date'].str.strip()

    # Debug: Inspect unique 'Order Date' values in raw data
    print("Unique 'Order Date' values in raw sales data:")
    print(sales['Order Date'].unique())

    print("Unique 'Order Date' values in raw time data:")
    print(time['Order Date'].unique())

    # Convert 'Order Date' to datetime format in cleaned datasets
    sales['Order Date'] = pd.to_datetime(sales['Order Date'], format='%Y-%m-%d', errors='coerce')
    time['Order Date'] = pd.to_datetime(time['Order Date'], format='%Y-%m-%d', errors='coerce')

    # Drop rows with NaT values in 'Order Date'
    sales = sales.dropna(subset=['Order Date'])
    time = time.dropna(subset=['Order Date'])

    # Debug: Inspect 'Order Date' after conversion
    print("Sample 'Order Date' values in cleaned sales dataset after conversion:")
    print(sales['Order Date'].head())

    print("Sample 'Order Date' values in cleaned time dataset after conversion:")
    print(time['Order Date'].head())

    # ---- Data Transformation ----
    # 1--- Create Dimension Tables

    # Customer Dimension
    customer_dim = customers[['Customer ID', 'Customer Name', 'Segment', 'City', 'State', 'Country', 'Region']]
    customer_dim = customer_dim.drop_duplicates(subset=['Customer ID'])

    # Product Dimension
    product_dim = products[['Product ID', 'Product Name', 'Category', 'Sub-Category']]
    product_dim = product_dim.drop_duplicates(subset=['Product ID'])

    # Time Dimension
    time_dim = time[['Order Date', 'order year', 'order month']]
    time_dim = time_dim.drop_duplicates(subset=['Order Date'])

    # Initialize missing_time_dim as an empty DataFrame
    missing_time_dim = pd.DataFrame(columns=['Order Date', 'order year', 'order month'])

    # Add missing Order Dates from sales to time_dim
    missing_dates = sales[~sales['Order Date'].isin(time_dim['Order Date'])]['Order Date'].drop_duplicates()
    if not missing_dates.empty:
        missing_time_dim = pd.DataFrame({
            'Order Date': missing_dates,
            'order year': missing_dates.dt.year,
            'order month': missing_dates.dt.month
        })
        time_dim = pd.concat([time_dim, missing_time_dim], ignore_index=True)

    # Debug: Check for missing dates
    print("Missing dates added to Time_Dim:")
    print(missing_time_dim)

    # Shipping Dimension
    shipping_dim = shipping[['Order ID', 'Ship Date', 'Ship Mode', 'Delivery Days', 'Shipping Cost']]
    shipping_dim = shipping_dim.drop_duplicates(subset=['Order ID'])

    # 2--- Create Fact Table

    # Merge sales data with shipping to get Shipping Cost
    sales_fact = sales.merge(
        shipping[['Order ID', 'Shipping Cost']], on='Order ID', how='left'
    )

    # Select relevant columns for the fact table
    sales_fact = sales_fact[[
        'Order ID', 'Product ID', 'Customer ID', 'Order Date', 
        'Sales', 'Profit', 'Quantity', 'Discount', 'Shipping Cost'
    ]]

    # Convert 'Order Date' in sales_fact to datetime format
    sales_fact['Order Date'] = pd.to_datetime(sales_fact['Order Date'], format='%Y-%m-%d', errors='coerce')

    # Debug: Inspect 'Order Date' in sales_fact
    print("Sample 'Order Date' values in sales_fact:")
    print(sales_fact['Order Date'].head())

    # Ensure no duplicates in the fact table
    sales_fact = sales_fact.drop_duplicates()

    # Validate that all Order Dates in sales_fact exist in time_dim
    missing_dates = sales_fact[~sales_fact['Order Date'].isin(time_dim['Order Date'])]
    if not missing_dates.empty:
        print("Warning: The following Order Dates are missing in Time_Dim:")
        print(missing_dates['Order Date'].unique())
    else:
        print("All Order Dates in Sales_Fact are present in Time_Dim.")

    # 3--- Validate Data Integrity

    # Check if all foreign keys in the fact table exist in dimension tables
    assert sales_fact['Customer ID'].isin(customer_dim['Customer ID']).all(), "Invalid Customer ID in fact table"
    assert sales_fact['Product ID'].isin(product_dim['Product ID']).all(), "Invalid Product ID in fact table"
    assert sales_fact['Order Date'].isin(time_dim['Order Date']).all(), "Invalid Order Date in fact table"
    assert sales_fact['Order ID'].isin(shipping_dim['Order ID']).all(), "Invalid Order ID in fact table"

    # 4--- Save Transformed Data

    # Save dimension tables
    customer_dim.to_csv('data/transformed/customer_dim.csv', index=False)
    product_dim.to_csv('data/transformed/product_dim.csv', index=False)
    time_dim.to_csv('data/transformed/time_dim.csv', index=False)
    shipping_dim.to_csv('data/transformed/shipping_dim.csv', index=False)

    # Save fact table
    sales_fact.to_csv('data/transformed/sales_fact.csv', index=False)

    print("Data transformation completed.")

# ---- Main Function ----
def main():
    clean_data()
    transform_data()
    validate_data()

if __name__ == "__main__":
    main()