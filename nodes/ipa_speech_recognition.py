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
from std_srvs.srv import SetBool,SetBoolRequest,SetBoolResponse
        
    
class speech_recognition:
    def __init__(self):
        self.is_speaking = False
        self.speech_on = False
        self.status = False
        self.engine = pyttsx3.init(driverName='espeak')
        self.speech_successfull = False
        self.authorized = False
        
        self.sub = rospy.Subscriber("/is_speeching",Bool,self.statusCallback)
        # self.sub = rospy.Subscriber("/audio",AudioData,self.audioCallback)
        self.audio_data = []
        self.approach = False
        
    
    def statusCallback(self,msg):
        
        self.status = msg.data
        self.speech_successfull = False
        while not self.speech_successfull:
            self.is_speaking = True
            self.speak(" please say i am here")
            result1 = self.listen()
            for name in result1:
                print(name)
                print "result is :",name
                
                if name.find('closer') != -1 or name.find('come') != -1 or name.find('here') != -1: 
                    # self.speak("Alright then i will adjust my orientation first")
                    self.callService(True)
                    self.approach = True
                    
                else: 
                    self.approach = False
                   
    def speak(self,msg):
        # tts = gTTS(text=msg, lang='en')
        # tts.save("say_something.mp3")
        # os.system("mpg321 say_something.mp3")
        self.engine.say(msg)
        self.engine.runAndWait() 
        
    def listen(self):
        client = SpeechRecognitionClient()
        result = client.recognize() 
        real_result = result.transcript 
        return real_result

    def callService(self,status):
        
        if status:
            rospy.wait_for_service('approach')
            try:
                approaching_service = rospy.ServiceProxy('approach', SetBool)
                
                # SetBoolRequest(True)
                resp = approaching_service(status)
                
                print "Service is called! "
                return resp
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
        else:
            pass

            
if __name__ == "__main__":
    rospy.init_node("client_speech_recognizion")
    speech = speech_recognition()
    rospy.spin()

