
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


def check(email):   
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT USERNAME FROM USERBASE WHERE (EMAIL = '{0}')".format(email))
    taken = mycursor.fetchall()
    f = 0
    if not(re.search(regex,email)):
        f = 1
    elif taken:
        f = 2
    return f   

        
def sign_in():
    
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
    mycursor = mydb.cursor()
    
    user_id = input('Enter E-Mail/Username --> ')
    password = input('Enter Password --> ')  
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
            
        
def sign_up():
    
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
    mycursor = mydb.cursor()
    email = input('Enter your E-Mail --> ')
    f = check(email)
    while f:
        print(f)
        if f == 1:     
            email = input('Please Enter Valid E-Mail --> ')
        elif f == 2:
            email = input('This Email is Already Registered, Please Enter Another E-Mail --> ')
        f = check(email)
        
    dob = input('Enter your Date of Birth (yyyy/mm/dd) --> ')
    username = input('Create a username --> ')
    while not(username):
        username = input('Username cannot be blank, Create a username --> ')
    password = input('Create a password --> ')
    while not(password):
        password = input('Password cannot be blank, Create a password --> ')
        
    user_data = [email, dob, username, password, '', 100000]
    f = 1
    while f:
        try:
            mycursor.execute('INSERT INTO USERBASE VALUES{0}'.format(tuple(user_data)))
            mydb.commit()
            print('Your user_id has been created, Thank You')
            f = 0
        
        except mysql.connector.errors.DataError:
            user_data[1] = input('Enter Valid Date of Birth (yyyy/mm/dd) --> ')
            
        except mysql.connector.errors.IntegrityError:
            user_data[2] = input('This Username is not available, Please Create Some Other --> ')            
            
    return user_data[2]
  

def name_format(name):
    return '-'.join(name.lower().replace('.', ' ').split())


def get_data(currency_name):
    
    url = 'https://coinmarketcap.com/currencies/{0}'.format(currency_name)
    soup = BeautifulSoup(requests.get(url).text.encode('utf-8'), 'html.parser')
    
    try:
        table = soup.find_all('table')[0]
        elements = table.find_all("tr")
        cypto_data = [i.get_text(' ').strip().split('/n')[0].split() for i in elements]
        
        return cypto_data[0][-1], (cypto_data[1][-3], cypto_data[1][-2] + '%'), (cypto_data[2][-3], cypto_data[2][-1]) ,(cypto_data[3][-3], cypto_data[3][-2] + '%'), cypto_data[4][-1], cypto_data[5][-2] + '%', cypto_data[6][-1]
    
    except IndexError:
        pass


def show_data(crypto_name):
   
    x = get_data(crypto_name)
    if x:
        
        print('Cryptocurrency:', crypto_name)
        print('Current Price: ', x[0])
        print('Price changed: ', x[1][0],'/', x[1][1])
        print('24h Low: ', x[2][0])
        print('24h high: ',x[2][1])
        print('Trading Volume: ', x[3][0], '/', x[3][1])
        print('Market Cap: ', '$' + str(eval(x[3][0][1:].replace(',', ''))/eval(x[4].replace(',', ''))))
        print('Market Dominance: ', x[5])
        print('Market rank: ', x[6])
        print()
        return 1
    
    else:
        print("Sorry, we couldn't find cryptocurrency with this name. Please re-check the spelling.")


