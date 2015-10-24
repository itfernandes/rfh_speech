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
		global ct
		global word
		ct = 0
		word = 0
		self.verbs = ['go','find','get', 'follow']
		self.places = ['kitchen','bedroom','living','bathroom','hall']
		self.questions = ['time', 'capital', 'two plus two',
						  'symbol', 'where', 'square', 'state', 'elevator', 'redeemer',
			   			  'located', 'university','robocup league', ]
		self.people = ['joseph','mary', 'john']
		#rospy.on_shutdown(self.cleanup)
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
		global ct
		global word
		speech = msg.data
		sl = 'jude'
		if sl in speech:
			ct = 1
			word = word + 1
			#self.soundhandle.playWave(self.wavepath + "R2D2a.wav")
			rospy.sleep(0.02)
			if word == 1:
				self.soundhandle.say('i am here!', self.voice)
			elif word == 2:
				self.soundhandle.say('hello!', self.voice)
			elif word == 3:
				self.soundhandle.say('say!', self.voice)	
			elif word == 4:
				self.soundhandle.say('hi!', self.voice)	
			elif word >= 5:
				word = 1		



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
			
			if wquestion not in self.questions:
				self.soundhandle.say('Sorry, i did not under stand what you said, but i am beautiful', self.voice)
				rospy.sleep(5)
				self.soundhandle.say('please repeat your question', self.voice)
				rospy.sleep(3)		

			if 'follow' in wverb:
				alo = 1
				pub.publish(str(alo))
				ct = 0

			elif 'capital' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('brasi lia', self.voice)
				ct = 0
			
			elif 'two plus two' in cquestion:
				rospy.sleep(0.1)
				self.soundhandle.say('fawr', self.voice)
				ct = 0							
				
			elif 'symbol' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('five', self.voice)
				ct = 0
			
			elif 'where' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('Leipzig', self.voice)
				rospy.sleep(1.5)
				self.soundhandle.say('Germany', self.voice)
				ct = 0

			elif 'square' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('fawr', self.voice)
				ct = 0

			elif 'elevator' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('baea', self.voice)
				ct = 0

			elif 'redeemer' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('rio de ja nei ro', self.voice)
				ct = 0

			elif 'located' in wquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('mi nas j r eyes', self.voice)
				ct = 0

			elif 'university' in wquestion:
				rospy.sleep(0.02) 
				self.soundhandle.say('federal', self.voice)
				rospy.sleep(1)
				self.soundhandle.say('university of uber landia', self.voice)
				ct = 0 

			elif 'robocup league' in cquestion:
				rospy.sleep(0.02)
				self.soundhandle.say('at home', self.voice)
				ct = 0

def main(args):
	vc = voice_analyzer()
	rospy.init_node('voice_analyzer', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"

if __name__ == '__main__':
	pub = rospy.Publisher('followme', String, queue_size=10)
	main(sys.argv)


