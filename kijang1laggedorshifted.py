import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
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

df = pd.DataFrame({'timestamp': timestamp, 'selling': selling})
df.head()

def df_shift(df, lag=0, start=1, skip=1, rejected_columns=[]):
    df = df.copy()
    if not lag:
        return df
    cols = {}
    for i in range(start, lag + 1, skip):
        for x in list(df.columns):
            if x not in rejected_columns:
                if not x in cols:
                    cols[x] = ['{}_{}'.format(x, i)]
                else:
                    cols[x].append('{}_{}'.format(x, i))
    for k, v in cols.items():
        columns = v
        dfn = pd.DataFrame(data=None, columns=columns, index=df.index)
        i = start - 1
        for c in columns:
            dfn[c] = df[k].shift(periods=i)
            i += skip
        df = pd.concat([df, dfn], axis=1, join='outer')
    return df

df_crosscorrelated = df_shift(
    df, lag=12, start=4, skip=2, rejected_columns=['timestamp']
)
df_crosscorrelated['ma7'] = df_crosscorrelated['selling'].rolling(7).mean()
df_crosscorrelated['ma14'] = df_crosscorrelated['selling'].rolling(14).mean()
df_crosscorrelated['ma21'] = df_crosscorrelated['selling'].rolling(21).mean()

plt.figure(figsize=(20, 4))
plt.subplot(1, 3, 1)
plt.scatter(df_crosscorrelated['selling'], df_crosscorrelated['selling_4'], alpha=0.5)
mse = ((df_crosscorrelated['selling_4'] - df_crosscorrelated['selling']) ** 2).mean()
plt.title(f'Shifted 4, MSE: {mse:.2f}')
plt.xlabel('Original Selling')
plt.ylabel('Shifted Selling')

plt.subplot(1, 3, 2)
plt.scatter(df_crosscorrelated['selling'], df_crosscorrelated['selling_8'], alpha=0.5)
mse = ((df_crosscorrelated['selling_8'] - df_crosscorrelated['selling']) ** 2).mean()
plt.title(f'Shifted 8, MSE: {mse:.2f}')
plt.xlabel('Original Selling')
plt.ylabel('Shifted Selling')

plt.subplot(1, 3, 3)
plt.scatter(df_crosscorrelated['selling'], df_crosscorrelated['selling_12'], alpha=0.5)
mse = ((df_crosscorrelated['selling_12'] - df_crosscorrelated['selling']) ** 2).mean()
plt.title(f'Shifted 12, MSE: {mse:.2f}')
plt.xlabel('Original Selling')
plt.ylabel('Shifted Selling')

plt.tight_layout()
plt.show()
