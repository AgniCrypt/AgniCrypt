from crypto_module_org import *

f = 1
while f:
    try:
        sign = int(input('Enter 0 to SIGN UP, 1 to SIGN IN --> '))
        if not(sign):
            user_id = sign_up([input('Enter your E-Mail --> '), input('Enter your Date of Birth (yyyy/mm/dd) --> '), input('Create a username --> '), input('Create a password --> '), '', 100000])
            f = 0
            t = 1
            
        elif sign == 1:
            user_id = sign_in(input('Enter E-Mail/Username --> '), input('Enter Password --> ') )
            if user_id:
                f = 0
                t = 1
            else:
                if input('DO YOU WANT TO TRY AGAIN(Y/N) --> ') not in 'Yy':
                    f = 0
                    t = 0
                
        else:
            print('PLEASE ENTER A VALID VALUE')
            if input('DO YOU WANT TO ENTER A NEW VALUE(Y/N) --> ') not in 'Yy':
                f = 0
                t = 0
        
    except ValueError:
    
        print('PLEASE ENTER A VALID VALUE')
        if input('DO YOU WANT TO ENTER A NEW VALUE(Y/N) --> ') not in 'Yy':
             f = 0
             t = 0
        
while  t:  
    tasks(user_id)
    flag = input('Do you want to perform another task(Y/N) --> ')
    if flag not in 'yY':
        t = 0    
        
