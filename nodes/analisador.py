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
        global ct
        ct = 0
        self.verbs = ['go','find','get']
        self.places = ['kitchen','bedroom','living','bathroom','hall']
        self.questions = ['what time is it', 'what is the capital of brazil', 'how much is two plus two',
			  'how many rings have the symbol of the olympics', 'where will be the robocup two thousand and sixteen',
			  'how many sides have a square', 'in what state is the lacerda elevator', 'in what state is the christ redeemer',
			  'in what state is located the city spain sea', 'what is the name of this university',
			  'what is the name of this robocup league', 'where will be the robocup twenty sixteen'
			 ]
        self.people = ['joseph','mary', 'john']
        #rospy.on_shutdown(self.cleanup)
        #self.rate = rospy.get_param("~rate", 5)
        #r = rospy.Rate(self.rate)
        self.paused = False
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('/recognizer/output', String, self.speechcommands)
        rospy.Subscriber('/recognizer/output', String, self.startlistening)
        rospy.loginfo("Ready to receive voice commands")

    def startlistening(self, msg):
        global ct
        speech = msg.data
        sl = 'jude'
        if sl in speech:
            ct = 1
            print 'Yes'

    def speechcommands(self, msg):
        
        global ct 
        
        speech = msg.data

        if ct == 1:
            
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
            
            ct = 0
        

def main(args):
    vc = voice_cmd()
    rospy.init_node('voice_cmd', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)
