import serial
from time import sleep
import io
import board
import adafruit_dht
import binascii

ser = serial.Serial('/dev/ttyS0', 57600)  # open serial port
print(ser.name)         # check which port was really used

#Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17, False)
global temp

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
            
def sendRadio():
    global temp
    print(temp+' radio')
    msg = temp.encode("utf-8").hex()       
    print(msg)
    send = 'radio tx '
    ser.write(send.encode('utf_8')+msg.encode('utf_8')+'\r\n'.encode('utf_8'))     # write a string
    sleep(.2)
    response = ser.readline().decode()
    print(response)
    sleep(2)
    getValues()

def getValues():
    while True:
        try:
            global temp
            temperature_c = dhtDevice.temperature
            print(temperature_c)
            temp = str(temperature_c)
            print(temp+' values')
            sendRadio()
        except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        sleep(2.0)            

getValues()
