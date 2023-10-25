import requests as req
import json
import matplotlib.pyplot as plt

header = {
    "Accept": "application/vnd.BNM.API.v1+json"
}

url = "https://api.bnm.gov.my/public/kijang-emas/year/{year}/month/{month}"

onez_buy = {}

for y in range(2019, 2024):
    buy = []
    for m in range(1, 13):
        resp = req.get(url.format(year=y, month=m), headers=header)
        result = json.loads(resp.text)

        if len(result['data']) > 0:
            for i in range(len(result['data'])):
                one_oz = result['data'][i]['one_oz']['buying']
                buy.append(one_oz)
        else:
            # If no data available for a month, append a placeholder value (e.g., 0)
            buy.append(0)

    # Ensure `buy` contains only 12 values by truncating or averaging if necessary
    buy = buy[:12]  # Truncate to first 12 values

    onez_buy[y] = buy

# Visualizing the data using a line chart
for year, prices in onez_buy.items():
    plt.plot(range(1, 13), prices, label=str(year))

plt.xlabel('Month')
plt.ylabel('Price (in MYR)')
plt.title('Gold Buying Prices (One Ounce) from 2019 to 2023')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend()
plt.grid(True)
plt.show()
