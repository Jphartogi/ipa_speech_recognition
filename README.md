Speech_recognition using Respeaker in ROS platform
=============



respeaker mic array
======================
A ROS Package for Respeaker Mic Array
## Supported Devices

- [Respeaker Mic Array v2.0](http://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/)

    ![Respeaker Mic Array v2.0](https://github.com/SeeedDocument/ReSpeaker_Mic_Array_V2/raw/master/img/Hardware%20Overview.png)

## Preparation

1. Install this package

    Assumed that ROS is properly installed.

    You can install this package via `apt-get`.

    ```bash
    sudo apt-get install ros-$ROS_DISTRO-respeaker-ros
    ```

    Or you can also build from the source.

    ```bash
    mkdir -p ~/catkin_ws/src && ~/catkin_ws/src
    git clone https://github.com/jsk-ros-pkg/jsk_3rdparty.git
    cd ~/catkin_ws
    source /opt/ros/kinetic/setup.bash
    rosdep install --from-paths src -i -r -n -y
    catkin config --init
    catkin build respeaker_ros
    source ~/catkin_ws/devel/setup.bash
    ```

1. Register respeaker udev rules

    Normally, we cannot access USB device without permission from user space.
    Using `udev`, we can give the right permission on only respeaker device automatically.

    Please run the command as followings to install setting file:

    ```bash
    roscd respeaker_ros
    sudo cp -f $(rospack find respeaker_ros)/config/60-respeaker.rules /etc/udev/rules.d/60-respeaker.rules
    sudo systemctl restart udev
    ```

    And then re-connect the device.

1. Update firmware

    ```bash
    git clone https://github.com/respeaker/usb_4_mic_array.git
    cd usb_4_mic_array
    sudo python dfu.py --download 6_channels_firmware.bin  # The 6 channels version 
    ```

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
