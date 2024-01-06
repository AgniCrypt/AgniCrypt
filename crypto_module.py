import re
import sys
import csv
import time
import random
import requests
import datetime 
import pandas
from bs4 import BeautifulSoup
import mysql.connector
mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '123123', database = 'agnicrypt')
mycursor = mydb.cursor(buffered = True)
mydb.autocommit = True


def email_check(email):   
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    mycursor.execute("SELECT USERNAME FROM USERBASE WHERE (EMAIL = '{0}')".format(email))
    taken = mycursor.fetchall()
    f = 0
    if not(re.search(regex,email)):
        f = 1
    elif taken:
        f = 2
    return f   

        
def sign_in(user_id, password):
     
    mycursor.execute("SELECT PASSWORD, USERNAME FROM USERBASE WHERE (EMAIL = '{0}') OR (USERNAME = '{0}')".format(user_id))
    pw = mycursor.fetchall()
    f = 1
    if pw:
        if password == pw[0][0]:
            print('Welcome To AGNICRYPT ' + pw[0][1])
            f = 0
            return pw[0][1]
    if f:
       print('Incorrect Credentials')
            
        
def sign_up(user_data):

    check = email_check(user_data[0])
    
    while check:
        if check == 1:     
            user_data[0] = input('Please Enter Valid E-Mail --> ')
        elif check == 2:
            user_data[0] = input('This Email is Already Registered, Please Enter Another E-Mail --> ')
        check = email_check(user_data[0])
        
    while not(user_data[2]):
        user_data[2] = input('Username cannot be blank, Create a username --> ')

    while not(user_data[3]):
        user_data[3] = input('Password cannot be blank, Create a password --> ')
    
    f = 1
    while f:
        try:
            mycursor.execute('INSERT INTO USERBASE VALUES{0}'.format(tuple(user_data)))
            print('Your user_id has been created, Thank You')
            f = 0
        
        except mysql.connector.errors.DataError:
            user_data[1] = input('Enter Valid Date of Birth (yyyy/mm/dd) --> ')
            
        except mysql.connector.errors.IntegrityError:
            user_data[2] = input('This Username is not available, Please Create Some Other --> ')            
            user_data[3] = input('Create a password --> ')
    
    return user_data[2]
    

def name_format(name):
    return '-'.join(name.lower().replace('.', ' ').split())


def get_data(currency_name):
    
    import requests
    api_key = 'c7b6b5d4-6917-400e-82e4-ab8c93c6dc57'
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'slug': currency_name,
        'convert':'USD'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    # Make the API request
    response = requests.get(api_url, headers=headers, params=parameters)

    if response.status_code == 200:
        data = response.json()['data']
        for i in data:
            pass
        data = data[i]
        name = data['name']
        symbol = data['symbol']
        rank = data['cmc_rank']
        data = data['quote']['USD']
        price = data['price']
        volume = data['volume_24h']
        percent_change_1h = data['percent_change_1h']
        percent_change_24h = data['percent_change_24h']
        percent_change_7d = data['percent_change_7d']
        percent_change_30d = data['percent_change_30d']
        market_cap = data['market_cap']
        dominance = data['market_cap_dominance']
        
        return price, name, symbol, volume, market_cap, dominance, rank, percent_change_1h, percent_change_24h, percent_change_7d, percent_change_30d

def show_data(crypto_name):
   
    x = get_data(crypto_name)
    if x:
        
        print('Cryptocurrency:', x[1])
        print('Symbol:', x[2])
        print('Current Price: $', x[0])
        print('Volume(24h):', x[3])
        print('Market Capitalization: $', x[4])
        print('Market Dominance: ', x[5])
        print('Market rank: ', x[6])
        print('Percent Change(1h)', x[7])
        print('Percent Change(24h)', x[8])
        print('Percent Change(7d)', x[9])
        print('Percent Change(30d)', x[10])
        print()
        
        return x[0]
    
    else:
        print("Sorry, we couldn't find cryptocurrency with this name. Please re-check the spelling.")


def user_data(user_id, crypto):
    mycursor.execute("SELECT * FROM PORTFOLIO WHERE (USER_ID = '{0}'".format(user_id) + " AND CRYPTO_NAME = '{0}')".format(crypto))
    data = mycursor.fetchall()
    if data:    
        data = data[0]
        print('CryptoCurrency Name:', data[1])
        print('Total Bought Quantity:', data[2])
        print('Total Sold Quantity:', data[3])
        print('Coins Left:', data[4])
        print('Average Bought Price: $', data[5])
        print('Average Sell Price:  $', data[6])
        print('Average Earnings on coins sold:  $', data[7])
    return data


