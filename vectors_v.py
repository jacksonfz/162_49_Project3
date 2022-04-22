# Custom IMU functions written for semseter 1 project 3, based on IMU example code
"""
NOTES
    don't import individual functions it won't work
"""

from GEARS_Setup import *   # put all the settings in one place

from MPU9250 import MPU9250
from math import sqrt, sin, cos, pi, acos, asin
mpu9250 = MPU9250()

#%% SENSOR FUNCTIONS

def accel(): #reads acceleration
    accel = mpu9250.readAccel()
    return(accel)

def gyro(): #reads angular velocity
    gyro = mpu9250.readGyro()
    return(gyro)

def mag(): #reads magnet sensor
    mag = mpu9250.readMagnet()
    return(mag)

#%% MATH FUNCTIONS

def vec0(): #an empty 0 vector dictionary
    v0 = {
        "x": 0,
        "y": 0,
        "z": 0
    }
    return (v0)

def sign(number): #returns the sign of a number (+1/-1)
    try:
        sign = abs(number) / number
    except ZeroDivisionError:
        sign = 0
    return int(sign)

def scale(vector, scale): #multiplies to each component of the vector
    v1 = {} #get a new empty dict to avoid weird pass-by-address errors
    v1["x"] = vector["x"] * scale
    v1["y"] = vector["y"] * scale
    v1["z"] = vector["z"] * scale
    return(v1)

def dotProduct(vector1, vector2): #dot product of 2 vectors
    dot = vector1["x"] * vector2["x"] + \
          vector1["y"] * vector2["y"] + \
          vector1["z"] * vector2["z"]
    return(dot)

def length(vector): #length of a vector
    length = sqrt(vector["x"]**2 + vector["y"]**2 + vector["z"]**2)
    return(length)

def add(vector1, vector2): # adds 2 vectors component-wise
    comps = ["x", "y", "z"]
    vector = {}
    for i in comps:
        vector[i] = vector1[i] + vector2[i]
    return vector

def printVec(vector):
    print("Vector: <{0:3.4}, {1:3.4}, {2:3.4}> Length: {3:3.4}".format(\
    float(vector["x"]), float(vector["y"]), float(vector["z"]), float(length(vector))))

#%% UPDATE LOOPS

def velocityLoop(refreshRate):
    velocity = {
        "x": 0,
        "y": 0,
        "z": 0
    }
    acceleration = 0
    while True:
        acceleration = accel()
        velocity["x"] += refreshRate * acceleration["x"]
        velocity["y"] += refreshRate * acceleration["y"]
        velocity["z"] += refreshRate * acceleration["z"]
        print("VELOCITY: {}cm/s, {}".format(100 * length(velocity), velocity))
        time.sleep(refreshRate)

#%% LOOP UPDATE FUNCTIONS

# VELOCITY FUNCTION (to be used in loops)
velocity = {
        "x": 0,
        "y": 0,
        "z": 0}

def velocityUpdate(time):
    accelData = accel()
    velocity["x"] += time * accelData["x"]
    velocity["y"] += time * accelData["y"]
    velocity["z"] += time * accelData["z"]
    return(length(velocity))

# ANGLE FUNCTION (to be used in loops)
angle = {
    "x": 0,
    "y": 0,
    "z": 0}

def angleUpdate(time):
    gyroData = gyro()
    angle["x"] += time * gyroData["x"]
    angle["y"] += time * gyroData["y"]
    angle["z"] += time * gyroData["z"]
    # printVec(angle)

# DISTANCE TRACKING (from speed, to be used in loops)
pos = {
    "x": 0,
    "y": 0,
    "z": 0}
def distanceUpdate(speed, timeStep, heading):
    pos["x"] += timeStep * speed * round(sin(heading * pi / 180), 3)
    pos["y"] += timeStep * speed * round(cos(heading * pi / 180), 3)
    # printVec(pos)
    add = [timeStep * speed * round(sin(heading * pi / 180), 3), timeStep * speed * round(cos(heading * pi / 180), 3)]
    print("pos: {}, heading: {}, add: {}".format(pos, heading, add))

#%% OTHER SENSOR FUNCTIONS

# def sensorUpdate(): # For 3 ultrasonic sensors
#     s1 = grovepi.ultrasonicRead(sonarPort1) * ultrasonicCalibration # left side sensor distance 
#     s2 = grovepi.ultrasonicRead(sonarPort2) * ultrasonicCalibration # center sesnor distance
#     s3 = grovepi.ultrasonicRead(sonarPort3) * ultrasonicCalibration # right side sesnor distance
#     return(0, s1, s2, s3) #first spot isn't used for easy indexing

wall = [0,0,0,0] #first spot isn't used for easy indexing
def detectWall(sensorData): # for 3 sesnors
    for i in range(1,len(sensorData)): # for 3 walls (0, l, c ,r)
        if sensorData[i] < wallCalibration:
            wall[i] = True
        else:
            wall[i] = False
    return wall

