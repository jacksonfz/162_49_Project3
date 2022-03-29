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
#wheelCirc = 14

# GROVE PORT VAR DEFINITIONS & INITIALIZATIONS
# use digital port (D) for all
sonarPort1 = 2 # left
sonarPort2 = 7 # center
sonarPort3 = 4 # right

#SETTING VARS
global dT
dT = 0.2
heading = 180


# MAIN SCRIPT

print("starting loop")
try:
    d.driveToPoints([-20, 20, 0, 0])

except KeyboardInterrupt:
        d.drive(0,0)
        d.end()
        
print("done")
