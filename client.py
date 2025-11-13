import socket
import json
import random
import time

CLIENT_PORT = 68
SERVER_IP = "127.0.0.1"
SERVER_PORT = 67
BUFFER_SIZE = 1024

# Generate random MAC for demonstration
def get_mac():
    addr = input("Enter a MAC address (format- AA:BB:CC:DD:EE:FF): ")
    return addr.strip()

client_mac = get_mac()

# Create UDP Socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("", CLIENT_PORT))
client.settimeout(5)

# Send BOOTREQUEST
request = json.dumps({"message": "BOOTREQUEST", "mac": client_mac})
client.sendto(request.encode(), (SERVER_IP, SERVER_PORT))
print(f"[BOOTP CLIENT] Sent BOOTREQUEST for MAC {client_mac}")

# Wait for BOOTREPLY
try:
    data, addr = client.recvfrom(BUFFER_SIZE)
    reply = json.loads(data.decode())

    if reply["message"] == "BOOTREPLY":
        print("\nBOOTREPLY received:")
        print(f"Assigned IP   : {reply['ip']}")
        print(f"Gateway       : {reply['gateway']}")
        print(f"Boot File     : {reply['bootfile']}")
    else:
        print("\nServer reply:", reply["message"])

except socket.timeout:
    print("\nNo BOOTREPLY received (timeout).")

finally:
    client.close()