def checkWall(sensorData): # for 5 sensors
    wall[2] = sensorData[0] < wallCalibration # front
    wall[1] = (sensorData[3] < wallCalibration) #+ (sensorData[4] < wallCalibration) # left
    wall[3] = (sensorData[1] < wallCalibration) + (sensorData[2] < wallCalibration) # right
    # sensor l2 doesn't exist
    return(wall)


# WallPos setup stuff

prevOffset = 0 # store for derivative
s1Prev = 0 # storage for hallway detection
s2Prev = 0
errorThreshold = 10 # if delta s > this readings are assumed to be wrong because of a right/left hallway
# hallWidth = 57 # cm, maybe move back to args

wallPosStorage = [prevOffset, s1Prev, s2Prev] # passing things to be updated just works better in a list idk

def wallPos(sensorData): # with 1 sensor on each size
    
    # # Get sensor data and convert to cm
    # s1 = grovepi.ultrasonicRead(sonarPort1) * ultrasonicCalibration # left side sensor distance 
    # s2 = grovepi.ultrasonicRead(sonarPort3) * ultrasonicCalibration # right side sesnor distance
    s1 = sensorData[1]
    s2 = sensorData[3] # s2 = sensor 3 = right 

    # check for side hallways
        # NOTE FOR LATER: Return sensor values or way to override error if very close to wall
    if abs(s1 - wallPosStorage[1]) > errorThreshold or abs(s2 - wallPosStorage[2]) > errorThreshold:
        error = 1 
    else: error = 0
    wallPosStorage[1] = s1
    wallPosStorage[2] = s2
    
    # calculate stuff
    offset = (s1 - s2) * hallWidth / (s1 + s2 + 2 * sensorOffset) # distance in cm from center, - is left
    direction = sign(offset - wallPosStorage[0]) # for angle sign, watch for noise
    wallPosStorage[0] = offset # update prev value
    try:
        theta = 180 / pi * acos(hallWidth /(s1 + s2 + 2 * sensorOffset)) * direction # angle of the robot relative to walls, + is clockwise
    except ValueError:
        theta = 0 #float("NAN")
        
    

    # debug printing
    ow = s1 + s2 + sensorOffset * 2
    print("s1: {0:5.1f}cm, s2: {1:5.1f}cm, offset: {2:5.1f}cm, WallAngle: {3:5.3f}, IMU: {6:4.1f} width: {5:4.1f}, error: {4}".format(s1, s2, offset, theta, error, ow, angle["z"]))


    return(offset, theta, bool(error))

def updateWallSensors(): # for 5 sensors
    sr1 = grovepi.ultrasonicRead(sonarPortR1) * ultrasonicCalibration # right side sensor 1 distance 
    sr2 = grovepi.ultrasonicRead(sonarPortR2) * ultrasonicCalibration # center sensor distance
    try: #left side is optional
        sl1 = grovepi.ultrasonicRead(sonarPortL1) * ultrasonicCalibration # right side sesnor distance
        sl2 = grovepi.ultrasonicRead(sonarPortL2) * ultrasonicCalibration # right side sesnor distance
    except IOError:
        sl1 = float("NAN")
        sl2 = float("NAN")

    try: #front sensor
        sf = BP.get_sensor(sonarPortF) * EV3ultrasonicCalibration
    except brickpi3.SensorError as error:
        sf = float("NAN")
        print(error)
    #sf = 50
    return(sf, sr1, sr2, sl1, sl2)



wallStorgae1 = [0,0,0] #angle, s1, s2
def singleWallPos(wallSensorData):

    s1 = wallSensorData[1]
    s2 = wallSensorData[2]
    distance = (s1 + s2) / 2
    if abs(s1 - wallStorgae1[1]) > errorThreshold or abs(s2 - wallStorgae1[2]) > errorThreshold:
        error = 1 
    else: error = 0
    wallStorgae1[1] = s1
    wallStorgae1[2] = s2
    try:
        angle = 180 / pi * asin((s2 - s1) / sensorDistance)
        angle = min(max(angle, -25), 25)
    except ValueError:
        angle = float("NAN")
    return(distance, angle, error)

def fixPos():
    print(pos)
    gridPos = (round(pos["x"] / hallWidth), round(pos["y"] / hallWidth))
    pos["x"] = gridPos[0] * hallWidth
    pos["y"] = gridPos[1] * hallWidth
    print(pos)
    return(gridPos)


#%% HAZARDS DETECTION
from IR_Functions import * # import these (from example code)
IR_setup(grovepi) # it needs grovepi as an argument idk why

def detectHazards():    
    ir1, ir2 = IR_Read(grovepi)
    avg = (ir1 + ir2) / 2
    magVec = mag()
    magLen = length(magVec)

    if avg > irDetectionThreshold:
        hazard = True
        print("IR hazard detected!")
    if magLen > magDetectionThreshold:
        hazard = True
        print("EM hazard detected!")
    else: hazard = False
    # Need to figure out how to do loggin in a way that it doesn't log the same hazard many times
    return(hazard)
