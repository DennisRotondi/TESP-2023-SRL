#!/usr/bin/env python
import rospy
import paramiko

from std_msgs.msg import String

def connect_to_robot(ip,username,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    return client

robot_ip = '10.42.0.252'
robot_connection_1 = connect_to_robot(robot_ip,'robot','maker')

 
def turn_left(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(50), SpeedPercent(-50))"')

def turn_right(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(-50), SpeedPercent(50))"')

def move_forward(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(50), SpeedPercent(50))"')

def move_backward(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(-50), SpeedPercent(-50))"')

def callback(data):
    message = data.data
    #log message to ros console
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", message)
    print(message)
    if message == 'right':
        turn_right(robot_connection_1)
    elif message == 'left':
        turn_left(robot_connection_1)
    elif message == 'forward':
        move_forward(robot_connection_1)
    elif message == 'backward':
        move_backward(robot_connection_1)
    print(message)


def disconnect_from_robot(robot_connection):
    robot_connection.close()

if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    # pub = rospy.Publisher('action_tesp', String, queue_size=10)
    rospy.Subscriber("action_tesp", String, callback)
    rospy.spin()
