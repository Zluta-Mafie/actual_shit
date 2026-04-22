import time
import sys
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient
import convertVisualToMovement as cm

if len(sys.argv) < 2:
    print("Usage: python3 followLine.py eth0")
    sys.exit(-1)

# 1. Initialize the communication channel
#ChannelFactoryInitialize(0, sys.argv[1])

# 2. Setup the Sport Client
sport_client = SportClient()
sport_client.SetTimeout(10.0)
sport_client.Init()

start_time = time.time()
duration = 3
print("Starting movement...")
while(time.time()-start_time<duration):
    lateralMove, rotation = cm.getMoveInstructions()
    sport_client.Move(0.5, lateralMove, rotation)
    time.sleep(0.5)
