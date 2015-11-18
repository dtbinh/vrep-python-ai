__author__ = 'Lothas'

import vrep
import sys
import time

print ('Program started')

vrep.simxFinish(-1)  # just in case, close all opened connections

# Connect to the simulation using V-REP's remote API (configured in V-REP, not scene specific)
# http://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

# Use port 19999 and add simExtRemoteApiStart(19999) to some child-script in your scene for scene specific API
# (requires the simulation to be running)

if clientID != -1:
    print ('Connected to remote API server')
else:
    print ('Failed connecting to remote API server')
    sys.exit('Could not connect')

# Reset running simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
time.sleep(0.2)

# Initialize simulation parameters
RobotNames = ["LineTracer", "LineTracer#0", "LineTracer#1"]
Params = [[[0.1, 0.2, 0, 0], [0.1, 0, 0, 0.2]],
          [[0.2, 0.2, 0, 0], [0.2, 0, 0, 0.2]],
          [[0.3, 0.3, 0, 0], [0.3, 0, 0, 0.4]]]
for i in range(len(RobotNames)):
    rN = RobotNames[i]
    Par = Params[i]
    for j in range(len(Par)):
        # For each motor
        for k in range(len(Par[j])):
            # For each sensor (+ base value)
            SignalName = rN+"_"+str(j+1)+"_"+str(k+1)
            res = vrep.simxSetFloatSignal(clientID, SignalName, Par[j][k],
                                            vrep.simx_opmode_oneshot)

# Start running simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

time.sleep(10)  # wait 10 seconds

# Stop running the simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

time.sleep(0.1)
vrep.simxFinish(clientID)  # close connection to API
print ('Program ended')
