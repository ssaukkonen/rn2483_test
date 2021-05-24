import serial
from time import sleep
import io
import binascii
import codecs
import textwrap

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
            if (((msg3 % 2) == 0) and (msg3 == 60)):
                msg = binascii.unhexlify(msg2.encode()).decode()
                codeS, temp, humi, date = msg.split(';')               
                if code == codeS:
                    #print(msg)
                    print(temp, humi, date)
                    writeToFile()
                else:
                        print('wrong code')
            else:
                print('odd length string')
    else:
        print('loppu')
        
def writeToFile():
    global temp, humi, date
    data = open('../data.txt', 'a')
    data.write('{};{};{}\n'.format(temp, humi, date))
    printData()
    
def printData():
    with open('../data.txt') as data:
        sumTemp = 0 # initialize here, outside the loop
        sumHumi = 0
        maxT = 0
        minT = 1000
        maxH = 0
        minH = 100
        count = 0 # and a line counter
        for line in data:
            count += 1 # increment the counter
            data2 = line.split(';')
            #print(data2[0])
            sumTemp += float(data2[0]) # add here, not in a nested loop
            sumHumi += float(data2[1])
            if int(maxT) < int(data2[0]):
                maxT = (data2[0])
            if int(minT) > int(data2[0]):
                minT = (data2[0])
            if int(maxH) < int(data2[1]):
                maxH = (data2[1])
            if int(minH) > int(data2[1]):
                minH = (data2[1])      
        averageT = sumTemp / count
        averageH = sumHumi / count
        

        print(averageT, averageH, maxT, minT, maxH, minH)
    #print(lampo)
    
receive()