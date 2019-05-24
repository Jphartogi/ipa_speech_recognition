Speech_recognition using Respeaker in ROS platform
=============

respeaker mic array
======================
A ROS Package for Respeaker Mic Array

https://github.com/furushchev/respeaker_ros

ros_speech_recognition
======================

A ROS package for speech-to-text services.  
This package uses Python package [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition) as a backend.

## Preparation

1. Install this package ( this is a normal package, there is also this package included in the file, if you want to use the this installation mode, then just delete the package from this repo ros_speech_recognition. But then to change the speech recognition engine ( google, sphinx etc ) must be done manually

  ```bash
  sudo apt install ros-${ROS_DISTRO}-ros-speech-recognition
  ```
  
## How to run
1. Run the respeaker node, move_robot node, person_pose_publisher node , and person_approach.py
  ```bash
      roslaunch speech_recognition approach_person_sr.launch 
  ```

2. Then run the speech recognition , but in this tutorial, the ros_speech_recognition is build in an independent folder.
   ```bash
      for online version ( Google ) 
      roslaunch ros_speech_recognition speech_recognition_google.launch 
      for offline version ( Sphinx ) 
      roslaunch ros_speech_recognition speech_recognition_sphinx.launch 
  ```
  Then run the desired code
  ```bash
      rosrun speech_recognition test_online.py/test_offfline.py ( for testing the speech recognition in infinite loop of recognizing speech )
      rosrun speech_recognition ros_voice_control.py ( for a simple conversation which include some decision making )
      rosrun speech_recognition ipa_speech_recognition.py ( for sending a command in this case " come closer or come here " to send a robot to come near to you ) 
  ```

## Topics
### Subscribed

/scan [(sensor_msgs/LaserScan)](http://docs.ros.org/melodic/api/sensor_msgs/html/msg/LaserScan.html) 
Obstacle detection for stopping the robot
### Published
/cmd_vel [(geometry_msgs/Twist)](http://docs.ros.org/api/geometry_msgs/html/msg/Twist.html)  
Velocity commands for the mobile base.

## Services
for ipa_speech_recognition.py 
/approach : set True to give command to move_robot.py to approach a person according to its orientation from the TF published by the respeaker
/move_forward : trigger this service so the robot will move forward until some specific minimum distance.

## Parameter
|Parameter|Default|Definition|
|-----|----------|-------|
|min_dist|0.15|Min dist of an obstacle detected by the laser scanner|

## Author
used repo from https://github.com/jsk-ros-pkg/jsk_3rdparty


## License

[Apache License](LICENSE)
