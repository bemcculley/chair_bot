'''
@author: Brian McCulley

'''

import pygame
import time
from chair_controller import HardwareControl

class XboxHandler(HardwareControl):
    def __init__(self):
        self.devMaxX = 1
        self.devMinX = -1
        self.devMaxY = -1
        self.devMinY = 1

        pygame.init()
        # is the following needed?
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print 'Initialized Joystick : %s' % self.j.get_name()

    def joystickHandler(self):
        try:
            while True:
                pygame.event.pump()
                event = pygame.event
                for thing in event.get():
                    if thing.type == 7:
                        try:
                            #Joystick 1 (left)
                            if thing.dict['axis'] == 0: 
                                #Y Axis?
                                self.drive(thing.dict['axis'], thing.dict['value'])
                        
                            if thing.dict['axis'] == 1:
                                #X Axis?
                                self.drive(thing.dict['axis'], thing.dict['value'])
                        except Exception, e:
                            print e
                        print
        except KeyboardInterrupt:
            j.quit()

    def buttonHandler(self):
        #Mappings for xbox buttons, trigger on depress
        # 0 = A, 1 = B, 2 = Y, 3 = X
        if thing.type == 10:
            if thing.dict['button'] == 0:
                self.drive(0x05, 2,5,5)
            if thing.dict['button'] == 1:
                self.drive(0x03, 2,5,5)
            if thing.dict['button'] == 3:
                self.drive(0x06, 0,0,0)
            if thing.dict['button'] == 2:
                self.drive(0x04, 2,5,5)

            print 'Button: %s pressed' % thing.dict['button']
            print
            if thing.type == 11:
                print 'Button: %s released' % thing.dict['button']
            print

