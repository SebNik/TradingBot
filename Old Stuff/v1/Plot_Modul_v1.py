#Das Modul soll alle Möglichen Plot Möglichkeiten haben
#Es soll einfache Module haben 
#Es muss einfache Graphen aber auch Candelsticks können

def graph_simple(x,y,style_use):
    try:
        import matplotlib.pyplot as plt
        from matplotlib import style
        style.use(style_use)
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        plt.plot(x,y)
        # plt.xlable('Date')
        # plt.ylabel('Data')
        for lable in ax1.xaxis.get_ticklabels():
            lable.set_rotation(45)
        plt.show()
    except:
        return 'error4'