#!/usr/bin/env python

"""
  Based on voice_nav.py.
"""

import roslib; roslib.load_manifest('rfh_speech')
import rospy
import sys

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import copysign
from sound_play.libsoundplay import SoundClient

class voice_analyzer:
    def __init__(self):
        self.ct = 0
        self.word = 0
        self.node_init_pub = rospy.Publisher('node_initializer', String, queue_size=10)

        self.verbs = ['follow', 'go']
        self.places = ['kitchen', 'bedroom', 'living', 'bathroom', 'hall', 'ts', 'uh', 'um', 'ahn', 'sss']
        self.questions = ['time', 'brazil', 'two plus two', 'olympics', 'thousand',
                          'sides', 'state', 'elevator', 'christ', 'located',
                          'university', 'robocup league']
        self.people = ['joseph', 'mary', 'john']
        self.paused = False

        #initialize the soundplay service
        self.soundhandle = SoundClient()
        self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        self.sc_sub = rospy.Subscriber('/recognizer/output', String, self.speechcommands)
        self.sl_sub = rospy.Subscriber('/recognizer/output', String, self.startlistening)
        rospy.loginfo("Ready to receive voice commands")


    def startlistening(self, msg):
        speech = msg.data
        sl = 'jude'
        if sl in speech:
            self.ct = 1
            self.soundhandle.say('i am here', self.voice)
            rospy.sleep(0.02)


    def speechcommands(self, msg):
        speech = msg.data

        if self.ct == 1:
            
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

            for y in range(0,len(words)):
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

            #print self.questions
            #print cquestion
            #print wquestion
            #print cquestion in self.questions
            #print wquestion in self.questions
            #print speech 
            #print words


            if words:
                if not wquestion and not cquestion and not wverb:
                    self.soundhandle.say('Sorry, i did not under stand what you said', self.voice)
                    rospy.sleep(3.2)
                    self.soundhandle.say('please repeat your question', self.voice)
                    rospy.sleep(2)

                # if 'follow' in wverb:
                #     self.node_init_pub.publish('follow_person')

                if len(words) == 1 and words[0] == 'go':
                    self.node_init_pub.publish('find_and_go')

                if 'brazil' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('brasi lia', self.voice)
                
                elif 'two plus two' in cquestion:
                    rospy.sleep(0.1)
                    self.soundhandle.say('fawr', self.voice)

                elif 'olympics' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('five', self.voice)
                
                elif 'thousand' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('Leipzig', self.voice)
                    rospy.sleep(1.5)
                    self.soundhandle.say('Germany', self.voice)

                elif 'sides' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('fawr', self.voice)

                elif 'elevator' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('baea', self.voice)

                elif 'christ' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('rio de ja nei ro', self.voice)

                elif 'located' in wquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('mi nas j r eyes', self.voice)

                elif 'university' in wquestion:
                    rospy.sleep(0.02) 
                    self.soundhandle.say('federal', self.voice)
                    rospy.sleep(1)
                    self.soundhandle.say('university of uber landia', self.voice)

                elif 'robocup league' in cquestion:
                    rospy.sleep(0.02)
                    self.soundhandle.say('at home', self.voice)

                self.ct = 0


def main(args):
    voice_analyzer()
    rospy.init_node('voice_analyzer', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)