def add_to_watchlist(user_id, crypto = ''):
    
    
    mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    watchlist = mycursor.fetchall()[0][0] 
    print('Your Existing Watchlist -->', watchlist.split())
    f = 'y'
    
    while not(get_data(crypto)):
        print("Sorry, we couldn't find this cryptocurrency")
        f = input('Do you want to add other cryptocurrency?(Y/N) --> ')
        if f in 'Yy':
            crypto = name_format(input('Enter the Name of Cryptocurrency You want to Add to Watchlist --> '))
    if f in 'yY' and crypto not in watchlist:
        watchlist += crypto + ' '
        mycursor.execute("UPDATE USERBASE SET WATCHLIST = '{0}' ".format(watchlist) + "WHERE (USERNAME = '{0}')".format(user_id))
        print('Cryptocurrency added to watchlist')
    elif crypto in watchlist:
        print('This cryptocurrency is already in your watchlist')


def rem_from_watchlist(user_id, crypto = ''):

    mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    watchlist = mycursor.fetchall()[0][0].split()
    if not(crypto):
        print('Your Existing Watchlist --> ', watchlist)
        crypto = name_format(input('Enter the Name of Cryptocurrency You want to Remove from Watchlist --> '))
    if crypto in watchlist:
        watchlist.remove(crypto)
        watchlist_new = ''
        for i in watchlist:
            watchlist_new += i + ' '
        mycursor.execute("UPDATE USERBASE SET WATCHLIST = '{0}' ".format(watchlist_new) + "WHERE (USERNAME = '{0}')".format(user_id))
        print('Cryptocurrency removed from watchlist')
    
    else:
        print('The cryptocurrency was not in your watchlist')
        
        
def see_watchlist(user_id):

    mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    watchlist = mycursor.fetchall()[0][0].split()
    if watchlist:
        for i in watchlist:
            show_data(i)
    else:
        print('Your Watchlist is empty.')


