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

# def driveSpeed (speed, turn): #drive at the desired speed (cm/s), turn is a factor of speed
#     dps = -1 * speed * (360 / wheelCirc)
#     BP.set_motor_dps(motorL, dps + (dps * turn))
#     BP.set_motor_dps(motorR, dps - (dps * turn))
#     return

def stop():
    BP.set_motor_dps(motorPort, 0)
    
wheelIncrement = 15 / 1.05
go = 0

try:
    for y in range(0,yMax):
        print("waiting...")
        while not go:
            go = BP.get_sensor(BP.PORT_1)
            time.sleep(0.05)
            
        for x in range(0,xMax):
            zeroPositionA = BP.get_motor_encoder(motorPort)
            BP.offset_motor_encoder(motorPort, zeroPositionA) # Set current position of motor A to 'zero' position.
            BP.set_motor_position(motorPort, wheelIncrement) # turn wheel
            time.sleep(0.25)            
            sensor_value = grovepi.analogRead(light_sensor)
            fid.write("{},{},{}\n".format(x, y, sensor_value))
            print("log ", sensor_value)
            # time.sleep(0)

        print("loop")
        go = 0

except KeyboardInterrupt:
    stop()
    print("stopped")

fid.close()
print("done")
