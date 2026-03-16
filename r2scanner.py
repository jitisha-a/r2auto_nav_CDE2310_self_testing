# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy # ROS2 Python client library
from rclpy.node import Node # base class for ROS nodes
from rclpy.qos import qos_profile_sensor_data # QoS preset good for sensors
from sensor_msgs.msg import LaserScan # message type for LiDAR scans
import numpy as np # used to process arrays easily

class Scanner(Node):
    #Python OOP: Scanner is a class that inherits from Node. That means it becomes a ROS node.

    def __init__(self):
        super().__init__('scanner')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning. Just to keep the variable referenced (common ROS template style)

    #Creates a subscriber:
#type: LaserScan
#topic: 'scan' (that’s /scan)
#callback: self.listener_callback
#QoS: sensor QoS

    def listener_callback(self, msg): #msg is a LaserScan object
        # create numpy array
        laser_range = np.array(msg.ranges) # msg.ranges is a Python list of distances. Converts to numpy array. ####check ros workspace notes####
        # replace 0's with nan
        laser_range[laser_range==0] = np.nan
        # find index with minimum value - closest obstacle direction index
        lr2i = np.nanargmin(laser_range)

        # log the info
        self.get_logger().info('Shortest distance at %i degrees' % lr2i)


def main(args=None):
    rclpy.init(args=args)

    scanner = Scanner()

    rclpy.spin(scanner)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    scanner.destroy_node()
    rclpy.shutdown()

# rclpy.init() starts ROS communications.

# Create node.

# spin() keeps it alive, processing callbacks.

# Shutdown cleanly.


if __name__ == '__main__':
    main()
