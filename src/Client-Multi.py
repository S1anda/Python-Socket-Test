import socket
import sys
import selectors
import types

# Create selector
sel = selectors.DefaultSelector()

# Create messages to send
messages = [b"Hello", b"Goodbye"]

# Create function for starting connections
def start_connections(host, port, num_conns):
    server_addr = (host, port)
    # Loop for multiple connections
    for i in range(0, num_conns):
        connectionID = i + 1
        print(f"Starting connection {connectionID} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connectionID,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)

# Create function for handling connections
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        # Close connection if no data or all data received
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

# Connect the socket to the port where the server is listening
host, port, num_conns = sys.argv[1:4]

# Start connections
start_connections(host, int(port), int(num_conns))

# After a connections are accepted, receive data
try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
            if not sel.get_map():
                break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
