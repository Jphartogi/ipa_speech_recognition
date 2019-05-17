#!/usr/bin/env python

from std_msgs.msg import String
import rospy, math, random
import numpy as np
from sensor_msgs.msg import LaserScan
from laser_geometry import LaserProjection 
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import Joy
from std_srvs.srv import Empty
from std_srvs.srv import Trigger


class robot_move():
	def __init__(self):

		# set service , publisher and subscriber
		self.f = rospy.Service('move_forward', Trigger, self.move_robot_forward)
		# self.b = rospy.Service('move_backward', Trigger, self.move_robot_backward)
		self.scan_sub =rospy.Subscriber('scan', LaserScan, self.callback_scan_forward)
		self.joy_sub = rospy.Subscriber("/joy", Joy, self.callback_joy)
		self.pub_ = rospy.Publisher('cmd_vel', Twist, queue_size=1000)
		self.msg = Twist()
		#set some parameter
		self.min_dist = float(rospy.get_param("~min_dist","0.15"))

		# set some variable
		self.forward = False
		self.backward = False
		self.counter_forward = 0
		self.camera_dist = 0.0
		self.camera_dist_old = 0.0
		self.goal_reached = False
		self.service_called = False
		self.sucess_forward = False
		self.sucess_backward = False

	def callback_scan_forward(self,scan):
		if self.service_called:
			rangelist = []
			for i, range in enumerate(scan.ranges):
					if range != np.inf:		# if we got a measurement
						y = math.cos( (scan.angle_increment * i))* range	# check if it is in potential colision area
						x = math.sin( (scan.angle_increment * i))* range
						if x > -0.28 and x < 0.28:
							rangelist.append(abs(y))	# create list of relevant x values
			
			if len(rangelist) > 0:
				
				dist = min(rangelist) - 0.18 # dist form base_link to robot cover in x
				print "nearest distance detected", dist
				
				# sort if the distance is close enough
				if dist < self.min_dist:
					dist = 0.0
					self.forward == False
					self.sucess_forward = True
					
				#print "min", dist, camera_dist

				if self.forward and not self.goal_reached:
					if dist != 0.0:
						self.msg.linear.x = 0.05
						self.msg.linear.y = 0.0
						self.msg.angular.z = 0.0
						if dist < 0.2 and dist > 0.1:
							self.msg.linear.x = 0.03

					self.pub_.publish(self.msg)
					print "move forward front", dist

				else:
					self.counter_forward +=1
					
					self.msg.linear.x = 0.00
					self.msg.linear.y = 0.0
					self.msg.angular.z = 0.0
					self.pub_.publish(self.msg)
					if self.counter_forward == 10:
						self.self.counter_forward = 0
						print "reached goal"
						self.sucess_forward = True
						self.forward = False
						self.goal_reached = True
		else:
			print "service not called!"
			pass

	# def callback_scan_backward(scan):
	# 	 self.backward
	# 	 camera_dist
	# 	 self.sucess_backward 
	# 	 camera_dist_old

	# 	if self.backward == True: #and camera_dist != camera_dist_old:
	# 		rangelist = []
			
	# 		for i, range in enumerate(scan.ranges):
	# 				if range != np.inf:		# if we got a measurement
	# 					y = math.cos( (scan.angle_increment * i))* range	# check if it is in potential colision area
	# 					x = math.sin( (scan.angle_increment * i))* range
	# 				if i > 300 or i < 60:
	# 					if x > -0.28 and x < 0.28:
	# 						rangelist.append(y)	# create list of relevant x values
	# 		if len(rangelist) > 0:
	# 			dist = min(rangelist) - 0.18 # dist form base_link to robot cover in x
	# 			if dist < 0.0:
	# 				dist = 0.0
	# 			#print "min", dist, camera_dist

	# 			self.pub_ = rospy.Publisher('cmd_veloa', Twist, queue_size=1000)

	# 			if camera_dist < 0.23:	# drive back until we ve space
	# 				self.msg.linear.x = - 0.06
	# 				self.msg.linear.y = 0.0
	# 				self.msg.angular.z = 0.0
	# 			if camera_dist < 0.1:
	# 				self.msg.linear.x = -0.04

	# 			if dist > 0.2:	# just if we have no obstacle backwards
	# 				self.pub_.publish(self.msg)
	# 				print "move backwards front",camera_dist, "back",  dist

	# 			else:
	# 				print "reached goal"
	# 				self.sucess_backward = True
	# 				self.backward = False
	# 		else:
	# 			print "empty data, stop"

	# 	camera_dist_old = camera_dist


	def callback_joy(self,joy): # using joy buttons to move
		
		if joy.buttons[3] == 1:
			print "move forward"
			self.forward = True

			
		if joy.buttons[0] == 1:
			print "move backward"
			self.backward = True

	def move_robot_forward(self,req):
		print "move forward"
		self.goal_reached = False
		self.forward = True
		self.service_called = True
		while not self.sucess_forward:
			pass
		self.sucess_forward = False
		self.service_called = False
		
		return [True, ""]



	def move_robot_backward(self,req):
		print "move_backward"
		self.backward = True
		while not self.sucess_backward:
			pass
		self.sucess_backward = False
		return [True, ""]



if __name__ == '__main__':
	rospy.init_node('listener', anonymous=True)
	rospy.loginfo("robot move node starting")
	robot_move = robot_move()
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()



