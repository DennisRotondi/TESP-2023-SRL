#!/usr/bin/env python
import rospy
import paramiko
import time
import re

from std_msgs.msg import String

def connect_to_robot(ip,username,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    rospy.loginfo(rospy.get_caller_id() + "Client: %s", client)
    return client

robot_ip = '10.42.0.252'
# robot_ip = '10.240.20.63'
# robot_ip = '192.168.10.103'
robot_connection_1 = connect_to_robot(robot_ip,'robot','maker')
 
def turn_left(robot_connection, timer = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(50), SpeedPercent(-50));"')
    time.sleep(timer)
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(0), SpeedPercent(0));"')

def turn_right(robot_connection, timer = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(-50), SpeedPercent(50));"')
    time.sleep(timer)
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(0), SpeedPercent(0));"')

def move_forward(robot_connection, timer = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(50), SpeedPercent(50));"')
    time.sleep(timer)
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(0), SpeedPercent(0));"')

def move_backward(robot_connection, timer = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(-50), SpeedPercent(-50));"')
    time.sleep(timer)
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(0), SpeedPercent(0));"')

import re

def callback(data):
    message = data.data
    time_match = re.match(r'(\w+)(\d+)', message)
    
    if time_match:
        direction, time_ms = time_match.groups()
        time_s = int(time_ms) / 1000.0
    else:
        direction = message
        time_s = 0.0

    if direction == 'right':
        turn_right(robot_connection_1)
    elif direction == 'left':
        turn_left(robot_connection_1)
    elif direction == 'up':
        move_forward(robot_connection_1)
    elif direction == 'down':
        move_backward(robot_connection_1)

    if time_s > 0:
        delay_ms(robot_connection_1, time_s)

    print(message)



def disconnect_from_robot(robot_connection):
    robot_connection.close()

if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    # pub = rospy.Publisher('action_tesp', String, queue_size=10)
    rospy.Subscriber("action_tesp", String, callback)
    rospy.spin()
