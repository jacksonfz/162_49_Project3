
from GEARS_Setup import *   # put all the settings in one place
                            # might get imported twice sometimes but that's fine

import vectors_v as IMU      # import custom IMU/vector math functions
import GEARS_DriveFunctions_v as d # import drive control functions
import GEARS_Mapping as m
#from vectors_v import customError
print("modules imported")
time.sleep(2) # let the sensors warm up

    
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
        #print(IMU.detectHazards())
        hazard, hazardType = IMU.detectHazards()                        # check for IR & EM hazards, assuming hazards are in front
        #print("hazard: ", hazard)                                                            # returns hazard value

        # TURNING
        if intersection or hazard: # Do turn stuff
            print("turn point")
            wallSensorData = IMU.updateWallSensors()        # get more sensor data (make sure there's a wall)
            wallSensorData[0] *= not hazard                 # treat hazard as a wall in front
            d.turnPoint(wallSensorData, heading, hazard, hazardType)            # do turn point stuff based on wall data
            t0 = time.time()                                # reset time so it doesn't count the time it took to turn
            
        # print('heading in main: {} id: {}'.format(heading[0], id(heading))) # check heading
        IMU.distanceUpdate(speed,rdt,heading[0])            # update the pos vector (DOING WEIRD STUFF SOMETIMES???)

        
        time.sleep(dT)              # time management
        rdt = time.time() - t0
        t0 = time.time()
        
except KeyboardInterrupt:
        print("ending loop")
        d.drive(0,0)
        dropCargo()
        d.end()
        m.saveMap("team_49", m.map)
        m.saveHazards("team_49", m.hazards)
except d.customError:
        print("ending loop")
        d.drive(0,0)
        lockCargo()
        dropCargo()
        time.sleep(0.5)
        dropCargo()
        d.end()
        m.saveMap("test", m.map)
        m.saveHazards("test", m.hazards)
        
print("done")
