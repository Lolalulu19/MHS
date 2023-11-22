import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set()

data_2023 = []
for i in range(12):
    data_2023.append(requests.get(
        'https://api.bnm.gov.my/public/kijang-emas/year/2023/month/%d' % (i + 1),
        headers={'Accept': 'application/vnd.BNM.API.v1+json'},
    ).json())

# Extracting data for plotting
timestamp, selling = [], []
for year_data in [data_2023]:
    for month in year_data:
        for day in month['data']:
            timestamp.append(day['effective_date'])
            selling.append(day['one_oz']['selling'])

# Plotting
plt.figure(figsize=(15, 5))
plt.plot(selling)
plt.xticks(np.arange(len(timestamp))[::15], timestamp[::15], rotation=45)
plt.title('Kijang Emas Selling Prices Over Time (2023)')
plt.xlabel('Date')
plt.ylabel('Selling Price')
plt.show()

# Check the length of the timestamp and selling lists
len(timestamp), len(selling)
