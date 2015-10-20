#!/usr/bin/env python
import roslib; roslib.load_manifest('rfh_speech')
import sys
import rospy
from std_msgs.msg import String

from sound_play.libsoundplay import SoundClient


class voice_play:
	def __init__(self):
		self.voice = rospy.get_param("~voice", "voice_cmu_us_clb_arctic_clunits")
		self.wavepath = rospy.get_param("~wavepath", "")

		self.sound_handle = SoundClient()

		rospy.sleep(1)
		rospy.loginfo("Say node ready to play...")

		rospy.Subscriber('speech', String, self.talkback)

	def talkback(self, msg):
		rospy.loginfo(msg.data)
		self.sound_handle.stopAll()
		rospy.sleep(1)
		self.sound_handle.playWave(self.wavepath + "R2D2a.wav")
		rospy.sleep(1)
		self.sound_handle.say(msg.data, self.voice)

def main(args):
	vp = voice_play()
	rospy.init_node('voice_play', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)