#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import  LaserScan
from std_msgs.msg import Bool
import numpy as np


class Random_obstacles:
    def __init__(self): 	
    	self.scan_sub = rospy.Subscriber('scan', LaserScan, self.clbk_laser) #subscriber to the scan topic, to estimate distances from the diffrent obstacles that are placed randomly
    	self.mvt_1 = Bool()
    	self.mvt_l = Bool()
    	self.mvt_r = Bool()
	
    def clbk_laser(self, msg):
    	vec_1 = []   #left distances vector
    	vec_2 = []   #right distances vector
    	
    	#each 2 degrees angle, we estimate the mean distance mesured by the lidar sensor, and then store them in a vector

    	for i in range(1,60,2): #60 degrees, for each side
    		vec_1.append(np.mean(msg.ranges[i:2*i])) #left
    		vec_2.append(np.mean(msg.ranges[360-2*i:360-i])) #right
    		
    	if min(vec_1)>0.35 and min(vec_2)>0.35:  
    		self.mvt_1 = True                #if the minmum distaces of both of the vectors are larger then 0.35 the boolen mvt_1 will be take the TRUE STATE
    	else:
    		self.mvt_1 = False
    		
    	if min(vec_1)<=0.35 :
    		self.mvt_l = True                #if the minmum distaces of the vector mesuring the left distances is smaller then 0.35 the boolen mvt_l will be take the TRUE STATE
    	else:
    		self.mvt_l = False
    		
    	if min(vec_2)<=0.35:                     
    		self.mvt_r = True                #if the minmum distaces of the vector mesuring the right distances is smaller then 0.35 the boolen mvt_r will be take the TRUE STATE
    	else:
    		self.mvt_r = False

