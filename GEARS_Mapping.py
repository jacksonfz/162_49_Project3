# from GEARS_Setup import *
import numpy as np


# MAPPING FUNCTIONS
mapSize = 12
gridSize = 40
origin = (0,0)
map = np.zeros([mapSize, mapSize], dtype=np.int8)
hazards = []

# Map codes
path = 1
start = 5
heat = 2
magnet = 3
end = 4

mapNumber = 0 #idk what this is for


def logPoint(x, y, value):
    map[x - origin[0], y - origin[0]] = int(value)
    # print(map)

def logHazard(type, pos, data):
    if type == "heat": 
        value = heat
        parameter = "Radiated Power (W)"
    if type == "magnet": 
        value = magnet
        parameter = "Feild Strength (uT)"
    logPoint(pos, value)
    hazards.append([type, parameter,value, pos[0], pos[1]])
    
def saveMap(fileName, array):
    logPoint(origin[0],origin[1],5)
    fid = open(fileName + "_map.csv", "w") # add check if file exists so it doesn't overwrite
    fid.write("Team: {} \nMap: {} \n Unit Length: {} \nUnit: {} \nOrigin: {} \nNotes{} \n\n".format(49, mapNumber, gridSize, "cm", origin, "Test map"))
    formattedMap = str(array)                       # convert to string
    formattedMap = formattedMap.strip()             # remove extra spaces
    formattedMap = formattedMap.replace("\n ", "\n")
    formattedMap = formattedMap.replace(" ", ",")   # replace space with ,
    formattedMap = formattedMap.replace("[", "")    # remove brackets
    formattedMap = formattedMap.replace("]", "")
    print(formattedMap)

    fid.write(formattedMap)
    fid.close()
    return()

def saveHazards(fileName, array):
    fid = open(fileName + "_hazards.csv", "w") # add check if file exists so it doesn't overwrite
    fid.write("Team: {} \nMap: {} \nNotes{} \n\n".format(49, mapNumber, "Test map"))
    fid.write("Hazard Type, Parameter of Interest, Parameter Value, Hazard X Coordinate, Hazard Y Coordinate \n")
    for h in hazards:
        formattedHazard = str(h)
        formattedHazard = formattedHazard.replace("[", "")    # remove brackets
        formattedHazard = formattedHazard.replace("]", "")
        fid.write(formattedHazard + "\n")

prev = list(origin)
def logPath(point): # update the map with a striaght line path from prev to point
    try:
        if point[0] == prev[0]: # x is constant
            x = point[0]
            direction = int(1 - 2 * (point[1] < prev[1])) # +/- 1
            for y in range(prev[1], point[1] + direction, direction):
                logPoint(x,y,1) # log points as path
            prev[1] = point[1]
        elif point[1] == prev[1]: # y is constant
            y = point[1]
            direction = int(1 - 2 * (point[0] < prev[0])) # +/- 1
            print(range(prev[1] + direction < 0 * 1, point[1] + direction > 0 * 1, direction))
            for x in range(prev[0], point[0] + direction, direction):
                logPoint(x,y,1) # log points as path
            prev[0] = point[0]
        else:
            print("Path log error: points {} and {} are diagonal".format(prev, point))
        print(map)
    except IndexError as e:
        print("Map error: ", e)
