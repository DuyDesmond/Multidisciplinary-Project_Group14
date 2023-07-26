import time
import requests

#Getting weather info (mostly if it rains or not) 
configFile = open("config")
config = configFile.read().strip().split("\n")

API_KEY = config[6].strip().split("=")[-1]
CITY = config[7].strip().split("=")[-1]

configFile.close()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

response = requests.get(BASE_URL + "appid=" + API_KEY + "&q=" + CITY).json()
current_weather = response['weather'][0]['main']

#Left these lines here for troubleshooting
print(response)
print()
print(f'Current weather: {current_weather}')

plantdb = open("Plant_data")
pdb = plantdb.read().split("\n")
#User type in their plant type
inp = input("Please enter your type of plant: ").strip()
i = 1
#Check for plant type in database
for index in range(5,len(pdb)):
    if pdb[index] == inp:
        name = inp
        print(f"For {name}, we suggest the following:")
        lo_temp = pdb[index+1].strip()
        hi_temp = pdb[index+2].strip()
        print(f"Temperature: {lo_temp}-{hi_temp} °C")
        water_v = pdb[index+3].strip()
        print(f"Waterring volume per day: {water_v} Liter")
        position = pdb[index+4].strip()
        print(f"Plant is best placed: {position}")
        print(f"Setting up systems for plant type: {name}...")
        i = 0
        break
#Default detting if can't find plant type in database
if i: 
    print("Plant type not found\nReverting to default setting...")
    time.sleep(2)
    lo_temp = 20
    hi_temp = 35
    water_v = 1
plantdb.close()