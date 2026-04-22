import time
import sys
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

def run_test():
    # 'lo' is the internal loopback interface for the robot's onboard PC
    # If this fails, you can pass the interface as an argument: python3 movement.py eth0
    internal_interface = "lo" 
    
    print(f"Initializing internal connection on {internal_interface}...")
    ChannelFactoryInitialize(0, internal_interface)

    # Setup the client
    client = SportClient()
    client.SetTimeout(10.0)
    client.Init()

    print("--- Starting Sequence ---")

    # 1. Sit Down
    print("Action: Sitting Down...")
    client.StandDown()
    
    # 2. Wait for 3 seconds
    print("Waiting for 3 seconds...")
    time.sleep(3)

    # 3. Stand Up
    print("Action: Standing Up...")
    client.StandUp()

    print("--- Sequence Complete ---")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"An error occurred: {e}")
