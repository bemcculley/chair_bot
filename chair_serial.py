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

DEBUG_JOYSTICK_MOVEMENT = False
DEBUG_BUTTON_ACTION = False


class SparkFunAVC_routine(object):
    def __init__(self,ser):
        self.ser = ser
        
    def turn_left(self):
        self.ser.write('2128\n')
        time.sleep(1.4)
        self.ser.write('0000\n')

    def turn_right(self):
        self.ser.write('2168\n')
        time.sleep(1.4)
        self.ser.write('0000\n')

    def move_forward(self, tim = 2):
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

class ChairControl_Xbox(object):
    def __init__(self):
        self.xDefault = 148
        self.yDefault = 176 
        self.ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=0)
        if not self.ser.isOpen():
            self.ser.open()
        self.ser.write('0000\n')
        time.sleep(5)
        
        self.routine = None
        print "Starting script"

    def __del__(self):
        if self.ser.isOpen():
            self.ser.write('0000\n')
            self.ser.close()

    def convertValueX(self, OldValue):
	OldMax = 1
	OldMin = -1
	NewMax = 188
	NewMin = 118
	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

    def convertValueY(self, OldValue):
	OldMax = -1
	OldMin = 1
	NewMax = 240
	NewMin = 122
	OldRange = (OldMax - OldMin)
	NewRange = (NewMax - NewMin)
	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

    def handle_routine(self):
        if self.routine is None:
            self.routine = SparkFunAVC_routine(self.ser)
        self.routine.run()

    def joystickHandler(self):
        '''
        Gets joystick data and prints it
        '''
        pygame.init()
        j = pygame.joystick.Joystick(0) # 0 = device id
        j.init()
        print 'Initialized Joystick : %s' % j.get_name()
        self.ser.flushInput()
        try:
            while True:
                pygame.event.pump()
                event = pygame.event
#                self.ser.write('9999\n')
#                waits = self.ser.inWaiting()
#                while waits >0:
#                    print "ARDUINO OUTPUT FROM SERIAL: ", str(self.ser.readlines()).replace('\n','')
#                    print"Waiting : %d " % waits
#                time.sleep(1)
#                self.ser.flushInput()
                for thing in event.get():
                    #if thing.type == 9: # DPAD
                        # if thing.dict['value'][0] == 1:
                        # elif thing.dict['value'][0] == -1:
                        # elif thing.dict['value'][1] == 1:
                        # elif thing.dict['value'][1] == -1:

                    if thing.type == 7: # Left and Right Joystick
                        #LEFT JOYSTICK
                        if thing.dict['axis'] == 0:
                            val = float(thing.dict['value']) # small, decimal between -1 and + 1
                            if val < 0:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS LEFT"
                            else:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS RIGHT"

                            xNewVal = self.convertValueX(val)
                            try:
                                self.ser.write('2'+str(xNewVal)+'\n')
                            except Exception, e:
                                print e

                        if thing.dict['axis'] == 1:
                            val = float(thing.dict['value']) # small, decimal between -1 and + 1
                            if val < 0:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS FORWARD"
                            else:
                                if DEBUG_JOYSTICK_MOVEMENT:
                                    print "LEFT JOYSTICK AXIS BACK"

                            yNewVal = self.convertValueY(val)
                            try:
                                self.ser.write('1'+str(yNewVal)+'\n')
                            except Exception, e:
                                print e


                        # RIGHT JOYSTICK
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

                    #Buttons - Depress
                    if thing.type == 10:
                        if thing.dict['button'] == 0: # A button
                            if DEBUG_BUTTON_ACTION:
                                print 'A Button: depressed'
                            self.ser.write('5255\n')
                        elif thing.dict['button'] == 1: # B button
                            if DEBUG_BUTTON_ACTION:
                                print 'B Button: depressed'
                            self.ser.write('3255\n')
                        elif thing.dict['button'] == 2: # Y button
                            if DEBUG_BUTTON_ACTION:
                                print 'Y Button: depressed'
                            self.ser.write('4255\n')
                        elif thing.dict['button'] == 3: # X button
                            if DEBUG_BUTTON_ACTION:
                                print 'X Button: depressed'
                            self.ser.write('6000\n')
                        elif thing.dict['button'] == 6: # Select Button
                            if DEBUG_BUTTON_ACTION:
                                print 'SELECT Button: depressed'
