# -*- coding: utf-8 -*-
"""swiggy.ipynb"""

#importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#reading the dataset
data_df = pd.read_excel('/content/Dataset - Data Analysis.xlsx', sheet_name='Data')
data_df

#checking for the shape
data_df.shape

#dropping the duplicates if present
data_df.drop_duplicates()

#revarifying the shape
data_df.shape

#checking for missing values
data_df.isnull().sum()

#drop the rows of missing values
data_df=data_df.dropna()

#revarifying if any missing value is present
data_df.isnull().sum()

#shape
data_df.shape

#exploring the data types and non-null counts of rows
data_df.info()

#change data type from object to category
data_df["Data_Plan"]=data_df["Data_Plan"].astype("category")
data_df["Customer_Attrition"]=data_df["Customer_Attrition"].astype("category")

#revarifying the data types
data_df.info()

#exploring more for any unusual data 
print(data_df["Data_Plan"].value_counts)
print(data_df["Customer_Attrition"].value_counts)

"""All fine, we can proceed with the Questions to Answer

#1.What is the correlation between the number of calls to customer care and customer attrition?
"""

# Convert the categorical column to numerical using one-hot encoding
one_hot_encoded = pd.get_dummies(data_df['Customer_Attrition'])

# Concatenate the one-hot encoded column to the original DataFrame
data_df = pd.concat([data_df, one_hot_encoded], axis=1)

# Calculate the correlation between the numerical column and the one-hot encoded columns
correlations = data_df.corr()['Calls_To_Customer_Care'][2:]

print(correlations)

"""As we can see there is a possitive correlation between the number of calls to customer care and customer attrition

#2.	Which data plan (Yes or No) has a higher average monthly charge?
"""

# calculating the average monthly charge
avg_monthly_charge = data_df.groupby('Data_Plan')['MonthlyCharge'].mean()
print(avg_monthly_charge)

"""Hence,Yes has higher monthly average charge

#7.Is there a relationship between customer attrition and contract renewal?
"""

from scipy.stats import chi2_contingency
contingency_table = pd.crosstab(data_df['Customer_Attrition'], data_df['Contract_Renewal'])

#chi-squared test of independence
chi2, p_value, dof, expected = chi2_contingency(contingency_table)


print("Chi-squared value:", chi2)
print("P-value:", p_value)

"""since p-value is greater than 0.05,we fail to reject the null hypothesis and conclude that there is no significant relationship between the customer attrition and contract renewal

#8.Which feature(s) have the highest correlation with customer attrition?
"""

#correlation matrix
corr_matrix = data_df.corr()

#sort the correlation values for the "Yes" column
corr_values_yes = corr_matrix['Yes']


#top 5 correlations
print(corr_values_yes.head())

"""#	9.Is there a difference in data usage between customers who have a data plan and those who do not?"""

from scipy.stats import ttest_ind


# Spliting the data based on whether customers have a data plan or not
data_plan_yes = data_df[data_df['Data_Plan'] == 'Yes']['Data_Usage']
data_plan_no = data_df[data_df['Data_Plan'] == 'No']['Data_Usage']

#means and standard deviations of the two groups
mean_yes = data_plan_yes.mean()
mean_no = data_plan_no.mean()
std_yes = data_plan_yes.std()
std_no = data_plan_no.std()

#two-sample t-test to determine if there is a significant difference in means
t_stat, p_value = ttest_ind(data_plan_yes, data_plan_no, equal_var=False)
alpha = 0.05
if p_value < alpha:
    print("There is a statistically significant difference in data usage between customers with and without a data plan.")
else:
    print("There is no statistically significant difference in data usage between customers with and without a data plan.")

"""#10.	What is the total revenue from customers who have a data plan and used greater than 3 GB of data"""

#customers with a data plan and data usage greater than 3 GB
filtered_df = data_df[(data_df['Data_Plan'] == 'Yes') & (data_df['Data_Usage'] > 3)]

#total revenue for these customers
total_revenue = (filtered_df['MonthlyCharge'] * filtered_df['Weeks'] / 4).sum()


print("Total revenue from customers with a data plan and usage > 3GB: ${:.2f}".format(total_revenue))



"""#11.What % of total revenue comes from customers who do not have a data plan?"""

#total revenue from all customers
total_revenue_all = (data_df['MonthlyCharge'] * data_df['Weeks'] / 4).sum()

#total revenue from customers who do not have a data plan
no_data_plan_df = data_df[data_df['Data_Plan'] == 'No']
total_revenue_no_data_plan = (no_data_plan_df['MonthlyCharge'] * no_data_plan_df['Weeks'] / 4).sum()

#percentage of total revenue that comes from customers who do not have a data plan
percent_revenue_no_data_plan = total_revenue_no_data_plan / total_revenue_all * 100

#percentage of total revenue
print("{:.2f}% of total revenue comes from customers who do not have a data plan.".format(percent_revenue_no_data_plan))



"""#12.What is the ratio of average total revenue between customers who have a data plan and those who do not?"""

#average monthly charge for customers who have a data plan
avg_monthly_charge_with_data_plan = data_df[data_df['Data_Plan'] == 'Yes']['MonthlyCharge'].mean()

#average monthly charge for customers who do not have a data plan
avg_monthly_charge_without_data_plan = data_df[data_df['Data_Plan'] == 'No']['MonthlyCharge'].mean()

