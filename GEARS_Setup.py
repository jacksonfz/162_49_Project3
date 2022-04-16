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
turnPower = 50 # dps of wheels, for turning functions

# GROVE PORT VAR DEFINITIONS & INITIALIZATIONS
# use digital port (D) for all

# # OLD SETUP
# sonarPort1 = 2 # left
# sonarPort2 = 7 # center
# sonarPort3 = 4 # right

# EV3 Ultrasonic
sonarPortF = BP.PORT_1
BP.set_sensor_type(sonarPortF, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM) # Configure for an EV3 ultrasonic sensor.

sonarPortR1 = 2 # right front
sonarPortR2 = 4 # right back
sonarPortL1 = 7 # left front
sonarPortL2 = 0 # left back

sensorDistance = 13.4 # cm between sensors
targetWallOffset = 10 # cm


#SETTING VARS
# global dT
dT = 0.2
centerOffsetThreshold = 4 # how far off center does robot need to be to react
angleOffsetThreshold = 25 # how far off center does robot need to be to react
speed = 10 # cm/s

# Ultrasonic Calibration
ultrasonicCalibration = 1.15 # 
EV3ultrasonicCalibration = 1
sensorOffset = 25 / 2 # distance from CoM in cm
hallWidth = 40 # cm
wallCalibration = 25 # distance to detect walls, cm

pTurn = 0.03
dTurn = 0.01


#INITIALIZE STUFF
heading = 0
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
