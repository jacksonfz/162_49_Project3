from GEARS_Setup import *
from GEARS_DriveFunctions_v import *


# Just old stuff that was taking up space in drive functions


# Idea: put all sensor updates into a single function that updates all values in an object that can be referenced by all functions
#       and update it every loop iteration. Will allow for faster loop runtime
def followWalls(sensorData): # this goes inside a while loop
    offset, angle, gap = IMU.wallPos(sensorData)
    if gap: # probably a turn hallway, wallPos data can't be trusted
        #do turn stuff
        #turnTime(90)
        print("not turning")
        #time.sleep(1)
        walls = IMU.detectWall(sensorData)
        print(walls)
        if walls[3] == 0:
            print("Doing right turn")
            driveDistance(10, speed, 0)
            drive(0,0)
            turnTime(90)
            time.sleep(dT)
            sensorData = IMU.sensorUpdate()
            walls = IMU.detectWall(sensorData)
            if walls[2] == 0:
                #driveSpeed(speed, 0)
                driveDistance(30, speed, 90)
                print("going straight")
                #time.sleep(5)
            else: print("THERES A WALL IN THE WAY")
            IMU.angle = IMU.vec0()
            print("reset angle")
        elif walls[1] == 0: turnTime(-90)
        turnCorrection = 0
    elif (abs(offset) > centerOffsetThreshold) or (abs(angle) > angleOffsetThreshold): # robot needs to correct
        turnCorrection = pTurn * offset - dTurn * IMU.sign(IMU.angle["z"]) * angle
        print("turning: ", turnCorrection)
    else: 
        turnCorrection = 0
    driveSpeed(speed, turnCorrection)

def driveWalls (speed): # old
    dps = -1 * speed * 360 / wheelCirc
    leftPort = 2
    rightPort = 4
    coefProp = 0.02
    coefInt = 0
    integral = 0
    derivative = 0.01
    coefDer = 0
    error0 = 0
    
    try:
        while True:
            IMU.angleUpdate(dT)
            turn = IMU.sign(IMU.angle['z']) * IMU.length(IMU.angle)
            print(turn)
            
            
            leftD = grovepi.ultrasonicRead(leftPort)
            rightD = grovepi.ultrasonicRead(rightPort)
            error = leftD - rightD
            integral += dT * error
            derivative = (error - error0) / dT
            error0 = error

            correction = error * coefProp + integral * coefInt + derivative * coefDer
            BP.set_motor_dps(motorL, dps * (1 + (correction)))
            BP.set_motor_dps(motorR, dps * (1 - (correction)))

            # print("PID: {}, {}, {}, correction: {})".format(error * coefProp, integral, derivative, correction))

            time.sleep(dT)
            
    except KeyboardInterrupt:
        drive(0, 0)
        
    return
        


# DRIVE LOOPS FOR EASY TESTING
def driveLoop(): #dps
    while True:
        try:
            driveInput = (input("drive: ")).split()
            speed, turn = float(driveInput[0]), float(driveInput[1]) 
            # print("{}, {}".format(speed, turn))
            drive(speed, turn)
        except KeyboardInterrupt:
            drive(0,0)
            print("stopped")
            try:
                driveInput = (input("drive: ")).split()
                speed, turn = float(driveInput[0]), float(driveInput[1])
                drive(speed, turn)
            except KeyboardInterrupt:
                break

def driveSpeedLoop(): #cm/s
    while True:
        try:
            driveInput = (input("drive: ")).split()
            if len(driveInput) < 2: speed, turn = driveInput, 0
            else: speed, turn = float(driveInput[0]), float(driveInput[1]) 
            # print("{}, {}".format(speed, turn))
            driveSpeed(speed, turn)
        except IndexError:
                turn = 0
        except KeyboardInterrupt:
            driveSpeed(0,0)
            print("stopped")
            try:
                driveInput = (input("drive: ")).split()
                if len(driveInput) < 2: speed, turn = driveInput, 0
                else: speed, turn = float(driveInput[0]), float(driveInput[1])
                driveSpeed(speed, turn)
            except IndexError:
                turn = 0
            except KeyboardInterrupt:
                break

def drivePowerLoop(): #power [0,100]
    while True:
        try:
            driveInput = (input("drive: ")).split()
            speed, turn = float(driveInput[0]), float(driveInput[1]) 
            # print("{}, {}".format(speed, turn))
            drivePower(speed, turn)
        except KeyboardInterrupt:
            drivePower(0,0)
            print("stopped")
            try:
                driveInput = (input("drive: ")).split()
                speed, turn = float(driveInput[0]), float(driveInput[1])
                drivePower(speed, turn)
            except KeyboardInterrupt:
                break
