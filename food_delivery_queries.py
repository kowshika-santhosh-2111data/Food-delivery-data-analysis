import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pprint import pprint
from sqlalchemy import select,func,and_,desc,case,text

password = quote_plus("Kowshika*1999")

engine = sqlalchemy.create_engine(
    f"mysql+pymysql://root:{password}@localhost/food_delivery_cleaned",echo = True)
Connection = engine.connect()
metadata = sqlalchemy.MetaData()
food_delivery = sqlalchemy.Table(
    'food_delivery',
    metadata,
    autoload_with=engine)   
#Identify top-spending customers
q1 = (
    select(
        food_delivery.c.Customer_ID,
        func.sum(food_delivery.c.Order_Value).label('Total_Spent'),
        func.max(food_delivery.c.Order_Value).label('Max_Order_Value')
    )
    .group_by(food_delivery.c.Customer_ID)
    .order_by(desc('Total_Spent'))
    .limit(10)
)
df_top_spenders = pd.read_sql(q1, engine)
print("Top-Spending Customers:")
print(df_top_spenders)
#Analyze age group vs order value
from sqlalchemy import select, case, func, desc

q2 = (
    select(
        case(
            
                (food_delivery.c.Customer_Age < 18, 'Under 18'),
                (and_(food_delivery.c.Customer_Age >= 18, food_delivery.c.Customer_Age < 25), '18-25'),
                (and_(food_delivery.c.Customer_Age >= 26, food_delivery.c.Customer_Age < 35), '26-35'),
                (and_(food_delivery.c.Customer_Age >= 36, food_delivery.c.Customer_Age < 45), '36-45'),
                (and_(food_delivery.c.Customer_Age >= 46, food_delivery.c.Customer_Age < 55), '45-55'),
                (food_delivery.c.Customer_Age >= 56, '55+')
            ,
            else_='Other'
        ).label('Age_Group'),
        func.count().label('Order_Count'),
        func.avg(food_delivery.c.Order_Value).label('Average_Order_Value'),
        func.sum(food_delivery.c.net_revenue).label('Total_Net_Revenue')
    )
    .group_by('Age_Group')
    .order_by(desc('Total_Net_Revenue'))
)
df_age_order_value = pd.read_sql(q2, engine)
print("Age Group vs Order Value:")
print(df_age_order_value)


#Weekend vs weekday order patterns

Day_Type = case(
    (func.dayofweek(food_delivery.c.Order_Date)
    .in_(['Saturday','Sunday']), "Weekend"),
    others ="Weekday"
    ).label("day_type")

q3= (
    select(
        Day_Type,
        func.count().label("total_orders"),
        func.sum(food_delivery.c.Net_Revenue).label("total_revenue"),
        func.avg(food_delivery.c.Delivery_time_min).label("average_delivery_time")
    )
    .group_by(Day_Type)
)
df_weekend_weekday = pd.read_sql(q3, engine)
print("Weekend vs Weekday Order Patterns:")
print(df_weekend_weekday)



#Monthly revenue trends
#month_name_case = case(
   # (func.month(food_delivery.c.Order_Date) == 1, 'January'),
   # (func.month(food_delivery.c.Order_Date) == 2, 'February'),
    #(func.month(food_delivery.c.Order_Date) == 3, 'March'),
    #(func.month(food_delivery.c.Order_Date) == 4, 'April'),
    #(func.month(food_delivery.c.Order_Date) == 5, 'May'),
    #(func.month(food_delivery.c.Order_Date) == 6, 'June'),
    #(func.month(food_delivery.c.Order_Date) == 7, 'July'),
    #(func.month(food_delivery.c.Order_Date) == 8, 'August'),
    #(func.month(food_delivery.c.Order_Date) == 9, 'September'),
    #(func.month(food_delivery.c.Order_Date) == 10, 'October'),
    #(func.month(food_delivery.c.Order_Date) == 11, 'November'),
    #(func.month(food_delivery.c.Order_Date) == 12, 'December')
#).label('month_name')

#year_case = case(
 #   (func.year(food_delivery.c.Order_Date) == 2023, '2023'),
  #  (func.year(food_delivery.c.Order_Date) == 2024, '2024'),
   # else_='Other'
