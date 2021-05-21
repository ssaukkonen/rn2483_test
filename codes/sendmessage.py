import serial
from time import sleep
import io

ser = serial.Serial('/dev/ttyS0', 57600)  # open serial port
print(ser.name)         # check which port was really used

komennot = [
    'sys get ver',
    'sys get hweui',
    'mac pause',
    'radio set pwr 14'
]
for m in komennot:
        ser.write(m.encode())
        ser.write(b'\r\n')
        r = ser.readline().decode()
        if len(r):
            print('{r}'.format(r=r[:-2]))
        else:
            print('\t<< no response')
            
msg = 'hello worldäää'.encode("utf-8").hex()
print(msg)
send = 'radio tx '
ser.write(send.encode('utf_8')+msg.encode('utf_8')+'\r\n'.encode('utf_8'))     # write a string
sleep(.2)
response = ser.readline().decode()
print(response)
ser.close()             # close port
exit()
