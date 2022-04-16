# from GEARS_Setup import *
import numpy as np


# MAPPING FUNCTIONS
mapSize = 10
gridSize = 40
map = np.zeros([mapSize, mapSize], dtype=np.int8)

def saveMap(fileName, array):
    fid = open(fileName, "w") # add check if file exists so it doesn't overwrite
    fid.write("Team: {} \nMap: {} \n Unit Length: {} \nUnit: {} \nOrigin: {} \nNotes{} \n".format(49, 0, gridSize, "cm", "(0,0)", "Test map"))
    # for y in range(0,mapSize):
    #     mapRow = []
    #     for x in range(0,mapSize):
    #         mapRow.append(array[x,y])
    formattedMap = str(array)
    formattedMap = formattedMap.replace(" ", ",")
    formattedMap = formattedMap.replace("[", "")
    formattedMap = formattedMap.replace("]", "")
    print(formattedMap)

    fid.write(formattedMap)
    fid.close()
    return(fid)

def logPoint(x, y, value):
    map[x,y] = int(value)
    print(map)

