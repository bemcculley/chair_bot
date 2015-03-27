import serial
import sys
import time

ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600)

ser.open()
ser.isOpen()

while True:

    inp = raw_input("input x or 0-180, 0-180:\n")

    if inp == 'x':
        sys.exit(0)

    ser.write(inp + '\n')

    time.sleep(1)
    
    thing = ser.readline()
    print len(thing)
    print type(thing)
    print thing
#    ''.join(ser.read())
