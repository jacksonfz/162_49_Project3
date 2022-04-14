# File: DC3_Scan_Team49.py
# Date: 04/13/22
# By: 
# Jack Brunner
# jrbrunne
# Jackson Ferry-Zamora
# jferryza
# Vera Fong
# lfong22
# Hannah Kadlec
# hkadlec
# Section: 3
# Team: 49
#
# ELECTRONIC SIGNATURE
# Jack Brunner
# Jackson Ferry-Zamora
# Vera Fong
# Hannah Kadlec
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# PROVIDE A BRIEF DESCRIPTION OF WHAT THE PROGRAM OR FUNCTION DOES 
# This codecontrols the scanner robot. The robot drives forward and scans data in increments. 
# It waits for the button to be pushed before each row

import time
import grovepi
import brickpi3 # import BrickPi3 library
BP = brickpi3.BrickPi3() #initialize birckpi

# PORT DEFINITIONS
motorPort = BP.PORT_A

# OTHER DEFINITIONS
wheelCirc = 16.4 # cm

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

grovepi.pinMode(light_sensor,"INPUT")

#TOUCH SENSOR
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

fileName = "DC3_Scan_Team49_image2.csv"
fid = open(fileName, "w")
xMax = 25
yMax = 25

def stop():
    BP.set_motor_dps(motorPort, 0)
    
wheelIncrement = 15 / 1.05
go = 0

try:
    for y in range(0,yMax): # move robot between each comumn

        print("waiting...")
        while not go: # wait for touch sensor
            go = BP.get_sensor(BP.PORT_1)
            time.sleep(0.05)
            
        for x in range(0,xMax): # get data
            zeroPositionA = BP.get_motor_encoder(motorPort)
            BP.offset_motor_encoder(motorPort, zeroPositionA) # Set current position of motor A to 'zero' position.
            BP.set_motor_position(motorPort, wheelIncrement) # turn wheel
            time.sleep(0.25)            
            sensor_value = grovepi.analogRead(light_sensor)
            fid.write("{},{},{}\n".format(x, y, sensor_value)) # write to file
            print("log ", sensor_value)
            # time.sleep(0)

        print("loop")
        go = 0

except KeyboardInterrupt:
    stop()
    print("stopped")

fid.close()
print("done")
