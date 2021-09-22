from crypto_module import *

mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Pragyaat@123', database = 'agnicrypt')
mycursor = mydb.cursor()

try:
    sign = int(input('Enter 0 to SIGN IN, 1 to SIGN UP --> '))
    if sign:
        user_id = sign_up()
    
    else:
        user_id = sign_in()
    
except ValueError:
        user_id = sign_up()

f = 1        
while  f:  
    print('Please Enter A Valid Number from the List')
    buy = ''
    watch = ''
    try:
        act = int(input('What action do you want to perform: \n 1. SEE STATISTICS \n 2. BUY \n 3. SELL \n --> '))
        if act == 1:
            crypto = name_format(input('Enter the Name of Cryptocurrency --> '))
            flag = show_data(crypto)
            if flag:
                buy = input('Do you want to Buy this currency(Y/N) --> ')
        
        if act == 2 or buy in 'yY':
            pass
        
        if act ==3:
            pass
        a = input('Do you want to perform another action(Y/N) --> ')
        
        if a not in 'Yy':
            f = 0
    
    except ValueError:
        pass
        
