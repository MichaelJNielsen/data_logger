#!/usr/bin/env python
import rospy
import signal
import json
import datetime
from std_msgs.msg import String
from geometry_msgs.msg import Transform

filename = input("enter filename enclosed in quotation marks. ")

date = datetime.date.today()
time = datetime.datetime.now().time()

data = {
    "test id": 
	{
	"name": filename,
	"date": int(date.strftime("%Y%m%d")),
	"start time": int(time.strftime("%H%M%S"))
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
    endtime = datetime.datetime.now().time()
    data["test id"]["duration"] = int(endtime.strftime("%H%M%S"))

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
