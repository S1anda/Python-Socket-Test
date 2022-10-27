import socket

HOST = "127.0.0.1"
PORT = 10000

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
s.connect((HOST, PORT))

# Send data
s.sendall(b"Hello, world")

# Receive data
data = s.recv(1024)

# Print received data
print(f"Received {data!r}")
