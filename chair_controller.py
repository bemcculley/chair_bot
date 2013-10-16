'''
@author: Brian McCulley

'''

#import serial
import pygame
import time

import spi


class HardwareControl(object):
    def __init__(self):
        self.xDefault = 148
        self.yDefault = 176 
        
        self.xMin = 128
        self.xMax = 168
        self.yMin = 136
        self.yMax = 216

        self.devMaxX = None
        self.devMinX = None
        self.devMaxY = None
        self.devMinY = None

        spi.openSPI(speed=1000000, mode=0)


    def __convertValueX(self, OldValue):
	OldRange = (self.devMaxX - self.devMinX)
	NewRange = (self.xMax - self.xMin)
	NewValue = (((OldValue - self.devMinX) * NewRange) / OldRange) + self.xMin
	return NewValue

    def __convertValueY(self, OldValue):
	OldRange = (self.devMaxY - self.devMinY)
	NewRange = (self.yMax - self.yMin)
	NewValue = (((OldValue - self.devMinY) * NewRange) / OldRange) + self.yMin
	return NewValue


    def __getBits(self, bitstring):
        try:
            a = int(str(bitstring)[0])
            b = int(str(bitstring)[1])
            c = int(str(bitstring)[2])
        except Exception, e:
            print "Need numeric bits"
        return a, b, c
        


    def drive(self, dev, value):
        if self.devMaxX or self.devMinX or self.devMaxY or self.devMinY is None:
            raise Exception("Must override X min and max values")
        try:
            try:
                dev = int(dev)
            except ValueError,e:
                print "need numeric device ID"

            if dev == 1:
                newVal = self.__convertValueX(value)
            if dev == 2:
                newVal = self.__convertValueY(value)
            else:
                newVal = value
            spi.transfer((dev, self.__getBits(newVal)))

        except Exception, e:
            spi.transfer((0x00, 0, 0, 0))
            print 'Shutting Down'
            j.quit()
            spi.closeSPI()            

