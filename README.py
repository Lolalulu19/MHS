# MHS
Monthly Highlight Statistics

import json
import matplotlib.pyplot as plt
from datetime import datetime

# Sample JSON response with the full dataset (replace this with your actual data)
full_json_response = '''
{
    "data": {
        "effective_date": "2023-10-20",
        "one_oz": {
            "buying": 9613,
            "selling": 10003
        },
        "half_oz": {
            "buying": 4807,
            "selling": 5096
        },
        "quarter_oz": {
            "buying": 2403,
            "selling": 2595
        }
    }
}
'''

# Parse the JSON response
parsed_response = json.loads(full_json_response)

# Extract data for scatter plot
effective_date = datetime.strptime(parsed_response['data']['effective_date'], "%Y-%m-%d")
denominations = ["One Ounce", "Half Ounce", "Quarter Ounce"]
buying_prices = [parsed_response['data']['one_oz']['buying'],
                 parsed_response['data']['half_oz']['buying'],
                 parsed_response['data']['quarter_oz']['buying']]

selling_prices = [parsed_response['data']['one_oz']['selling'],
                  parsed_response['data']['half_oz']['selling'],
                  parsed_response['data']['quarter_oz']['selling']]

# Create scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(buying_prices, selling_prices, color='blue')

plt.xlabel('Buying Prices')
plt.ylabel('Selling Prices')
plt.title(f'Buying vs Selling Prices on {effective_date.strftime("%Y-%m-%d")}')
plt.grid(True)
plt.tight_layout()
plt.show()


