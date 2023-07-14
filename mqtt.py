import time
import random
import sys
from Adafruit_IO import MQTTClient
from pushbullet import PushBullet

configFile = open("config")
config = configFile.read().split("\n")

AIO_USERNAME = config[0].strip().split("=")[-1]
AIO_KEY = config[1].strip().split("=")[-1]

configFile.close()

#This is where you put you PushBullet device access token
DEVICE_ACCESS_TOKEN = ""

#Create a PushBullet Instance with the access token
pb = PushBullet(DEVICE_ACCESS_TOKEN)

# Get the list of devices associated with the PushBullet account
devices = pb.devices

# Get the device you want to push to
device = devices[0] # Change the index to the device you want

def connected(client):
    client.subscribe("lightsensor")
    client.subscribe("moistsensor")
    client.subscribe("on-slash-off")
    client.subscribe("rainsensor")
    client.subscribe("reservoir")
    client.subscribe("tempsensor")
    print("Server connected ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

def message(client , feed_id , payload):
    print(f"Received payload from \"{feed_id}\": {payload}")
    
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
Mal_noti_halt = 0

while True:  
    # Reservoir amount
    client.publish("reservoir", reservoir)
    time.sleep(2)
    # Whether it's day or night/ raining or not.
    sun = random.randint(0,1) # Day (5am - 7pm)/Night (7pm - 5am).
    rain =random.randint(0,1) # Rain
    client.publish("lightsensor", sun)
    client.publish("rainsensor", rain)
    time.sleep(3)

    #Check if sensors work
    
    #sun sensor
    if (isinstance(sun, int)): 
        Sun_sensor_check = True
    else: Sun_sensor_check = False
    
    #rain sensor
    if (isinstance(rain, int)): 
        Rain_sensor_check = True
    else: Rain_sensor_check = False


    # Daytime  
    if sun == 1:  
        temp = random.randint(30, 35)
    # Nighttime
    else:
        temp = random.randint(25,29)

    #temperature sensor
    if (isinstance(temp, int)): 
        Temp_sensor_check = True
    else: Temp_sensor_check = False

    #When moisture data comes in
    #moisture sensor
    if (isinstance(moisture, int)): 
        Moist_sensor_check = True
    else: Moist_sensor_check = False

    # Rain
    if rain == 1:
        client.publish("tempsensor", temp-2)
        time.sleep(1)
        client.publish("moistsensor", 100)
        time.sleep(1)
        client.publish("on-slash-off", 0)
        time.sleep(1)
        client.publish("wateramount",0)
        time.sleep(1)
    # No rain
    else:
        client.publish("tempsensor", temp)
        time.sleep(1)   
        moisture = random.randint(50,99)
        client.publish("on-slash-off", 1)
        time.sleep(1)
        client.publish("moistsensor", moisture)
        time.sleep(1)
        
        if moisture >= 85: 
            reservoir -= 5
            client.publish("wateramount",5)           
        
        elif moisture <= 60: 
            reservoir -= 15
            client.publish("wateramount",15)
        
        else: 
            reservoir -= 10
            client.publish("wateramount",10)
        client.publish("reservoir", reservoir)

    #Notification with PushBullet (Extra feature 1)
    if(reservoir <= 0):
        pb.push_note("Water ran out, ", "Request refill", device=device)
    #Rain-dependent turn off
    if (rain == 1):
        pb.push_note("Rain detected","Temporarily turn off watering system", device=device)
    #Nighttime turn off
    if (sun == 0):
        pb.push_note("Nighttime mode", "No more sunlight detected, turning off system for the night", device=device)
    #Sensor malfunction notification
    if (Mal_noti_halt == 0): 
        if (Sun_sensor_check == False or Rain_sensor_check == False or Moist_sensor_check == False or Temp_sensor_check == False):
            pb.push_note("One or more of the sensors may not be functioning correctly", "Request checkup", device=device)
            print("Detected System Anomaly, Printing Out Anomaly Location...")
            print("f{sensor_list}")
            Mal_noti_halt += 1
    #Pause for 12 seconds
    time.sleep(12)
