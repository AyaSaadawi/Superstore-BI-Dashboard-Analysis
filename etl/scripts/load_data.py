import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

column_mappings = {
    'Customer_Dim': {
        'Customer ID': 'CustomerID',
        'Customer Name': 'CustomerName',
        'Segment': 'Segment',
        'City': 'City',
        'State': 'State',
        'Country': 'Country',
        'Region': 'Region'
    },
    'Product_Dim': {
        'Product ID': 'ProductID',
        'Product Name': 'ProductName',
        'Category': 'Category',
        'Sub-Category': 'SubCategory'
    },
    'Time_Dim': {
        'Order Date': 'OrderDate',
        'order year': 'OrderYear',
        'order month': 'OrderMonth'
    },
    'Shipping_Dim': {
        'Order ID': 'OrderID',
        'Ship Date': 'ShipDate',
        'Ship Mode': 'ShipMode',
        'Delivery Days': 'DeliveryDays',
        'Shipping Cost': 'ShippingCost'
    },
    'Sales_Fact': {
        'Order ID': 'OrderID',
        'Product ID': 'ProductID',
        'Customer ID': 'CustomerID',
        'Order Date': 'OrderDate',
        'Sales': 'Sales',
        'Profit': 'Profit',
        'Quantity': 'Quantity',
        'Discount': 'Discount',
        'Shipping Cost': 'ShippingCost'
    }
}

def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error creating connection: {e}")
    return connection

def check_connection(connection):
    """Check if the connection is still active."""
    if connection is None or not connection.is_connected():
        print("Connection is not active. Reconnecting...")
        return create_connection()
    return connection

def create_tables(connection):
    """Create the dimension and fact tables in the MySQL database."""
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS Customer_Dim (
        CustomerID VARCHAR(50) PRIMARY KEY,
        CustomerName VARCHAR(255),
        Segment VARCHAR(50),
        City VARCHAR(50),
        State VARCHAR(50),
        Country VARCHAR(50),
        Region VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS Product_Dim (
        ProductID VARCHAR(50) PRIMARY KEY,
        ProductName VARCHAR(255),
        Category VARCHAR(50),
        SubCategory VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS Time_Dim (
        OrderDate DATE PRIMARY KEY,
        OrderYear INT,
        OrderMonth INT
    );

    CREATE TABLE IF NOT EXISTS Shipping_Dim (
        OrderID VARCHAR(50) PRIMARY KEY,
        ShipDate DATE,
        ShipMode VARCHAR(50),
        DeliveryDays INT,
        ShippingCost DECIMAL(10, 2)
    );

    CREATE TABLE IF NOT EXISTS Sales_Fact (
        OrderID VARCHAR(50),
        ProductID VARCHAR(50),
        CustomerID VARCHAR(50),
        OrderDate DATE,
        Sales DECIMAL(10, 2),
        Profit DECIMAL(10, 2),
        Quantity INT,
        Discount DECIMAL(5, 2),
        ShippingCost DECIMAL(10, 2),
        PRIMARY KEY (OrderID, ProductID, CustomerID, OrderDate),
        FOREIGN KEY (CustomerID) REFERENCES Customer_Dim(CustomerID),
        FOREIGN KEY (ProductID) REFERENCES Product_Dim(ProductID),
        FOREIGN KEY (OrderDate) REFERENCES Time_Dim(OrderDate),
        FOREIGN KEY (OrderID) REFERENCES Shipping_Dim(OrderID)
    );
    """
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(create_tables_sql)
        print("Tables created successfully")
    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if cursor:
            cursor.close()

def load_data(connection, table_name, csv_file):
    cursor = None
    try:
        connection = check_connection(connection)
        if connection is None:
            print(f"Failed to load data into {table_name}: Connection not available")
            return
        
        cursor = connection.cursor()
        df = pd.read_csv(csv_file)

        # Debug: Print the original column names
        print(f"Original columns in {csv_file}:")
        print(df.columns)

        # Map CSV column names to MySQL column names
        if table_name in column_mappings:
            df.rename(columns=column_mappings[table_name], inplace=True)

        # Debug: Print the column names after renaming
        print(f"Columns after renaming for {table_name}:")
        print(df.columns)
        
        # Convert DataFrame to a list of tuples
        data = [tuple(row) for row in df.to_numpy()]
        
        # Escape column names with backticks
        columns = ', '.join([f'`{col}`' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        
        # Use INSERT IGNORE to handle duplicate entries
        insert_sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Debug: Print the generated SQL query
        print(f"Generated SQL for {table_name}: {insert_sql}")
        
        # Execute the INSERT statement and log skipped rows
        skipped_rows = []
        for row in data:
            try:
                cursor.execute(insert_sql, row)
            except Error as e:
                skipped_rows.append((row, str(e)))
        
        connection.commit()
        print(f"Data loaded successfully into {table_name}")
        
        if skipped_rows:
            with open("skipped_rows.log", "w") as log_file:
                for row, error in skipped_rows:
                    log_file.write(f"Row: {row}\nError: {error}\n\n")
            print(f"Warning: {len(skipped_rows)} rows skipped. See skipped_rows.log for details.")
        
    except Error as e:
        print(f"Error loading data into {table_name}: {e}")
    finally:
        if cursor:
            cursor.close()

def main():
    # Create a database connection
    connection = create_connection()
    
    if connection is not None:
        try:
            create_tables(connection)
            
            load_data(connection, 'Customer_Dim', 'data/transformed/customer_dim.csv')
            load_data(connection, 'Product_Dim', 'data/transformed/product_dim.csv')
            load_data(connection, 'Time_Dim', 'data/transformed/time_dim.csv')
            load_data(connection, 'Shipping_Dim', 'data/transformed/shipping_dim.csv')
            
            load_data(connection, 'Sales_Fact', 'data/transformed/sales_fact.csv')
        except Error as e:
            print(f"Error during data loading: {e}")
        finally:
            if connection.is_connected():
                connection.close()
                print("Database connection closed")
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()