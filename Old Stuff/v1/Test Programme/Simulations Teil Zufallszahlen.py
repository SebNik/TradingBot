import random
import matplotlib.pyplot as pl

def gen(range_max):
    all_numbers=[]
    counts=[]
    x_achse=[]
    random.seed(1)
    for x in range(0,range_max):
        a=random.randrange(0,100)
        all_numbers.append(a)
    for j in range(0,100):
        print('Number: ', j, 'Value: ', all_numbers.count(j))
        counts.append(all_numbers.count(j))
        x_achse.append(j)
    print('der Durchschnitt war: ', sum(counts)/len(counts))
    pl.plot(x_achse,counts,'b--')
    pl.show()
gen(100000000)
