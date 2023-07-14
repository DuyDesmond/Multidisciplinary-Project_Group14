plantdb = open("Multidisciplinary-Project_Group14\Plant_data")
pdb = plantdb.read().split("\n")
inp = input("Please enter your type of plant: ").strip()
for index in range(5,len(pdb)):
    if pdb[index] == inp:
        name = inp
        print(f"For \"{name}\", we suggest the following:")
        lo_temp = pdb[index+1].strip()
        hi_temp = pdb[index+2].strip()
        print(f"Temperature: \"{lo_temp}\"-\"{hi_temp}\"°C")
        water_v = pdb[index+3].strip()
        print(f"Waterring volume per day: \"{water_v}\" Liter")
        position = pdb[index+4].strip()
        print(f"Plant is best placed: \"{position}\"")
        print(f"Setting up systems for plant type: \"{name}\"...")
        break
    plantdb.close()