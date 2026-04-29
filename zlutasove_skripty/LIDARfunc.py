import time
import numpy as np
from unitree_sdk2py.core.channel import ChannelSubscriber
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.idl.unitree_lidar_sdk import UnitreeLidarCloud

class Go2SafetyShield:
    def __init__(self):
        # Initialize SportClient to send movement commands
        self.client = SportClient()
        self.client.SetTimeout(10.0)
        self.client.Init()

        # Obstacle State
        self.obstacle_detected = False

        # Define Bounding Box (in meters)
        self.X_RANGE = (0.1, 0.8)  # 10cm to 80cm in front
        self.Y_RANGE = (-0.25, 0.25)  # 25cm left/right of center
        self.Z_RANGE = (-0.3, 0.3)  # Relative to LiDAR height (excludes floor)

        # Subscriber for LiDAR Point Cloud
        self.sub = ChannelSubscriber("rt/utlidar/cloud_deskewed", UnitreeLidarCloud)
        self.sub.Init(self.lidar_callback, 10)

    def lidar_callback(self, msg):
        # Convert raw buffer to numpy array (x, y, z)
        # Note: Go2 LiDAR data usually comes in as a packed float array
        points = np.frombuffer(msg.data, dtype=np.float32).reshape(-1, 3)

        # Filter points within the Bounding Box
        in_x = (points[:, 0] > self.X_RANGE[0]) & (points[:, 0] < self.X_RANGE[1])
        in_y = (points[:, 1] > self.Y_RANGE[0]) & (points[:, 1] < self.Y_RANGE[1])
        in_z = (points[:, 2] > self.Z_RANGE[0]) & (points[:, 2] < self.Z_RANGE[1])

        danger_points = points[in_x & in_y & in_z]

        # If more than 20 points are in the box, trigger stop
        if len(danger_points) > 20:
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False

    def move_forward(self, speed):
        if self.obstacle_detected:
            print("!!! CRASH PREVENTION ACTIVE: Stopping Robot !!!")
            self.client.Move(0, 0, 0)  # Force Stop
        else:
            print(f"Path Clear. Moving at {speed} m/s")
            self.client.Move(speed, 0, 0)


# --- Main Execution ---
shield = Go2SafetyShield()

try:
    while True:
        # Simulate your "External Code" trying to go forward
        shield.move_forward(speed=0.5)
        time.sleep(0.1)
except KeyboardInterrupt:
    shield.client.StandDown()
