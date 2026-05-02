import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('/content/ONINE_FOOD_DELIVERY_ANALYSIS.csv')
data.head()

data.shape

data.info()

data.describe()

missing_count = data.isnull().sum()
print(missing_count)

missing_pct = (data.isnull().sum()/len(data))*100
print(missing_pct)

#Handle missing value
numeric = data.select_dtypes(include = ['int64','float64']).columns
numeric

data.isnull().sum()

numeric = pd.DataFrame({
    'Missing Count': missing_count,
    'Missing Percentage': missing_pct,
    'Data type': data.dtypes
})

print(numeric[numeric['Missing Count'] > 0].sort_values('Missing Percentage', ascending=False))

numeric

skew_values = data[['Customer_Age',
 'Delivery_Time_Min',
 'Distance_km',
 'Order_Value',
 'Discount_Applied',
 'Final_Amount',
 'Delivery_Rating',
 'Restaurant_Rating',
 'Profit_Margin']].skew()
print(skew_values)

data.describe()

numeric = ['Customer_Age', 'Delivery_Time_Min', 'Distance_km', 'Order_Value',
       'Discount_Applied', 'Final_Amount', 'Delivery_Rating',
       'Restaurant_Rating', 'Profit_Margin']
#handling mean
mean = mean_cols = ['Customer_Age','Order_Value','Delivery_Rating',
                    'Restaurant_Rating','Profit_Margin']

median = ['Delivery_Time_Min','Distance_km','Discount_Applied',
          'Final_Amount']
#fill with mean
for cols in mean:
  data[cols].fillna(data[cols].mean(),inplace= True)

#fill with median
for cols in median:
  data[cols].fillna(data[cols].median(),inplace = True)

categorical = data.select_dtypes(include=['object','category']).columns
categorical

#fill with mode
for cols in categorical:
  data[cols].fillna(data[cols].mode()[0],inplace=True)

#duplicate
data.duplicated().sum()

#convert data types
from datetime import date
# ID columns
data['Order_ID'] = data['Order_ID'].astype(str)
data['Customer_ID'] = data['Customer_ID'].astype(str)
data['Restaurant_ID'] = data['Restaurant_ID'].astype(str)
data['Delivery_Partner_ID'] = data['Delivery_Partner_ID'].astype(str)

# categorical columns
data['Customer_Gender'] = data['Customer_Gender'].astype('category')
data['City'] = data['City'].astype('category')
data['Area'] = data['Area'].astype('category')
data['Cuisine_Type'] = data['Cuisine_Type'].astype('category')
data['Payment_Mode'] = data['Payment_Mode'].astype('category')
data['Order_Status'] = data['Order_Status'].astype('category')
data['Cancellation_Reason'] = data['Cancellation_Reason'].astype('category')

# date & time
data['Order_Date'] = pd.to_datetime(data['Order_Date'], errors='coerce')
data['Order_Time'] = pd.to_datetime(data['Order_Time'], errors='coerce')

# numeric columns
data['Customer_Age'] = data['Customer_Age'].astype(float)
data['Delivery_Time_Min'] = data['Delivery_Time_Min'].astype(int)
data['Distance_km'] = data['Distance_km'].astype(float)
data['Order_Value'] = data['Order_Value'].astype(float)
data['Discount_Applied'] = data['Discount_Applied'].astype(float)
data['Final_Amount'] = data['Final_Amount'].astype(float)
data['Delivery_Rating'] = data['Delivery_Rating'].astype(float)
data['Restaurant_Rating'] = data['Restaurant_Rating'].astype(float)
data['Profit_Margin'] = data['Profit_Margin'].astype(float)

#check invalid numeric values
['Customer_Age','Delivery_Time_Min','Distance_km',
'Order_Value','Final_Amount','Profit_Margin','Delivery_Rating',
'Restaurant_Rating']
data[data['Customer_Age']<0]
data[(data['Delivery_Time_Min']>30)|(data['Delivery_Time_Min']<90)]
data[data['Delivery_Rating']<1|(data['Delivery_Rating']>5)]
data[data['Restaurant_Rating']<1|(data['Restaurant_Rating']>5)]

#check date & time format
data['Order_Date'] = pd.to_datetime(data['Order_Date'], errors='coerce')
data['Order_Date'].fillna(data['Order_Date'].mode()[0],inplace = True)

data['Order_Time'] = pd.to_datetime(data['Order_Time'], errors='coerce')
data['Order_Time'].fillna(data['Order_Time'].mode()[0],inplace = True)

data[['Order_Date','Order_Time']]

