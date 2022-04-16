from GEARS_Setup import *   # put all the settings in one place

import vectors_v as IMU      # import custom IMU/vector math functions



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

def driveWalls (speed):
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
        

def turn (deg): # based on IMU data
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

def turnTime (deg): # time based turning
    const = 0.0767
    t0 = time.time()
    t1 = time.time()
    drive(0, IMU.sign(deg) * turnPower)
    timeStop = const * abs(deg)
    turn = 0
    a0 = IMU.sign(IMU.angle['z']) * IMU.length(IMU.angle)
    if IMU.sign(deg) > 0:
        print('turning right...')
    elif IMU.sign(deg) < 0:
        print('turning left...')
    while abs(time.time()-t0) <= abs(timeStop):
        time.sleep(dT)
        turn = IMU.sign(IMU.angle['z']) * IMU.length(IMU.angle) - a0
        
        rdt = time.time() - t1
        t1 = time.time()
        IMU.angleUpdate(rdt)
        
        
    drive(0, 0)
    print(turn)
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

def driveSingleWall(sensorData):
    distance, angle, gap = IMU.singleWallPos(sensorData)
    error = targetWallOffset - distance
    if sensorData[0] < wallCalibration: # there's a wall in front
        print("THERES A WALL IN THE WAY")
        turnTime(90)
    elif not error:
        turnCorrection = pTurn * error - dTurn * angle
        drive(speed, turnCorrection)
    elif error:
        if distance > wallCalibration:
            print("right turn")
            driveDistance(10, speed, 0)
            drive(0,0)
            turnTime(90)
            heading += 90
            time.sleep(dT)
            
            # sensorData = IMU.updateWallSensors()

            # walls = IMU.detectWall(sensorData)
            # if walls[2] == 0:
            #     #driveSpeed(speed, 0)
            #     driveDistance(30, speed, 90)
            #     print("going straight")
            #     #time.sleep(5)
            # else: print("THERES A WALL IN THE WAY")
            IMU.angle = IMU.vec0()
            print("reset angle")






#def updateMotorPos

def end (): #resets stuff/stops wheels
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    print("program ended")
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
