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
    robot_connection.sendall(command.encode('utf-8'))

def callback(data):
    message = data.data
    time_match = re.match(r'([a-zA-Z]+)(\d*)', message)
    
    if time_match:
        direction, time_ms = time_match.groups()
        time_s = int(time_ms) / 1000.0 if time_ms else 0
    else:
        direction = message
        time_s = 1

    print("Sending command: ",direction)
    send_command(robot_connection_1, direction)

    # print("Sleeping for: ",time_s," seconds")
    # rospy.sleep(time_s)

    # print("Stopping")
    # send_command(robot_connection_1, 'stop')

if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    rospy.Subscriber("action_tesp", String, callback)
    rospy.spin()
