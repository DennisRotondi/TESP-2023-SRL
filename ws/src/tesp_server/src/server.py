#!/usr/bin/env python
import rospy
import paramiko

from std_msgs.msg import String
 
def turn_left(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(50), SpeedPercent(-50))"')
    time.sleep(time)

def turn_right(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(-50), SpeedPercent(50))"')
    time.sleep(time)

def move_forward(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(50), SpeedPercent(50))"')
    time.sleep(time)

def move_backward(robot_connection, time = 1):
    robot_connection.exec_command('python3 -c "from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent; tank_drive = MoveTank(OUTPUT_A, OUTPUT_B); tank_drive.on(SpeedPercent(-50), SpeedPercent(-50))"')
    time.sleep(time)

def callback(data, robot_connection):
    if data.data == 'right':
        turn_right(robot_connection)
    elif data.data == 'left':
        turn_left(robot_connection)
    elif data.data == 'forward':
        move_forward(robot_connection)
    elif data.data == 'backward':
        move_backward(robot_connection)
    print(data.data)

def connect_to_robot(ip,username,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    return client
def disconnect_from_robot(robot_connection):
    robot_connection.close()

if __name__ == '__main__':
    rospy.init_node('server', anonymous=True)
    robot_connection_1 = connect_to_robot('10.240.20.66','robot','maker')
    # pub = rospy.Publisher('action_tesp', String, queue_size=10)
    rospy.Subscriber("action_tesp", String, callback(robot_connection_1))
    rospy.spin()
