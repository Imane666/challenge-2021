#!/usr/bin/env python3
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
#from sensor_msgs.msg import CompressedImage  #simulation REELE
from sensor_msgs.msg import Image             #simulation GAZEBO         
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
import numpy as np
from Random_Obstacles import Random_obstacles
       
class Challenge_3(object):
  def __init__(self):     
    self.bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)
    #self.image_sub = rospy.Subscriber('/raspicam_node/image/compressed',CompressedImage, self.challenge)      #subscribe to the topic of camera to visualize the enviroment (simulation REELE) 
    self.image_sub = rospy.Subscriber('/camera/image',Image, self.challenge_3)                                 #subscribe to the topic of camera to visualize the enviroment (simulation GAZEBO)
    self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)                                        #velocities are published on the topic /cmd_vel_pub
    self.twist = Twist()         
    self.random_obstacles = Random_obstacles()                                                                 #use the class random obstacles (for the crowded area)
    

  def challenge_3(self, msg):
    
    #Image processing, 
    #image = self.bridge.compressed_imgmsg_to_cv2(msg,desired_encoding='bgr8')                                 #simulation REELE
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')                                             #simulation GAZEBO
    h, w, d = image.shape
    c = w
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    #YELLOW detection
    lower_yellow = numpy.array([ 10,  10, 10])
    upper_yellow = numpy.array([255, 255, 190])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    M_Y = cv2.moments(mask_yellow)
    self.twist.linear.x = 0.05                        #initial velocities         
    self.twist.angular.z = 0.0
    self.cmd_vel_pub.publish(self.twist)
                            
    if M_Y['m00']> 0:                                 #during the challenge 3 the yellow color is followed so that the robot will keep going forward while keeping avoiding the obstacles
    	cx_y = int(M_Y['m10']/M_Y['m00'])             #gravity center of the orange object detected
    	cy_y = int(M_Y['m01']/M_Y['m00'])
    	cv2.circle(image, (cx_y, cy_y), 20, (0,255,255), -1)  #displaying the center of gravity
    	err_y = cx_y - c/2                            #the diffrence between the x coordonate of the center of gravity of the object detected and the x coordonate of the center of the image
    		
    	self.twist.linear.x = 0.1                     #publishing the diffrent velocities so that the robot keeps following the yellow color when detected
    	self.twist.angular.z = -float(err_y)/200
    	self.cmd_vel_pub.publish(self.twist)
		
    #avoid the obstacles put randomly
    if self.random_obstacles.mvt_l == True:               #go left if and obstacle is detected, the velocities are published so that the robot avoid the present obstacle
    	self.twist.linear.x = 0.04                    
    	self.twist.angular.z = -0.5
    	self.cmd_vel_pub.publish(self.twist)
    		
    		   			
    if self.random_obstacles.mvt_r == True:               #go right if and obstacle is detected, the velocities are published so that the robot avoid the present obstacle
    	self.twist.linear.x = 0.04
    	self.twist.angular.z = 0.5
    	self.cmd_vel_pub.publish(self.twist)
    

    cv2.imshow("window", image)                           #displaying the viewed enviroment 
    cv2.waitKey(1)                                        #frequency of displaying
    		
    	
rospy.init_node('Challenge_3')                                # run the node by creating an object challenge 3
Challenge_3 = Challenge_3()   
rospy.spin()                                                
