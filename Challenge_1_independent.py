#!/usr/bin/env python3
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
#from sensor_msgs.msg import CompressedImage  #simulation REELE
from sensor_msgs.msg import Image             #simulation GAZEBO         
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import numpy as np
from obstacle_1 import Obstacle_1 
from Random_Obstacles import Random_obstacles

       
class Challenge_1(object):
  def __init__(self):     
    self.bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)
    #self.image_sub = rospy.Subscriber('/raspicam_node/image/compressed',CompressedImage, self.challenge)    #simulation REELE
    self.image_sub = rospy.Subscriber('/camera/image',Image, self.challenge_1)                                 #simulation GAZEBO
    self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)               #publish the velocities according the received data,
    self.twist = Twist()                
    self.obstacle_mobile = Obstacle_1()                                               #use the class Obstacle_1 (line orange, moving wall)
    self.random_obstacles = Random_obstacles()                                        #use the class random_obstacles (line green, cylinder)
  
  
  def challenge_1(self, msg):
    #image = self.bridge.compressed_imgmsg_to_cv2(msg,desired_encoding='bgr8')                               #simulation REELE
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')                                           #simulation GAZEBO
    h, w, d = image.shape
    c = w
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #ORANGE detection
    lower_orange = numpy.array([5,50,50])
    upper_orange = numpy.array([15,255,255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    M_O = cv2.moments(mask_orange)
    #print("Orange = ", M_O['m00'])
    
    #GREEN detection
    lower_green = numpy.array([90, 100, 20])
    upper_green = numpy.array([120, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    M_G = cv2.moments(mask_green)

        
    if M_O['m00'] > 0 and M_O['m00'] > M_G['m00']:   #follow the orange line only and neglect green
    	print("challenge_1_o")
    	cx_o = int(M_O['m10']/M_O['m00'])                                       #gravity center of the orange object detected
    	cy_o = int(M_O['m01']/M_O['m00'])
    	err_o = cx_o - c/2                           #the diffrence between the x coordonate of the center of gravity of the object detected and the x coordonate of the center of the image
    	
    	if self.obstacle_mobile.STOP == False:                                  #if the previous condition is satisfied then an obstacle will be taken into account (moving one)
    			self.twist.linear.x = 0.1
    			self.twist.angular.z = -float(err_o)/200
    			self.cmd_vel_pub.publish(self.twist)
    	else:
    			self.twist.linear.x = 0.0                               #stop the robot when the obstacle is present
    			self.twist.angular.z = 0.0        
    			self.cmd_vel_pub.publish(self.twist)

    #GREEN LINE:
    
    if M_G['m00'] > 0 and M_G['m00'] > M_O['m00']:   #follow the green line only and neglect orange
    	print("challenge_1_g")
    	
        # follow only green and neglect orange to keep FOLLOWING THE GREEN LINE ONLY!
    	cx_g = int(M_G['m10']/M_G['m00'])
    	cy_g = int(M_G['m01']/M_G['m00'])
    	err_g = cx_g - c/2                      #the diffrence between the x coordonate of the center of gravity of the object detected and the x coordonate of the center of the image 
    	
    	
	#if the previous condition is satisfied then an obstacle will be taken into account (MOTIONLESS CYLINDER)
    	self.twist.linear.x = 0.05
    	self.twist.angular.z = -float(err_g)/200
    	self.cmd_vel_pub.publish(self.twist)

    	if self.random_obstacles.mvt_l == True:               #go left if the obstacle is detected 
    		self.twist.linear.x = 0.02
    		self.twist.angular.z = -0.5
    		self.cmd_vel_pub.publish(self.twist)
    		
    		
    	if self.random_obstacles.mvt_r == True:               #go right if the obstacle is detected 
    		self.twist.linear.x = 0.02
    		self.twist.angular.z = 0.5
    		self.cmd_vel_pub.publish(self.twist)
    		
    		
    if M_G['m00'] <= 0 and M_O['m00'] <= 0: # stop when no color is visualised
    	self.twist.linear.x = 0.0
    	self.twist.angular.z = 0.0
    	self.cmd_vel_pub.publish(self.twist)
    			
rospy.init_node('Challenge_1')                                # run the node by creating an object challenge 1
Challenge_1 = Challenge_1()   
rospy.spin()      
