import socket
import json
import random
import time

CLIENT_PORT = 68
SERVER_IP = "127.0.0.1"
SERVER_PORT = 67
BUFFER_SIZE = 1024

# Generate random MAC for demonstration
def random_mac():
    return "AA:BB:CC:DD:EE:{:02X}".format(random.randint(1, 99))

client_mac = random_mac()

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
        print("\n✅ BOOTREPLY received:")
        print(f"Assigned IP   : {reply['ip']}")
        print(f"Gateway       : {reply['gateway']}")
        print(f"Boot File     : {reply['bootfile']}")
    else:
        print("\n❌ Server reply:", reply["message"])

except socket.timeout:
    print("\n❌ No BOOTREPLY received (timeout).")

finally:
    client.close()