def portfolio(user_id):

    mycursor.execute("SELECT BALANCE FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    val = float(mycursor.fetchall()[0][0])
    print ('Your balance is -', val)
    print()
    mycursor.execute("SELECT CRYPTO_NAME FROM PORTFOLIO WHERE (USER_ID = '{0}')".format(user_id))
    crypto_list = mycursor.fetchall()
    if crypto_list:
        for crypto in crypto_list:
            
            data = user_data(user_id, crypto[0])
            avg_buy_price, qty = float(data[5]), float(data[4])
            price = show_data(crypto[0])

            if avg_buy_price > price:
                print('Loss on Current holdings: $', (price - avg_buy_price) * qty)
            else:
                print('Profit on Current holdings: $', (price - avg_buy_price) * qty)
            print()


def buy_crypto(user_id, crypto):
    
    mycursor.execute("SELECT BALANCE FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    val = float(mycursor.fetchall()[0][0])
    print ('Your balance is: $', val)
    price = show_data(crypto)

    data = user_data(user_id, crypto)
    qty = abs(eval(input('Enter Number of Coins you want to Buy --> ')))
    dt = str(datetime.datetime.now()).split()
    if qty:
        balance = val - qty * price
        while balance < 0:
            qty = eval(input('You have low balance, buy lesser quantity --> '))
            balance = val - qty * price
        print('Your balance is: $', balance)
        mycursor.execute("UPDATE USERBASE SET BALANCE = {0} ".format(balance) + "WHERE (USERNAME = '{0}')".format(user_id))
        if data:
            buy_qty, cur_qty, avg_buy_price = float(data[2]) + qty, float(data[4]) + qty, float(data[5]*data[2]) + qty*price
            avg_buy_price /= buy_qty 
            mycursor.execute("UPDATE PORTFOLIO SET TOTAL_BOUGHT = {0}, ".format(buy_qty) + "CURRENT_QTY = {0}, ".format(cur_qty) + "AVG_BUY_PRICE = {0} ".format(avg_buy_price) + "WHERE (USER_ID = '{0}' ".format(user_id) + "AND CRYPTO_NAME = '{0}')".format(crypto))
    
        else:
            values = (user_id, crypto, qty, 0, qty, price, 0, 0)
            mycursor.execute('INSERT INTO PORTFOLIO VALUES{0}'.format(values))
    
        values = (user_id, crypto, qty, price, dt[0].replace('-','/'), dt[1][:8])  
        mycursor.execute('INSERT INTO TRANSACTIONS VALUES{0}'.format(values))
         
         
    else:
        print('No coins Bought')


def sell_crypto(user_id, crypto):
   
    price = show_data(crypto) 
    mycursor.execute("SELECT BALANCE FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    val = float(mycursor.fetchall()[0][0])
    print('Your Current Balance: $', val)
    
    data = user_data(user_id, crypto)
    if data:
        sold_qty, cur_qty, avg_buy_price, avg_sell_price = float(data[3]), float(data[4]), float(data[5]), float(data[6])
        qty = abs(eval(input('Enter the Amount of Coins you want to Sell --> ')))   
        if cur_qty < qty:
            print('You cannot sell more coins than you have')
        else:
             balance = val + qty * price
             cur_qty -= qty
             avg_sell_price = avg_sell_price*sold_qty + price*qty
             sold_qty += qty
             avg_sell_price /= sold_qty
             earn = (avg_sell_price - avg_buy_price)*sold_qty
             dt = str(datetime.datetime.now()).split()
             mycursor.execute("UPDATE USERBASE SET BALANCE = {0} ".format(balance) + "WHERE (USERNAME = '{0}')".format(user_id))
             values = (user_id, crypto, -qty, price, dt[0].replace('-','/'), dt[1][:8])  
             mycursor.execute("UPDATE PORTFOLIO SET TOTAL_SOLD = {0}, ".format(sold_qty) + "CURRENT_QTY = {0}, ".format(cur_qty) + "AVG_SELL_PRICE = {0}, ".format(avg_sell_price) +"EARNINGS = {0} ".format(earn) + "WHERE (USER_ID = '{0}' ".format(user_id) + "AND CRYPTO_NAME = '{0}')".format(crypto))
             mycursor.execute('INSERT INTO TRANSACTIONS VALUES{0}'.format(values))
             print('Your balance is: $', balance)
             
    else:
        print('You have not bought this Cryptocurrency')


def tasks(user_id):
    print('Please Enter A Valid Number from the List')
    buy = ''
    watch = ''
    try:
        act = int(input('What task do you want to perform: \n 1. SEARCH CRYPTOCURRENCY \n 2. SEE PORTFOLIO \n 3. BUY \n 4. SELL \n 5. SEE WATCHLIST \n 6. ADD TO WATCHLIST \n 7. REMOVE FROM WATCHLIST \n --> '))
        
        if act == 1:
            crypto = name_format(input('Enter the Name of Cryptocurrency --> '))
            flag = show_data(crypto)
            if flag:
                buy = input('Do you want to Buy this currency(Y/N) --> ')
                if buy in 'Yy':
                    buy_crypto(user_id, crypto)
                
                mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
                watchlist = mycursor.fetchall()[0][0] 
                if crypto not in watchlist:
                    watch = input('Do you want to Add this currency to Watchlist(Y/N) --> ')
                    if watch in 'yY':
                        add_to_watchlist(user_id, crypto)            
        
        elif act == 2 :
             portfolio(user_id)
             
        elif act == 3:
            crypto = name_format(input('Enter the Name of Cryptocurrency you want to Buy --> '))
            if get_data(crypto):    
                buy_crypto(user_id, crypto)
                mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
                watch = mycursor.fetchall()[0][0] 
                if crypto not in watch:
                    watch = input('Do you want to Add this currency to Watchlist(Y/N) --> ')
                    if watch in 'yY':
                        add_to_watchlist(user_id, crypto)
            else:
                print('Sorry, we could not find cryptocurrency with this name. Please re-check the spelling' )
                
        elif act == 4:
            crypto = name_format(input('Enter the Name of Cryptocurrency you want to Sell --> '))
            if get_data(crypto):
                sell_crypto(user_id, crypto)
        
        elif act == 5:
            see_watchlist(user_id)
            
        elif act == 6: 
            add_to_watchlist(user_id)
        
        elif act == 7:
            rem_from_watchlist(user_id)
        
    except ValueError:
        print('The Value entered is invalid')