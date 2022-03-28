# Custom IMU functions written for semseter 1 project 3, based on IMU example code
"""
NOTES
    Don't import individual functions it won't work. Import/run the whole file
    It also won't work without an IMU connected
"""
from MPU9250 import MPU9250
# except: print("IMU setup error")

import sys 
import time
from math import sqrt, sin, cos, pi
mpu9250 = MPU9250() #from IMU example code

# SETTING VARS 
wallCalibration = 10 # ultrasonic units

#%% SENSOR FUNCTIONS
# All return vectors as dictionaries

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

def vec0(): # an empty 0 vector dictionary
    v0 = {
        "x": 0,
        "y": 0,
        "z": 0
    }
    return (v0)

def sign(number): # returns the sign of a number (+1/-1)
    try:
        sign = abs(number) / number
    except ZeroDivisionError:
        sign = 0
    return int(sign)

def scale(vector, scale): # multiplies each component of the vector by a scalar
    v1 = {} #get a new empty dict to avoid weird pass-by-address errors
    v1["x"] = vector["x"] * scale
    v1["y"] = vector["y"] * scale
    v1["z"] = vector["z"] * scale
    return(v1)

def dotProduct(vector1, vector2): # dot product of 2 vectors
    dot = vector1["x"] * vector2["x"] + \
          vector1["y"] * vector2["y"] + \
          vector1["z"] * vector2["z"]
    return(dot)

def length(vector): # length of a vector
    length = sqrt(vector["x"]**2 + vector["y"]**2 + vector["z"]**2)
    return(length)

def add(vector1, vector2): # adds 2 vectors component-wise
    comps = ["x", "y", "z"]
    vector = {} # empty dictionary
    for i in comps:
        vector[i] = vector1[i] + vector2[i]
    return vector

def printVec(vector): # prints vector with nice-ish formatting
    print("Vector: <{0:3.4}, {1:3.4}, {2:3.4}> Length: {3:3.4}".format(\
    float(vector["x"]), float(vector["y"]), float(vector["z"]), float(length(vector))))

#%% UPDATE LOOPS
    # run as loops, not very useful to use in actual code
def velocityLoop(refreshRate):
    velocity = {    #initialize velocity vector
        "x": 0,
        "y": 0,
        "z": 0
    }
    acceleration = 0
    while True: # integrate accel
        acceleration = accel()
        velocity["x"] += refreshRate * acceleration["x"]
        velocity["y"] += refreshRate * acceleration["y"]
        velocity["z"] += refreshRate * acceleration["z"]
        print("VELOCITY: {}cm/s, {}".format(100 * length(velocity), velocity))
        time.sleep(refreshRate) #this isn't using the actual dT so it's probably inaccurate

#%% LOOP UPDATE FUNCTIONS

# VELOCITY FUNCTION (to be used in loops/main)
velocity = { # initialize velocity, access this var from main to read current value
        "x": 0,
        "y": 0,
        "z": 0}

def velocityUpdate(time): #updates the velocity vector by integrating accel
    accelData = accel()
    velocity["x"] += time * accelData["x"]
    velocity["y"] += time * accelData["y"]
    velocity["z"] += time * accelData["z"]
    return(length(velocity))

# ANGLE FUNCTION (to be used in loops)
angle = { # initialize angle, access this var from main to read current value
    "x": 0,
    "y": 0,
    "z": 0}

def angleUpdate(time): # VOID, updates current angle by integrating angular velocity
    gyroData = gyro()
    angle["x"] += time * gyroData["x"]
    angle["y"] += time * gyroData["y"]
    angle["z"] += time * gyroData["z"]
    printVec(angle)

# DISTANCE TRACKING (from speed, to be used in loops)
pos = { # cm
    "x": 0,
    "y": 0,
    "z": 0}
def distanceUpdate(speed, timeStep, heading): # VOID, updates current position by integrating assumed velocity (from wheel dps setting and circ)
    pos["x"] += timeStep * speed * cos(heading * pi / 2) 
    pos["y"] += timeStep * speed * sin(heading * pi / 2)
    printVec(pos)

#%% OTHER SENSOR FUNCTIONS

# WALL DETECTION
wall = [0,0,0]
def detectWall(sensorData):
    for i in range(0,2): # for 3 walls (left, center ,right)
        if sensorData[i] < wallCalibration:
            wall[i] = True
        else:
            wall[i] = False
    return wall # returns list


