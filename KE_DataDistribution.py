import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

sns.set()

data_2020 = []
for i in range(12):
    response = requests.get(
        f'https://api.bnm.gov.my/public/kijang-emas/year/2020/month/{i + 1}',
        headers={'Accept': 'application/vnd.BNM.API.v1+json'},
    )
    if response.status_code == 200:
        data_2020.append(response.json())
    else:
        print(f"Failed to fetch data for 2020, month {i + 1}")

data_2021 = []
for i in range(12):
    response = requests.get(
        f'https://api.bnm.gov.my/public/kijang-emas/year/2021/month/{i + 1}',
        headers={'Accept': 'application/vnd.BNM.API.v1+json'},
    )
    if response.status_code == 200:
        data_2021.append(response.json())
    else:
        print(f"Failed to fetch data for 2021, month {i + 1}")

timestamp, selling = [], []
for year_data in [data_2020, data_2021]:
    for month in year_data:
        for day in month.get('data', []):
            effective_date = datetime.strptime(day['effective_date'], '%Y-%m-%d')
            timestamp.append(effective_date.strftime('%b %Y'))
            selling.append(day['one_oz']['selling'])

# Convert timestamp to numerical values for a smoother line
x_values = np.arange(len(timestamp))

# Get the indices of the first occurrence of each month
unique_month_indices = [i for i, month in enumerate(timestamp) if i == 0 or month != timestamp[i - 1]]

plt.figure(figsize = (15, 5))
sns.distplot(selling)
plt.show()
