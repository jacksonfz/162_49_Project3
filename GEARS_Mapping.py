# from GEARS_Setup import *
import numpy as np


# MAPPING FUNCTIONS
mapSize = 12
gridSize = 40
origin = (0,0)
map = np.zeros([mapSize, mapSize], dtype=np.int8)

# Map codes
path = 1


def logPoint(x, y, value):
    map[x,y] = int(value)
    # print(map)
    
def saveMap(fileName, array):
    logPoint(origin[0],origin[1],5)
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


prev = list(origin)
def logPath(point):
    try:
        if point[0] == prev[0]:
            x = point[0]
            direction = int(1 - 2 * (point[1] < prev[1])) # +/- 1
            for y in range(prev[1] + (direction < 0), point[1] + (direction > 0), direction):
                logPoint(x,y,1) # log points as path
            prev[1] = point[1]
        elif point[1] == prev[1]:
            y = point[1]
            direction = int(1 - 2 * (point[0] < prev[0])) # +/- 1
            print(range(prev[1] + direction < 0 * 1, point[1] + direction > 0 * 1, direction))
            for x in range(prev[0] + (direction < 0), point[0] + (direction > 0), direction):
                logPoint(x,y,1) # log points as path
            prev[0] = point[0]
        else:
            print("Path log error: the points are diagonal")
        print(map)
    except IndexError as e:
        print("Map error: ", e)
