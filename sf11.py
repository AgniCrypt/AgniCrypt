import re
import sys
import csv
import time
import random
import requests
from datetime import date
from bs4 import BeautifulSoup

end_date = str(date.today()).replace("-","")
base_url = "https://coinmarketcap.com/currencies/{0}"

currency_name_list = ["bitcoin"]


def get_data(currency_name):
    print("Currency : ", currency_name)
    url = base_url.format(currency_name)
    html_response = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(html_response, 'html.parser')
    a = soup.find_all('table')
    if a :
        table = a[0]
        elements = table.find_all("tr")
        x = []
        
        for element in elements:
            a = element.get_text(' ').strip().split('/n')
            b = a[0]
            x.append(b)
        
        cur_price = x[0]
        pr_chg = x[1].split()
        low_high = x[2].split()
        trd_vol = x[3].split()
        market_cap = x[4].split()
        market_dom = x[5]
        rank = x[6]

        print(cur_price)
        print("Price changed=", pr_chg[3],'or', pr_chg[4],'%')
        print('24hr Low =', low_high[5])
        print('24hr high =',low_high[7])
        print('Trading Volume =', trd_vol[3], 'or', trd_vol[4],'%')
        print('Volume/ Market Cap =', market_cap[4])
        print(market_dom)
        print(rank)
        time.sleep(1)

if __name__ == "__main__":
    for currency_name in currency_name_list:
        get_data(currency_name)
        pass
