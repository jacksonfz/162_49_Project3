
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
wheelCirc = 16.4 # cm
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

def turnTime (deg):
    const = 0.0775
    t0 = time.time()
    drive(0, IMU.sign(deg) * turnPower)
    timeStop = const * abs(deg)
    if IMU.sign(deg) > 0:
        print('turning right...')
    elif IMU.sign(deg) < 0:
        print('turning left...')
    while time.time() - t0 <= timeStop:
        time.sleep(dT)
    drive(0, 0)
    print('done turning')

def driveDistance(distance, speed, heading): # drives distance in whichever direction it is facing and tracks pos
    # can correctly update pos on angles
    # pos y+ is default forward, x+ is right
    correction = -0.017
    p0 = IMU.pos.copy() # copy or else the reference the same object and change together
    distTravelled = 0
    
    t0 = time.time()
    driveSpeed(speed, correction)
    try:
        while distTravelled < distance: # while delta pos < distance
            rdT = time.time() - t0
            # print("p0: {}, dx: {}".format(p0, distTravelled))
            IMU.distanceUpdate(speed, rdT, heading)
            t0 = time.time()
            time.sleep(dT)
            distTravelled = IMU.length(IMU.add(IMU.pos, IMU.scale(p0, -1)))
        print(heading)
    except KeyboardInterrupt:
        drive(0,0)
    drive(0, 0)
        
def driveToPoint(x, y, heading):
    # on start forward is y+, right is x+
    # distance units = cm, speed = cm/s
    speed = 15 # maybe move this elsewhere/inherit

    if IMU.sign(y) < 0:
        targetHeading = 180
    elif IMU.sign(y) > 0:
        targetHeading = 0
    else:
        targetHeading = heading

    print("target heading: ", targetHeading)
    turnTime(targetHeading - heading)
    heading = targetHeading
        
    # turnTime(90 - (90 * IMU.sign(y)))
    #heading += (90 - (90 * IMU.sign(y)))

    driveDistance(abs(y), speed, heading) # drives distance and updates pos

    time.sleep(1)

    
    if IMU.sign(x) < 0:
        targetHeading = -90
    elif IMU.sign(x) > 0:
        targetHeading = 90
    else:
        targetHeading = heading

    print("target heading: ", targetHeading)
    turnTime(targetHeading - heading)
    heading = targetHeading

       
    # turnTime(90 * IMU.sign(x))
    # heading += 90 * IMU.sign(x)
    
    driveDistance(abs(x), speed, heading) # drives distance and updates pos
    return heading

def driveToPoints(points):
    heading = 0
    #gridSize = 40
    #points *= gridSize
    
    for i in range(0, int(len(points)), 2):
        x = points[i]
        y = points[i + 1]
        posIn = IMU.pos.copy()
        print('absolute: {}, {} relative: {}, {}'.format(x, y, x - posIn['x'], y - posIn['y']))
        heading = driveToPoint(x - posIn['x'], y - posIn['y'], heading)
        variable = input('Press any button, then enter...')
        print('driveToPoint iteration')


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
