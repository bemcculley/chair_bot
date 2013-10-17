'''
@author: Brian McCulley

'''

#import serial
import pygame
import time
import sys
import spi


class HardwareControl(object):
    def __init__(self, devMaxX, devMinX, devMaxY, devMinY):
        self.xDefault = 148
        self.yDefault = 176 
        
        self.xMin = 128
        self.xMax = 168
        self.yMin = 146
        self.yMax = 206

        self.devMaxX = devMaxX
        self.devMinX = devMinX
        self.devMaxY = devMinY
        self.devMinY = devMaxY


        spi.openSPI(speed=1000000, mode=0)


    def __convertValueX(self, OldValue):
        print "convert X"
	OldRange = (self.devMaxX - self.devMinX)
	NewRange = (self.xMax - self.xMin)
	NewValue = (((OldValue - self.devMinX) * NewRange) / OldRange) + self.xMin
	return int(NewValue)

    def __convertValueY(self, OldValue):
        print "convert Y"
	OldRange = (self.devMaxY - self.devMinY)
	NewRange = (self.yMax - self.yMin)
	NewValue = (((OldValue - self.devMinY) * NewRange) / OldRange) + self.yMin
	return int(NewValue)


    def __getBits(self, bitstring):
        bitstring = str(bitstring).zfill(3)
        print 'bitstring', bitstring
        try:
            a = int(bitstring[0])
            b = int(bitstring[1])
            c = int(bitstring[2])
        except Exception, e:
            print "Need numeric bits"
            print 'bitstring', bitstring
        return (a, b, c)
        

    def drive(self, dev, value):
#        if self.devMaxX or self.devMinX or self.devMaxY or self.devMinY is None:
#            raise Exception("Must override X min and max values")
#        print HardwareControl.__convertValueX(value)
#        print HardwareControl.__convertValueY(value)
        try:
            try:
                dev = int(dev)
                value = int(value)
            except ValueError,e:
                print "need numeric device ID or value"

            newVal = value
            if dev == 1:
                newVal = self.__convertValueY(value)
            if dev == 2:
                newVal = self.__convertValueX(value)

        except Exception, e:
            print dev, value, newVal
#            spi.transfer((0x00, 0, 0, 0))
            print 'Shutting Down', e
            spi.closeSPI()
            sys.exit(1)

        try:
            a,b,c = self.__getBits(newVal)
            if dev == 1:
                dev = 0x01
            if dev == 2:
                dev = 0x02
            send = (dev,a,b,c)
            print 'sending: ', send
            print spi.transfer(send)


        except Exception, e:
            print "Couldn't transfer over SPI",e
            spi.closeSPI()
            print dev,  newVal, self.__getBits(newVal)
            sys.exit(1)



