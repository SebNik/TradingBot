import Read_Modul_v1
import Plot_Modul_v1
import Kurs_Modul_v1

print(Kurs_Modul_v1.new_share('AAPL'))

while True:
    x,y=Read_Modul_v1.read_share_live('AAPL',0.5)
    Kurs_Modul_v1.write_data(x,y,'AAPL')

    