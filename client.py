import socket
import json
import tkinter as tk

CLIENT_PORT = 68
SERVER_IP = "127.0.0.1"
SERVER_PORT = 67
BUFFER_SIZE = 1024


def send_request(mac_entry, output_box):
    mac = mac_entry.get().strip()
    if not mac:
        output_box.config(text="Enter MAC first")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(("", CLIENT_PORT))
    client.settimeout(5)

    req = json.dumps({"message": "BOOTREQUEST", "mac": mac})
    client.sendto(req.encode(), (SERVER_IP, SERVER_PORT))

    try:
        data, addr = client.recvfrom(BUFFER_SIZE)
        reply = json.loads(data.decode())

        if reply["message"] == "BOOTREPLY":
            txt = f"IP: {reply['ip']}\nGateway: {reply['gateway']}\nBootfile: {reply['bootfile']}"
        else:
            txt = reply["message"]

    except:
        txt = "No reply (timeout)"

    output_box.config(text=txt)
    client.close()


def run_client_gui():
    root = tk.Tk()
    root.title("BOOTP Client")
    root.geometry("350x200")

    tk.Label(root, text="Enter MAC Address:").pack()
    mac_entry = tk.Entry(root, width=30)
    mac_entry.pack()

    output = tk.Label(root, text="", justify="left", fg="blue")
    output.pack(pady=10)

    tk.Button(root, text="Request IP", command=lambda: send_request(mac_entry, output)).pack()

    root.mainloop()


if __name__ == "__main__":
    run_client_gui()
