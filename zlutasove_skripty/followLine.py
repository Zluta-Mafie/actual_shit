import time
import sys
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient
import convertVisualToMovement as cm
import math

if len(sys.argv) < 2:
    print("Usage: python3 followLine.py eth0")
    sys.exit(-1)

# 1. Initialize the communication channel
#ChannelFactoryInitialize(0, sys.argv[1])

# 2. Setup the Sport Client
sport_client = SportClient()
sport_client.SetTimeout(10.0)
sport_client.Init()

sport_client.Euler(0, 0.75, 0)
start_time = time.time()
duration = 20
print("Starting movement...")
while(time.time()-start_time<duration):
    lateralMove, rotation = cm.getMoveInstructions()
    sport_client.Move(0.3, lateralMove/4, rotation/60)
    time.sleep(0.5)

