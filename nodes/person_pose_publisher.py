#!/usr/bin/env python

import roslib
import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import tf

def poseCallback(msg):
    
    position = msg.pose.position
    orientation = msg.pose.orientation
    
    (roll, pitch, yaw) = euler_from_quaternion ([orientation.x,orientation.y,orientation.z,orientation.w])
    br = tf.TransformBroadcaster()
    print "orientation of person speaking is ",roll,pitch,yaw
    br.sendTransform((position.x, position.y, 0),
                    tf.transformations.quaternion_from_euler(roll, pitch, yaw),
                    rospy.Time.now(),
                    "person_orientation",
                    "base_link")


if __name__ == "__main__":
    rospy.init_node("person_pose_publisher")
    rospy.loginfo("person pose publisher node starting")
    pose_sub = rospy.Subscriber('sound_localization',PoseStamped,poseCallback)
    rospy.spin()

