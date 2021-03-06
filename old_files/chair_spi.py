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

#import spi


class ChairControl_Xbox(object):
    def __init__(self):
        self.xDefault = 148
        self.yDefault = 176 
        
        self.xPin = 10
        self.yPin = 11
        sefl.ser = serial.Serial('/dev/USB0')
#        spi.openSPI(speed=1000000, mode=0)


    def convertValueX(self, OldValue):
	OldMax = 1
	OldMin = -1
	NewMax = 178
	NewMin = 118

	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

    def convertValueY(self, OldValue):
	OldMax = -1
	OldMin = 1
	NewMax = 208
	NewMin = 138

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
        button_history = [0,0,0,0,0,0,0,0,0,0,0,0]
    
        try:
            while True:
                pygame.event.pump()
                event = pygame.event
                for thing in event.get():
                    if thing.type == 7:
#                        print thing.dict['joy'], thing.dict['axis'], thing.dict['value'], 
                        print thing.dict['value']
                        if False:
                            pass
#                            spi.transfer((0x00, 0,0,0))
#                            spi.transfer((0x01, 1,7,6))
                        else:
                            if thing.dict['axis'] == 0:

                                xNewVal = self.convertValueX(thing.dict['value'])
                                try:
                                    a = int(str(xNewVal)[0])
                                    b = int(str(xNewVal)[1])
                                    c = int(str(xNewVal)[2])
                                    print "X: ",a,b,c
                                    print spi.transfer((0x02, a,b,c))
                            #                                time.sleep(0.01)
                                except Exception, e:
                                    print e

                            if thing.dict['axis'] == 1:
                                yNewVal = self.convertValueY(thing.dict['value'])
                                try:
                                    a = int(str(yNewVal)[0])
                                    b = int(str(yNewVal)[1])
                                    c = int(str(yNewVal)[2])
                                    print "Y: ",a,b,c
                                    print spi.transfer((0x01, a,b,c))
                            #                                time.sleep(0.01)
                                except Exception, e:
                                    print e
                        print
                    
                    #Mappings for xbox buttons, trigger on depress
                    # 0 = A, 1 = B, 2 = Y, 3 = X
                    if thing.type == 10:
                        if thing.dict['button'] == 0:
                            spi.transfer((0x05, 2,5,5))
                        if thing.dict['button'] == 1:
                            spi.transfer((0x03, 2,5,5))
                        if thing.dict['button'] == 3:
                            spi.transfer((0x06, 0,0,0))
                        if thing.dict['button'] == 2:
                            spi.transfer((0x04, 2,5,5))

                        print 'Button: %s pressed' % thing.dict['button']
                        print
                    if thing.type == 11:
                        print 'Button: %s released' % thing.dict['button']
                        print

        except KeyboardInterrupt:
            j.quit()
            spi.closeSPI()

ChairControl_Xbox().joystickHandler()
