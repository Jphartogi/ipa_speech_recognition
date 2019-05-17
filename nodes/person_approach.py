#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import numpy as np
import tf
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool,SetBoolRequest,SetBoolResponse
from std_srvs.srv import Trigger,TriggerRequest,TriggerResponse
import math

class person_approach:
    def __init__(self):
        self.sub                        = rospy.Subscriber('sound_localization',PoseStamped,self.poseCallback)
        self.from_frame                 = '/person_orientation'
        self.to_frame                   = '/base_link'
        self.listener                   = tf.TransformListener()
        self.person_orientation         = []
        self.robot_person_orientation   = []
        self.twist_pub                  = rospy.Publisher('cmd_vel',Twist,queue_size=10)
        self.orientation_fixed          = False
        self.service                    = rospy.Service('approach', SetBool, self.moveCloser)
        self.approach_now               = False

    def moveCloser(self,req):

        if req.data:
            self.approach_now = True
            self.orientation_fixed = False
            self.update_robot_pose()
            return SetBoolResponse(True,"Service is successfully called")
           
        else:
            self.approach_now = False
            return SetBoolResponse(False,"Service is not successfully called")

        

    def poseCallback(self,msg):
    #     detected_orientation = msg.pose.orientation
    #     (roll, pitch, yaw) = euler_from_quaternion ([detected_orientation.x,detected_orientation.y,detected_orientation.z,detected_orientation.w])
    #     self.person_orientation = [roll,pitch,yaw]
    #     self.update_robot_pose(self.person_orientation)

        # just to call the update_robot_pose and make sure that the sound localization topic is already up
        # self.update_robot_pose()
        pass

    def update_robot_pose(self):
        
        try:
            time = rospy.Time.now()
            # self.listener.waitForTransform(self.from_frame, self.to_frame, time, rospy.Duration(0.5))
            # (trans,rot) = self.listener.lookupTransform(self.from_frame, self.to_frame, time)
            (trans,rot) = self.listener.lookupTransform('/person_orientation', '/map', rospy.Time(0))
            print rot
            self.trans = trans
            self.rot = rot
            (roll, pitch, yaw) = euler_from_quaternion ([self.rot[0],self.rot[1],self.rot[2],self.rot[3]])
            # in this phase, the difference between the orientation detected from the respeaker
            # and the orientation of the robot is obtained
            
            self.robot_person_orientation = [roll,pitch,yaw]
            # print " apa sih valuenya orientation robot ", self.robot_person_orientation

        except (tf.Exception, tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
            rospy.logdebug("Unable to update robot pose: %s" %str(e))
            return
        
        except rospy.ROSException:
            rospy.logerr("The current service never showed up!")
        except rospy.ServiceException as e:
            rospy.logerr("Service call to set_current failed: %s" % (e))
        except:
            rospy.logwarn("something went wrong while call to set_current service")
        
        # service need to be called first, then can approach 
        if self.approach_now:
            self.approach(self.robot_person_orientation)

    def approach(self,orientation):
        #compare the orientation, mostly only the yaw matters because it is in 2D space
        twist = Twist()
       
        yaw_person = orientation[2] 
        if yaw_person > 0:
            yaw_person = yaw_person * 180.0 / math.pi
        else:
            yaw_person = 360.0 - abs((yaw_person * 180 / math.pi))

        print "yawnya person",yaw_person
        while not self.orientation_fixed:
            twist.linear.x = 0        
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0
            

            (trans,rot) = self.listener.lookupTransform('/base_link', '/map', rospy.Time(0))
            (roll_robot, pitch_robot, yaw_robot) = euler_from_quaternion ([rot[0],rot[1],rot[2],rot[3]])

            # convert the yaw to be in degree! and fixed the situation where if degree > 180, it becomes - 180 and go down
            
            if yaw_robot > 0:
                yaw_robot = yaw_robot * 180.0 / math.pi
            else:
                yaw_robot = 360.0 - abs((yaw_robot * 180 / math.pi))
            
            print "yawnya person",yaw_person
            print "yawnya robot ",yaw_robot
            yaw = abs(yaw_robot - yaw_person)
           
            print "yaw total ",yaw

            if 1 > yaw:
                twist.angular.z = 0.00
                rospy.loginfo("orientation is now the same")
                self.twist_pub.publish(twist)
                self.orientation_fixed = True
                break
            else:

                if yaw_robot > yaw_person:
                    if yaw < 15:
                        twist.angular.z = 0.04
                        self.twist_pub.publish(twist)
                    else:
                        twist.angular.z = 0.2
                        self.twist_pub.publish(twist)
                
                else:
                    if yaw < 15:
                        twist.angular.z = -0.04
                        self.twist_pub.publish(twist)
                    else:
                        twist.angular.z = -0.2
                        self.twist_pub.publish(twist)
                
                   
        if self.orientation_fixed:
            #call service to move forward
            rospy.wait_for_service('move_forward')
            try:
                move_forward = rospy.ServiceProxy('move_forward',Trigger)
                resp = move_forward()
               
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
          
            
if __name__ == '__main__':
    rospy.init_node('person_approach')
    rospy.loginfo("person approach node starting")
    person_approach = person_approach()
    rospy.spin()