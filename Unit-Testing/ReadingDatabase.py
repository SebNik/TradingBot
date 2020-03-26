def check_database(file='/home/niklas/Desktop/TradingBot/api-key_logs.db'):
    import sqlite3
    import os
    import sys
    if not os.path.isfile(file):
        print('not found')
        sys.exit(0)
    else:
        conn = sqlite3.connect(file)
        c = conn.cursor()
    data = c.execute("SELECT * FROM ApiKeyLog")
    for i in data:
        print(i)
    conn.close()


if __name__ == "__main__":
    check_database()
