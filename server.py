import socket
import json
import threading
import tkinter as tk
from tkinter import ttk

SERVER_IP = "0.0.0.0"
SERVER_PORT = 67
BUFFER_SIZE = 1024

ip_pool = [f"192.168.1.{i}" for i in range(10, 51)]
leased = {}
gateway = "192.168.1.1"
bootfile = "netboot.img"


def assign_ip(mac):
    if mac in leased:
        return leased[mac]
    if ip_pool:
        new_ip = ip_pool.pop(0)
        leased[mac] = new_ip
        return new_ip
    return None


def start_server(gui_table):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_IP, SERVER_PORT))
    print("[BOOTP SERVER] Listening on UDP port 67...")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        message = json.loads(data.decode())
        mac = message.get("mac")
        print(f"[REQUEST] From {mac}")

        assigned_ip = assign_ip(mac)

        if assigned_ip:
            reply = {
                "message": "BOOTREPLY",
                "ip": assigned_ip,
                "gateway": gateway,
                "bootfile": bootfile
            }
        else:
            reply = {"message": "No IP available"}

        server.sendto(json.dumps(reply).encode(), (addr[0], 68))
        print(f"[REPLY SENT] → {addr[0]}")

        gui_table.delete(*gui_table.get_children())
        for m, ip in leased.items():
            gui_table.insert("", "end", values=(m, ip))


def run_server_gui():
    root = tk.Tk()
    root.title("BOOTP Server - Lease Table")
    root.geometry("420x400")

    cols = ("MAC Address", "Assigned IP")
    table = ttk.Treeview(root, columns=cols, show="headings", height=15)
    table.heading("MAC Address", text="MAC Address")
    table.heading("Assigned IP", text="Assigned IP")
    table.pack(fill="both", expand=True)

    threading.Thread(target=start_server, args=(table,), daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    run_server_gui()
