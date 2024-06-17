def Create_Database_AgniCrypt():
    import mysql.connector
    mycon=mysql.connector.connect(host='localhost',user='root',passwd='123123')    
    cursor=mycon.cursor()
    mycon.autocommit=True
    s1="create database AgniCrypt"
    cursor.execute(s1)
Create_Database_AgniCrypt()

def connection():
    import mysql.connector
    mycon=mysql.connector.connect(host='localhost',user='root',passwd='123123',database='AgniCrypt')
    if mycon.is_connected():
        print("successfully connected")
connection()

def table_creation_userbase():
    import mysql.connector
    mycon=mysql.connector.connect(host='localhost',user='root',passwd='123123',database='AgniCrypt')
    cursor=mycon.cursor()
    mycon.autocommit=True
    s1="create table userbase (email varchar(256) not null, dob date not null, username varchar(128) not null primary key, password varchar(128) not null, watchlist varchar(10000), balance decimal(64,16))"
    cursor.execute(s1)
table_creation_userbase()

def table_creation_transactions():
    import mysql.connector
    mycon=mysql.connector.connect(host='localhost',user='root',passwd='123123',database='AgniCrypt')
    cursor=mycon.cursor()
    mycon.autocommit=True
    s1 = "create table transactions (username varchar(128) not null, crypto_name varchar(128) not null, qty decimal(64,16), price decimal(64,16), tran_date date not null, tran_time time)"
    cursor.execute(s1)
table_creation_transactions()

def table_creation_portfolio():
    import mysql.connector
    mycon=mysql.connector.connect(host='localhost',user='root',passwd='123123',database='AgniCrypt')
    cursor=mycon.cursor()
    mycon.autocommit=True
    s1="create table portfolio (user_id varchar(128) not null, crypto_name varchar(128) not null, total_bought decimal(64,16), total_sold decimal(64,16), current_qty decimal(64,16), avg_buy_price decimal(64,16), avg_sell_price decimal(64,16), earnings decimal(64,16))"
    cursor.execute(s1)
table_creation_portfolio()
