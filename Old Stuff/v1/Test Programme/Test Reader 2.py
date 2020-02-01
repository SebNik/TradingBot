from iexfinance.stocks import Stock
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
start=time.time()

end=0
diff=[]
xs = []
ys = []
#price_alt=0
def animate(i):
    tsla = Stock('AAPL')
    price_neu=tsla.get_price()
    xs.append(price_neu)
    ys.append(time.time())
    ax1.clear()
    ax1.plot(ys, xs)
    print(price_neu)
    # if price_neu!=price_alt:
    #     end=time.time()
    #     diff.append((end-start)/1000)
    #     print(diff)
    #     start=time.time()
    #price_alt=price_neu
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()