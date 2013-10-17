'''
@author: Brian McCulley

'''

import pygame
import time
from chair_controller import HardwareControl

class XboxHandler(object):
    def __init__(self):
        self.control = HardwareControl(devMaxX = 1, devMinX = -1, devMaxY = 1, devMinY = -1)
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
                                self.control.drive(2, thing.dict['value'])
                        
                            if thing.dict['axis'] == 1:
                                #X Axis?
                                
                                self.control.drive(1, thing.dict['value'])
                        except Exception, e:
                            print e
                        print
                    if thing.type == 10:
                        self.buttonHandler(thing)

        except KeyboardInterrupt:
            self.j.quit()

    def buttonHandler(self,thing):
        #Mappings for xbox buttons, trigger on depress
        # 0 = A, 1 = B, 2 = Y, 3 = X
        if thing.dict['button'] == 0:
            self.control.drive(0x05, 255)
        if thing.dict['button'] == 1:
            self.control.drive(0x03, 255)
        if thing.dict['button'] == 3:
            self.control.drive(0x06, 000)
        if thing.dict['button'] == 2:
            self.control.drive(0x04, 255)

        print 'Button: %s pressed' % thing.dict['button']
        print
        if thing.type == 11:
            print 'Button: %s released' % thing.dict['button']
        print


if __name__ == '__main__':
    XboxHandler().joystickHandler()
