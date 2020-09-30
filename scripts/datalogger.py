#!/usr/bin/env python
import rospy
import signal
from std_msgs.msg import String

filename = input("enter filename enclosed in quotation marks ")
print("file created \n")
file = open(filename,"w")
line = "Hello ROS world \n"
file.write(line)

def keyboardInterruptHandler(signal,frame):
    file.close()
    print("interrupted")
    exit(0)

signal.signal(signal.SIGINT,keyboardInterruptHandler)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    file.write(data.data + " %s" % rospy.get_time() + "\n")

def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/vicon/TestObj/TestObj", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
