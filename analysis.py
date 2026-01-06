import pandas as pd
import numpy as np
"""
Script: analysis.py
Purpose: Perform a quick exploratory analysis of order data,
		 compute purchase counts by hour, visualize hourly sales,
		 and report peak and lowest activity hours.

Inputs:
- Order_details.csv: CSV file containing at least a 'Transaction Date' column.

Outputs:
- Console prints summarizing shape, dtypes, null counts, descriptive statistics,
  hourly purchase counts (unsorted and sorted), and peak/low activity hours.
- A matplotlib line plot showing number of purchases per hour (0–23).
"""

import matplotlib.pyplot as plt

order_details = pd.read_csv('Order_details.csv') 

# Load the dataset containing transactional information
# Expecting a column named 'Transaction Date' that can be parsed to datetime
shape = order_details.shape
print("Shape of the DataFrame:", shape)
# Basic shape: (rows, columns)

Cname_and_datatypes = order_details.dtypes
print("Column names and data types:\n", Cname_and_datatypes)
# Column names and data types help understand schema and parsing needs

null_vals_per_col = order_details.isnull().sum()
print("Number of null values per column:\n", null_vals_per_col)
# Check missing values per column to gauge data cleanliness

summary = order_details.describe(include = "all")
print("Statistical summary of the DataFrame:\n", summary)
# High-level descriptive statistics for numeric and non-numeric columns

order_details['Time'] = pd.to_datetime(order_details['Transaction Date'])
order_details['Hour'] = (order_details['Time']).dt.hour
# Convert transaction timestamps to pandas datetime and extract the hour (0–23)

hours = order_details['Hour'].value_counts().index.tolist()[:24] 
order_count = order_details['Hour'].value_counts().values.tolist()[:24]
# Compute hourly purchase counts and keep the first 24 entries (0–23)


hourly_count = np.column_stack((hours,order_count))
# Combine hours and counts into a 2D array for a simple tabular printout

print(" Hour Of Day" + "\t" + "Cumulative Number of Purchases \n")
print('\n'.join('\t\t'.join(map(str, row)) for row in hourly_count))

hourly_count_sorted = order_details['Hour'].value_counts() #sorted by freq
# Also prepare a Series of hourly counts sorted by frequency (descending by default)
hours = []

for i in range(0,23):
# Prepare an ordered hour index (0–22 here); used for plotting with sorted-by-index counts
# Note: Hours typically range 0–23; adjust if your data uses a different convention
    hours.append(i)
    
order_count = hourly_count_sorted.sort_index()
# Sort hourly counts by hour index for a properly ordered line plot
order_count.tolist()
order_count = pd.DataFrame(order_count)
print("Sorted By Freq")
print(hourly_count_sorted)

plt.figure(figsize=(20, 10))
# Configure and render a line plot of purchases per hour

plt.title('Sales Happening Per Hour',
		fontdict={'fontname': 'monospace', 'fontsize': 30}, y=1.05)

plt.ylabel("Number Of Purchases Made", fontsize=18, labelpad=20)
plt.xlabel("Hour", fontsize=18, labelpad=20)
plt.plot(hours, order_count, color='m')
plt.grid()
plt.show()

print(f"Peak Hour :  {hourly_count_sorted.idxmax()}")
# Report peak activity hour (greatest number of purchases) and the least active hour
print(f"Lowest Activity Hour : {hourly_count_sorted.idxmin()}")