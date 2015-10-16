#!/usr/bin/env python

"""
  Based on voice_nav.py.

"""

import roslib; roslib.load_manifest('rfh_speech')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign

class voice_cmd:
    def __init__(self):
        self.verbs = ['go','find','get']
        self.places = ['kitchen','bedroom','living','bathroom','hall']
        self.questions = ['what time is it']
        self.people = ['joseph','mary', 'john']
        #rospy.on_shutdown(self.cleanup)
        self.rate = rospy.get_param("~rate", 5)
        r = rospy.Rate(self.rate)
        self.paused = False
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('/recognizer/output', String, self.speechcommands)
    

	rospy.loginfo("Ready to receive voice commands")


    def speechcommands(self, msg): 
        speech = msg.data
        
        #Separating the words
        
        words = speech.split()
        print words

	#Creating lists to store the parsed information

        wverb = []
        wplace = []
        wquestion = []
        wpeople = []
        pverb =[]
        pquestion =[]
        cquestion = []

        #Parsing the sentence
        
        n = len(words)

        for y in range(0,n):
            for x in range(0,49): 
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
                if (len(self.people)-1) >= x :
                    if self.people[x] in words[y] :
                        wpeople.append(self.people[x])

        lenght_questions = len(self.questions)

        for z in range(0, (lenght_questions)) :
            if speech.find(self.questions[z]) >= 0 :
                cquestion.append(self.questions[z])
                pquestion.append(len(cquestion))

        print 'actions: ', wverb, ', positions : ', wplace, ', people: ', wpeople,', questions: ', cquestion
        rospy.loginfo("Command: " + str(speech))
        
if __name__=="__main__":
    rospy.init_node('voice_nav')
    voice_cmd()
    rospy.spin() 
