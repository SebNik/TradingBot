#Das Kurs Modul soll alle Daten welche gelesen werden speichern
#Diese sollen jeweils in einem Neuen Ordner gespeichert werden
#Dabei werden der Aktien Preis die Uhrzeit und andere Dinge festgehalten

def new_share(name):
    import os, os.path
    pfad = "d:\Python/Programme/Wirtschaft"
    if os.path.isdir(pfad+'/'+name) is False:
        os.makedirs(os.path.join(pfad,name))
        f=open(pfad+'/'+name+'/'+name+'-Kurs File.txt','x')
        f.close()
        return True
    else:
        return 'error1'

def write_data(date,data,name):
    import os, os.path
    pfad = "d:\Python/Programme/Wirtschaft"
    if os.path.isdir(pfad+'/'+name):
        f=open(pfad+'/'+name+'/'+name+'-Kurs File.txt','r')
        lines=0
        for line in f.readlines():
            lines+=1
        f.close()
        f=open(pfad+'/'+name+'/'+name+'-Kurs File.txt','a')
        f.write(str(lines+1)+' '+name+' '+str(data)+' '+str(date)+'\n')
        f.close()
        return True
    else:
        return 'error2'