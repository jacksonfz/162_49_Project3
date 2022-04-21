
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
        
        wallSensorData = IMU.updateWallSensors()            # get ultrasonic data
 
        # STRAIGHT WALL FOLLOWING
        intersection = d.driveSingleWall(wallSensorData)    # follows wall and returns check for interesection
        IMU.detectHazards()                                 # check for IR & EM hazards

        # TURNING
        if intersection: # Do turn stuff
            print("turn point")
            wallSensorData = IMU.updateWallSensors()        # get more sensor data (make sure there's a wall)
            d.turnPoint(wallSensorData, heading)            # do turn point stuff based on wall data
                
        print('heading in main: {} id: {}'.format(heading[0], id(heading))) # check heading
        IMU.distanceUpdate(speed,rdt,heading[0])            # update the pos vector (DOING WEIRD STUFF SOMETIMES???)

        time.sleep(dT)              # time management
        rdt = time.time() - t0
        t0 = time.time()
        
except KeyboardInterrupt:
        d.drive(0,0)
        d.end()
        m.saveMap("test", m.map)
        m.saveHazards("test", m.hazards)
        
print("done")
