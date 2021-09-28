import cryptocompare

#Get price of crypto in USD
#print(cryptocompare.get_price('BTC',currency='USD')['BTC']['USD'])

#Get full name of cryptocurrency
#cryptocompare.get_coin_list()['BTC']['FullName']

def get_crypto_price(cryptocurrency,currency):
    return cryptocompare.get_price(cryptocurrency, currency=currency)[cryptocurrency][currency]

def get_crypto_name(cryptocurrency):
    return cryptocompare.get_coin_list()[cryptocurrency]['FullName']

#print(get_crypto_price('BTC','USD'))
#print(get_crypto_name('BTC'))

import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

plt.style.use('seaborn')

# x: datetime objects, y: price
x_vals = []
y_vals = []

def animate(i):
    x_vals.append(datetime.now())
    y_vals.append(get_crypto_price('BTC','USD'))

    plt.cla()
    plt.title(get_crypto_name('BTC')+'Price Live Plotting')
    plt.xlabel('Date')
    plt.ylabel('Price(USD)')
    
    #actual plotting
    plt.plot_date(x_vals,y_vals,linestyle='solid',ms=0)
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(),animate,interval=1000)

plt.show()