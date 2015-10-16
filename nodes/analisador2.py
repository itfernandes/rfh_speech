#!/usr/bin/python

"""
  Based on voice_nav.py.
  
"""

import roslib; roslib.load_manifest('speech_rfpb')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign

class voice_cmd:
    def __init__(self):
        self.verbs = ['go','find','get']
        self.places = ['kitchen', 'bedroom', 'living', 'bathroom', 'hall']
        self.questions = ['what time is it']
	self.people = ['Joseph', 'Mary', 'John', 'Espermatoclarson']
        #rospy.on_shutdown(self.cleanup)
        self.rate = rospy.get_param("~rate", 5)
        r = rospy.Rate(self.rate)
        self.paused = False
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('/recognizer/output', String, self.speechcommands)
	
	#self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)

        rospy.loginfo("Ready to receive voice commands")


    def speechcommands(self, msg): 

        speech = msg.data
        
        #Separating the words
        
        words = speech.split()

        wverb = []
        wplace = []
        wquestion = []
        pverb =[]
        pquestion =[]
        cquestion = []

        #Parsing the sentence
        
        n = len(words)

        for y in range(0,(n-1)):
            print y
            for x in range(0,49):
                print x 
                if (len(self.verbs)-1) >= x :
                    if self.verbs[x] in words[y]:
                        wverb.append(self.verbs[x])
                        pverb.append(len(wverb))
                if (len(self.places)-1) >= x :
                    if self.places[x] in words[y] :
                        wplace.append(self.places[x])
                if (len(self.questions)-1) >= x :
                    if self.questions[x] in words[y] :
                        wquestion.append(self.questions[x])
		
        for z in range(0, (lenght_questions)):
	    print speech.find(self.questions[z])
            if speech.find(self.questions[z]) >= 0 :
                cquestion.append(self.questions[z])
                pquestion.append(len(cquestion))
	

        print 'actions: ', wverb, ', positions : ', wplace, ', questions: ', cquestion

        rospy.loginfo("Command: " + str(speech))
        
if __name__=="__main__":
    rospy.init_node('voice_nav')
    voice_cmd()
    rospy.spin() 
