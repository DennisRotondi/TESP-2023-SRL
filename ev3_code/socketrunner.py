import socket
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, MediumMotor, SpeedPercent
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
servo = MediumMotor(OUTPUT_C) # Assuming the servo motor is connected to port C

def handle_command(command):
    command = command.strip()
    if command == 'forward':
        tank_drive.on(SpeedPercent(50), SpeedPercent(50))
    elif command == 'backward':
        tank_drive.on(SpeedPercent(-50), SpeedPercent(-50))
    elif command == 'left':
        tank_drive.on(SpeedPercent(50), SpeedPercent(-50))
    elif command == 'right':
        tank_drive.on(SpeedPercent(-50), SpeedPercent(50))
    elif command == 'stop':
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    elif command.startswith('servo'): # Handle servo commands
        degrees = int(command[5:])
        servo.on_to_position(SpeedPercent(50), degrees)
        
    return str(servo.position) # return current position of the servo

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('10.42.0.252', 50001)
sock.bind(server_address)
sock.listen(1)

print("[EV3 TCP Socket] Socket Ready")

while True:
    connection, client_address = sock.accept()
    try:
        while True:  # Changed this to keep the connection open
            data = connection.recv(16)
            if not data:  # If data is empty, break the loop
                break
            print(data)
            servo_position = handle_command(data.decode('utf-8'))
            connection.sendall(servo_position.encode('utf-8')) # send servo position to the main laptop
    finally:
        connection.close()
