import time

configFile = open("config")

config = configFile.read().split("\n")
plant_name = config[6].strip().split("=")[-1]

configFile.close()

plantdb = open("Plant_data")
pdb = plantdb.read().split("\n")
i=1

#Check for plant type in database
for index in range(8,len(pdb)):
    if pdb[index] == plant_name:
        i = 0

        print(f"For {plant_name}, we suggest the following:")
        time.sleep(1)
        
        lo_temp = float(pdb[index+1].strip())
        hi_temp = float(pdb[index+2].strip())
        print(f"Temperature: {lo_temp}-{hi_temp} °C")
        time.sleep(1)
        
        water_v = pdb[index+3].strip()
        duration = float(pdb[index+4].strip())
        print(f"Waterring volume per day: {water_v} Liter")
        time.sleep(1)

        position = pdb[index+5].strip()
        print(f"Plant is best placed: {position}")
        time.sleep(1)

        print(f"Setting up systems for plant type: {plant_name}...")
        

        break

plantdb.close()

#Default detting if can't find plant type in database
if i: 
    time.sleep(1)

    print("Plant type not found\nReverting to default setting...")
    time.sleep(2)
    
    lo_temp = 20
    hi_temp = 35
    water_v = 1