#ratio of average monthly charge
monthly_charge_ratio = avg_monthly_charge_with_data_plan / avg_monthly_charge_without_data_plan

print(f"The ratio of average monthly charge between customers who have a data plan and those who do not is: {monthly_charge_ratio:.2f}")

"""#13.Is there a difference in contract renewal rates between customers who have a data plan and those who do not?"""

from scipy.stats import chi2_contingency

# Creating a contingency table
contingency_table = pd.crosstab(data_df['Data_Plan'], data_df['Contract_Renewal'])

#chi-square test of independence
chi2_statistic, p_value, degrees_of_freedom, expected_values = chi2_contingency(contingency_table)

print(f"The p-value of the chi-square test of independence is: {p_value:.4f}")



"""#14.What % of revenue comes from overage fees for customers with no data plan, customers using 1-3 GB of data and customers using greater than 3 GB of data?"""

#three categories of customers
no_data_plan = data_df[data_df['Data_Plan'] == 'No']
data_1_3_gb = data_df[(data_df['Data_Usage'] >= 1) & (data_df['Data_Usage'] <= 3)]
data_gt_3_gb = data_df[data_df['Data_Usage'] > 3]

#revenue from overage fees for each category of customer
revenue_no_data_plan = no_data_plan['OverageFee'].sum()
revenue_data_1_3_gb = data_1_3_gb['OverageFee'].sum()
revenue_data_gt_3_gb = data_gt_3_gb['OverageFee'].sum()

#total revenue
total_revenue = data_df['OverageFee'].sum()

#percentage of revenue from overage fees for each category of customer
pct_revenue_no_data_plan = revenue_no_data_plan / total_revenue * 100
pct_revenue_data_1_3_gb = revenue_data_1_3_gb / total_revenue * 100
pct_revenue_data_gt_3_gb = revenue_data_gt_3_gb / total_revenue * 100


print(f"Percentage of revenue from overage fees for customers with no data plan: {pct_revenue_no_data_plan:.2f}%")
print(f"Percentage of revenue from overage fees for customers using 1-3 GB of data: {pct_revenue_data_1_3_gb:.2f}%")
print(f"Percentage of revenue from overage fees for customers using greater than 3 GB of data: {pct_revenue_data_gt_3_gb:.2f}%")

"""#15.	Do customers with weeks more than 50 have a lower minute per call ratio or customers with weeks between 31 and 50 ?"""

#customers with weeks more than 50
df_weeks_gt_50 = data_df[data_df['Weeks'] > 50]

#average minute per call ratio for this dataframe
avg_min_per_call_gt_50 = df_weeks_gt_50['DayMins'] / df_weeks_gt_50['DayCalls']

#customers with weeks between 31 and 50
df_weeks_31_50 = data_df[(data_df['Weeks'] >= 31) & (data_df['Weeks'] <= 50)]

#average minute per call ratio for this dataframe
avg_min_per_call_31_50 = df_weeks_31_50['DayMins'] / df_weeks_31_50['DayCalls']

# Comparing the two average minute per call ratios
if avg_min_per_call_gt_50.mean() < avg_min_per_call_31_50.mean():
    print("Customers with weeks more than 50 have a lower minute per call ratio.")
else:
    print("Customers with weeks between 31 and 50 have a lower minute per call ratio.")

"""#16	What is the average overage fee for customers whose contracts are more than 30 weeks old and have a data plan and have used less than 1GB of data?"""

# filter the data based on the conditions
filtered_data = data_df[(data_df["Weeks"] > 30) & (data_df["Data_Plan"] == "yes") & (data_df["Data_Usage"] < 1)]

#average overage fee
average_overage_fee = filtered_data["OverageFee"].mean()


print("The average overage fee for customers whose contracts are more than 30 weeks old and have a data plan and have used less than 1GB of data is:", average_overage_fee)

"""#17.What is the average monthly charge for customers whose contracts are more than 50 weeks old and have a data plan and have renewed their contract?"""

# filter the dataset based on conditions
filtered_df = data_df[(data_df['Weeks'] > 50) & (data_df['Data_Plan'] == 'yes') & (data_df['Contract_Renewal'] == 1)]

#average of MonthlyCharge
avg_monthly_charge = filtered_df['MonthlyCharge'].mean()

print("The average monthly charge for customers whose contracts are more than 50 weeks old and have a data plan and have renewed their contract is:", avg_monthly_charge)

"""#18.	What is the average roam minutes for customers whose contracts are between 31-50 weeks and have a data plan and have used greater than 3GB of data?"""

# filter the data
filtered_data = data_df[(data_df['Weeks'] >= 31) & (data_df['Weeks'] <= 50) & (data_df['Data_Plan'] == 'yes') & (data_df['Data_Usage'] > 3)]

#average roaming minutes
average_roam_minutes = filtered_data['RoamMins'].mean()

print("The average roaming minutes for customers whose contracts are between 31-50 weeks and have a data plan and have used greater than 3GB of data is:", average_roam_minutes)

"""#19.What is the average data usage for customers whose contracts are more than 30 weeks old and have renewed their contract?"""

#customers whose contracts are more than 30 weeks old and have renewed their contract
filtered_data = data_df[(data_df['Weeks'] > 30) & (data_df['Contract_Renewal'] == 1)]

#average data usage
avg_data_usage = filtered_data['Data_Usage'].mean()

print(f"The average data usage for customers whose contracts are more than 30 weeks old and have renewed their contract is {avg_data_usage:.2f} GB.")





