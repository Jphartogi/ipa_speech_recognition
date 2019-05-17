#!/usr/bin/env python

import pyaudio
import os
import speech_recognition as SR
import rospy
from ros_speech_recognition import SpeechRecognitionClient
from audio_common_msgs.msg import AudioData
from respeaker_ros.msg import AudioDataRespeaker
from speech_recognition_msgs.msg import SpeechRecognitionCandidates
from std_msgs.msg import Bool
import pyttsx3
from gtts import gTTS
import tf
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion, quaternion_from_euler

        
    
class speech_recognition:
    def __init__(self):
        self.is_speaking = False
        self.speech_on = False
        self.status = False
        self.engine = pyttsx3.init(driverName='espeak')
        self.speech_successfull = False
        self.authorized = False
        self.pose_sub = rospy.Subscriber('sound_localization',PoseStamped,self.poseCallback)
    
        self.sub = rospy.Subscriber("/is_speeching",Bool,self.statusCallback)
        # self.sub = rospy.Subscriber("/audio",AudioData,self.audioCallback)
        self.audio_data = []
        
    def poseCallback(self,msg):
        position = msg.pose.position
        orientation = msg.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion ([orientation.x,orientation.y,orientation.z,orientation.w])
        
        br = tf.TransformBroadcaster()
        br.sendTransform((position.x, position.y, 0),
                        tf.transformations.quaternion_from_euler(roll, pitch, yaw),
                        rospy.Time.now(),
                        "person_orientation",
                        "map")


    def statusCallback(self,msg):
        self.trial_count = 0
        self.status = msg.data
        self.speech_successfull = False
        while not self.speech_successfull:
            self.is_speaking = True
            self.speak("Hello my name is Mobika, You may speak something but wait, what my password?")
            result1 = self.listen()
            for name in result1:
                print(name)
                print "result is :",name
                if str(name) == "Joshua":
                    self.authorized = True
                    name = name.replace("I","You")
                    name = name.replace("am","are")
                    self.understanding()
                    self.decide()
                    self.authorized = False
                        
                else:
                    self.speak("That is a wrong password, you have 3 chances remaining")
                    while self.trial_count < 3 and not self.authorized:
                        
                        trial = self.listen()
                        
                        for name in trial:
                            
                            if str(name) == "Joshua":
                                self.authorized = True
                                name = name.replace("I","You")
                                name = name.replace("am","are")
                                self.understanding()
                                self.decide()
                            else:        
                                chances_left = 2 - self.trial_count
                                self.speak("You have  "+str(chances_left)+"chances remaining")
                                self.trial_count = self.trial_count + 1
                    if not self.authorized:   
                        self.speak("Get the fuck out, or i wiill call the police!")
            self.speech_successfull = True
            if self.speech_successfull:
                break

    def understanding(self):
        self.speak("Alright you may proceed, Please say something")
        result3 = self.listen()
        for input in result3:
            print(input)
            print "result is :",input 
            input = input.replace("I","You")
            input = input.replace("am","are")
            self.speak("I understand what you are saying, i am 100 percent sure you are saying "+str(input)+", right?")
        

    def decide(self):
        self.speak("please answer yes if i am right, or no if i am wrong")
        answer_raw = self.listen()
        
        for answer in answer_raw:
            print ("the answer is ",answer)
            if not answer == "yes" or answer == "YES" or answer == "Yes":
                self.speak("My apologizes because i am still learning, please repeat once more")
                result3 = self.listen()
                for input in result3:
                    print(input)
                    print "result is :",input 
                    input = input.replace("I","You")
                    input = input.replace("am","are")
                    self.speak("I understand what you are saying, i am 100 percent sure you are saying "+str(input)+", right?")
                    self.decide()
            else:
                self.speak("Alright i understand you, bye for now! Goodbye")
                rospy.signal_shutdown("Process has done successfully")

    def speak(self,msg):
        self.engine.say(msg)
        self.engine.runAndWait() 
        
    def listen(self):
        client = SpeechRecognitionClient()
        result = client.recognize() 
        real_result = result.transcript 
        return real_result



if __name__ == "__main__":
    rospy.init_node("client_speech_recognizion")
    speech = speech_recognition()
    rospy.spin()

