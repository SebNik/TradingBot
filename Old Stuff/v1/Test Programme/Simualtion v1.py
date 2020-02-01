import time
import random
import matplotlib.pyplot as pl

def cal(min,max,kurs):
    change=random.randint(min,max)
    change_fac=1/change
    abs=change_fac*kurs
    return abs

def Simulation():
    win_min=30
    win_max=500
    lose_min=30
    lose_max=500
    big_lose_min=5
    big_lose_max=10
    gewinn_w=[1,2,3]
    verlust_w=[4,5,6]
    big_verlust_w=[6]
    time_x=[0]
    kurs_y=[]
    global kurs
    kurs=0
    kurs=random.randint(0,3600000)
    kurs_y.append(kurs)
    for j in range(0,100):
        choice_1=random.randint(1,6)
        if choice_1 in gewinn_w:
            change=cal(win_min,win_max,kurs)
            kurs+=change
        if choice_1 in verlust_w:
            change=cal(lose_min,lose_max,kurs)
            kurs-=change
        # if choice_1 in big_verlust_w:
        #     change=cal(big_lose_min,big_lose_max,kurs)
        #     kurs-=change
        time_x.append(j)
        kurs_y.append(kurs)
        #time.sleep(1)
    #print(time_x)
    pl.plot(time_x,kurs_y,'b--')
    pl.show()
    
Simulation()