#!/usr/bin/env python
import rospy
import socket
import re
from std_msgs.msg import String, Int32
from sensor_msgs.msg import CompressedImage

def connect_to_robot(ip, port=50001):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    rospy.loginfo(rospy.get_caller_id() + "Connected to %s:%s", ip, port)
    return client

robot_ip = '10.42.0.252'
robot_connection_init = connect_to_robot(robot_ip)

def send_command(robot_connection, command):
    try:
        robot_connection.sendall(command.encode('utf-8'))
    except BrokenPipeError:
        print("Connection lost, reconnecting...")
        global robot_connection_init
        robot_connection_init = connect_to_robot(robot_ip, 50001)
        robot_connection_init.sendall(command.encode('utf-8'))

def callback(data):
    message = data.data
    send_command(robot_connection_init, message)

def callback_picture(data):
    ros_image_msg = rospy.wait_for_message('/camera/color/image_raw/compressed', CompressedImage)
    pub.publish(ros_image_msg)

def recv_servo_position(robot_connection):
    data = robot_connection.recv(1024) # get servo position from EV3
    if data:
        servo_pub.publish(int(data)) # publish servo position

if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    rospy.Subscriber("action_tesp", String, callback)
    pub = rospy.Publisher('/camera/rgb/image_raw_3', CompressedImage, queue_size=10)
    servo_pub = rospy.Publisher('/servo_position', Int32, queue_size=10) # publisher for servo position
    rospy.Timer(rospy.Duration(0.1), callback_picture)
    rospy.Timer(rospy.Duration(0.1), recv_servo_position)
    rospy.spin()
