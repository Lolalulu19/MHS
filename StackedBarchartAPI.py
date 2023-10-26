import requests
import matplotlib.pyplot as plt

# Retrieve data from the API

# Define the header parameters
headers = {
        "Accept": "application/vnd.BNM.API.v1+json"
}


api_url = "https://api.bnm.gov.my/public/kijang-emas"

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()["data"]
    quantities = ['One Ounce', 'Half Ounce', 'Quarter Ounce']
    buying_prices = [data["one_oz"]["buying"], data["half_oz"]["buying"], data["quarter_oz"]["buying"]]
    selling_prices = [data["one_oz"]["selling"], data["half_oz"]["selling"], data["quarter_oz"]["selling"]]

    # Create a stacked bar chart
    x = range(len(quantities))
    plt.bar(x, buying_prices, label='Buying Price', color='b')
    plt.bar(x, selling_prices, label='Selling Price', color='g', bottom=buying_prices)
    plt.xlabel('Quantities')
    plt.ylabel('Prices')
    plt.title('Stacked Bar Chart: Gold Prices for Different Quantities')
    plt.xticks(x, quantities)
    plt.legend()
    plt.tight_layout()
    plt.show()

else:
    print("Failed to retrieve data from the API.")





