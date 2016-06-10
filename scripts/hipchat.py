import socket
from enterprise_data.utilities import send_hipchat
from utils import network, speak

room_url = "https://boojers.hipchat.com/v2/room/2455898/notification" \
    "?auth_token=rFauRgBl8BH94Pea2KB7ZRdGcRad0YXfukEAkJe2"


def on_boot_up():
    message = "SocietyBot is alive at %s" % network.get_ip()
    print message
    speak.speak(message)
    # send_hipchat.SendHipChat().go(room_url, message)

on_boot_up()

# End File: scripts/hipchat.py
