import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def create_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        logging.info("Connected to MySQL database")
        return connection
    except Exception as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

def load_sales_data(connection):
    """Load sales data from the DWH."""
    query = """
    SELECT 
        t.OrderDate,
        t.OrderYear,
        t.OrderMonth,
        SUM(f.Sales) AS TotalSales,
        SUM(f.Profit) AS TotalProfit,
        SUM(f.Quantity) AS TotalQuantity,
        AVG(f.Discount) AS AvgDiscount,
        AVG(f.ShippingCost) AS AvgShippingCost
    FROM Sales_Fact f
    JOIN Time_Dim t ON f.OrderDate = t.OrderDate
    GROUP BY t.OrderDate, t.OrderYear, t.OrderMonth
    ORDER BY t.OrderDate;
    """
    try:
        df = pd.read_sql(query, connection)
        logging.info("Sales data loaded successfully from DWH")
        return df
    except Exception as e:
        logging.error(f"Error loading sales data from DWH: {e}")
        return None

def preprocess_data(df):
    """Preprocess the data for time-series forecasting."""
    # Convert OrderDate to datetime
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    
    # Extract additional time-based features
    df['DayOfWeek'] = df['OrderDate'].dt.dayofweek
    df['DayOfMonth'] = df['OrderDate'].dt.day
    df['WeekOfYear'] = df['OrderDate'].dt.isocalendar().week
    
    # Drop the original OrderDate column (not needed for training)
    df = df.drop(columns=['OrderDate'])
    
    return df

def evaluate_model(model, X_test, y_test):
    """Evaluate the model and return performance metrics."""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    logging.info(f"Model: {model.__class__.__name__}")
    logging.info(f"Mean Squared Error: {mse:.4f}")
    logging.info(f"Mean Absolute Error: {mae:.4f}")
    return {
        "model": model.__class__.__name__,
        "mse": mse,
        "mae": mae
    }

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Train and evaluate multiple models."""
    models = {
        "Random Forest": RandomForestRegressor(random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
        "Linear Regression": LinearRegression()
    }
    
    best_model = None
    best_model_name = ""
    best_metrics = {"mse": float('inf'), "mae": float('inf')}
    
    for name, model in models.items():
        logging.info(f"Training {name}...")
        model.fit(X_train, y_train)
        
        logging.info(f"Evaluating {name}...")
        metrics = evaluate_model(model, X_test, y_test)
        
        # Check if this model is the best based on MSE and MAE
        if metrics["mse"] < best_metrics["mse"] and metrics["mae"] < best_metrics["mae"]:
            best_model = model
            best_model_name = name
            best_metrics = metrics
    
    logging.info(f"Best model: {best_model_name} with MSE: {best_metrics['mse']:.4f}, MAE: {best_metrics['mae']:.4f}")
    return best_model, best_model_name

def save_model(model, filename):
    """Save the trained model to a file."""
    joblib.dump(model, filename)
    logging.info(f"Model saved to {filename}")

# Main execution
if __name__ == "__main__":
    # Connect to the database and load data
    connection = create_connection()
    if connection:
        sales_data = load_sales_data(connection)
        connection.close()
        
        if sales_data is not None:
            # Preprocess the data
            sales_data = preprocess_data(sales_data)
            
            # Split the data into features (X) and target (y)
            X = sales_data.drop(columns=['TotalSales'])
            y = sales_data['TotalSales']
            
            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train and evaluate models
            best_model, best_model_name = train_and_evaluate_models(X_train, X_test, y_train, y_test)
            
            # Save the best model
            save_model(best_model, f"best_{best_model_name.lower().replace(' ', '_')}_model.pkl")

            # Save the training data columns
            joblib.dump(X.columns, 'training_columns.pkl')
        else:
            logging.error("Failed to load sales data from DWH.")
    else:
        logging.error("Failed to connect to the database.")