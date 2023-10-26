import csv
import datetime
import matplotlib.pyplot as plt

# Open the CSV file
with open('C:\\Users\\pc\\Downloads\\kijang-emas-prices SELLING.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Initialize dictionaries to store data by category and year
    data_by_category = {
        '1 oz': {},
        '1/2 oz': {},
        '1/4 oz': {}
    }
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the date, price, and category
        date = row['Date']
        parsed_date = datetime.datetime.strptime(date, '%d-%b-%y')
        year = parsed_date.year
        oz_1 = float(row['1 oz'].replace(',', ''))
        oz_1_2 = float(row['1/2 oz'].replace(',', ''))
        oz_1_4 = float(row['1/4 oz'].replace(',', ''))
        
        # Store the prices in the respective category dictionary for the specific year
        data_by_category['1 oz'][year] = oz_1
        data_by_category['1/2 oz'][year] = oz_1_2
        data_by_category['1/4 oz'][year] = oz_1_4

# Plot line charts for each category
for category, data in data_by_category.items():
    years = list(data.keys())
    prices = list(data.values())
    plt.plot(years, prices, label=f'{category}')

# Set labels and title
plt.xlabel('Year')
plt.ylabel('Price')
plt.title('Selling Gold Price Trends (Differentiated by Weight)')
plt.legend()
plt.show()
