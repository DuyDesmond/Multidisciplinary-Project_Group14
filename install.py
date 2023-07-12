print("========================")
print("Starting up...")
print("========================", end="\n\n")

from time import sleep
from platform import python_version_tuple
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

librariesStatus = [True for _ in range(5)]
librariesName = ["adafruit-io", "tensorflow", "keras", "opencv-python", "pyserial"]

TIME_DELAY = 0.3
flag = False

try:
    import Adafruit_IO
except:
    librariesStatus[0] = False
    flag = True

try:
    import tensorflow
except:
    librariesStatus[1] = False
    flag = True

try:
    import keras
except:
    librariesStatus[2] = False
    flag = True

try: 
    import cv2
except:
    librariesStatus[3] = False
    flag = True

try:
    import serial
except:
    librariesStatus[4] = False
    flag = True

sleep(TIME_DELAY) #slowing down the script

print("Checking Python version...")

sleep(TIME_DELAY)

pythonVersion = python_version_tuple()
print(f"Python {'.'.join(pythonVersion)}", end=" - ")

if pythonVersion[0] == "3" and pythonVersion[1] == "8":
    print("OK", end="\n\n")
else:
    print("Mismatched Python version, expected Python 3.8", end="\n\n")
    flag = True

sleep(TIME_DELAY)

print("Checking Python Libraries...")

sleep(TIME_DELAY)

for index in range(5):
    print(f"{librariesName[index]} - {'OK' if librariesStatus[index] == True else 'Not found. Please check if you have installed this library correctly.'}")
    sleep(TIME_DELAY)

print("")

if flag:
    print("Please resolve the issue(s) above before trying again. Exiting...")
    sys.exit()

print("========================")
print("Configuring system...")
print("========================", end="\n\n")

adaUsername = input("Please enter your Adafruit IO username: ")
adaKey = input("Please enter your Adafruit IO key: ")
portName = input("Please enter the name of the port that your hardware is connected to: ")

try:
    settingFile = open("config", "w")
except:
    print("Cannot write settings!")
    sys.exit()

settingFile.write(f"USERNAME={adaUsername}\n")
settingFile.write(f"KEY={adaKey}\n")
settingFile.write(f"PORT={portName}\n")
settingFile.close()

sleep(TIME_DELAY)
print("")
print("Setup complete! Exiting...")