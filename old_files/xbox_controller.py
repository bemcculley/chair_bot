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

        self.green = 255
        self.red = 255
        self.blue = 255




    def joystickHandler(self):
        try:
            while True:
                pygame.event.pump()
                event = pygame.event
                for thing in event.get():
                    print thing.type
                    print thing
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
                    if thing.type == 9 or thing.type == 10:
                        self.buttonHandler(thing)

        except KeyboardInterrupt:
            self.j.quit()

    def buttonHandler(self,thing):
        print self.green
        #Mappings for xbox buttons, trigger on depress
        # 0 = A, 1 = B, 2 = Y, 3 = X

        if thing.type == 10:
            if thing.dict['button'] == 0:
                self.control.drive(0x05, self.green)

            if thing.dict['button'] == 1:
                self.control.drive(0x03, self.red)

            if thing.dict['button'] == 3:
                self.control.drive(0x06, 000)

            if thing.dict['button'] == 2:
                self.control.drive(0x04, self.blue)

            print 'Button: %s pressed' % thing.dict['button']
            print

        if thing.type == 9:
            if self.j.get_button(0) == 1:
                #green
                self.green = self.green + (thing.dict['value'][1] * 25)
                if self.green > 255:
                    self.green = 255
                if self.green < 0:
                    self.green = 0
                self.control.drive(0x05, self.green)
            if self.j.get_button(1) == 1:
                #red
                self.red = self.red + (thing.dict['value'][1] * 25)
                if self.red > 255:
                    self.red = 255
                if self.red < 0:
                    self.red = 0
                self.control.drive(0x03, self.red)
            if self.j.get_button(2) == 1:
                #blue
                self.blue = self.blue + (thing.dict['value'][1] * 25)
                if self.blue > 255:
                    self.blue = 255
                if self.blue < 0:
                    self.blue = 0
                self.control.drive(0x04, self.blue)


        if thing.type == 11:
            print 'Button: %s released' % thing.dict['button']
        print


if __name__ == '__main__':
    XboxHandler().joystickHandler()
