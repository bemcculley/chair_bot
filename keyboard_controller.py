'''
@author: Brian McCulley

'''

from chair_controller import HardwareControl
import pygame



class KeyboardHandler(object):
    def __init__(self):
        self.control = HardwareControl(devMaxX = 1, devMinX = -1, devMaxY = 1, devMinY = -1)
        pygame.init()
        # is the following needed?
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print 'Initialized Joystick : %s' % self.j.get_name()



    def keyboard(self):
        try:
            while True:
                pygame.event.pump()
                event = pygame.event
                for thing in event.get():
                    #Key down
                    if thing.type == 2:
                        try:
                            print thing
                        except Exception, e:
                            print e
                        print

        except KeyboardInterrupt:
            self.j.quit()


KeyboardHandler().keyboard()
