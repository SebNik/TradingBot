#Dieses Modul soll alle Transaktionen und Konten verwalten
#Die Konten werden mit einer Klasse verwaltet 
#Dabei werden alle Transaktionen von einem serperten Modul mitgeschrieben
#Dieses Modul ist das Log File Modul
#Es gibt für ein Konto immer drei Optionen
#1:     Geld auf das Konto buchen
#2:     Geld von einem Konto abhheben also minus
#Dabei muss dann angegebn werden was gekauft wurde und wie viel
#3:     Geld auf ein Konto buchen
#Die Daten zu dem buchen und abbuchen kommen von noch einem weitern Modul
#Das ermittelt mit Hilfe der Kurs Files den Gewinn bzw. Verlust des Kaufs
#Es gibt auch ein Besitzmodul

class Konto():
    def __init__(self,start_kapital,konto_type,konto_id):
        self.__value=start_kapital
        self.__type=konto_type
        self.__konto_id=konto_id
        self.__verkaufgebühr=0.003
        global name
        name=self.__konto_id
        global pfad
        pfad="d:\Python/Programme/Wirtschaft"
        import Error_Modul_v1
        import os, os.path
        try:
            if os.path.isdir(pfad+'/'+name) is False:
                os.makedirs(os.path.join(pfad,name))
                f=open(pfad+'/'+name+'/'+name+'-Konto File.txt','x')
                f.close()
                f=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','x')
                f.close()
            else:
                Error_Modul_v1.error('error1')
        except:
            Error_Modul_v1.error('error5')

    def buchen(self,wert):
        self.__value+=wert
    
    def buy(self,symbol,anzahl):
        import Read_Modul_v1
        import Error_Modul_v1
        x,price=Read_Modul_v1.read_share_live(symbol,0)
        self.__value-=(price*anzahl)+(price*anzahl*self.__verkaufgebühr)
        try:
            f=open(pfad+'/'+name+'/'+name+'-Konto File.txt','r')
            inhalt_transaktion=f.readlines()
            f.close()
            #Es werden jetzt viele Daten notiert
            #Dir Reihenfolge beträgt: ID:B oder S buy or Sell;Aktien Name;Aktueller Preis;Preis aller Aktien;Verkausgebhren;Summe;neuer Kontostand
            ID=0
            if len(inhalt_transaktion)!=0:
                zahlen=[]
                for i in inhalt_transaktion:
                    zahlen.append(int(i.split(':')[0]))
                ID=max(zahlen)+1
            else:
                ID=1
            import time
            lt=time.localtime()
            time_real=time.strftime('%d.%m.%Y;%H.%M.%S',lt)
            f=open(pfad+'/'+name+'/'+name+'-Konto File.txt','a')
            f.write(str(ID)+':'+'B'+str(symbol)+';'+str(price)+';'+str(anzahl)+';'+str(price*anzahl)+';'+str(price*anzahl*self.__verkaufgebühr)+';'+str((price*anzahl)+(price*anzahl*self.__verkaufgebühr))+';'+str(self.__value)+';'+str(time_real)+'\n')
            f.close()
            b=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','r')
            inhalt=b.readlines()
            b.close()
            if len(inhalt)!=0:
                if symbol in inhalt[len(inhalt)-1]:
                    b=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','a')
                    inhalt_format=inhalt[len(inhalt)-1].split(';')
                    #print(inhalt_format)
                    stelle=inhalt_format.index(symbol)
                    #print(stelle)
                    inhalt_format[stelle+1]=int(inhalt_format[stelle+1])+anzahl
                    #print(inhalt_format)
                    summe=''
                    for j in inhalt_format:
                        summe+=';'+str(j) 
                    #print(summe)
                    b.write(summe+'\n')
                    b.close()
                else:
                    b=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','a')
                    b.write(str(inhalt[-1]).strip()+';'+symbol+';'+str(anzahl)+'\n')
                    b.close()
            else:
                b=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','a')
                b.write(';'+symbol+';'+str(anzahl)+'\n')
                b.close()
        except:
            Error_Modul_v1.error('error2')

    def sell(self,symbol,anzahl,id_verkauf):
        f=open(pfad+'/'+name+'/'+name+'-Konto File.txt','r')
        inhalt_transaktion=f.readlines()
        f.close()
        f=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','r')
        inhalt_besitz=f.readlines()
        f.close()
        vorhanden=None
        for i in inhalt_besitz:
            if symbol in i:
                vorhanden=True
        if vorhanden==False:
            import Error_Modul_v1
            Error_Modul_v1.error('error6')
        if len(inhalt_besitz)==1:
            inhalt_besitz_format=inhalt_besitz[-1].split(';')
        else:
            inhalt_besitz_format=inhalt_besitz[-2].split(';')
        stelle=inhalt_besitz_format.index(symbol)
        if anzahl>int(inhalt_besitz_format[stelle+1]):
            import Error_Modul_v1
            Error_Modul_v1.error('error7')
        import Read_Modul_v1
        x,price=Read_Modul_v1.read_share_live(symbol,0)
        #print('Price now: ', price)
        if id_verkauf=='all':
            None
        zahlen=[]
        for i in inhalt_transaktion:
            zahlen.append(int(i.split(':')[0]))
        if id_verkauf in zahlen:
            inhalt_transaktion_format=[]
            for i in inhalt_transaktion:
                inhalt_transaktion_format.append(str(i.split(':')[0]))
                inhalt_transaktion_format.append(str(i.split(':')[1]))
            #print(inhalt_transaktion_format)
            stelle=inhalt_transaktion_format.index(str(id_verkauf))
            relevante_daten=inhalt_transaktion_format[stelle+1].split(';')
            #print(relevante_daten[1])
            delta=float(relevante_daten[1])-float(price)
            self.__value=self.__value+(price-(delta+(delta*self.__verkaufgebühr)))*anzahl
            neue_anzahl=int(relevante_daten[2])-anzahl
        else:
            import Error_Modul_v1
            Error_Modul_v1.error('error8')
        f=open(pfad+'/'+name+'/'+name+'-Konto File.txt','a')
        f.write(str(id_verkauf)+':'+'S'+';'+str(price)+';'+str(relevante_daten[1])+';'+str(delta)+';'+str(float(price)*100/float(relevante_daten[1])-100)+'\n')
        f.close()
        f=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','a')
        if len(inhalt_besitz)==1:
            last_line=inhalt_besitz[-1].split(';')
        else:
            last_line=inhalt_besitz[-2].split(';')
        stelle=last_line.index(symbol)
        #print(last_line)
        last_line[stelle+1]=int(last_line[stelle+1])-neue_anzahl
        #print(last_line)
        write=''
        for i in last_line:
            if i != '':
                write+=';'
            write+=str(i)
        print(write)
        f.write(write+'\n')
        f.close()
    def __str__(self):
        print('')
        print('Die Konto ID ist: ', self.__konto_id)
        print('Der Kontotyp ist: ',self.__type)
        print('Der aktuelle Kontostand beträgt: ',self.__value)
        print('')
        print('-----Status-Bericht abgeschlossen-----')

test=Konto(500,'manuell','Test_Konto')
#print(test)
test.buy('AAPL',3)
#print(test)
# test.buy('TSLA',3)
# test.buy('AMZN',2)
# test.buy('AAPL',2)
test.sell('AAPL',1,1)
# test.buy('TSLA',3)
# test.buy('AAPL',4)
#print(test)