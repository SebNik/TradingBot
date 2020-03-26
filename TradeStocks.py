# this file is responsible for all buying and selling actions and their logging
def check_database():
    import sqlite3
    import os

    if os.path.isfile('test.db') == False:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE stocks
                         (date text, trans text, symbol text, qty real, price real)''')
    else:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    conn.commit()
    data = c.execute("SELECT * FROM stocks")
    for i in data:
        print(i)
    conn.close()


if __name__ == "__main__":
    check_database()
