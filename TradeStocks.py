# this file is responsible for all buying and selling actions and their logging
class Stock:
    def __init__(self):
        None


def check_database():
    import sqlite3
    import os
    x = 'test'
    if not os.path.isfile('test.db'):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('CREATE TABLE {} (date TEXT, trans text, symbol text, qty real, price real)'.format(x + '2'))
    else:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
    tableName = x + '2'
    stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tableName)
    c.execute(stmt)
    result = c.fetchone()
    if result:
        # there is a table named "tableName"
        print('existing')
    else:
        # there are no tables named "tableName"
        print('not found')

    # Insert a row of data
    sql = "INSERT INTO {} VALUES".format(x + '2')
    c.execute(sql + " ('2006-01-05','BUY','RHAT', {} ,35.14)".format(1562))
    # c.execute("INSERT INTO ? VALUES (?,?,?,5,5);", ('213', 'RHAT', '5'),(x))
    conn.commit()
    data = c.execute("SELECT * FROM {}".format(x + '2'))
    for i in data:
        print(i)
    conn.close()


if __name__ == "__main__":
    check_database()
