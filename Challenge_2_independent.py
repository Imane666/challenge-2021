#!/usr/bin/env python3
# BEGIN ALL
import rospy     
from geometry_msgs.msg import Twist
from sensor_msgs.msg import  LaserScan
from std_msgs.msg import Bool
import numpy as np
from Corridor import Corridor
   


class Challenge_2(object):
  def __init__(self):
    self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)  #velocities are published on the topic /cmd_vel_pub
    self.scan_sub = rospy.Subscriber('scan', LaserScan, self.challenge_2)  
    self.corridor = Corridor()                                           #use the class corridor (to follow the wall and finish challenge 2)
    self.twist = Twist() 

    
  def challenge_2(self, msg):
    print("challenge_2")
    self.twist.linear.x = 0.04                  #initial velocities   
    self.cmd_vel_pub.publish(self.twist)

    if self.corridor.mvt_1 == True:               #go forward if nothing detected
    	self.twist.linear.x = 0.04
    	self.twist.angular.z = 0.0
    	self.cmd_vel_pub.publish(self.twist)
    
    if self.corridor.mvt_l == True:               #go left if and obstacle is detected 
    	self.twist.linear.x = 0.04
    	self.twist.angular.z = -0.3
    	self.cmd_vel_pub.publish(self.twist)

    if self.corridor.mvt_r == True:               #go right if and obstacle is detected 
    	self.twist.linear.x = 0.04
    	self.twist.angular.z = 0.3
    	self.cmd_vel_pub.publish(self.twist)
	

rospy.init_node('Challenge_2')                        # run the node by creating an object challenge 2
Challenge_2 = Challenge_2()   
rospy.spin()   
