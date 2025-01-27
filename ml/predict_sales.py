import joblib
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the saved model
model = joblib.load('best_linear_regression_model.pkl')

# Load the training data columns
training_columns = joblib.load('training_columns.pkl')

# Example new data (replace with actual data)
new_data = pd.DataFrame({
    'OrderYear': [2025],
    'OrderMonth': [1],
    'DayOfWeek': [2],
    'DayOfMonth': [27],
    'WeekOfYear': [4],
    'TotalProfit': [5000],
    'TotalQuantity': [100],
    'AvgDiscount': [0.1],
    'AvgShippingCost': [10]
})

# Ensure the columns are in the same order as the training data
new_data = new_data[training_columns]

# Make predictions
predictions = model.predict(new_data)
logging.info(f"Predicted Total Sales: {predictions[0]:.2f}")