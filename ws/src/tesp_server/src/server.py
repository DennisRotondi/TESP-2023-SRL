#!/usr/bin/env python
import rospy
import socket
import re
from std_msgs.msg import String

def connect_to_robot(ip, port=50001):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    rospy.loginfo(rospy.get_caller_id() + "Connected to %s:%s", ip, port)
    return client

robot_ip = '10.42.0.252'
robot_connection_1 = connect_to_robot(robot_ip)

def send_command(robot_connection, command):
    try:
        robot_connection.sendall(command.encode('utf-8'))
    except BrokenPipeError:
        print("Connection lost, reconnecting...")
        global robot_connection_1
        robot_connection_1 = connect_to_robot(robot_ip, 50001)
        robot_connection_1.sendall(command.encode('utf-8'))


def callback(data):
    message = data.data
    send_command(robot_connection_1, message)


if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    rospy.Subscriber("action_tesp", String, callback)
    rospy.spin()
