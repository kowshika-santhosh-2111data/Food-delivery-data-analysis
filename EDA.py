import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
data = pd.read_csv("C:/Users/Kowsh/Documents/mini project/online food delivery/food_delivery_clean_colab_data.csv")
data.head()
data.isnull().sum()
num_cols = data.select_dtypes(include=['int64','float64']).columns
cat_cols = data.select_dtypes(include=['object','category']).columns
print("Numerical Columns:", num_cols)
print("Categorical Columns:", cat_cols)
# Summary statistics for numerical columns
print(data[num_cols].describe())

#Univariate Analysis
#analysing delivery time distribution
fig, ax = plt.subplots(1,2, figsize=(12,4))
sns.histplot(data['Delivery_Time_Min'], bins=40, kde=True, ax=ax[0])
sns.boxplot(x=data['Delivery_Time_Min'], ax=ax[1])
plt.show()

#analysing order value distribution
fig, ax = plt.subplots(1,2, figsize=(12,4))
sns.histplot(data['Order_Value'], bins=40, kde=True, ax=ax[0])
sns.boxplot(x=data['Order_Value'], ax=ax[1])
plt.show()

#BIVARIATE
for col in ['Cuisine_Type','Payment_Mode','Order_Status','Cancellation_Reason','Peak_Hour','Order_Day']:
    plt.figure(figsize=(6,4))
    sns.countplot(x=data[col])
    plt.title(f'Distribution of {col}')
    plt.xticks(rotation=45)
    plt.show()


#Weekend vs Weekday Demand
sns.countplot(data = data,x = 'Order_Day')
plt.xticks(rotation = 45)
plt.show()

#Distance vs Delivery Delay Relationship
sns.scatterplot(x='Distance_km', y='Delivery_Time_Min', data=data)
plt.show()


#Multi variate analysis
#Correlation Analysis Among Numeric Features
plt.figure(figsize=(10,6))
sns.heatmap(data[num_cols].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()