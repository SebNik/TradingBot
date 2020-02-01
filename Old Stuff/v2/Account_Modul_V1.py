#this is the account modul it is going to manage all transactions and the portfolio
#it is going to mange all the data in two cvs files
#the two files are the portfolio.cvs file
#and the transactions.cvs file

def create_files(path):
    f=open(path+'portfolio.csv','x')
    f.close()
    f=open(path+'transactions.csv','x')
    f.close()

def update(path):
    import csv
    with open(path+'portfolio.csv', 'r') as portfolio_file:
        csvreader_portfolio=csv.reader(portfolio_file)
        data_portfolio=list(csvreader_portfolio)
    data_portfolio_format=[]
    for i in range(0,len(data_portfolio)-1):
        data_portfolio_format.append(data_portfolio[i][0].split(';'))
    #print(data_portfolio_format)
    #['ID', 'Symbol', 'Avg Buy Price', 'Untis', 'Value', 'Last Price', 'Profit/Lost', 'Broker Fee']
    #   0      1             2            3        4          5              6              7
    import Read_Stock_V1
    for i in data_portfolio_format:
        if (i[0]=='ID'):
            continue
        last_price=Read_Stock_V1.read_share_live(i[1],0)
        #last_price=Read_Stock_V1.sim()
        #last_price=200
        i[5]=last_price
        i[4]=float(last_price)*float(i[3])
        i[6]=float(i[4])-float(i[2])*float(i[3])+float(i[7])
        print(i)

    #print(data_portfolio[0][0].split(';'))
    # with open(path+'transactions.csv', 'r') as transactions_file:
    #     csvreader_transactions=csv.reader(transactions_file)
    #     data_transactions=list(csvreader_transactions)

pfad="d:\Python/Programme/Wirtschaft/v2 Niklas ein weniger Noob/"
#create_files(pfad)
update(pfad)

