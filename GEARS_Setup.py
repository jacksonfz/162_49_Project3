# All port and other thing that need to be set/initialized go here. 
# This will be import* at the begining of all relevant files
# This should solve the problem of trying to pass settings and port definitions through multiple layer of functions
# Everything here will be stored in objects (dictionaries) so it can be referenced wherever. 
# Using dictionaries since idk how classes/objects work 

import brickpi3 # import BrickPi3 library
BP = brickpi3.BrickPi3() #initialize birckpi
import grovepi  # import GrovePi library
import sys 
import time

motorL = BP.PORT_C
motorR = BP.PORT_B
wheelCirc = 14.13675

# GROVE PORT VAR DEFINITIONS & INITIALIZATIONS
# use digital port (D) for all
sonarPort1 = 2 # left
sonarPort2 = 7 # center
sonarPort3 = 4 # right

#SETTING VARS
# global dT
dT = 0.2

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
