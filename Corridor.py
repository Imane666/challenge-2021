#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import  LaserScan
from std_msgs.msg import Bool
import numpy as np


class Corridor:
    def __init__(self): 
    	self.scan_sub = rospy.Subscriber('scan', LaserScan, self.clbk_laser)	
    	self.mvt_1 = Bool()
    	self.mvt_r = Bool()
    	self.mvt_l = Bool()
    	self.sw = Bool()
	
    def clbk_laser(self, msg):
    	vec_1 = []
    	vec_2 = []
    	a =min(msg.ranges[255:285])
    	b = min(msg.ranges[75:105])
    	for i in range(1,60,1):
    		vec_1.append(np.mean(msg.ranges[i:2*i]))
    		vec_2.append(np.mean(msg.ranges[360-2*i:360-i]))
    		
    	if min(vec_1) == min(vec_2):
    		self.mvt_1 = True
    	else:
    		self.mvt_1 = False
    	
    	if min(vec_1)<=min(vec_2) :
    		self.mvt_l = True
    	else:
    		self.mvt_l = False
    	
    	if min(vec_2)<=min(vec_1):
    		self.mvt_r = True
    	else:
    		self.mvt_r = False
    	
    	if a<=0.4 and b<=0.4:
    		self.sw = True
    	else:
    		self.sw = False

