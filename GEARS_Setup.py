"""
# All port and other thing that need to be set/initialized go here. 
# This will be import* at the begining of all relevant files
# This should solve the problem of trying to pass settings and port definitions through multiple layer of functions
"""

import brickpi3 # import BrickPi3 library
BP = brickpi3.BrickPi3() #initialize birckpi
import grovepi  # import GrovePi library
import sys 
import time

motorL = BP.PORT_C
motorR = BP.PORT_B
motorC = BP.PORT_A
# wheelCirc = 14.13675 # idk which of these is right
wheelCirc = 16.4 # cm

# GROVE PORT VAR DEFINITIONS & INITIALIZATIONS
# use digital port (D) for all
sonarPort1 = 2 # left
sonarPort2 = 7 # center
sonarPort3 = 4 # right

#SETTING VARS
# global dT
dT = 0.2
centerOffsetThreshold = 4 # how far off center does robot need to be to react
angleOffsetThreshold = 25 # how far off center does robot need to be to react
speed = 10 # cm/s

# Ultrasonic Calibration
ultrasonicCalibration = 1.15 # currently calibrated to my desk
sensorOffset = 25 / 2 # distance from CoM in cm
hallWidth = 40 # cm
wallCalibration = 20 # ultrasonic units

def lockCargo():
    zeroPositionA = BP.get_motor_encoder(motorC)
    BP.offset_motor_encoder(motorC, zeroPositionA) # Set current position of motor A to 'zero' position.
    BP.set_motor_position(motorC, 0) # turn wheel


def dropCargo():
    BP.set_motor_position(motorC, -60) # turn wheel



# portConfig = {  # create a dictionary object with all the port configurations so all the functions can easily reference this
#             # most of this info is taken from vars above so it's repetitive but whatever
#     "motorL": BP.PORT_C,
#     "motorR": BP.PORT_B,
#     "sonar1": 2,
#     "sonar2": 7,
#     "sonar1": 4,
# }

# robotConfig= {
#     "wheelCirc": 14.13675
# }



# #%%
# class portConfig:
#     def __init__(self, motorR, motorL, sonar1, sonar2, sonar3):
#         self.motorR = 1
#         self.motorL = 2
#         self.sonar1 = 1
#         self.sonar2 = 2
#         self.sonar3 = 3
# print 
