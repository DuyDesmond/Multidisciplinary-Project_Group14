import time
import serial.tools.list_ports
import sys

configFile = open("config")
config = configFile.read().strip().split("\n")
selectedPort = config[2].strip().split("=")[-1]
configFile.close()


try:
    port = serial.Serial(port=selectedPort, baudrate=115200)
except:
    print("Cannot open port.")
    sys.exit()

def sendCommand(command):
    port.write(command.encode())

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    return splitData

def readSerial():
    bytesToRead = port.inWaiting()
    message = ""
    returnData = ""
    if bytesToRead > 0:
        message = message + port.read(bytesToRead).decode("UTF-8")

        while "#" in message and "!" in message:
            start = message.find("!")
            end = message.find("#")
            returnData = processData(message[start:end+1])

            if (end == len(message)):
                message = ""
            else: 
                message = message[end+1:]

    return returnData
