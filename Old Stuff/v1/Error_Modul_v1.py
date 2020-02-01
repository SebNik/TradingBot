#Das Error Modul hat einen sehr einfachen Job
#Es liest die Error Textdatei aus und beim Aufrufe git es den Fehler aus un schließt das Programm
#Die Error Datei ist eine Textdatei welche augelesen wird 

def error(fehlermeldung_sum):
    import sys
    import time
    path_file='d:\Python/Programme/Wirtschaft/'
    f=open(path_file+'Errors.txt','r')
    inhalt_Fehler=f.readlines()
    print('Hey Hey Hey du Sack\ndu hast falsch programmiert Opfer es gab einen Fehler: ')
    print(inhalt_Fehler[int(fehlermeldung_sum[5])-1])
    #print(int(fehlermeldung_sum[5]))
    f.close()
    time.sleep(5)
    #print(inhalt_Fehler[int(fehlermeldung_sum[5])-1][12])
    if int(inhalt_Fehler[int(fehlermeldung_sum[5])-1][12])==1:
        print('')
        print('-------------------')
        print('')
        print('Das Programm wird getötet hahahhahahahahah')
        print('')
        print('-------------------')
        print('')
        sys.exit()