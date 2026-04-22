import time
import sys
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

if len(sys.argv) < 2:
    print("Usage: python3 neco.py eth0")
    sys.exit(-1)

# 1. Initialize the communication channel
ChannelFactoryInitialize(0, sys.argv[1])

# 2. Setup the Sport Client
sport_client = SportClient()
sport_client.SetTimeout(10.0)
sport_client.Init()

# 3. Give it a tiny moment to heartbeat
time.sleep(0.5)

print("Sending StandDown command...")
sport_client.Move(0, 0, 2)
time.sleep(1)
#sport_client.Move(0, 0, 1)
time.sleep(1)
#sport_client.Move(0, 0, 1)
time.sleep(1)

