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

currency_name_list = ["bitcoin", "ethereum", "ripple", "bitcoin-cash", "nem", "litecoin", "dash", "ethereum-classic", "iota", "neo", "stratis", "monero", "waves", "bitconnect", "omisego", "qtum", "numeraire"]


def get_data(currency_name):
    print("Currency : ", currency_name)
    url = base_url.format(currency_name)
    html_response = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(html_response, 'html.parser')
    a = soup.find_all('table')
    if a :
        table = a[0]
        elements = table.find_all("tr")
        
        for element in elements:
            print(element.get_text().strip().split("\n") )
        time.sleep(1)

if __name__ == "__main__":
    for currency_name in currency_name_list:
        get_data(currency_name)
        pass
