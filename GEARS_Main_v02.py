
from GEARS_Setup import *   # put all the settings in one place
                            # might get imported twice sometimes but that's fine

import vectors_v as IMU      # import custom IMU/vector math functions
import GEARS_DriveFunctions_v as d # import drive control functions
import GEARS_Mapping as m

print("modules imported")
time.sleep(0.5) # let the sensors warm up

    
# MAIN SCRIPT
t0 = time.time()
rdt = 0
heading = [0]
lockCargo()

print("starting main loop")

try:
    while True:
        
        wallSensorData = IMU.updateWallSensors()
        #print(IMU.singleWallPos(wallSensorData))
 
        intersection = d.driveSingleWall(wallSensorData)
        if intersection: # Do turn stuff
            print("turn point")
            wallSensorData = IMU.updateWallSensors()
            # savePos = IMU.pos.copy() # it will update during turning
            d.turnPoint(wallSensorData)
                

        IMU.distanceUpdate(speed,rdt,heading[0])
        time.sleep(dT)
        rdt = time.time() - t0
        t0 = time.time()
except KeyboardInterrupt:
        d.drive(0,0)
        d.end()
        m.saveMap("testmap.csv", m.map)
        
print("done")
