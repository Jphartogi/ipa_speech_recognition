#!/usr/bin/env python

import numpy as np
import pyaudio
import rospy
from std_msgs.msg import String, Int32
from audio_common_msgs.msg import AudioData


class SpeechProcessor(object):
    def __init__(self):
        self.SOUND_DIRECTION = None

    def callback(self,data, stream):
        # data is of variable length (depends on length of sound event)
        data = np.reshape(data.data, (len(data.data)/6,6))
        # only grab channel 0 (preprocessed for ASR)
        ch0 = np.array(data[:, 0], dtype=np.int16)

        rospy.loginfo("Received sound event from angle {1} with duration of {0}s".format((len(ch0) / 16000.0), self.SOUND_DIRECTION))
        stream.start_stream()
        stream.write(ch0, num_frames = len(ch0))
        stream.stop_stream()
        self.SOUND_DIRECTION = None

    def callback_direction(self,data):
        if not self.SOUND_DIRECTION:
            self.SOUND_DIRECTION = data

    def callbackAudio(self,data, stream):
        # data is one chunk of size 1024*6channels samples
        data = np.reshape(data.data, (1024, 6))
        # only grab channel 0 (preprocessed for ASR)
        ch0 = np.array(data[:, 0], dtype=np.int16)
        stream.write(ch0, num_frames = len(ch0))

def listener():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024*CHANNELS

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    rospy.init_node('listener', anonymous=True)
    sp = SpeechProcessor()
    #rospy.Subscriber('speech_audio', AudioData, sp.callback, (stream))
    #rospy.Subscriber('sound_direction', Int32, sp.callback_direction)
    rospy.Subscriber("/audio", AudioData, sp.callbackAudio, (stream))

    rospy.spin()

if __name__ == '__main__':
    listener()
