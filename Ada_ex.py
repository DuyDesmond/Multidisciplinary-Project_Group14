print("MQTT with Adafruit IO, initiating ...")

#libraries
from Adafruit_IO import Client
from pushbullet import PushBullet
import time
import random

#This is where you put Adafruit information
AIO_FEED_ID = ""
AIO_USERNAME = ""
AIO_KEY = ""

#This is where you put you PushBullet device access token
DEVICE_ACCESS_TOKEN = ""

# Create an instance of the Adafruit IO Client class
# using your Adafruit IO username and key
client = Client(AIO_USERNAME, AIO_KEY)

#Create a PushBullet Instance with the access token
pb = PushBullet(DEVICE_ACCESS_TOKEN)

# Get the list of devices associated with the PushBullet account
devices = pb.devices

# Get the device you want to push to
device = devices[0] # Change the index to the device you want

# #PushBullet API (Don't look, this is bullshit)
# def send_notification(title, message, device_id):
#     url = "https://api.pushbullet.com/v2/users/me"
#     data = {
#         "type": "note",
#         "title": title,
#         "message": message,
#         "device_id": device_id
#     }
#     response = requests.post(url, data=data)

#Push up and print out randomized data every five seconds
def execute_every_fiveseconds():

  while True:

    #Create randomized values (This code is to simulate when the data of the sensors come in)
    value1 = random.randint(756, 2000)
    value2 = random.randint(40, 100)
    value3 = random.randint(1, 7)

    #publish randomized values (Sensor readings gets published to Adaafruit)
    client.send("sensor1", value1)
    client.send("sensor2", value2)
    client.send("sensor3", value3)

    #Receive data (Adafruit data is taken)
    sensor1 = client.receive("sensor1").value
    sensor2 = client.receive("sensor2").value
    sensor3 = client.receive("sensor3").value

    #Convert data to integer
    readable_val1 = int(sensor1)
    readable_val2 = int(sensor2)
    readable_val3 = int(sensor3)

    #Print out data
    print("Sensor 1 gives: ", readable_val1)
    print("Sensor 2 gives: ", readable_val2)
    print("Sensor 3 gives: ", readable_val3)

    #Notification with PushBullet (Extra feature 1)
    if(readable_val1 >= 500):
      pb.push_note("Test Notification", "Water ran out, request refill", device=device)
    time.sleep(5)

execute_every_fiveseconds()




