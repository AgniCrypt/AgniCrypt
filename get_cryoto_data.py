import re
import sys
import csv
import time
import random
import requests
from datetime import date
from bs4 import BeautifulSoup

def get_data(currency_name):

    url = 'https://coinmarketcap.com/currencies/{0}'.format(currency_name)
    html_response = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(html_response, 'html.parser')
    f = soup.find_all('table')
    
    if f:
        table = f[0]
        elements = table.find_all("tr")
        cypto_data = [i.get_text(' ').strip().split('/n')[0].split() for i in elements]
        
        return cypto_data[0][-1], (cypto_data[1][-3], cypto_data[1][-2] + '%'), (cypto_data[2][-3], cypto_data[2][-1]) ,(cypto_data[3][-3], cypto_data[3][-2] + '%'), cypto_data[4][-1], cypto_data[5][-2] + '%', cypto_data[6][-1]

crypto_name = input('Enter the complete name of cryptocurrency --> ').strip().lower().replace(' ', '-')

    
x = get_data(crypto_name)
if x:
    
    print('Current Price: ', x[0])
    print('Price changed: ', x[1][0],'/', x[1][1])
    print('24hr Low: ', x[2][0])
    print('24hr high: ',x[2][1])
    print('Trading Volume: ', x[3][0], '/', x[3][1])
    print('Volume/ Market Cap: ', x[4])
    print('Market Dominance: ', x[5])
    print('Market rank: ', x[6])
    
else:
    print("Sorry, we couldn't find cryptocurrency with this name. Please re-check the spelling.")
