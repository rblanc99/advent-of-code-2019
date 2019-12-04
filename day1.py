from math import floor

def fuel(mass) :
    return floor(mass/3)-2

def total_fuel(list) :
    total = 0
    for x in list:
        total+=fuel(int(x))
    return total

def read_file(name) :
    input = open(name, "r").read()
    lines = input.split("\n")
    if lines[-1] == "":
        lines.pop()
    return lines

input = read_file("input-day1")

def real_fuel(mass) :
    fuelAmount = fuel(mass)
    neededFuel = fuel(fuelAmount)
    while neededFuel >0 :
        fuelAmount+=neededFuel
        neededFuel = fuel(neededFuel)
    return fuelAmount

def total_real_fuel(list) :
    total = 0
    for x in list:
        total+=real_fuel(int(x))
    return total


    
