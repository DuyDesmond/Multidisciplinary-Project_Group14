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

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected  #callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

#Detect which sensor has malfunctioned
def Sensor_Checkup(sun_sensor_check, rain_sensor_check, moist_sensor_check, temp_sensor_check):
    sensor_list = []
    if sun_sensor_check == False:
        sensor_list.append("Sun sensor")
    if rain_sensor_check == False:
        sensor_list.append("Rain sensor")
    if moist_sensor_check == False:
        sensor_list.append("Moist sensor")
    if temp_sensor_check == False:
        sensor_list.append("Temp sensor")
    return sensor_list

reservoir = 100
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
    #sun sensor
    if light == "sensor error": 
        Sun_sensor_check = True
    else: Sun_sensor_check = False

    #temperature sensor
    if temp == "sensor error": 
        Temp_sensor_check = True
    else: Temp_sensor_check = False
    #moisture sensor
    if moisture == "sensor error": 
        Moist_sensor_check = True
    else: Moist_sensor_check = False

    if reservoir == "sensor error": 
        Reservoir_sensor_check = True
    else: Temp_sensor_check = False


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
        if not malfunctionNotified: 
            if (Sun_sensor_check == False or Moist_sensor_check == False or Temp_sensor_check == False):
                pb.push_note("One or more of the sensors may not be functioning correctly", "Request checkup", device=device)
                print("Detected System Anomaly, Locating Abnormal Sensor(s)...")
                AbnormalSensorList = Sensor_Checkup(Sun_sensor_check, Moist_sensor_check, Temp_sensor_check, Reservoir_sensor_check)
                for index in AbnormalSensorList: print("Abnormal sensor(s) include: " + ', '.join(AbnormalSensorList))
                malfunctionNotified = True

    #Pause for 12 seconds
    sleep(10)
