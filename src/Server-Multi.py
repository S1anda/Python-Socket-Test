import socket

HOST = "127.0.0.1"
PORT = 10000

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
s.bind((HOST, PORT))

# Listen for incoming connections
s.listen()

# Wait for a connection and store the connection and client address
conn, addr = s.accept()

# After a connection is accepted, print the client address
print(f"Connected by {addr}")
try:
    data = conn.recv(1024)
    if data:
        conn.sendall(data)
finally:
    conn.close()
