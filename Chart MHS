import json
import matplotlib.pyplot as plt

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

# Extract data for bar chart
denominations = ["One Ounce", "Half Ounce", "Quarter Ounce"]
buying_prices = [parsed_response['data']['one_oz']['buying'],
                 parsed_response['data']['half_oz']['buying'],
                 parsed_response['data']['quarter_oz']['buying']]

selling_prices = [parsed_response['data']['one_oz']['selling'],
                  parsed_response['data']['half_oz']['selling'],
                  parsed_response['data']['quarter_oz']['selling']]

# Create a bar chart
plt.figure(figsize=(8, 6))
bar_width = 0.35
index = range(len(denominations))

plt.bar(index, buying_prices, bar_width, label='Buying Price')
plt.bar([p + bar_width for p in index], selling_prices, bar_width, label='Selling Price')

plt.xlabel('Gold Denomination')
plt.ylabel('Prices')
plt.title(f'Gold Prices on {parsed_response["data"]["effective_date"]}')
plt.xticks([p + bar_width/2 for p in index], denominations)
plt.legend()
plt.tight_layout()
plt.show()
