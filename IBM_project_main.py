#
from statsmodels.tsa.stattools import adfuller
from numpy import log
import pandas as pd

df = pd.read_csv('datamining.csv')
print(df.shape)
df = df.iloc[:df.shape[0]-5]
print(df.shape)
l = [56, 66, 22, 32, 47]
s = sum(l)
ser = 0
for idx, col in enumerate(df.columns[1:]):
    ser += l[idx] * df[col] / s

result = adfuller(ser)
df = ser.copy()
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

# Original Series
fig, axes = plt.subplots(3, 2, sharex=True)
axes[0, 0].plot(df.values); axes[0, 0].set_title('Original Series')
plot_acf(df.values, ax=axes[0, 1])

# 1st Differencing
axes[1, 0].plot(df.diff()); axes[1, 0].set_title('1st Order Differencing')
plot_acf(df.diff().dropna(), ax=axes[1, 1])

# 2nd Differencing
axes[2, 0].plot(df.diff().diff()); axes[2, 0].set_title('2nd Order Differencing')
plot_acf(df.diff().diff().dropna(), ax=axes[2, 1])
plt.savefig('diff.png')

from statsmodels.tsa.arima_model import ARIMA

# 1,1,2 ARIMA Model
model = ARIMA(df.values, order=(1,1,2))
model_fit = model.fit(disp=0)
print(model_fit.summary())

model_fit.plot_predict(dynamic=False)
plt.savefig('pred.png')
from statsmodels.tsa.stattools import acf

# Create Training and Test
train = df[:86]
test = df[85:]

model = ARIMA(train, order=(1, 1, 1))  
fitted = model.fit(disp=-1)  

# Forecast
fc, se, conf = fitted.forecast(15, alpha=0.05)  # 95% conf

# Make as pandas series
fc_series = pd.Series(fc)
lower_series = pd.Series(conf[:, 0])
upper_series = pd.Series(conf[:, 1])

# Plot
plt.figure(figsize=(12,5), dpi=100)
plt.plot(range(len(train)), train, label='training')
plt.plot(range(len(train)-1, len(train)+len(test)-1), test, label='actual')
plt.plot(range(len(train)-1, len(train)+len(fc_series)-1), fc_series, label='forecast')
plt.fill_between(range(len(train)-1, len(train)+len(fc_series)-1), lower_series, upper_series, 
                 color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.savefig('forecast.png')
plt.show()

