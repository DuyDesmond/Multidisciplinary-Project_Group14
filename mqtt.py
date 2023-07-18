from time import sleep
import random
import sys
from Adafruit_IO import MQTTClient
import plant_type
import sensor

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
            sensor.sendCommand("2")
            sleep(5)
            sensor.sendCommand("3")
            client.publish("on-slash-off", 0)
            return
        
def requestData(command):
    sensor.sendCommand(command)
    sleep(2)
    returnData = sensor.readSerial()
    
    if returnData == "": return "sensor error"
 
    return returnData[2]
requestData("0")

#Setting default sensor status
sensor_status = {
    "Light Sensor" : 1,
    "Moist Sensor": 1,
    "Temperature Sensor": 1,
    "Reservoir Sensor" : 1
}

#Detect which sensor has malfunctioned
def Sensor_Checkup(SensorCheckList, notifyStatus):
    for sensor, status in SensorCheckList.items(): 
        if status == 0: print(sensor, " ")
        notifyStatus = True 

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected  #callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

reservoir = 100
notBrokenNumber = 0
malfunctionNotified = False
is_daytime = True
is_rainy = False

while True:  
    temp = requestData("0")
    sleep(2)
    hum = requestData("1")
    sleep(2)
    reservoir = requestData("7")
    sleep(2)
    moisture = requestData("6")
    sleep(2)
    light = requestData("8")  
    sleep(2)

    #Check if sensors work
    if light == "sensor error": sensor_status["Light Sensor"] = 0
    if temp == "sensor error": sensor_status["Temperature Sensor"] = 0
    if moisture == "sensor error": sensor_status["Moist Sensor"] = 0
    if reservoir == "sensor error": sensor_status["Reservoir Sensor"] = 0

    #Check number of broken sensors
    for check in sensor_status.values(): 
        if check == 1: notBrokenNumber += 1
    if notBrokenNumber == 4: malfunctionNotified = False

    client.publish("lightsensor", light)
    sleep(2)
    client.publish("tempsensor", temp)
    sleep(2)
    client.publish("moistsensor", moisture)
    sleep(2)
    client.publish("reservoir", (36.5-float(reservoir))/36.5 if reservoir != "sensor error" else reservoir)
    sleep(2)
    client.publish("humidity", hum)
    sleep(2)
    
    if float(moisture) <= 60:
        client.publish("on-slash-off", 1)
      
    #Notification with PushBullet
    if PUSH_BULLET_TOGGLE:
        if(reservoir <= 0):
            pb.push_note("Water ran out, ", "Requesting refill", device=device)
    
        #Nighttime turn off (It is recommended that smart watering systems turn off at night)
        if not is_daytime:
            pb.push_note("Nighttime mode", "Sunlight undetected, stop watering for the night", device=device)

        #Sensor malfunction notification
        if (not malfunctionNotified) and (notBrokenNumber < 4) :
            pb.push_note("One or more of the sensors may not be functioning correctly", "Request checkup", device=device)
            print("Detected System Anomaly, Locating Abnormal Sensor(s)...")
            Sensor_Checkup(sensor_status, malfunctionNotified)

    #Pause time
    sleep(10)
