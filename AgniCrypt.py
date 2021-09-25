from crypto_module import *

f = 1
while f:
    try:
        sign = int(input('Enter 0 to SIGN UP, 1 to SIGN IN --> '))
        if not(sign):
            user_id = sign_up()
            f = 0
            
        elif sign == 1:
            user_id = sign_in()
            if user_id:
                f = 0
        else:
            print('PLEASE ENTER A VALID VALUE')
    
    except ValueError:
        print('PLEASE ENTER A VALID VALUE')

f = 1        
while  f:  
    actions(user_id)
    flag = input('Do you want to perform another action(Y/N) --> ')
    if flag not in 'yY':
        f = 0
        