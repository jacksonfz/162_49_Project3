
from GEARS_Setup import *   # put all the settings in one place
                            # might get imported twice sometimes but that's fine

import vectors_v as IMU      # import custom IMU/vector math functions
import GEARS_DriveFunctions_v as d # import drive control functions

    
# MAIN SCRIPT
t0 = time.time()
rdt = 0
heading = 0
print("starting loop")
lockCargo()
try:
    while True:
        
        #ultrasonicData = IMU.sensorUpdate()

        #IMU.angleUpdate(rdt)
        #IMU.wallPos(ultrasonicData)
        
        
        # d.followWalls(ultrasonicData)


        wallSensorData = IMU.updateWallSensors()
        IMU.distanceUpdate(speed,rdt,heading)
        d.driveSingleWall(wallSensorData)
        time.sleep(dT)
        rdt = time.time() - t0
        t0 = time.time()
except KeyboardInterrupt:
        d.drive(0,0)
        d.end()
        
print("done")
