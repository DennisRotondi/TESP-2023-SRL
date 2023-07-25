#!/usr/bin/env python
import rospy
from std_msgs.msg import String
 
def callback(data):
    print(data.data)

if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    # pub = rospy.Publisher('action_tesp', String, queue_size=10)
    rospy.Subscriber("action_tesp", String, callback)
    rospy.spin()