#                        elif thing.dict['button'] == 7: # Start button
#                            if DEBUG_BUTTON_ACTION:
#                                print 'START Button: depressed'
#                            self.handle_routine()

                    #Buttons - Release
                    if thing.type == 11:
                        if thing.dict['button'] == 0: # A button
                            if DEBUG_BUTTON_ACTION:
                                print 'A Button: released'
                        elif thing.dict['button'] == 1: # B button
                            if DEBUG_BUTTON_ACTION:
                                print 'B Button: released'
                        elif thing.dict['button'] == 2: # Y button
                            if DEBUG_BUTTON_ACTION:
                                print 'Y Button: released'
                        elif thing.dict['button'] == 3: # X button
                            if DEBUG_BUTTON_ACTION:
                                print 'X Button: released'
                        elif thing.dict['button'] == 6: # Select Button
                            if DEBUG_BUTTON_ACTION:
                                print 'SELECT Button: released'
                        elif thing.dict['button'] == 7: # Start button
                            if DEBUG_BUTTON_ACTION:
                                print 'START Button: released'
#
                # time.sleep(0.1)
        except KeyboardInterrupt:
            j.quit()
            self.ser.write('0000\n')
            self.ser.close()
            sys.exit()






# THIS CLASS IS THE OLD, ORIGINAL CLASS
# IT HAS EXTRA SERVO / OTHER EXPERIMENTAL CONTROLS
# THE ABOVE, UNCOMMENTED CLASS of the same name
# IS paired down, essentials of what is currently working 
# 


# class ChairControl_Xbox(object):
#     def __init__(self):
#         self.ser = serial.Serial('/dev/ttyAMA0', baudrate=57600)
#         self.xPin = 10
#         self.yPin = 11
#         self.xDefault = 148
#         self.yDefault = 176 
#         self.xServoDefault = 90
#         self.yServoDefault = 90 
#         self.ser.open()
#         self.hatA = 90
#         self.hatB = 90
#         self.routine = None

#     def __del__(self):
#         if self.ser.isOpen():
#             self.ser.write('0000\n')
#             self.ser.close()

#     def convertValueX(self, OldValue):
# 	OldMax = 1
# 	OldMin = -1
# 	NewMax = 188
# 	NewMin = 118

# 	OldRange = (OldMax - OldMin)
# 	NewRange = (NewMax - NewMin)
# 	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
# 	return NewValue

#     def convertValueY(self, OldValue):
# 	OldMax = -1
# 	OldMin = 1
# 	NewMax = 240
# 	NewMin = 122

# 	OldRange = (OldMax - OldMin)
# 	NewRange = (NewMax - NewMin)
# 	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

# 	return NewValue

#     def convertValuePWM(self, OldValue):

# 	OldMax = 32768
# 	OldMin = -32768
# 	NewMax = 255
# 	NewMin = 0

# 	OldRange = (OldMax - OldMin)
# 	NewRange = (NewMax - NewMin)
# 	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

# 	return NewValue

#     def convertValueServo(self, OldValue):

# 	OldMax = 1
# 	OldMin = -1
# 	NewMax = 180
# 	NewMin = 0

# 	OldRange = (OldMax - OldMin)
# 	NewRange = (NewMax - NewMin)
# 	NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

# 	return str(NewValue).zfill(3)

#     def handle_routine(self):
#         if self.routine is None:
#             self.routine = SparkFunAVC_routine(self.ser)
#         self.routine.run()

#     def kill_all(self):
#         if self.ser.isOpen():
#             self.ser.write('0000\n')
#             self.ser.close()
#         sys.exit(1)

#     def joystickHandler(self):
#         '''
#         Gets joystick data and prints it
#         '''

#         a = 0
#         b = 0
#         c = 0
#         pygame.init()
#         j = pygame.joystick.Joystick(0)
#         j.init()
#         print 'Initialized Joystick : %s' % j.get_name()

#         # Keeps a history of buttons pressed so that one press does
#         # not send multiple presses to the Arduino Board
# #        button_history = [0,0,0,0,0,0,0,0,0,0,0,0]
    
