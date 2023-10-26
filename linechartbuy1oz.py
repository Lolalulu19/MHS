import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Open the CSV file
with open('C:\\Users\\pc\\Downloads\\kijang-emas-prices.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Initialize a dictionary to store data by year and month
    data_by_year_month = {}
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the date and price
        date = datetime.strptime(row['Date'], '%d-%b-%y')
        year = date.year
        month = date.strftime('%b')
        
        # Extract and clean the 'Buying' value
        buying_value = row['Buying'].replace(',', '').strip()
        
        # Check if 'Buying' value is not empty and is numeric
        if buying_value and buying_value.isdigit():
            price = float(buying_value)
            
            # If the year is not in the dictionary, add it with an empty dictionary as the value
            if year not in data_by_year_month:
                data_by_year_month[year] = {}
            
            # If the month is not in the year's dictionary, add it with an empty list as the value
            if month not in data_by_year_month[year]:
                data_by_year_month[year][month] = []
            
            # Append the price to the corresponding year and month
            data_by_year_month[year][month].append(price)

# List of months for X-axis
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plot line charts for each year, differentiating by month
for year, month_data in data_by_year_month.items():
    # Prepare data for each month (fill with 0 if no data available)
    prices = [month_data.get(month, [0])[0] for month in months]
    plt.plot(months, prices, label=f'Year {year}')

# Set labels and title
plt.xlabel('Month')
plt.ylabel('Price')
plt.title('Buying Gold Price Trends by Year for 1 oz')
plt.legend()
plt.show()
