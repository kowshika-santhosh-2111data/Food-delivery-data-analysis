create database food_delivery;
use food_delivery;

CREATE TABLE Customers (
    Customer_ID VARCHAR(50) PRIMARY KEY,
    Customer_Age INT,
    Customer_Gender VARCHAR(20),
    City VARCHAR(50),
    Area VARCHAR(50)
);
CREATE TABLE Restaurants (
    Restaurant_ID VARCHAR(50) PRIMARY KEY,
    Restaurant_Name VARCHAR(100),
    Cuisine_Type VARCHAR(50),
    Restaurant_Rating DECIMAL(3,2)
);
CREATE TABLE Delivery_Partners (
    Delivery_Partner_ID VARCHAR(50) PRIMARY KEY
);
CREATE TABLE Orders (
    Order_ID VARCHAR(50) PRIMARY KEY,
    
    Customer_ID VARCHAR(50),
    Restaurant_ID VARCHAR(50),
    Delivery_Partner_ID VARCHAR(50),

    Order_Date DATE,
    Order_Time TIME,
    Order_Day VARCHAR(20),
    Peak_Hour VARCHAR(20),

    Order_Value DECIMAL(10,2),
    Discount_Applied DECIMAL(10,2),
    Final_Amount DECIMAL(10,2),
    Profit_Margin DECIMAL(6,4),

    Payment_Mode VARCHAR(30),
    Order_Status VARCHAR(30),
    Cancellation_Reason VARCHAR(100),
	is_cancalled boolean,
    Delivery_Time_Min INT,
    Distance_km DECIMAL(6,2),
    Delivery_Rating DECIMAL(3,2),
	net_revenue decimal,
    -- Foreign Keys
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Restaurant_ID) REFERENCES Restaurants(Restaurant_ID),
    FOREIGN KEY (Delivery_Partner_ID) REFERENCES Delivery_Partners(Delivery_Partner_ID)
);

show tables;
select database();
select count(*) from food_delivery;

select * 
from food_delivery;

#customer & order analysis
select 
    Customer_ID,
    count(Order_ID) as Total_Orders,
    sum(Order_Value) as Total_Spent,
    max(Order_Value) as Max_Order_Value
from food_delivery
group by Customer_ID
order by Total_Spent desc
limit 10;

select 
	case
		when customer_Age < 18 then 'under 18'
		when customer_Age between 18 and 25 then '18-25'
        when customer_Age between 26 and 35 then '26-35'
        when customer_Age between 36 and 45 then '36-45'
        when customer_Age between 46 and 55 then '46-55'
        when customer_Age >= 56 then '55+'
        else 'other'
	end as Age_Group,
    
    count(*) as Total_Orders,
    avg(Order_Value) as Avg_Order_Value,
    sum(net_revenue) as Total_Revenue
from food_delivery
group by Age_Group
order by Total_Revenue desc;

select
    case
        when dayofweek(
            case
                when order_date like '%/%'
                    then str_to_date(order_date,'%m/%d/%Y')
                else str_to_date(order_date,'%d-%m-%Y')
            end
        ) in (1,7)
        then 'weekend'
        else 'weekday'
    end as day_type,

    count(*) as total_orders,
    sum(net_revenue) as tot_revenue,
    round(avg(delivery_time_min),2) as avg_deli_time

from food_delivery
group by day_type;


alter table orders
add Order_Year YEAR,
add Order_Month VARCHAR(20);

#Revenue & profit analysis
select
    date_format(clean_date,'%Y-%m') as month,
    sum(order_value) as monthly_revenue,
    count(*) as total_orders,
    avg(order_value) as average_order_value
from (
    select *,
        case
            when order_date like '%/%'
                then str_to_date(order_date,'%m/%d/%Y')
            else str_to_date(order_date,'%d-%m-%Y')
        end as clean_date
    from food_delivery
) t
group by month
order by month;