#).label('year')

#q4 = (
 #   select(
#      month_name_case,
 #    year_case,
  #      func.date_format(food_delivery.c.Order_Date, '%Y-%m').label('month_year'),
   #     func.sum(food_delivery.c.order_value).label('monthly_revenue'),
    #    func.count().label('total_orders'),
     #   func.avg(food_delivery.c.order_value).label('average_order_value')
    #)
    #.group_by(month_name_case, year_case)
    #.order_by(func.date_format(food_delivery.c.Order_Date, '%Y-%m'))
#)




# --- clean date conversion ---
clean_date = case(
    (food_delivery.c.order_date.like('%/%'),
     func.str_to_date(food_delivery.c.order_date, '%m/%d/%Y')),
    else_=func.str_to_date(food_delivery.c.order_date, '%d-%m-%Y')
).label("clean_date")

# --- month-year label ---
month_year = func.date_format(clean_date, '%Y-%m').label("month")

# --- query ---
q4 = (
    select(
        month_year,
        func.sum(food_delivery.c.order_value).label("monthly_revenue"),
        func.count().label("total_orders"),
        func.avg(food_delivery.c.order_value).label("average_order_value")
    )
    .where(clean_date.isnot(None))
    .group_by(month_year)
    .order_by(month_year)
)
df_monthly_revenue = pd.read_sql(q4, engine)
print("Monthly Revenue Trends:")    
print(df_monthly_revenue)


#Impact of discounts on profit
discount_category = case(
    (food_delivery.c.discount_percent == 0, 'no discount'),
    (and_(food_delivery.c.discount_percent > 0,
          food_delivery.c.discount_percent <= 10), 'low discount'),
    (and_(food_delivery.c.discount_percent > 10,
          food_delivery.c.discount_percent <= 25), 'medium discount'),
    else_='high discount'
).label('discount_category')

q5 = (
    select(
        food_delivery.c.City,
        discount_category,
        func.count().label('order_count'),
        func.avg(food_delivery.c.Profit_Margin).label('avg_profit_margin'),
        func.sum(food_delivery.c.Net_Revenue).label('total_net_revenue')
    )
    .group_by(food_delivery.c.City, discount_category)
    .order_by(desc('avg_profit_margin'))
)

df_discount_profit = pd.read_sql(q5, engine)
#High-revenue cities and cuisines
q6 = (
    select(
        food_delivery.c.City,
        food_delivery.c.Cuisine_Type,
        func.sum(food_delivery.c.Order_Value).label('total_revenue')
    )
    .group_by(food_delivery.c.City, food_delivery.c.Order)
    .order_by(desc('total_revenue'))
    .limit(10)
)
df_high_revenue = pd.read_sql(q6, engine)
print("High-Revenue Cities and Cuisines:")
print(df_high_revenue)
#Average delivery time by city
q7 = (
    select(
        food_delivery.c.city,
        food_delivery.c.delivery_time_min,
        func.avg(food_delivery.c.delivery_time_min).label('avg_delivery_time_min')
    )
    .group_by(food_delivery.c.city,food_delivery.c.delivery_time_min)
    .order_by(desc('avg_delivery_time_min'))
    .limit(10)
)
df_delivery_time_city = pd.read_sql(q7, engine)
print("Average Delivery Time by City:")
print(df_delivery_time_city)

#Distance vs delivery delay analysis
q8 = (
    select(
        food_delivery.c.Distance_km,
        func.avg(food_delivery.c.delivery_delay).label('avg_delivery_delay'),
        func.count().label('total_orders')
    )
    .group_by(food_delivery.c.Distance_km)
    .order_by(desc('avg_delivery_delay'))
    .limit(10)
)
df_distance_delivery_delay = pd.read_sql(q8, engine)
print("Distance vs Delivery Delay Analysis:")
print(df_distance_delivery_delay)
#Delivery rating vs delivery time
q9 = (
    select(
        food_delivery.c.Delivery_Rating,
        func.avg(food_delivery.c.Delivery_Time_Min).label('avg_delivery_time')
    )
    .group_by(food_delivery.c.Delivery_Rating)
    .order_by(desc('avg_delivery_time'))
)
df_rating_delivery_time = pd.read_sql(q9, engine)
print("Delivery Rating vs Delivery Time:")
print(df_rating_delivery_time)

