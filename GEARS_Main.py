import time     # this library contains the sleep (delay) function
import brickpi3 # import BrickPi3 library
import grovepi  # import GrovePi library
import vectors_v as IMU      # import custom IMU/vector math functions
import GEARS_DriveFunctions_v as d # import drive control functions

# SETUP SENSORS AND MOTORS
BP = brickpi3.BrickPi3() #initialize birckpi

# PORT DEFINITIONS (should move to DriveFunctions)
motorL = BP.PORT_C
motorR = BP.PORT_B
wheelCirc = 14.13675

# GROVE PORT VAR DEFINITIONS & INITIALIZATIONS
# use digital port (D) for all
sonarPort1 = 2 # left
sonarPort2 = 7 # center
sonarPort3 = 4 # right

#SETTING VARS
global dT
dT = 0.2


# MAIN SCRIPT

print("starting loop")
try:
    while True:
        ultrasonicData = [grovepi.ultrasonicRead(sonarPort1), grovepi.ultrasonicRead(sonarPort2), grovepi.ultrasonicRead(sonarPort3)]
        
        walls = IMU.detectWall(ultrasonicData)
        print("wall: {}, data: {}".format(walls, ultrasonicData))
        if walls[2] == 0: #if there is a not wall to the right
            d.turn(90)
        elif walls[1] == 1: #if there is a wall center and right
            d.turn(-90)
        else: 
            d.driveSpeed(10,0) #go straight

        time.sleep(dT)

except KeyboardInterrupt:
        d.drive(0,0)
        d.end()
        
print("done")
