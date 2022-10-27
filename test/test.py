# A test to start the Server and Client
# Uses a subprocess to start
import subprocess
import time

# Start the Server as a subprocess
print("Starting server")
server = subprocess.Popen(["python", "src/Server.py"])

# Start a Client as a subprocess
print("Starting client")
client = subprocess.Popen(["python", "src/Client.py"])
