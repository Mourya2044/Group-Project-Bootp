import socket
import json
import time

SERVER_IP = "0.0.0.0"
SERVER_PORT = 67
BUFFER_SIZE = 1024

# Dynamic IP Pool
ip_pool = [f"192.168.1.{i}" for i in range(10, 51)]  # 192.168.1.10–50
leased = {}  # MAC -> IP mapping
gateway = "192.168.1.1"
bootfile = "netboot.img"

def assign_ip(mac):
    # If MAC already has a lease
    if mac in leased:
        return leased[mac]
    # If IPs available, assign one
    if ip_pool:
        new_ip = ip_pool.pop(0)
        leased[mac] = new_ip
        return new_ip
    # Pool exhausted
    return None

# Create UDP Socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f"[BOOTP SERVER] Listening on UDP port {SERVER_PORT}...")

while True:
    data, addr = server.recvfrom(BUFFER_SIZE)
    message = json.loads(data.decode())
    mac = message.get("mac")

    print(f"\n[REQUEST] From {mac} ({addr})")

    assigned_ip = assign_ip(mac)
    if assigned_ip:
        reply = {
            "message": "BOOTREPLY",
            "ip": assigned_ip,
            "gateway": gateway,
            "bootfile": bootfile
        }
        print(f"[ASSIGNED] {mac} → {assigned_ip}")
    else:
        reply = {"message": "No IP available"}

    server.sendto(json.dumps(reply).encode(), (addr[0], 68))
    print(f"[REPLY SENT] To {addr[0]}:68")
