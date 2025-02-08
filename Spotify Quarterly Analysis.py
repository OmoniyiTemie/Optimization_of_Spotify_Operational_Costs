# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 22:19:36 2024

@author: dell
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import seaborn as sns

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                           READ THE FILE
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

file_path = 'C:/Users/dell/Desktop/WIU_ASDA/FALL_2024/ACCT_551/Team Project/Project A/Spotify Quarterly OR_Cleaned.xlsx'

df = pd.read_excel(file_path, sheet_name=1)
df

df.describe()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                           DISPLAY SETTINGS
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)  
pd.set_option('display.width', None)     



# Plot the histogram with a KDE using Seaborn
plt.figure(figsize=(10,6))  # Optional: adjust the size of the plot
sns.histplot(df['Gross Profit Margin'], bins=20, kde=True, color='green')  # Replace 'column_name' with your column name
plt.title('Histogram with KDE of Gross Profit Margin')  # Title of the histogram
plt.xlabel('Value')  # Label for the x-axis
plt.ylabel('Frequency')  # Label for the y-axis
plt.show()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                          CORRELATION ANALYSIS
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


correlation_CoR = df['Cost of Revenue'].corr(df['Gross Profit'])
correlation_CoR

correlation_SM = df['Sales and Marketing Cost'].corr(df['Gross Profit'])
correlation_SM

correlation_RD = df['Research and Development Cost'].corr(df['Gross Profit'])
correlation_RD

correlation_GA = df['General and Administrative Cost'].corr(df['Gross Profit'])
correlation_GA

# There is a strong positive relationship between Operational Costs and the Gross Profit.



#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                          CONTRIBUTION AND VARIANCE ANALYSIS
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Define the cost columns
cost_columns = [
    'Sales and Marketing Cost', 
    'Research and Development Cost', 
    'General and Administrative Cost'
]

# Calculate total operational costs
df['Total Operational Cost'] = df[cost_columns].sum(axis=1)

# Calculate the percentage contribution of each cost category
for cost_column in cost_columns:
    df[f'{cost_column} Contribution %'] = df[cost_column] / df['Total Operational Cost'] * 100

# Variance analysis (compare current period with previous period)
df['Sales and Marketing Cost Variance'] = df['Sales and Marketing Cost'].diff() * -1
df['R&D Cost Variance'] = df['Research and Development Cost'].diff() * -1
df['G&A Cost Variance'] = df['General and Administrative Cost'].diff() * -1



print(df)

df.to_csv('spotify_analysis_sorted.csv', index=False)




#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                          REGRESSION ANALYSIS
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Define dependent and independent variables
X = df[['Sales and Marketing Cost', 'Research and Development Cost', 'General and Administrative Cost']]
y = df['Gross Profit']

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Get the summary of the regression
print(model.summary())


#--------------------------------

# EXCLUDING G&A

# Define dependent and independent variables
X = df[['Sales and Marketing Cost', 'Research and Development Cost']]
y = df['Gross Profit']

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Fit the model
model = sm.OLS(y, X).fit()

# Get the summary of the regression
print(model.summary())


#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                          VARIANCE INFLATION FACTOR ANALYSIS
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


X = df[['Sales and Marketing Cost', 'Research and Development Cost', 'General and Administrative Cost']]

X = sm.add_constant(X)

# Create a DataFrame to store VIF values
vif_data = pd.DataFrame()
vif_data['Feature'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)

# MULTICOLLINEARITY IS EVIDENT!

# POSSIBILITY OF A CONFOUNDING EFFECT: It’s possible that General and Administrative Cost appears positively correlated with Gross Profit on its own, but when you account for the contributions of Sales and Marketing Cost and R&D Cost, the net effect becomes negative.

#...OR we just don't have enough data points to prove that.



#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                       OPTIMIZATION
#------------------------------------------------------------------------------------------------------------------------------------------------------------------


# MC = MR

# Calculate Marginal Revenue (MR)
df['Premium_MAUs_diff'] = df['Premium MAUs'].diff().fillna(0)  # Change in Premium MAUs
df['Ad_MAUs_diff'] = df['Ad MAUs'].diff().fillna(0)  # Change in Ad MAUs
df['Premium_Revenue_diff'] = df['Premium Revenue'].diff().fillna(0)  # Change in Premium Revenue
df['Ad_Revenue_diff'] = df['Ad Revenue'].diff().fillna(0)  # Change in Ad Revenue

# Marginal Revenue for Premium and Ad Revenue
df['MR_premium'] = df['Premium_Revenue_diff'] / df['Premium_MAUs_diff']
df['MR_ad'] = df['Ad_Revenue_diff'] / df['Ad_MAUs_diff']

# Calculate Marginal Cost (MC)
df['S_M_diff'] = df['Sales and Marketing Cost'].diff().fillna(0)  # Change in Sales & Marketing cost
df['R_D_diff'] = df['Research and Development Cost'].diff().fillna(0)  # Change in R&D cost
df['GA_diff'] = df['General and Administrative Cost'].diff().fillna(0)  # Change in General & Admin cost

# Total Marginal Cost (MC) as the sum of changes in costs
df['MC'] = df['S_M_diff'] + df['R_D_diff'] + df['GA_diff']

# Plotting MR and MC to visualize the optimal point where MR = MC
plt.plot(df['Premium MAUs'], df['MR_premium'], label="MR (Premium Revenue)")
plt.plot(df['Ad MAUs'], df['MR_ad'], label="MR (Ad Revenue)")
plt.plot(df['Premium MAUs'], df['MC'], label="MC (Total Cost)")


plt.xlabel('Number of Users (in millions)')
plt.ylabel('Revenue / Cost')
plt.title('Marginal Revenue (MR) vs Marginal Cost (MC)')
plt.legend()
plt.show()

# MR > MC (potential to acquire more users)
# and where MR < MC (potential overspending on operational costs).
























































