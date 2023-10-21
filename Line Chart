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

# Extract data for the time series chart
effective_date = datetime.strptime(parsed_response['data']['effective_date'], "%Y-%m-%d").date()
denominations = ["One Ounce", "Half Ounce", "Quarter Ounce"]
buying_prices = [parsed_response['data']['one_oz']['buying'],
                 parsed_response['data']['half_oz']['buying'],
                 parsed_response['data']['quarter_oz']['buying']]

selling_prices = [parsed_response['data']['one_oz']['selling'],
                  parsed_response['data']['half_oz']['selling'],
                  parsed_response['data']['quarter_oz']['selling']]

# Create a time series chart
plt.figure(figsize=(10, 6))

# Plot buying prices
plt.plot(denominations, buying_prices, marker='o', label='Buying Price', color='blue')
# Plot selling prices
plt.plot(denominations, selling_prices, marker='o', label='Selling Price', color='orange')

plt.xlabel('Gold Denomination')
plt.ylabel('Prices')
plt.title(f'Gold Prices on {effective_date.strftime("%B %Y")}')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

