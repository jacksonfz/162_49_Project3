
import time
from turtle import heading     # this library contains the sleep (delay) function
import brickpi3 # import BrickPi3 library
import grovepi  # import GrovePi library
import vectors_v as IMU      # import custom IMU/vector math functions


# SETUP SENSORS AND MOTORS
BP = brickpi3.BrickPi3() #initialize birckpi

# PORT DEFINITIONS
motorL = BP.PORT_C
motorR = BP.PORT_B

# OTHER DEFINITIONS
wheelCirc = 14.13675 # cm
turnPower = 50 # dps of wheels

try: dT = dT
except: dT = 0.25

# DRIVING FUNCTIONS
def drive (dps, turn): #makes the wheels go at a desired dps
    BP.set_motor_dps(motorL, (dps + turn))
    BP.set_motor_dps(motorR, (dps - turn))
    return

def driveSpeed (speed, turn): #drive at the desired speed (cm/s), turn is a factor of speed
    dps = -1 * speed * (360 / wheelCirc)
    BP.set_motor_dps(motorL, dps + (dps * turn))
    BP.set_motor_dps(motorR, dps - (dps * turn))
    return

def drivePower (power, turn):
    BP.set_motor_power(motorL, power + (power * turn))
    BP.set_motor_power(motorR, power - (power * turn))
    return

def turn (deg):
    t0 = time.time()
    drive(0, IMU.sign(deg) * turnPower)
    IMU.angle = {
    "x": 0,
    "y": 0,
    "z": 0}
    while IMU.length(IMU.angle) <= abs(deg): #(abs(IMU.angle["z"]) <= abs(deg)):
        rdT = time.time() - t0
        IMU.angleUpdate(rdT)
        t0 = time.time()
        print("timestep: ", rdT)
        time.sleep(dT)
    drive(0,0)
    print("done turning")

def driveDistance(distance, speed): # drives distance in whichever direction it is facing and tracks pos
    # can correctly update pos on angles
    # pos y+ is default forward, x+ is right
    p0 = IMU.pos.copy() # copy or else the reference the same object and change together
    distTravelled = 0
    try: heading = heading # inherit heading from main if it exists
    except: heading = 0

    
    t0 = time.time()
    driveSpeed(speed, 0)
    try:
        while distTravelled < distance: # while delta pos < distance
            rdT = time.time() - t0
            print("p0: {}, dx: {}".format(p0, distTravelled))
            IMU.distanceUpdate(speed, rdT, heading)
            t0 = time.time()
            time.sleep(dT)
            distTravelled = IMU.length(IMU.add(IMU.pos, IMU.scale(p0, -1)))
    except KeyboardInterrupt:
        drive(0,0)
    drive(0, 0)
        
def driveToPoint(x, y):
    # on start forward is y+, right is x+
    # distance units = cm, speed = cm/s
    speed = 15 # maybe move this elsewhere/inherit
    heading = 0

    if (y < 0):
        turn(180)
        heading = 180

    driveDistance(abs(y), speed) # drives distance and updates pos

    time.sleep(1)
    turn(90 * IMU.sign(x))
    heading += 90 * IMU.sign(x)
    
    driveDistance(abs(x), speed) # drives distance and updates pos



def end (): #resets stuff/stops wheels
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    print("program ended")
    return

def driveStop(): #for the speed challenge
    speed = int(input("Input speed in cm/s: "))
    driveSpeed(speed, 0)
    while True:
        sonarData = grovepi.ultrasonicRead(sonar1)
        if sonarData > stopDistance:
            break
    drive(0,0)
    return

# DISTANCE TRACKING



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
