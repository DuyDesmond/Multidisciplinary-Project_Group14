from random import randint

def sendCommand(command):
  print(command)

def readSerial():
  return [0, 0, randint(0, 100)]