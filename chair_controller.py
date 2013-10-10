'''
@author: Brian McCulley

'''

#import serial
import pygame
import time

import spi


class ChairControl_Xbox(object):
    def __init__(self):
        self.xDefault = 148
        self.yDefault = 176 
        
        self.xPin = 10
        self.yPin = 11

        spi.openSPI(speed=1000000, mode=0)


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
	NewMax = 216
	NewMin = 136

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

                        #Joystick 1 (left)
                        if thing.dict['axis'] == 0: 
                            #deadzoning
                            if -0.25 < float(thing.dict['value']) < 0.25:
                                spi.transfer((0x00, 0,0,0))
                            else:
                                xNewVal = self.convertValueX(thing.dict['value'])
                                try:
                                    a = int(str(xNewVal)[0])
                                    b = int(str(xNewVal)[1])
                                    c = int(str(xNewVal)[2])
                                    print "X: ",a,b,c
                                    spi.transfer((0x02, a,b,c))
                                except Exception, e:
                                    print e

                            if thing.dict['axis'] == 1:
                                #deadzoning
                                if -0.3 < float(thing.dict['value']) < 0.3:
                                    spi.transfer((0x00, 0,0,0))
                                else:
                                    yNewVal = self.convertValueY(thing.dict['value'])
                                    try:
                                        a = int(str(yNewVal)[0])
                                        b = int(str(yNewVal)[1])
                                        c = int(str(yNewVal)[2])
                                        print "Y: ",a,b,c
                                        spi.transfer((0x01, a,b,c))
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
