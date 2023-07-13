plantdb = open("Plant_data")
pdb = plantdb.read().split("\n")
inp = input("Please enter your type of plant: ").strip()
for index in range(5,len(pdb)):
    if pdb[index] == inp:
        print(f"For\"{inp}.capitalize()\", we suggest the following:")
        print(f"Temperature: \"{pdb[index+1].strip()}\"")
        print(f"Waterring volume per day: \"{pdb[index+2].strip()}\"")
        print(f"Plant is best placed: \"{pdb[index+3].strip()}\"")
        break
    plantdb.close()