#         try:
#             while True:
#                 pygame.event.pump()
#                 event = pygame.event
#                 for thing in event.get():
#                     print thing
#                     if thing.type == 9:
#                         print thing.dict['joy'], thing.dict['hat']

#                         if thing.dict['value'][0] == 1:
#                             if self.hatA <= 180:
#                                 self.hatA += 10
#                                 self.ser.write('7'+str(self.hatA)+'\n')
#                         elif thing.dict['value'][0] == -1:
#                             if self.hatA >= 0:
#                                 self.hatA = self.hatA - 10
#                                 self.ser.write('7'+str(self.hatA)+'\n')

#                         elif thing.dict['value'][1] == 1:
#                             if self.hatB <= 180:
#                                 self.hatB += 10
#                                 self.ser.write('8'+str(self.hatB)+'\n')
#                         elif thing.dict['value'][1] == -1:
#                             if self.hatB >= 0:
#                                 self.hatB = self.hatB - 10
#                                 self.ser.write('8'+str(self.hatB)+'\n')

#                     if thing.type == 7:
#                         print thing.dict['joy'], thing.dict['axis'], thing.dict['value'], 
#                         if thing.dict['axis'] == 0:
#                             xNewVal = self.convertValueX(thing.dict['value'])
#                             try:
#                                 self.ser.write('2'+str(xNewVal)+'\n')
#                                 print 'Wrote: 2', str(xNewVal)
#                             except Exception, e:
#                                 print e

#                         if thing.dict['axis'] == 1:
#                             yNewVal = self.convertValueY(thing.dict['value'])
#                             try:
#                                 self.ser.write('1'+str(yNewVal)+'\n')
#                                 print 'Wrote: 1', str(yNewVal)
#                             except Exception, e:
#                                 print e
#                         print

#                         if thing.dict['axis'] == 2:
#                             yNewVal = self.convertValueServo(thing.dict['value'])
#  #                           yNewVal = int(yNewVal)
#                             try:
#                                 self.ser.write('7'+str(yNewVal)+'\n')
#                                 print 'Wrote: 7', str(yNewVal)
#                             except Exception, e:
#                                 print e
#                         print

#                         if thing.dict['axis'] == 3:
#                             yNewVal = self.convertValueServo(thing.dict['value'])
# #                            yNewVal = int(yNewVal)
#                             try:
#                                 self.ser.write('8'+str(yNewVal)+'\n')
#                                 print 'Wrote: 8', str(yNewVal)
#                             except Exception, e:
#                                 print e
#                         print

#                     #Mappings for xbox buttons, trigger on depress
#                     # 0 = A, 1 = B, 2 = Y, 3 = X
#                     if thing.type == 10:
#                         if thing.dict['button'] == 0:
#                             self.ser.write('5255\n')
#                             print 'wrote 5255'
# #                            spi.transfer((0x05, 2,5,5))
#                         elif thing.dict['button'] == 1:
#                             self.ser.write('3255\n')
#                             print 'wrote 3255'
# #                            spi.transfer((0x03, 2,5,5))
#                         elif thing.dict['button'] == 3:
#                             self.ser.write('6000\n')
#                             print 'wrote 6000'
# #                            spi.transfer((0x06, 0,0,0))
#                         elif thing.dict['button'] == 2:
#                             self.ser.write('4255\n')
#                             print 'wrote 4255'
# #                            spi.transfer((0x04, 2,5,5))
#                         elif thing.dict['button'] == 6:
#                             #lets start the routine!
#                             pygame.event.clear()
#                             if self.routine is not None:
#                                 del self.routine
#                             self.ser.write('1240\n')
#                             time.sleep(5)
#                             self.ser.write('0000\n')
# #                            self.kill_all()
#                         elif thing.dict['button'] == 7:
#                             #lets start the routine!
#                             self.handle_routine()
#                         print 'Button: %s pressed' % thing.dict['button']
#                         print
#                     if thing.type == 11:
#                         print 'Button: %s released' % thing.dict['button']
#                         print
#                 time.sleep(0.1)
# #                print self.ser.readline()
#         except KeyboardInterrupt:
#             j.quit()
#             self.ser.write('0000\n')
#             self.ser.close()
#             sys.exit()
# #            spi.closeSPI()

ChairControl_Xbox().joystickHandler()
