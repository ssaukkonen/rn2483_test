import serial
from time import sleep
import io
import binascii
import codecs

ser = serial.Serial('/dev/ttyS0', 57600)  # open serial port
print(ser.name)         # check which port was really used

komennot = [
    'sys get ver',
    'sys get hweui',
    'radio set wdt 0',
    'mac pause',
    'radio rx 0'
]
for m in komennot:
        ser.write(m.encode())
        ser.write(b'\r\n')
        r = ser.readline().decode()
        if len(r):
            print('\t<<{r}'.format(r=r[:-2]))
        else:
            print('\t<< no response')
response = ser.readline().decode()
#print(response)
msg2 = response[10:][:-2]
#print(msg2)
msg = binascii.unhexlify(msg2.encode()).decode()
print(msg)
ser.close()
exit()