'''
basic_control.py
@author: Garrett Owen
@date: January 26, 2012

Based off code from 

http://iamtherockstar.com/archive/making-hid-devices-easier-using-pygame-joysticks/

Further modified for chair_bot control
'''

#import serial
import pygame
import time


'''
Gets joystick data and prints it
'''
pygame.init()
#joystick.init()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized Joystick : %s' % j.get_name()

# Keeps a history of buttons pressed so that one press does
# not send multiple presses to the Arduino Board
button_history = [0,0,0,0,0,0,0,0,0,0,0,0]

try:
    while True:
#        pygame.event.pump()

        # Used to read input from the two joysticks       
        for i in range(0, j.get_numaxes()):
            if j.get_axis(i) != 0.00:
                print 'Axis %i reads %.2f' % (i, j.get_axis(i))
        
        time.sleep(1)

#        print j.get_numbuttons()
        for i in range(0, j.get_numbuttons()):
#            print i
            if j.get_button(i) != 0:
                if not button_history[i]:
                    print 'Button %i reads %i' % (i, j.get_button(i))
                    button_history[i] = 1
                    print j.get_button(i)
                    writeNumber(int(i))
                    time.sleep(1)

                    #ser.write(str(i))
            else:
                try:
                    button_history[i] = 0
                except Exception, e:
                    print e

except KeyboardInterrupt:
    j.quit()
