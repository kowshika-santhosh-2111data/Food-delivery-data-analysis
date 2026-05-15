# ONLINE FOOD DELIVERY
## 1.1	INTRODUCTION
This project analyses given online food delivery data. The objective is to analyse understand customer ordering behaviour, delivery performance, revenue trends and restaurant performance.
	The project includes:
  ```text
•	Data cleaning and pre-processing
•	Exploratory Data Analysis
•	SQL database creation  & querying
•	Interactive dashboard using streamlit
```
The goal is to generate business insights that will help improve delivery operations & customer satisfaction.

## 1.2	TOOLS AND TECHNOLOGIES USED
```text
•	For programming Language – Python
•	Libraries used – Pandas, NumPy, Matplotlib, Seaborn, SQLAlchemy
•	Database – MySQL
•	Dashboard – Streamlit
•	Development Tools used – Jupyter Notebook, VS code
```
## 1.3	DATASET DESCRIPTION
The dataset contains information relate to food delivery orders. Such as Customer info, Restaurant info, Cuisine details, Delivery information, order status, cancellation . 
Also includes Payment details, distance etc…

## 1.4	DATA CLEANING
```text
•	The data is prepared for analysis by being cleaned & pre-processed
•	Missing Values Handling.
o	Different methods were used depending on data distribution.
	Mean     --   calculated avg of Customer_Age, Order_Value
	Median  –   delivery_Time_Min, Distance_Km
	Mode     –   Categorical columns
•	Data type conversion  --   Columns were converted  into appropriate types.

•	Data standardization  --  Categorical value were standardized.

•	Handling outliers  -- outliers were handled using IQR method & clipping method to limit values.
```

## 1.5	EXPLORATORY DATA ANALYSIS
EDA is used to identify patterns & relationship in data.
```text
•	Univariate Analysis – used for distribution analysing.
•	Bivariate Analysis  --  Relationship between variable.
•	Multi variate Analysis  - correlation heatmap used to analyse relation between numerical variables.
```
## 1.6	DATABASE DESIGN
The dataset was stored in MySQL database using tables that creates a database by connecting all entities with foreign keys.
To obtain business insights, a number of SQL queries were created.

## 1.7	DASHBOARD
An interactive dashboard was built using streamlit. It allows users to analyse the data interactively.
Dashboard Features 
```text
•	Dataset preview
•	Key metrics display
•	Analytical query selection
•	Visualization using charts and graphs
```
## 1.8	KEY INSIGHTS
```text
•	Delivery time increases as delivery distance increases.
•	Weekend orders are higher compared to weekdays.
•	Online payment methods such as UPI & Card are widely used.
•	Late Delivery is one of the major reasons for cancellation of orders.
```
