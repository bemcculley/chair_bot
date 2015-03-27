'''
basic_control.py
@author: Garrett Owen
@date: January 26, 2012

Based off code from 

http://iamtherockstar.com/archive/making-hid-devices-easier-using-pygame-joysticks/

adapted by Brian McCulley

'''

import serial
import pygame
import time
import sys
#import spi


class ChairControl_Xbox(object):
    def __init__(self):
        self.xDefault = 148
        self.yDefault = 176 

        self.xServoDefault = 90
        self.yServoDefault = 90 
        
        self.xPin = 10
        self.yPin = 11
        self.ser = serial.Serial('/dev/ttyAMA0', baudrate=57600)
        self.ser.open()
        self.ser.isOpen()
#        spi.openSPI(speed=1000000, mode=0)


    def convertValueX(self, OldValue):
	OldMax = 1
	OldMin = -1
	NewMax = 168
	NewMin = 128

	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

    def convertValueY(self, OldValue):
	OldMax = -1
	OldMin = 1
	NewMax = 188
	NewMin = 148

	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

	return NewValue

    def convertValuePWM(self, OldValue):

	OldMax = 32768
	OldMin = -32768
	NewMax = 255
	NewMin = 0

	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

	return NewValue

    def convertValueServo(self, OldValue):

	OldMax = 32768
	OldMin = -32768
	NewMax = 180
	NewMin = 0

	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

	return NewValue







    def joystickHandler(self):
        '''
        Gets joystick data and prints it
        '''

        a = 0
        b = 0
        c = 0
        pygame.init()
        j = pygame.joystick.Joystick(0)
        j.init()
        print 'Initialized Joystick : %s' % j.get_name()

        # Keeps a history of buttons pressed so that one press does
        # not send multiple presses to the Arduino Board
#        button_history = [0,0,0,0,0,0,0,0,0,0,0,0]
    
        try:
            while True:
                pygame.event.pump()
                event = pygame.event
                for thing in event.get():
                    print thing
                    if thing.type == 7:
                        print thing.dict['joy'], thing.dict['axis'], thing.dict['value'], 
#                        print thing.dict['value']
                        if thing.dict['axis'] == 0:
                            xNewVal = self.convertValueX(thing.dict['value'])
                            xNewVal = int(xNewVal)
#                            if xNewVal < self.xDefault - 5:
#                                xNewVal = self.xDefault
#                            if xNewVal > self.xDefault + 5:
#                                xNewVal = self.xDefault
                            try:
                                self.ser.write('2'+str(xNewVal))
                                print 'Wrote: 2', str(xNewVal)
                            except Exception, e:
                                print e

                        if thing.dict['axis'] == 1:
                            yNewVal = self.convertValueY(thing.dict['value'])
                            yNewVal = int(yNewVal)
#                            if yNewVal < self.yDefault - 5:
#                                yNewVal = self.yDefault
#                            if yNewVal > self.yDefault + 5:
#                                yNewVal = self.yDefault
                            try:
                                self.ser.write('1'+str(yNewVal))
                                print 'Wrote: 1', str(yNewVal)
                            except Exception, e:
                                print e
                        print
                    
                    #Mappings for xbox buttons, trigger on depress
                    # 0 = A, 1 = B, 2 = Y, 3 = X
                    if thing.type == 10:
                        if thing.dict['button'] == 0:
                            self.ser.write('5255')
#                            spi.transfer((0x05, 2,5,5))
                        if thing.dict['button'] == 1:
                            self.ser.write('3255')
#                            spi.transfer((0x03, 2,5,5))
                        if thing.dict['button'] == 3:
                            self.ser.write('6000')
#                            spi.transfer((0x06, 0,0,0))
                        if thing.dict['button'] == 2:
                            self.ser.write('4255')
#                            spi.transfer((0x04, 2,5,5))

                        print 'Button: %s pressed' % thing.dict['button']
                        print
                    if thing.type == 11:
                        print 'Button: %s released' % thing.dict['button']
                        print
                time.sleep(0.1)
#                print self.ser.readline()
        except KeyboardInterrupt:
            j.quit()
            self.ser.close()
            sys.exit()
#            spi.closeSPI()

ChairControl_Xbox().joystickHandler()
