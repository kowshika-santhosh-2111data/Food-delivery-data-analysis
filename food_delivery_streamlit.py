import streamlit  as st
st.set_page_config(layout="wide")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

st.title("Food Data Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Kowsh\OneDrive\Desktop\vscode_project\Food delivery project\data\food_delivery_cleaned.csv")
    return df
df = load_data()


with st.expander("Dataset Preview"):
    st.dataframe(df.head())

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Cities", df['City'].nunique())
col2.metric("Restaurants", df['Restaurant_Name'].nunique())
col3.metric("Customers", df['Customer_ID'].nunique())

st.header('Key Metrics')
total_orders = len(df)
total_revenue = df['Order_Value'].sum()
avg_order_value = df['Order_Value'].mean()
avg_delivery_time = df['Delivery_Time_Min'].mean()
avg_rating = df['Delivery_Rating'].mean()
cancel_rate = (df['Order_Status'].str.lower() == 'cancelled').mean() * 100

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)


col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3 = st.columns(1)[0]
col3.metric("Average Order Value", f"₹{avg_order_value:,.2f}")
col4.metric("Avg Delivery Time", f"{avg_delivery_time:.2f} min")
col5.metric("Cancellation Rate", f"{cancel_rate:.2f}%")
col6.metric("Avg Delivery Rating", f"{avg_rating:.2f}")

st.markdown("---")
st.header("Analytical Queries")
option = st.selectbox(  
    'Select a query to execute:',
    ('Identify top-spending customers',
     'Analyze age group vs order value',
     'Weekend vs weekday order patterns',
     'Monthly revenue trends',
     'Impact of discounts on profit',
     'High-revenue cities and cuisines',
     'Average delivery time by city',
     'Distance vs delivery delay analysis',
     'Delivery rating vs delivery time',
     'Top-rated restaurants',
    'Cancellation rate by restaurant',
    'Cuisine-wise performance',
    'Peak hour demand analysis',
    'Payment mode preferences',
    'Cancellation reason analysis'
)
)
if option == 'Identify top-spending customers':
    st.subheader("Top-Spending Customers")
    if st.button("Run Query",key="top_spenders"):
        top_spenders = df.groupby('Customer_ID')['Order_Value'].sum().nlargest(10).reset_index()
        st.dataframe(top_spenders)

elif option == 'Analyze age group vs order value':
    st.subheader("Age Group vs Order Value")
    if st.button("Run Query",key="age_order_value"):

        df['Age_Group'] = df['Customer_Age'].apply(
            lambda x: '18-25' if 18 <= x <= 25 else
                      '26-35' if 26 <= x <= 35 else
                      '36-45' if 36 <= x <= 45 else
                      '46-55' if 46 <= x <= 55 else
                      '55+'
        )
        age_order_value = df.groupby('Age_Group')['Order_Value'].mean().reset_index()
        st.dataframe(age_order_value)
        fig, ax = plt.subplots(figsize=(4,2.5))
        sns.barplot(data=age_order_value, x='Age_Group', y='Order_Value', ax=ax)
        ax.set_title('Average Order Value by Age Group',fontsize = 10)
        ax.set_xlabel('Age Group',fontsize = 9)
        ax.set_ylabel('Average Order Value',fontsize = 9)
        plt.xticks(rotation=0,fontsize = 8)
        plt.tight_layout()
        st.pyplot(fig)
        

elif option == 'Weekend vs weekday order patterns':
    st.subheader("Weekend vs Weekday Order Patterns")
    if st.button("Run Query",key="weekend_weekday"):

        temp_df = df.copy()
        # ---- create weekday/weekend ----
        temp_df['Order_Date'] = pd.to_datetime(temp_df['Order_Date'], dayfirst=True, errors='coerce')
        temp_df['Day_Type'] = temp_df['Order_Date'].dt.dayofweek.map(
            lambda x: 'weekend' if x >= 5 else 'weekday'
        )
        # ---- aggregation ----
        weekend_weekday = (
            temp_df.groupby('Day_Type')
              .agg(
                  Total_orders=('Day_Type','count'),
                  Total_revenue=('Order_Value','sum'),
                  avg_delivery_time=('Delivery_Time_Min','mean')
              ).reset_index()
        )
        st.dataframe(weekend_weekday)
        fig, ax = plt.subplots(figsize=(8,6))
        sns.barplot(data=weekend_weekday, x='Day_Type', y='Total_revenue', ax=ax, palette='Set2')
        ax.set_title('Weekend vs Weekday Order Patterns')
        ax.set_xlabel('Day Type')
        ax.set_ylabel('Total Revenue')
        st.pyplot(fig,use_container_width=True)

