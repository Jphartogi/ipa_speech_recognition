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

class speech_recognition:
    def __init__(self):
        self.audio_data = []
        self.is_speaking = False
        self.speech_on = False
        self.status = False
        self.engine = pyttsx3.init(driverName='espeak')
        self.speech_recognized = False
        self.sub = rospy.Subscriber("/is_speeching",Bool,self.statusCallback)
        # self.sub = rospy.Subscriber("/audio",AudioData,self.audioCallback)
     
    def statusCallback(self,msg):
        self.status = msg.data
        if self.status:
            while True:
                self.is_speaking = True
                tts = gTTS(text='Please say something', lang='en')
                tts.save("say_something.mp3")
                os.system("mpg321 say_something.mp3")
                # self.engine.say(" Please say something ")
                # self.engine.runAndWait() 
                self.recognize_speech()
            else:
                self.is_speaking = False
                
    def recognize_speech(self):
        client = SpeechRecognitionClient()
        result = client.recognize()  
        real_result = result.transcript
        for name in real_result:
            print(name)
            
            name = name.lower()
            if (name.find('i',0,2) != -1): 
                name = name.replace('i','You',1)
            else: 
                pass

            if (name.find('you',0,2) != -1): 
                name = name.replace('you','I',1)
            else: 
                name = name.replace('you','me',1)

            name = name.replace("your","My")
            

            name = name.replace("my", "Your",1)
            name = name.replace("am","are",1)

            if name == "shut up" or name == "Shut up" or name == "SHUT UP":
                tts = gTTS(text="Goodbye, see you later ", lang='en')
                tts.save("byebye.mp3")
                os.system("mpg321 byebye.mp3")
                # self.engine.say("I am truly sorry for making you bored, bye for now, see you later ")
                # self.engine.runAndWait() 
                rospy.signal_shutdown("User is bored")
            else:
                print "result after processing :",name
                tts = gTTS(text="I understand that you said "+str(name), lang='en')
                tts.save("response.mp3")
                os.system("mpg321 response.mp3")
                # self.engine.say("I just understand you are saying "+str(name)+", right?")
                # self.engine.runAndWait()
            
        

if __name__ == "__main__":
    rospy.init_node("speech_recognition_client")
    speech = speech_recognition()
    rospy.spin()


