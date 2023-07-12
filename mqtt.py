import time
import random
import sys
from Adafruit_IO import MQTTClient

configFile = open("config")
config = configFile.read().split("\n")

AIO_USERNAME = config[0].strip().split("=")[1]
AIO_KEY = config[1].strip().split("=")[1]

configFile.close()

def connected(client):
    client.subscribe("lightsensor")
    client.subscribe("moistsensor")
    client.subscribe("on-slash-off")
    client.subscribe("rainsensor")
    client.subscribe("reservoir")
    client.subscribe("tempsensor")
    client.subscribe("wateramount")
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

reservoir = 100

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
    
    # Daytime  
    if sun == 1:  
        temp = random.randint(30, 35)
    # Nighttime
    else:
        temp = random.randint(25,29)

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
    
    if reservoir <= 0: reservoir = 100
    time.sleep(12)