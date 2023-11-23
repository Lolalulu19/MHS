import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler
from itertools import product

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

train_selling = selling[: int(0.8 * len(selling))]
test_selling = selling[int(0.8 * len(selling)) :]

future_count = len(test_selling)

linear_regression = LinearRegression().fit(
    np.arange(len(train_selling)).reshape((-1, 1)), train_selling
)
linear_future = linear_regression.predict(
    np.arange(len(train_selling) + future_count).reshape((-1, 1))
)

Qs = range(0, 1)
qs = range(0, 2)
Ps = range(0, 1)
ps = range(0, 2)
D = 1
parameters = product(ps, qs, Ps, Qs)
parameters_list = list(parameters)

minmax = MinMaxScaler().fit(np.array([train_selling]).T)
minmax_values = minmax.transform(np.array([train_selling]).T)

best_aic = float('inf')
for param in parameters_list:
    try:
        model = sm.tsa.statespace.SARIMAX(
            minmax_values[:, 0],
            order = (param[0], D, param[1]),
            seasonal_order = (param[2], D, param[3], future_count),
        ).fit(disp = -1)
    except Exception as e:
        print(e)
        continue
    aic = model.aic
    print(aic)
    if aic < best_aic and aic:
        best_model = model
        best_aic = aic

arima_future = best_model.get_prediction(
    start = 0, end = len(train_selling) + (future_count - 1)
)
arima_future = minmax.inverse_transform(
    np.expand_dims(arima_future.predicted_mean, axis = 1)
)[:, 0]

fig, ax = plt.subplots(figsize = (15, 5))
ax.plot(selling, label = '20% test trend')
ax.plot(train_selling, label = '80% train trend')
ax.plot(linear_future, label = 'forecast linear regression')
ax.plot(arima_future, label = 'forecast ARIMA')
plt.xticks(
    np.arange(len(timestamp))[::10],
    np.arange(len(timestamp))[::10],
    rotation = 45,
)
plt.legend()
plt.show()
