import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyttsx3
from playsound import playsound
from ament_index_python.packages import get_package_share_directory
import re

from pocketsphinx_ros.srv import SpeechRecog



##########################
# The service can be requested for returned speech
##########################



class PocketSphinx(Node):
    def __init__(self):
        super().__init__('pocketsphinx_speech_service_node')
        self.topic_recog='/speech_recognition/output'
        self.srv = self.create_service(SpeechRecog, 'speech_recog_output',self.recog_callback)
    def publish(self,msg):
        _msg=String()
        _msg.data=str(msg)
        self.pub_recognizer.publish(_msg)
    def start_recognition(self):
        for phrase in LiveSpeech():
            #self.publish(phrase)
            phrase=str(phrase)
            self.publish(self.map_phrase(phrase))
            self.get_logger().info(f'Publishing "{phrase}" to {self.topic_recog}')
            break
    def map_phrase(self,s):
        s=re.sub("want a one","water",s)
        s=re.sub('why that is',"water please",s)
        s=re.sub('wanda',"water",s)
        s=re.sub('one of these','water please',s)
        s=re.sub('what the us','water please',s)
        s=re.sub('watch the new','water please',s)
        s=re.sub('what a', 'water', s)
        s=re.sub('what a reason', 'water please', s)
        return s

def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    print("Ready to listen")
    try:
        while True:
            node.start_recognition()
    except KeyboardInterrupt as e:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()