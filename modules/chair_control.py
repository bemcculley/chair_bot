import time
import serial


class ChairControl(object):
    def __init__(self):
        self.xDefault = 148
        self.yDefault = 176
        self.ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=0)
        if not self.ser.isOpen():
            self.ser.open()
        self.ser.write('0000\n')
        time.sleep(5)
        self.routine = None
        print "Starting script"

    def __del__(self):
        if self.ser.isOpen():
            self.ser.write('0000\n')
            self.ser.close()

    def convertValueX(self, OldValue):
        OldMax = 1
        OldMin = -1
        NewMax = 188
        NewMin = 118
        OldRange = (OldMax - OldMin)
        NewRange = (NewMax - NewMin)
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        return NewValue

    def convertValueY(self, OldValue):
        OldMax = -1
        OldMin = 1
        NewMax = 240
        NewMin = 122
        OldRange = (OldMax - OldMin)
        NewRange = (NewMax - NewMin)
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        return NewValue