def predict(crypto_currency):    
    
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import pandas_datareader as web
    import datetime as dt 
    
    from sklearn.preprocessing import MinMaxScaler
    from tensorflow.keras.layers import Dense, Dropout, LSTM
    from tensorflow.keras.models import Sequential
    
    crypto_currency = 'ETH'
    against_currency = 'USD'
    
    #This is the time frame that we will be going to teach the algorithm.
    start = dt.datetime(2019,1,1)
    end = dt.datetime.now()
    
    data = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo', start, end)
    
    #Prepare DATA
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data =  scaler.fit_transform(data['Close'].values.reshape(-1,1))
    
    #In this say if we are going to teach it for 40 days it will predict what the price will be after the number of future days
    prediction_days = 40
    
    #Future day is telling in the graph that at the moment what the price may be after those many days
    #If you want to know prediction of next day, set this as 1.
    future_day = 30
    
    
    x_train, y_train = [], []
    
    for x in range(prediction_days, len(scaled_data)-future_day):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x+future_day, 0])
    
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[1], 1))
    model = Sequential()
    
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)
    
    #Testing the model
    
    test_start = dt.datetime(2020,1,1)
    test_end = dt.datetime.now()
    
    test_data = web.DataReader(f'{crypto_currency}-{against_currency}','yahoo', test_start, test_end)
    actual_prices = test_data['Close'].values
    
    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)
    
    model_inputs = total_dataset[len(total_dataset) -len(test_data)- prediction_days:].values
    model_inputs = model_inputs.reshape(-1,1)
    model_inputs = scaler.fit_transform(model_inputs)
    
    x_test = []
    
    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x, 0])
    
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))
    
    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)
    
    
    plt.plot(actual_prices, color='blue', label='Actual Prices')
    plt.plot(prediction_prices, color='red', label='Predicted Prices')
    plt.title(f'{crypto_currency} price prediction')
    plt.xlabel('')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.show()        
  

def add_to_watchlist(user_id, crypto_name):
    
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    watch = mycursor.fetchall()[0][0] 
    if crypto_name not in watch:
        watch += crypto_name + ' '
        mycursor.execute("UPDATE USERBASE SET WATCHLIST = '{0}' ".format(watch) + "WHERE (USERNAME = '{0}')".format(user_id))
        mydb.commit()


def watchlist(user_id):
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT WATCHLIST FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    watchlist = mycursor.fetchall()[0][0].split()
    
    for i in watchlist:
        show_data(i)


def buy_crypto(user_id, crypto):
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT BALANCE FROM USERBASE WHERE (USERNAME = '{0}')".format(user_id))
    val = float(mycursor.fetchall()[0][0])
    print ('Your balance is -', val)
    
    price = eval(get_data(crypto)[0][1:].replace(',', ''))
    print('Price of each coin is - ', price)
    qty = abs(eval(input('Enter Number of Coins you want to Buy --> ')))
    dt = str(datetime.datetime.now()).split()
    
    if qty:
        balance = val - qty * price
        while balance < 0:
            qty = eval(input('You have low balance, buy lesser quantity --> '))
            balance = val - qty * price
        print('Your balance is -', balance)
        
        mycursor.execute("UPDATE USERBASE SET BALANCE = {0} ".format(balance) + "WHERE (USERNAME = '{0}')".format(user_id))
        values = (user_id, crypto, qty, price, dt[0].replace('-','/'), dt[1][:8])  
        mycursor.execute('INSERT INTO TRANSACTIONS VALUES{0}'.format(values))
        mydb.commit() 
     
    else:
        print('Enter some quantity if you want to buy')
        
def actions(user_id):
    print('Please Enter A Valid Number from the List')
    buy = ''
    watch = ''
    try:
        act = int(input('What action do you want to perform: \n 1. SEE WATCHLIST \n 2. SEE PORTFOLIO \n 3. BUY \n 4. SELL \n 5. SEARCH CRYPTOCURRENCY --> '))
        if act == 1:
            watchlist(user_id)
        
        if act == 2 :
            pass
        
        if act == 3:
            crypto = name_format(input('Enter the Name of Cryptocurrency --> '))
            if get_data(crypto):    
                buy_crypto(user_id, crypto)
                watch = input('Do you want to Add this currency to Watchlist(Y/N) --> ')
                if watch in 'yY':
                    add_to_watchlist(user_id, crypto)
            else:
                print('Sorry, we could not find cryptocurrency with this name. Please re-check the spelling' )
        
        if act == 4:
            pass
        
        if act == 5:
            crypto = name_format(input('Enter the Name of Cryptocurrency --> '))
            flag = show_data(crypto)
            
            if flag:
                buy = input('Do you want to Buy this currency(Y/N) --> ')
                if buy in 'Yy':
                    buy_crypto(user_id, crypto)
                
                watch = input('Do you want to Add this currency to Watchlist(Y/N) --> ')
                if watch in 'yY':
                    add_to_watchlist(user_id, crypto)
        
            
       
    
    except ValueError:
        pass
