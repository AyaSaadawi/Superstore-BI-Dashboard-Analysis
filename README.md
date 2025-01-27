# Superstore Dataset Analysis and Dashboard

## Project Overview
This project delves into analyzing the Superstore dataset to uncover actionable insights that can drive business growth and sustainability. By leveraging Python for ETL (Extract, Transform, Load) processes, MySQL for data storage, and Power BI for visualization, the project provides an end-to-end solution for analyzing and visualizing sales, customer behavior, and profitability metrics. The final output includes a dynamic, interactive BI dashboard highlighting trends and patterns essential for strategic decision-making.

---

## Key Objectives

### Data Cleaning and Transformation
Address inconsistencies, missing values, and redundant information in the dataset to ensure accuracy and reliability.

### Data Warehouse Development
Design and implement a structured schema in MySQL for efficient querying and reporting.

### Data Analysis
Extract insights on sales trends, customer segmentation, and profitability metrics to identify growth opportunities.

### Data Visualization
Develop an interactive Power BI dashboard to present findings effectively and support data-driven decision-making.

### Machine Learning Integration
Incorporate predictive analytics using machine learning models to forecast sales and enhance decision-making capabilities.

---

## Project Features

### ETL Pipeline
A comprehensive process to extract, clean, transform, and load data into MySQL for structured analysis.

### Database Schema Design
A star schema with the following components:

- *Fact Table:* Sales
- *Dimension Tables:*
  - Customers
  - Products
  - Regions
  - Time

### Interactive Dashboard
Power BI visualizations to explore:
- Regional sales performance
- Product category and segment trends
- Profitability metrics
- Customer demographics
- Sales forecasts using machine learning models

### Machine Learning Models
Sales Forecasting: Predict future sales using a Linear Regression model trained on historical sales data.

Model Comparison: Evaluate multiple models (Random Forest, Gradient Boosting, Linear Regression) to select the best-performing one based on metrics like Mean Squared Error (MSE) and Mean Absolute Error (MAE).

---

## Technologies Used

- *Python:* For ETL processes, utilizing libraries such as pandas and numpy.
- *MySQL:* Robust database for efficient data storage and querying.
- *Power BI:* For creating intuitive and interactive dashboards.
- *CSV:* Input format for raw data.
- *Excel:* Input format for raw data.
- *Scikit-learn:* For building and evaluating machine learning models.
- *Joblib:* For saving and loading trained models.

---

## Dataset

- *Source:* Kaggle’s Superstore dataset
- *Structure:*
  - Orders.csv: Detailed sales, order, and shipping information.
  - Customers.xlsx: Customer demographics and segmentation.
  - Products.csv: Product categories and specifications.
  - Shipping.xlsx: Shipping information.
  - Time.csv: Encapsulates temporal details for time-based analysis

---

## Key Files

### ETL Process
- extract_data.py: Script for extracting data from multiple data sources.
- transform_data.py: Script for cleaning and transforming the dataset.
- load_data.py: Script to load cleaned data into the MySQL DWH.

### Machine Learning
- ml_sales_prediction.py: Script to train and evaluate machine learning models for sales forecasting.
- predict_sales.py: Script to make predictions using the trained model.

### Data Files
- product data.csv
- sales data.csv
- shipping data.xlsx
- customer data.xlsx
- time data.csv

### Visualization
- project_bi_dashboard.pbix: Power BI dashboard file.

---

## How to Run the Project

### Step 1: Set Up the Environment
Clone this repository:
git clone https://github.com/AyaSaadawi/Superstore-BI-Dashboard-Analysis

### Step 2: Execute the ETL Process
1. Run extract_data.py to extract raw datasets:
   
   python extract_data.py
   
2. Run transform_data.py to clean and transform raw datasets:
   
   python data_cleaning.py
   
3. Run load_data.py to load data to the MySQL DWH:

   python load_data.py

### Step 3: Train and Evaluate Machine Learning Models
1. Run ml_sales_prediction.py to train and evaluate models:
    python ml_sales_prediction.py

2. Run predict_sales.py to make predictions using the trained model:
    python predict_sales.py

### Step 4: Visualize Data
Open project_bi_dashboard.pbix in Power BI and explore interactive visualizations.

---

## Key Insights

- *Regional Sales:* Highest sales observed in the West region.
- *Product Trends:* Office supplies consistently outperformed other categories.
- *Profitability:* High-profit margins in specific product sub-categories such as binders and art supplies.
- *Customer Insights:* Repeat customers contributed significantly to overall revenue.
- *Sales Forecasts:* Predictions for future sales using machine learning models.

---

## Future Work

- Incorporate machine learning models for predictive analysis.
- Extend the dashboard to include real-time data updates.
- Enhance visualizations for mobile accessibility.
- Deploy the machine learning model as an API for real-time predictions.
---

## Contributing
Contributions are welcomed! If you have ideas for improvement or new features, feel free to fork the repository and submit a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Datasets sourced from Kaggle for educational purposes.
- Thanks to the open-source community for tools and libraries used in this project.
