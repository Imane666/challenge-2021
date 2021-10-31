#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import  LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import numpy as np


class Obstacle_1:
    def __init__(self):
    
    	#subscriber to the scan topic, to estimate distances from the moving wall that is present by the beginning of the challenge_1 
    	self.scan_sub = rospy.Subscriber('scan', LaserScan, self.clbk_laser) 
    	self.STOP = Bool()
    	
    def clbk_laser(self, msg):
    	front = (np.mean(msg.ranges[0:20])+np.mean(msg.ranges[340:360]))/2 # the mean distance is estimated from -20 and 20     	
    	if front <= 0.4:  # if the previous distance is inferior then 0.4 then the boolen STOP will take the True STATE
    		self.STOP = True
    	else:
    		self.STOP = False

	
