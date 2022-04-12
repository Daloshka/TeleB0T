import sqlite3
import telebot
import datetime
import info as botconfig

def create_db():
    conn = sqlite3.connect('users.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INTEGER PRIMARY KEY,
        token text NOT NULL,
        balance INTEGER,
        today INTEGER
    )""")
    return conn

def create_task(info):
    conn = create_db()
    sql = "INSERT OR IGNORE INTO users(userid,token, balance, today) VALUES (?,?,?,?)"
    conn.execute(sql, info)
    conn.commit()
    sql = "INSERT OR IGNORE INTO launch(userid,balance, token) VALUES (?,?,?)"
    info = [info[0],0,info[1]]
    conn.execute(sql, info)
    conn.commit()

def update_task(info): # info = token, userid
    conn = create_db()
    cursor = conn.cursor()
    info = (info[0],info[1])
    sql = "UPDATE users SET token = ? WHERE userid = ?"
    conn.execute(sql, info)
    conn.commit()
    sql = "UPDATE launch SET token = ? WHERE userid = ?"
    conn.execute(sql, info)
    conn.commit()
    cursor.close()

def create_db_launch():
    conn = sqlite3.connect('users.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS launch(
        userid INTEGER PRIMARY KEY,
        balance INTEGER
    )""")


def create_db_random(userid):
    conn = sqlite3.connect('users.db')
    conn.execute("""CREATE TABLE IF NOT EXISTS random(
        userid INTEGER PRIMARY KEY,
        balance INTEGER,
        today INTEGER
    )""")
    return conn
    
def check_balance(userid):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    info = ([userid])
    sql = "SELECT balance, today FROM users WHERE userid = ?"
    balance = conn.execute(sql, info).fetchone()[0]
    return balance

def add_balance(userid, points):
    bot = telebot.TeleBot(botconfig.bot_token)
    today = datetime.datetime.today().day
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    info = ([userid])
    sql = "SELECT balance, today FROM users WHERE userid = ?"
    #print(conn.execute(sql, info).fetchone())
    balance = conn.execute(sql, info).fetchone()[0]
    # Проверка играл ли человек сегодня или нет
    if (today != conn.execute(sql, info).fetchone()[1]):
        balance += points
        info = (balance, userid)
        sql = "UPDATE users SET balance = ? WHERE userid = ?"
        conn.execute(sql, info)
        conn.commit()
        info = (today, userid)
        sql = "UPDATE users SET today = ? WHERE userid = ?"
        conn.execute(sql, info)
        conn.commit()
        conn.close()
        bot.send_message(userid, f"Вы выйграли {points}ч!")
        print(f"Balance of {userid} is updated! It's {balance}")
    else:
        print(userid)
        bot.send_message(userid, "Вы уже испытали удачу сегодня, приходите завтра")

def launch_farm(userid):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    info = ([userid])
    sql = "SELECT balance FROM users WHERE userid = ?"
    balance = conn.execute(sql, info).fetchone()[0]
    print(f"balance = {balance}")

    sql2 = "SELECT balance FROM launch WHERE userid = ?"
    balance2 = conn.execute(sql2, info).fetchone()[0]
    print(f"balance2 = {balance2}")

    balance += balance2
    info = ([balance,userid])
    sql = "UPDATE launch SET balance = ? WHERE userid = ?"
    conn.execute(sql, info)
    conn.commit()
    sql = "UPDATE users SET balance = 0 WHERE userid = ?"
    info = ([userid])
    conn.execute(sql, info)
    conn.commit()

    print(f"Накрутка запущена")

def get_active_tokes():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    sql = "SELECT token FROM launch WHERE balance <> 0"
    sqltokens = conn.execute(sql).fetchall()
    tokens = []
    for token in sqltokens:
        tokens.append(token[0])
    # RETURN LIST OF TOKENS WHERE BALANCE != 0
    return tokens

def minus_hour():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    sql = """UPDATE  launch SET balance = CASE WHEN balance <> 0 THEN balance - 1 ELSE balance END"""
    conn.execute(sql)
    conn.commit()


#minus_hour()
#get_active_tokes()
#reate_db()
