import csv
import datetime
import matplotlib.pyplot as plt

# Open the CSV file
with open('C:\\Users\\pc\\Downloads\\kijang-emas-year BUYING.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Initialize dictionaries to store data by category and year
    data_by_category = {
        '1 oz': {},
        '1/2 oz': {},
        '1/4 oz': {},
        '11 oz': {},
        '1/22 oz': {},
        '1/44 oz': {}
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
        oz_11 = float(row['11 oz'].replace(',', ''))
        oz_1_22 = float(row['1/22 oz'].replace(',', ''))
        oz_1_44 = float(row['1/44 oz'].replace(',', ''))
        
        # Store the prices in the respective category dictionary for the specific year
        data_by_category['1 oz'][year] = oz_1
        data_by_category['1/2 oz'][year] = oz_1_2
        data_by_category['1/4 oz'][year] = oz_1_4
        data_by_category['11 oz'][year] = oz_11
        data_by_category['1/22 oz'][year] = oz_1_22
        data_by_category['1/44 oz'][year] = oz_1_44

# Plot line charts for each category with different line styles, markers, and colors
for category, data in data_by_category.items():
    years = list(data.keys())
    prices = list(data.values())
    # Define different line styles, markers, and colors for each category
    line_style = '-'
    marker = 'o'
    color = 'b'
    
    # Use the same line style, marker, and color for '1 oz' (1st column) and '1/4 oz' (3rd column)
    if category == '1 oz' or category == '1/4 oz' or category == '1/22 oz':
        plt.plot(years, prices, label=f'{category}', linestyle=line_style, marker=marker, color=color)
    else:
        # Different line style, marker, and color for '1/2 oz' (2nd column)
        plt.plot(years, prices, label=f'{category}', linestyle='--', marker='s', color='g')

# Set labels and title
plt.xlabel('Year')
plt.ylabel('Price')
plt.title('Buying Gold Price Trends (Differentiated by Weight)')
plt.legend()
plt.show()
