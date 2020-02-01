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
        pfad = "d:\Python/Programme/Wirtschaft"
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
        #try:
        f=open(pfad+'/'+name+'/'+name+'-Konto File.txt','a')
        f.write(' \n')
        f.write('-----------------------------------------------------------------\n')
        f.write('Es wird nun die Aktie '+str(symbol)+' gekauft'+'\n')
        f.write('Ihr aktueller Preis beträgt: '+str(price)+'\n')
        f.write('Die Aktien die Sie kaufen Kosten: '+str(price*anzahl)+'\n')
        f.write('Die Verkausgebühren betragen: '+str(price*anzahl*self.__verkaufgebühr)+'\n')
        f.write('Die Summe beträgt: '+str((price*anzahl)+(price*anzahl*self.__verkaufgebühr))+'\n')
        f.write('Der neue Kontostand beträgt: '+str(self.__value)+'\n')
        f.write('-----------------------------------------------------------------\n')
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
                b.write(summe)
                b.close()
            else:
                b=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','a')
                b.write(str(inhalt[-1]).strip()+';'+symbol+';'+str(anzahl)+'\n')
                b.close()
        else:
            b=open(pfad+'/'+name+'/'+name+'-Besitz File.txt','a')
            b.write(';'+symbol+';'+str(anzahl)+'\n')
            b.close()
        #except:
            #Error_Modul_v1.error('error2')

    def __str__(self):
        print('')
        print('Die Konto ID ist: ', self.__konto_id)
        print('Der Kontotyp ist: ',self.__type)
        print('Der aktuelle Kontostand beträgt: ',self.__value)
        print('')
        return '-----Status-Bericht abgeschlossen-----'

test=Konto(500,'manuell','Test_Konto')
#print(test)
test.buy('AAPL',2)
# test.buy('TSLA',3)
# test.buy('AMZN',2)
# test.buy('AAPL',2)
# test.buy('TSLA',3)
# test.buy('AAPL',4)
# print(test)