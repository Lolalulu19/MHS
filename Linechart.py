import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Open the CSV file
with open('C:\\Users\\pc\\Downloads\\kijang-emas-year BUYING.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Initialize dictionaries to store data by category and year
    data_by_category = {
        '1 oz sell': {},
        '1 oz buy': {},
        '1/2 oz sell': {},
        '1/2 oz buy': {},
        '1/4 oz sell': {},
        '1/4 oz buy': {}
    }
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the date, price, and category
        date = row['Date']
        parsed_date = datetime.datetime.strptime(date, '%d-%b-%y')
        year = parsed_date.year
        oz_1_sell = float(row['1 oz sell'].replace(',', ''))
        oz_1_buy = float(row['1 oz buy'].replace(',', ''))
        oz_12_sell = float(row['1/2 oz sell'].replace(',', ''))
        oz_12_buy = float(row['1/2 oz buy'].replace(',', ''))
        oz_14_sell = float(row['1/4 oz sell'].replace(',', ''))
        oz_14_buy = float(row['1/4 oz buy'].replace(',', ''))
        
        # Store the prices in the respective category dictionary for the specific year
        data_by_category['1 oz sell'][year] = oz_1_sell
        data_by_category['1 oz buy'][year] = oz_1_buy
        data_by_category['1/2 oz sell'][year] = oz_12_sell
        data_by_category['1/2 oz buy'][year] = oz_12_buy
        data_by_category['1/4 oz sell'][year] = oz_14_sell
        data_by_category['1/4 oz buy'][year] = oz_14_buy

# Define line styles for each group of lines
selling_linestyle = '-'
buying_linestyle = 'dashdot'

# Define colors for each group of lines
selling_color = 'b'
buying_color1 = 'g'
buying_color2 = 'r'

# Plot line charts for each category with different line styles, markers, and colors
for i, (category, data) in enumerate(data_by_category.items()):
    years = list(data.keys())
    prices = list(data.values())
    
    # Assign colors based on the group of lines
    if category in ['1 oz sell', '1 oz buy']:
        color = selling_color
    elif category in ['1/2 oz sell', '1/2 oz buy']:
        color = buying_color1
    else:
        color = buying_color2
    
    # Assign line styles based on the group of lines
    linestyle = selling_linestyle if category in ['1 oz sell', '1/2 oz sell', '1/4 oz sell'] else buying_linestyle
    
    plt.plot(years, prices, label=f'{category}', linestyle=linestyle, color=color)

# Define custom legend entries for "Selling" and "Buying"
custom_legend = [
    Line2D([0], [0], color='black', linestyle=selling_linestyle, marker='', label='Selling'),
    Line2D([0], [0], color='black', linestyle=buying_linestyle, marker='', label='Buying')
]

# Set labels and title
plt.xlabel('Year')
plt.ylabel('Price')
plt.title('Gold Price Trends (Differentiated by Weight)')

# Display the custom legend with specified line styles and colors
plt.legend(handles=custom_legend)

# Display the plot
plt.show()