#Top-rated restaurants
q10  = (
    select(
        food_delivery.c.Restaurant_Name,
        func.max(food_delivery.c.Delivery_Rating).label('top_rating'),
        func.count().label('total_orders')
    )
    .group_by(food_delivery.c.Restaurant_Name)
    .order_by(desc('top_rating'))
    .limit(10)
)
df_top_rated_restaurants = pd.read_sql(q10, engine)
print("Top-Rated Restaurants:")
print(df_top_rated_restaurants)
#Cancellation rate by restaurant
q11  = (
    select(
        food_delivery.c.Restaurant_Name,
        func.count().label('total_orders'),
        func.sum(food_delivery.c.Is_Cancelled).label('cancelled_orders'),
        func.round(
            func.sum(food_delivery.c.Is_Cancelled)*100/func.count(),2).label('cancellation_rate_percent')
    )
    .group_by(food_delivery.c.Restaurant_Name)
    .order_by(desc('cancellation_rate_percent'))
    .limit(10)
)   
df_cancellation_rate = pd.read_sql(q11, engine)
print("Cancellation Rate by Restaurant:")
print(df_cancellation_rate)

#Cuisine-wise performance
q12 = (
    select(
        food_delivery.c.Cuisine_Type,
        func.count().label('total_orders'),
        func.sum(food_delivery.c.Order_Value).label('total_order_value'),
        func.avg(food_delivery.c.Delivery_Time_Min).label('avg_delivery_time_min'),
        func.avg(food_delivery.c.Order_Value).label('avg_order_value'),
        func.avg(food_delivery.c.Delivery_Rating).label('avg_delivery_rating')
    )
    .group_by(food_delivery.c.Cuisine_Type)
    .order_by(desc('total_order_value'))
)
df_cuisine_performance = pd.read_sql(q12, engine)
print("Cuisine-wise Performance:")
print(df_cuisine_performance)
#Peak hour demand analysis
q13 = (
    select(
        func.hour(food_delivery.c.Peak_Hour).label('Peak_Hour'),
        func.count().label('peak_hour_orders'),
        func.avg(food_delivery.c.Delivery_Time_Min).label('avg_delivery_time')
    )
    .group_by(func.hour(food_delivery.c.Peak_Hour))
    .order_by(func.hour(food_delivery.c.Peak_Hour))
)
df_peak_hour_demand = pd.read_sql(q13, engine)
print("Peak Hour Demand Analysis:")
print(df_peak_hour_demand)

#Payment mode preferences
q14 = (
    select(
        case(
            (food_delivery.c.Payment_Mode.in_(['Credit Card', 'Card','UPI']), 'online'),
            (food_delivery.c.Payment_Mode.in_(['Cash','COD']), 'offline'),
            else_='other'
        ).label('payment_mode_category'),
        food_delivery.c.Payment_Mode,
        func.count().label('count')
    )
    .group_by(food_delivery.c.Payment_Mode)
    .order_by(desc('count'))
)
df_payment_mode_preferences = pd.read_sql(q14, engine)
print("Payment Mode Preferences:")
print(df_payment_mode_preferences)

#Cancellation reason analysis

cancellation_category = case(
    (food_delivery.c.Cancellation_Reason.like('%Customer%'), 'Customer Cancelled'),
    (food_delivery.c.Cancellation_Reason.like('%Restaurant%'), 'Restaurant Issue'),
    ((food_delivery.c.Cancellation_Reason.like('%Late%')) |
     (food_delivery.c.Cancellation_Reason.like('%Delay%')), 'Late Delivery'),
    else_='Other'
).label('Cancellation_Category')
q15 = (
    select(
        cancellation_category,
        func.count().label('total_cancellations')
    )
    .where(food_delivery.c.Order_Status == 'Cancelled')
    .group_by(cancellation_category)
    .order_by(desc('total_cancellations'))
)
df_cancellation_reason_analysis = pd.read_sql(q15, engine)
print("Cancellation Reason Analysis:")
print(df_cancellation_reason_analysis)