from time import sleep
import random
import sys
from Adafruit_IO import MQTTClient
from plant_type import hi_temp,lo_temp,duration
from dummysensor import sendCommand, readSerial
from plant_detector import detectPlant

configFile = open("config")
config = configFile.read().split("\n")

AIO_USERNAME = config[0].strip().split("=")[-1]
AIO_KEY = config[1].strip().split("=")[-1]
PUSH_BULLET_TOGGLE = True if config[3].strip().split("=")[-1] == "true" else False

if PUSH_BULLET_TOGGLE:
    #Imports Pushbullet library if the user wishes to have notifications
    from pushbullet import PushBullet 
    DEVICE_ACCESS_TOKEN = config[4].strip().split("=")[-1]

    #Create a PushBullet Instance with the access token
    pb = PushBullet(DEVICE_ACCESS_TOKEN)

    # Get the device you want to push to
    device = pb.get_device(config[5].strip().split("=")[-1])

configFile.close()

def connected(client):
    client.subscribe("lightsensor")
    client.subscribe("moistsensor")
    client.subscribe("on-slash-off")
    client.subscribe("reservoir")
    client.subscribe("tempsensor")
    client.subscribe("comm")
    client.subscribe("plant_dectector")
    print("Server connected ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

def message(client , feed_id , payload):
    print(f"Received payload from \"{feed_id}\": {payload}")
    if (feed_id == "schedule"):
        print(f"Manual timeout override: \"{payload}\"")
        sleep(int(payload))
    if (feed_id == "on-slash-off"):
        if payload == "1":
            print("Turning the pump on...")
            sendCommand("2")
            sleep(3*duration)
            sendCommand("3")
            client.publish("on-slash-off", 0)
            return
        
def requestData(command):
    sendCommand(command)
    sleep(2)
    returnData = readSerial()
    
    if returnData == "": return "sensor error"
 
    return returnData[2]

requestData("0")

#Detect which sensor has malfunctioned
def sensorCheckup(SensorCheckList):
    for sensor, status in SensorCheckList.items(): 
        if status == 0: print(sensor, " ")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected  #callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

#Setting default sensor status
sensorStatus = {
    "Light Sensor" : 1,
    "Humidity Sensor": 1,
    "Moisture Sensor": 1,
    "Temperature Sensor": 1,
    "Reservoir Sensor" : 1
}

sensorValues = {
    "lightsensor": 0,
    "tempsensor": 0,
    "moistsensor": 0,
    "reservoir": 0,
    "humidity": 0
}

dataRequestQueue = ["8", "0", "6", "7", "1"]

malfunctionDetected = False
malfunctionNotified = False
isDaytime = True
plantDetected = False

while True:
    index = 0

    for sensorName in sensorValues.keys():
        sensorValues[sensorName] = requestData(dataRequestQueue[index])

        #Check if sensors work
        if sensorValues[sensorName] == "sensor error":
            malfunctionDetected = True
            sensorStatus[list(sensorStatus.keys())[index]] = 0
            index += 1
            sleep(2)
            continue

        sensorValues[sensorName] = float(sensorValues[sensorName])
        index += 1
        sleep(2)

    #Calculate reservoir value if it is working
    if sensorStatus["Reservoir Sensor"] != 0:
        sensorValues["reservoir"] = (36.5-sensorValues["reservoir"])/36.5

    #publish plant detection status to feed
    plantDetected = detectPlant()
    client.publish("plant_detector", plantDetected)
    sleep(1)
    
    #Arbitrary value for if it is daytime or not, could be changed
    #Putting this here since iirc day/night status is published
    if sensorStatus["Light Sensor"] != 0:
        isDaytime = sensorValues["lightsensor"] > 60

    for sensorName, value in sensorValues.items():
        client.publish(sensorName, value)
        sleep(2)
    
    #Using data from plant_type.py
    if sensorStatus["Temperature Sensor"] != 0:
        if sensorValues["tempsensor"] > hi_temp:
            print("Temperature is too high!")
        
        if sensorValues["tempsensor"] < lo_temp:
            print("Temperature is too low!")

    #Pump water when conditions are met: soil moisture < 40%, it is daytime, there is a plant and reservoir having somewhat enough water
    if sensorValues["moistsensor"] <= 40 and isDaytime and sensorValues["reservoir"] >= 15 and plantDetected:
        client.publish("on-slash-off", 1)
    #If no plant is detected, then stops the system
    else:
        client.publish("on-slash-off", 0)
      
    #Notification with PushBullet
    if PUSH_BULLET_TOGGLE:
        if not plantDetected:
            pb.push_note("No plant detected", "The system has stopped", device=device)   
                 
        if(sensorValues["reservoir"] <= 0):
            pb.push_note("Water ran out, ", "Requesting refill", device=device)
        
        #Nighttime turn off (It is recommended that smart watering systems turn off at night)
        if not isDaytime:
            pb.push_note("Nighttime mode", "Sunlight undetected, stop watering for the night", device=device)

        #Sensor malfunction notification
        if (not malfunctionNotified) and malfunctionDetected :
            pb.push_note("One or more of the sensors may not be functioning correctly", "Request checkup", device=device)
            print("Detected System Anomaly, Locating Abnormal Sensor(s)...")

            sensorCheckup(sensorStatus)
            malfunctionNotified = True

    #Pause time
    sleep(10)
