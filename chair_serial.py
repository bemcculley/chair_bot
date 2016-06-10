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
from modules.chair_control import ChairControl

DEBUG_JOYSTICK_MOVEMENT = False
DEBUG_BUTTON_ACTION = False


class SparkFunAVC_routine(object):
    def __init__(self, ser):
        self.ser = ser

    def turn_left(self):
        self.ser.write('2128\n')
        time.sleep(1.4)
        self.ser.write('0000\n')

    def turn_right(self):
        self.ser.write('2168\n')
        time.sleep(1.4)
        self.ser.write('0000\n')

    def move_forward(self, time=2):
        self.ser.write('1240\n')
        time.sleep(tim)
        self.ser.write('0000\n')

    def circle(self):
        self.ser.write('1196\n')
        time.sleep(0.5)
        self.ser.write('2168\n')
        time.sleep(6.4)
        self.ser.write('0000\n')

    def run(self):
        if not self.ser.isOpen():
            self.ser.open()
        self.move_forward(5)
        self.turn_left()
        self.turn_left()
        self.move_forward(5)
        self.turn_left()
        self.turn_left()
        self.ser.write('0000\n')
        print "done!"

    def __del__(self):
        if self.ser.isOpen():
            self.ser.write('0000\n')
            self.ser.close()


class Xbox_Control(object):

    def joystickHandler(self):
        '''
        Gets joystick data and prints it
        '''
        pygame.init()
        j = pygame.joystick.Joystick(0)  # 0 = device id
        j.init()
        print 'Initialized Joystick : %s' % j.get_name()
        chair = ChairControl()
        chair.ser.flushInput()
        try:
            while True:
                # pygame.event.pump()
                event = pygame.event
                print event
                # self.ser.write('9999\n')
                # waits = self.ser.inWaiting()
                # while waits >0:
                #     print "ARDUINO OUTPUT FROM SERIAL: ", str(self.ser.readlines()).replace('\n','')
                #    print"Waiting : %d " % waits
                # time.sleep(1)
                # self.ser.flushInput()
                for thing in event.get():
                    #  if thing.type == 9: # DPAD
                        # if thing.dict['value'][0] == 1:
                        # elif thing.dict['value'][0] == -1:
                        # elif thing.dict['value'][1] == 1:
                        # elif thing.dict['value'][1] == -1:

                    if thing.type == 7:  # Left and Right Joystick
                        #  LEFT JOYSTICK
                        if thing.dict['axis'] == 0:
                            val = float(thing.dict['value'])  # small, decimal between -1 and + 1
                            if val < 0:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS LEFT"
                            else:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS RIGHT"

                            xNewVal = chair.convertValueX(val)
                            try:
                                chair.ser.write('2'+str(xNewVal)+'\n')
                            except Exception, e:
                                print e

                        if thing.dict['axis'] == 1:
                            val = float(thing.dict['value'])  # small, decimal between -1 and + 1
                            if val < 0:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS FORWARD"
                            else:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS BACK"

                            yNewVal = chair.convertValueY(val)
                            try:
                                chair.ser.write('1'+str(yNewVal)+'\n')
                            except Exception, e:
                                print e

                        #  RIGHT JOYSTICK
                        if thing.dict['axis'] == 2:
                            val = float(thing.dict['value'])
                            if val < 0:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "RIGHT JOYSTICK AXIS LEFT"
                            else:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "RIGHT JOYSTICK AXIS RIGHT"

                        if thing.dict['axis'] == 3:
                            val = float(thing.dict['value'])
                            if val < 0:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "RIGHT JOYSTICK AXIS FORWARD"
                            else:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "RIGHT JOYSTICK AXIS BACK"

                    #  Buttons - Depress
                    if thing.type == 10:
                        if thing.dict['button'] == 0:  # A button
                            if DEBUG_BUTTON_ACTION:
                                print 'A Button: depressed'
                            chair.ser.write('5255\n')
                        elif thing.dict['button'] == 1:  # B button
                            if DEBUG_BUTTON_ACTION:
                                print 'B Button: depressed'
                            chair.ser.write('3255\n')
                        elif thing.dict['button'] == 2:  # Y button
                            if DEBUG_BUTTON_ACTION:
                                print 'Y Button: depressed'
                            chair.ser.write('4255\n')
                        elif thing.dict['button'] == 3:  # X button
                            if DEBUG_BUTTON_ACTION:
                                print 'X Button: depressed'
                            chair.ser.write('6000\n')
                        elif thing.dict['button'] == 6:  # Select Button
                            if DEBUG_BUTTON_ACTION:
                                print 'SELECT Button: depressed'
                        # elif thing.dict['button'] == 7: # Start button
                        #      if DEBUG_BUTTON_ACTION:
                        #          print 'START Button: depressed'
                        #      self.handle_routine()

                    #  Buttons - Release
                    if thing.type == 11:
                        if thing.dict['button'] == 0:  # A button
                            if DEBUG_BUTTON_ACTION:
                                print 'A Button: released'
                        elif thing.dict['button'] == 1:  # B button
                            if DEBUG_BUTTON_ACTION:
                                print 'B Button: released'
                        elif thing.dict['button'] == 2:  # Y button
                            if DEBUG_BUTTON_ACTION:
                                print 'Y Button: released'
                        elif thing.dict['button'] == 3:  # X button
                            if DEBUG_BUTTON_ACTION:
                                print 'X Button: released'
                        elif thing.dict['button'] == 6:  # Select Button
                            if DEBUG_BUTTON_ACTION:
                                print 'SELECT Button: released'
                        elif thing.dict['button'] == 7:  # Start button
                            if DEBUG_BUTTON_ACTION:
                                print 'START Button: released'
                # time.sleep(0.1)
        except KeyboardInterrupt:
            j.quit()
            chair.ser.write('0000\n')
            chair.ser.close()
            sys.exit()

    def handle_routine(self):
        if self.routine is None:
            self.routine = SparkFunAVC_routine(self.ser)
        self.routine.run()

Xbox_Control().joystickHandler()
