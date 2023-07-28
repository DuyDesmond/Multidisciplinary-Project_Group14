import time

plantdb = open("Plant_data")
pdb = plantdb.read().split("\n")

#User type in their plant type
inp = input("Please enter your type of plant: ").strip()
i = 1

#Check for plant type in database
for index in range(8,len(pdb)):
    if pdb[index] == inp:
        time.sleep(1)
        name = inp

        print(f"For {name}, we suggest the following:")
        lo_temp = pdb[index+1].strip()
        hi_temp = pdb[index+2].strip()
        time.sleep(1)

        print(f"Temperature: {lo_temp}-{hi_temp} °C")
        water_v = pdb[index+3].strip()
        time.sleep(1)

        print(f"Waterring volume per day: {water_v} Liter")
        position = pdb[index+4].strip()
        time.sleep(1)

        print(f"Plant is best placed: {position}")
        time.sleep(1)

        print(f"Setting up systems for plant type: {name}...")
        i = 0

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