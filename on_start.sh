#!/bin/sh
sleep 10
echo $(lsusb) > /home/pi/boot.log
#xboxdrv --silent &
#sleep 2
python /home/pi/chair_bot/chair_serial.py &