#handling string operation
#remove special charcters
data['Cuisine_Type'] = data['Cuisine_Type'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
#standaredize gender value
data['Customer_Gender'] = data['Customer_Gender'].str.replace(r'(?i)^m.*', 'Male', regex=True)
data['Customer_Gender'] = data['Customer_Gender'].str.replace(r'(?i)^f.*', 'Female', regex=True)
#standardize payment mode
data['Payment_Mode'] = data['Payment_Mode'].str.title()
#remove multiple space
data['Area'] = data['Area'].str.replace(r'\s+', ' ', regex=True)
#standardize time format
data['Order_Time'] = pd.to_datetime(data['Order_Time'], errors='coerce').dt.time
#detcet invalid charcters
data[data['City'].str.contains(r'[^a-zA-Z\s]', na=False)]

data['Peak_Hour'].unique()

#check catogorical inconsistency
#= [Customer_Gender,City,Area,Cuisine_Type,
#Payment_Mode,Order_Status,Cancellation_Reason]

#check string inconsistent data
data_inconsistent = {
    'Customer_Gender':['Female', 'Male', 'Other'],
    'City': ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Mumbai'],
    'Area': ['Central', 'East', 'North', 'South', 'West'],
    'Cuisine_Type':['Arabian', 'Chinese', 'Indian', 'Italian', 'Mexican'],
    'Payment_Mode':['COD', 'Card', 'UPI', 'Wallet'],
    'Order_Status':['Cancelled', 'Delivered'],
    'Cancellation_Reason': ['Customer Cancelled', 'Late Delivery', 'Restaurant Issue']

}

#standardize
data['Customer_Gender'] = data['Customer_Gender'].replace({
    'm': 'Male',
    'male': 'Male',
    'f': 'Female',
    'female': 'Female',
    'others': 'Other',
    'other': 'Other'
})

data['City'] = data['City'].replace({
    'che':'Chennai',
    'chennai':'Chennai',

    'delhi' :'Delhi',
    'mumbai':'Mumbai',
    'banglore':'Banglore',
    'hyderabad':'Hyderabad'
})

data['Area'] = data['Area'].replace({
    'central':'Central',
    'north':'North',
    'south':'South',
    'east':'East',
    'west':'West'
})

data["Cuisine_Type"] = data["Cuisine_Type"].replace({
    "arabian": "Arabian",
    "indian": "South Indian",
    "chinese": "Chinese",
    "italian":"Italian",
    "mexican":"Mexican"
})

data['Payment_Mode'] = data['Payment_Mode'].replace({
    "upi payment" :"UPI",
    "upi_payement": "UPI",
    "Cash On Delivery":"COD",
    'cod':'COD',
    'card':'Card',
    "Card":"Card",
    "Wallet":"Wallet"
})

data['Cancellation_Reason'] = data['Cancellation_Reason'].replace({
    'late delivery':'Late Delivery',
    'restaurant issue':'Restaurant Issue',
    'customer cancelled':'Customer Cancelled'
})

#check logical inconsistency
#delivered  should not have c.reason
data[(data['Order_Status']=='Delivered') & (data['Cancellation_Reason'].isna())]
#cancelled  - have reasons
data[(data['Order_Status'] == 'Cancelled') & (data['Cancellation_Reason'].isna())]
#final amount should not exceed order value
data[data['Final_Amount'] > data['Order_Value']]

#numeric range validation
# age should be positive
data = data[data['Customer_Age'] > 0]
# distance should not be negative
data = data[data['Distance_km'] >= 0]
# ratings must be between 1 and 5
data = data[(data['Delivery_Rating'] >= 1) & (data['Delivery_Rating'] <= 5)]

#feature engineeging

data['Profit_Margin'] = data['Final_Amount'] - data['Order_Value']

numeric

(data[['Customer_Age', 'Delivery_Time_Min', 'Distance_km', 'Order_Value',
       'Discount_Applied', 'Final_Amount', 'Delivery_Rating', 'Restaurant_Rating',
       'Profit_Margin']].skew())

(data['Customer_Age'].skew())*100

"""for customer age & restaturant rating no need to handel outliers because -0.42 & 0.07"""

#outlier
#n0rmal
outlier_cols = ['Delivery_Rating']
for col in outlier_cols:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = data[(data[col] < lower) | (data[col] > upper)]

    print(f"{col} → {len(outliers)} outliers ({len(outliers)/len(data)*100:.2f}%)")

#removing outliers #high skewed
cols =['Delivery_Time_Min', 'Distance_km','Order_Value',
       'Discount_Applied','Final_Amount','Profit_Margin']

for col in cols:

        lower = data[col].quantile(0.01)
        upper = data[col].quantile(0.99)

        outliers = data[
            (data[col] < lower) |
            (data[col] > upper)
        ]

        print(f"{col} → {len(outliers)} outliers ({len(outliers)/len(data)*100:.2f}%)")

        # Now clip
        data[col] = data[col].clip(lower, upper)

data.isna().sum()