elif option == 'Monthly revenue trends':
    st.subheader("Monthly Revenue Trends")
    if st.button("Run Query", key="monthly_revenue"):
        df['Order_Date'] = pd.to_datetime(
            df['Order_Date'],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        )
        df['month'] = df['Order_Date'].dt.to_period('M').astype(str)
        df = df.dropna(subset=['Order_Date', 'Order_Value'])
        monthly_revenue = (
            df.groupby('month')
              .agg(
                  monthly_revenue=('Order_Value','sum'),
                  total_orders=('Order_Value','count'),
                  average_order_value=('Order_Value','mean')
              ).reset_index()
        )
        st.dataframe(monthly_revenue)
        fig, ax = plt.subplots(figsize=(12,6))
        sns.lineplot(data=monthly_revenue, x='month', y='monthly_revenue', marker='o', ax=ax)
        ax.set_title('Monthly Revenue Trends')
        ax.set_xlabel('Month')
        ax.set_ylabel('Monthly Revenue')
        plt.xticks(rotation=45)
        st.pyplot(fig,use_container_width=True)

elif option == 'Impact of discounts on profit':
    st.subheader("Impact of Discounts on Profit")
    if st.button("Run Query", key="discount_profit"):
        # create discount groups
        df['discount_category'] = pd.cut(
            df['Discount_percent'],
            bins=[-1,0,10,25,100],
            labels=[
                'No Discount',
                'Low Discount',
                'Medium Discount',
                'High Discount'
            ]
        )
        # aggregation
        discount_profit = (
            df.groupby('discount_category', observed=False)
              .agg(
                  total_orders=('discount_category','count'),
                  avg_profit=('Profit_Margin','mean'),
                  total_revenue=('Order_Value','sum')
              ).reset_index()
        )
        st.dataframe(discount_profit)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=discount_profit, x='discount_category', y='avg_profit',palette='husl', ax=ax)
        ax.set_title('Impact of Discounts on Profit')
        ax.set_xlabel('Discount Category')
        ax.set_ylabel('Average Profit')
        st.pyplot(fig,use_container_width=True)

elif option == 'High-revenue cities and cuisines':
    st.subheader("High-Revenue Cities and Cuisines")
    if st.button("Run Query",key="high_revenue"):
        high_revenue = (
            df.groupby(['City', 'Cuisine_Type'], observed=False)
              .agg(                  
                  total_revenue=('Order_Value','sum'),
              ).reset_index()
                
        )
        st.dataframe(high_revenue)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=high_revenue, x='City', y='total_revenue', hue='Cuisine_Type', ax=ax)
        ax.set_title('Top Performing Cuisine by City')
        ax.set_xlabel('City')
        ax.set_ylabel('Total Revenue')
        plt.xticks(rotation = 0)
        plt.tight_layout()
        st.pyplot(fig,use_container_width=True)

elif option == 'Average delivery time by city':
    st.subheader("Average Delivery Time by City")
    if st.button("Run Query",key="delivery_time_city"):
        delivery_time_city = (
            df.groupby(['City'],observed=False)
              .agg(
                  avg_delivery_time=('Delivery_Time_Min','mean')
              ).reset_index()
               .sort_values('avg_delivery_time', ascending=False)
        )
        st.dataframe(delivery_time_city)
        
elif option == 'Distance vs delivery delay analysis':
    st.subheader("Distance vs Delivery Delay Analysis")
    if st.button("Run Query",key="distance_delivery_delay"):
        distance_delivery_delay = (
            df.groupby(pd.cut(df['Distance_km'], bins=10), observed=False)      
               .agg(
                  avg_delivery_delay=('Delivery_Time_Min','mean'), 
                    total_orders=('Distance_km','count')
                ).reset_index()  
        )
        # ✅ converts interval → midpoint
        distance_delivery_delay['Distance_km'] = (
             distance_delivery_delay['Distance_km']
             .apply(lambda x: x.mid)   
)
        st.dataframe(distance_delivery_delay)

        fig, ax = plt.subplots(figsize=(6,4))
        sns.scatterplot(data=distance_delivery_delay, x='Distance_km', y='avg_delivery_delay', size='total_orders',sizes = (50,300),
                        alpha = 0.7,legend = 'brief', ax=ax)
        ax.set_title('Distance vs Average Delivery Delay')
        ax.set_xlabel('Distance (km)')
        ax.set_ylabel('Average Delivery Delay')
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig,use_container_width=True)

elif option == 'Delivery rating vs delivery time':
    st.subheader("Delivery Rating vs Delivery Time")
    if st.button("Run Query",key="rating_delivery_time"):
        rating_delivery_time = (
            df.groupby('Delivery_Rating', observed=False)
              .agg(
                    avg_delivery_time=('Delivery_Time_Min','mean')
                )
                .reset_index()
                .sort_values('avg_delivery_time', ascending=False)
        )
        st.dataframe(rating_delivery_time)
        
elif option == 'Top-rated restaurants':
    st.subheader("Top-Rated Restaurants")
    if st.button("Run Query",key="top_rated_restaurants"):
        top_rated_restaurants =(
             df.groupby('Restaurant_Name', observed=False)
               .agg(
                    top_rated_restaurants_Rating=('Delivery_Rating','max'),
                    total_orders=('Restaurant_Name','count')
                ).reset_index()
                 .sort_values(by='top_rated_restaurants_Rating',ascending=False)
                 .head(10)
        )
        st.dataframe(top_rated_restaurants)
    
