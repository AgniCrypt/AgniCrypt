import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = web.DataReader('XRP-USD',data_source='yahoo', start='2021-01-01', end='2021-08-01')
plt.figure(figsize=(12,6))
plt.title('Close price history')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=12)
plt.ylabel('Close price USD', fontsize = 12)
plt.show()