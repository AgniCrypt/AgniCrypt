
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
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', database = 'agnicrypt')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT USERNAME FROM USERBASE WHERE (EMAIL = '" + email +"')" )
    taken = mycursor.fetchall()
    f = 0
    if not(re.search(regex,email)):
        f = 1
    elif taken:
        f = 2
    return f   

        
def sign_in():
    
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', database = 'agnicrypt')
    mycursor = mydb.cursor()
    
    user_id = input('Enter E-Mail/Username --> ')
    password = input('Enter Password --> ')  
    mycursor.execute("SELECT PASSWORD, USERNAME FROM USERBASE WHERE (EMAIL = '" + user_id +"') OR (USERNAME = '" + user_id +"')")
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
    
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', database = 'agnicrypt')
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
    password = input('Create a password --> ')
    user_data = [email, dob, username, password, '']
    f = 1
    while f:
        try:
            mycursor.execute('INSERT INTO USERBASE VALUES' + str(tuple(user_data)))
            mydb.commit()
            print('Your user_id has been created, Thank You')
            f = 0
        
        except mysql.connector.errors.DataError:
            user_data[1] = input('Enter Valid Date of Birth (yyyy/mm/dd) --> ')
            
        except mysql.connector.errors.IntegrityError:
            user_data[2] = input('This Username has Already Been Taken, Please Create Some Other --> ')            
            
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
        
        print('Current Price: ', x[0])
        print('Price changed: ', x[1][0],'/', x[1][1])
        print('24h Low: ', x[2][0])
        print('24h high: ',x[2][1])
        print('Trading Volume: ', x[3][0], '/', x[3][1])
        print('Market Cap: ', '$' + str(eval(x[3][0][1:].replace(',', ''))/eval(x[4].replace(',', ''))))
        print('Market Dominance: ', x[5])
        print('Market rank: ', x[6])
        return 1
    
    else:
        print("Sorry, we couldn't find cryptocurrency with this name. Please re-check the spelling.")
        