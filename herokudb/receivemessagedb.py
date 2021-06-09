import serial
from time import sleep
import io
import binascii
import codecs
import textwrap
import updatedb

ser = serial.Serial('/dev/ttyS0', 57600)  # open serial port
print(ser.name)         # check which port was really used

code = str(1234)
global temp
global humi
global date

komennot = [
    'sys get ver',
    'sys get hweui',
    'radio set wdt 0',
    'mac pause'
]
for m in komennot:
        ser.write(m.encode())
        ser.write(b'\r\n')
        r = ser.readline().decode()
        if len(r):
            print('\t<<{r}'.format(r=r[:-2]))
        else:
            print('\t<< no response')
            
def receive():
    i=1
    global temp, humi, date
    while i==1:
        #print('start')
        sleep(.2)
        ser.write('radio rx 0'.encode())
        ser.write(b'\r\n')
        #if ser.readable():                
        response = ser.readline().decode()
        if response.startswith('radio_rx'):
            print(response)
            msg2 = response[10:][:-2]
            msg3 = len(msg2)
            print(msg2)
            print(msg3)
            if (((not msg2.endswith('o'))) and (msg3 == 60)) and not msg2.endswith('k'):
                msg = binascii.unhexlify(msg2.encode()).decode()
                codeS, temp, humi, date = msg.split(';')               
                if code == codeS:
                    #print(msg)
                    print(temp, humi, date)
                    updatedb.database(temp, humi, date)
                else:
                        print('wrong code')
            else:
                print('odd length string')
    else:
        print('loppu')
            
receive()
