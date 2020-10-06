#!/usr/bin/env python
import rospy
import signal
import json
import datetime
import time
from std_msgs.msg import String
from geometry_msgs.msg import Transform

filename = input("enter desired filename. ")

date = datetime.date.today()
clockstamp = datetime.datetime.now().time()
exacttime_start = time.time()

data = {
    "test id": 
	{
	"name": filename,
	"date": int(date.strftime("%Y%m%d")),
	"start time": float(clockstamp.strftime("%H%M%S.%f"))
	},
    "vicon":
	{
	"translation": 
	    {
	    "x": [],
	    "y": [],
	    "z": []
	    },
	"rotation":
	    {
	    "x": [],
	    "y": [],
	    "z": [],
	    "w": []
	    }
	}
}

def keyboardInterruptHandler(signal,frame):
    print("interrupted")
    exacttime_end = time.time()
    data["test id"]["duration"] = exacttime_end - exacttime_start

    with open(filename + ".json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    exit(0)

signal.signal(signal.SIGINT,keyboardInterruptHandler)

def callback(sensor_data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", sensor_data.translation.x)
    data["vicon"]["translation"]["x"].append(sensor_data.translation.x)
    data["vicon"]["translation"]["y"].append(sensor_data.translation.y)
    data["vicon"]["translation"]["z"].append(sensor_data.translation.z)
    data["vicon"]["rotation"]["x"].append(sensor_data.rotation.x)
    data["vicon"]["rotation"]["y"].append(sensor_data.rotation.y)
    data["vicon"]["rotation"]["z"].append(sensor_data.rotation.z)
    data["vicon"]["rotation"]["w"].append(sensor_data.rotation.w)

def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/position_data", Transform, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
