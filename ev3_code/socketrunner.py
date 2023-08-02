import socket
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

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
    finally:
        connection.close()
