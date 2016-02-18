import socket
from enterprise_data.utilities import send_hipchat

room_url = "https://boojers.hipchat.com/v2/room/2455898/notification?auth_token=rFauRgBl8BH94Pea2KB7ZRdGcRad0YXfukEAkJe2"


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


message = "Robot is alive at %s" % get_ip()
send_hipchat.SendHipChat().go(room_url, message)


# End File: scripts/hipchat.py