elif option == 'Cancellation rate by restaurant':
    st.subheader("Cancellation Rate by Restaurant")
    if st.button("Run Query",key="cancellation_rate"):
        cancellation_rate = (
            df.groupby('Restaurant_Name')
                .agg(
                    total_orders=('Restaurant_Name','count'),
                    total_revenue=('Order_Value','sum'),
                    cancelled_orders=('Is_Cancelled','sum'),
                ).reset_index()
        )
        cancellation_rate['cancellation_rate_percent'] = (
            cancellation_rate['cancelled_orders'] * 100 / cancellation_rate['total_orders'] ).round(2)
        cancellation_rate = (
            cancellation_rate
                .sort_values(by=['cancellation_rate_percent','total_revenue'], ascending=False)
                .head(10)
        )
        st.dataframe(cancellation_rate)

elif option == 'Cuisine-wise performance':
    st.subheader("Cuisine-wise Performance")
    if st.button("Run Query",key="cuisine_performance"):
        cuisine_performance = (
            df.groupby('Cuisine_Type', observed=False)
              .agg(
                  total_orders=('Cuisine_Type','count'),
                  total_order_value=('Order_Value','sum'),
                  avg_delivery_time_min=('Delivery_Time_Min','mean'),
                  avg_order_value=('Order_Value','mean'),
                  avg_delivery_rating=('Delivery_Rating','mean')
              ).reset_index()
               .sort_values('total_order_value', ascending=False)
        )
        st.dataframe(cuisine_performance) 
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=cuisine_performance, x='Cuisine_Type', y='total_order_value', ax=ax, palette='Set2')
        ax.set_title('Cuisine-wise Performance')
        ax.set_xlabel('Cuisine Type')
        ax.set_ylabel('Total Order Value')
        st.pyplot(fig,use_container_width=True)

elif option == 'Peak hour demand analysis':
    st.subheader("Peak Hour Demand Analysis")
    if st.button("Run Query",key="peak_hour_demand"):
        #df['order_date'] = pd.to_datetime(df['order_date'])
        #df['hour'] = df['order_date'].dt.hour
        Peak_Hour = (
                df.groupby('Peak_Hour')
                .agg(
                        peak_hr_orders=('Peak_Hour','count'),
                        avg_delivery_time=('Delivery_Time_Min','mean'),
                        total_order_value=('Order_Value','sum'),
                    ).reset_index()
                     .sort_values(by='total_order_value',ascending=False)
        )       
        st.dataframe(Peak_Hour)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=Peak_Hour, x='Peak_Hour', y='total_order_value',palette='pastel',ax=ax)
        ax.set_title('Peak Hour Demand Analysis')
        ax.set_xlabel('Peak Hour')
        ax.set_ylabel('Total Order Value')
        st.pyplot(fig,use_container_width=True)

elif option == 'Payment mode preferences':
    st.subheader("Payment Mode Preferences")
    if st.button("Run Query",key="Payment_Mode"):
        df['Payment_Mode'] = df['Payment_Mode'].apply(
                            lambda x: 'Online' if x in ['UPI','Card','Wallet']
                              else 'Offline' if x == 'COD' else 'Other')
        payment_mode = (
            df.groupby('Payment_Mode', observed=False)
              .agg(
                    count=('Payment_Mode','count')
                ).reset_index()
                 .sort_values('count', ascending=False)
        )
        st.dataframe(payment_mode)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=payment_mode, x='Payment_Mode', y='count', ax=ax, palette='Set2')
        ax.set_title('Payment Mode Preferences')    
        ax.set_xlabel('Payment Mode')
        ax.set_ylabel('Count')
        st.pyplot(fig,use_container_width=True)

elif option == 'Cancellation reason analysis':
    st.subheader("Cancellation Reason Analysis")
    if st.button("Run Query", key="cancellation_reason_analysis"):
        df['Cancellation_Category'] = df['Cancellation_Reason'].str.lower().apply(
            lambda x: 'Restaurant Issue' if 'restaurant' in str(x)
            else 'Late Delivery' if 'late' in str(x) or 'delay' in str(x)
            else 'Customer Cancelled' if 'customer' in str(x)
            else 'Other'
        )
        cancellation_reason_analysis = (
            df[df['Order_Status'].str.lower() == 'cancelled']
            .groupby('Cancellation_Category')
            .agg(
                cancelled_orders=('Cancellation_Category','count'),
        ).reset_index()
         .sort_values('cancelled_orders', ascending=False)
        )
        st.dataframe(cancellation_reason_analysis)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.barplot(data=cancellation_reason_analysis, x='Cancellation_Category', y='cancelled_orders', ax=ax, palette='Set2')
        ax.set_title('Cancellation Reason Analysis')    
        ax.set_xlabel('Cancellation Category')
        ax.set_ylabel('Cancelled Orders')
        st.pyplot(fig,use_container_width=True)

