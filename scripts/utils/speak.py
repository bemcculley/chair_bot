import os


def speak(phrase):
    import os
    os.system("espeak -s80 '%s'" % phrase)

# End File: scripts/utils/speak.py