#Impact of discounts on profit
select 
	case
		when discount_percent = 0 then 'no discount'
        when discount_percent between 1 and 10 then 'low discount'
        when discount_percent between 11 and 25 then 'medium discount'
        else 'high discount'
	end as Discount_Category,
    
    count(*) as orders,
    avg(profit_margin) as avg_profit,
    sum(net_revenue) as  tot_revenue
    
    from food_delivery
    group by Discount_Category
    order by avg_profit desc;
    
   # select d.discount_category,
    #   count(f.discount_percent) as total_orders,
     #  avg(f.profit_margin) as avg_profit,
      # sum(f.net_revenue) as total_revenue
#from (
 ##  union all select 'Low Discount'
   # union all select 'Medium Discount'
    #union all select 'High Discount'
#) #d
#left join food_delivery f
#on (
 #   case
  #      when f.discount_percent = 0 then 'No Discount'
   ##    when f.discount_percent <= 25 then 'Medium Discount'
     #   else 'High Discount'
    #end = d.discount_category
#)
#group by d.discount_category;

#high revenue cities & cuisine
select 
	city, cuisine_type,
    sum(order_value) as tot_revenue
	from food_delivery
    group by city, cuisine_type
    order by tot_revenue desc
    limit 10;

#DELIVERY PERFORMACE
#Average delivery time by city

select 	City,
        avg(Delivery_time_min) as avg_deli_time_min
from food_delivery
group by City
order by avg_deli_time_min desc
limit 10;

#Distance vs delivery delay analysis

select
	Distance_Km,
    avg(Delivery_Time_Min) as avg_deli_time,
    count(*) as Total_Orders
from food_delivery
group by Distance_Km
order by avg_deli_time desc
limit 10;
		
#Delivery rating vs delivery time
select
	Delivery_Rating,
	avg(Delivery_Time_Min) as avg_deli_time
from food_delivery
group by Delivery_Rating
order by avg_deli_time desc;

#Restaurant Performance
#Top-rated restaurants
select
	Restaurant_Name,
    count(*) as total_orders,
	max(Delivery_Rating) as top_rate
from food_delivery
group by Restaurant_Name
order by top_rate desc
limit 10;
#Cancellation rate by restaurant

select 
	restaurant_name,
    count(*) as tot_order,
    sum(order_value) as total_revenue,
    sum(is_cancelled) as cancelled_orders,
    round(
		sum(is_cancelled) *100/count(*),2) as cancellation_rate
	from food_delivery
    group by restaurant_name
    order by cancellation_rate,total_revenue desc
    limit 10;

#Cuisine-wise performance
       
select 
	cuisine_Type,
	count(*) as tot_orders,
	sum(Order_Value) as tot_order_value,
	avg(Order_Value) as avg_order_rate,
    avg(Delivery_Time_Min) as avg_deli_time,
    avg(Delivery_Rating) as avg_deli_rate
from food_delivery
group by Cuisine_Type
order by tot_order_value desc;

#OPERATIONAL INSIGHTS Peak_Hour
#Peak hour demand analysis

select 
	 Peak_Hour,
     count(*) as peak_hr_val,
     avg(delivery_time_min) as avg_deli_time
	from food_delivery
    group by peak_hour;
     
#Payment mode preferences     
select
	case
		when payment_mode in ('UPI','Card','Wallet')
        then 'online'
		when payment_mode = 'Cash'then 'Offline'
		else 'other'
	end as payment_mode_category,
    
count(*) as total_order
from food_delivery
group by payment_mode_category;

#Cancellation reason analysis

select 
	case
		when Cancellation_Reason like '%restaurant%' then 'Restaurant Issue'
        when Cancellation_Reason like '%late%' 
			or Cancellation_Reason like '%delay%' then 'Late Delivery'
		when Cancellation_Reason like '%customer%' then 'Customer Cancelled'
        else 'other'
	end as Cancellation_Category,
count(*) as total_Cancellation
from food_delivery
where order_status = 'cancelled'
group by Cancellation_Category;


