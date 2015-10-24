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

def test(alo):
	ctr = str(alo)[6:]
	if ctr == '1':
		print 'ok'



if __name__ == '__main__':
	rospy.init_node('test', anonymous=True)
	rospy.Subscriber('vc', String, test)
	rospy.spin()
