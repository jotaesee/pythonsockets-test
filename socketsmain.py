import socket, threading, sys, json, os
    
def get_download_path(): ## esto esta importado por 
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

    
    

def getport():
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close
    return port

def sendFile(message : str, connection : socket.socket):
    try: 
        cmd, datapath = message.split(" ", 1) 
        filename = os.path.basename(datapath).split('/')[-1]
        file = open(datapath, "rb")
        filedata = file.read()
        filesize = os.path.getsize(datapath)
        
        data = json.dumps({"type" : "sendFileRequest", "user" : username, "message" : f"{filename}:{filesize}"}).encode("utf-8")
        connection.send(data) ## mensaje de aviso. empezamos a mandar data
        connection.sendall(filedata)
        file.close()
    except FileNotFoundError : 
        print ("File not found, command cancelled. keep chatting!")
        pass
    except Exception as e :
        print(e)

def receiveFile(message : str , connection : socket.socket):
    
    filename, filesize = message.split(":")
    os.path.basename(filename)
    path = get_download_path()
    path = f"{path}/{filename}"
    file = open(path, "wb")
    filesize = int(filesize)
    allbytes = 0
    while allbytes < filesize : 
        print(allbytes)
        print(filesize)
        newbytes = bytearray(1024)
        bytesreceived = connection.recv_into(newbytes)
        allbytes += bytesreceived
        file.write(newbytes[:bytesreceived])
    file.close()
    return 0



def listen(connection : socket.socket):
    while True :
        try: 
            data = connection.recv(1024)
            data = data.decode()
            data = json.loads(data)
            messageType = data["type"]
            peer = data["user"]
            message = data["message"]
            
            if messageType == "exitMessage" :
                print("the other user has disconnected") 
                break
            
            if messageType == "sendFileRequest" :
                print("FILE TRANSFER DETECTED, STARTING PROTOCOL...")
                receiveFile(message, connection)
                
            else : print(f"\r[{peer}] : {message} \nVos: ", end="")
            
        except (ConnectionResetError, BrokenPipeError):
            print("rip connection")
            break
        except Exception as e :
            print(e)
            break
    
    connection.close()
    sys.exit()

def startchatting(connection : socket.socket) :
    
    listening = threading.Thread(target=listen, args=(connection,))
    listening.daemon = True
    listening.start()
    
    while True:
        
        try:    
            message = input("You: ")
            
            
            if message.lower() == 'exit':
                data = {"type":"exitMessage", "user" : username, "message" : ""} 
                data = json.dumps(data).encode("utf-8")
                connection.send(data)
                connection.close()
                break
            
            if message.startswith("/filesend"):
                sendFile(message, connection)
                pass  
            else:
                data = {"type":"message", "user" : username, "message" : message}
                data = json.dumps(data).encode("utf-8")
                connection.send(data)
        
        except (EOFError, KeyboardInterrupt) :
            print("byeeeee")
            break
        except (ConnectionResetError, BrokenPipeError):
            print("rip connection")
            break
        except Exception:
            break
    
    connection.close()
    sys.exit()


def chatconnect(): 
    address = input("ip to connect to: \n")
    port = input("input port: ")
    if not port.isdigit():
        return print("error NaN, nv ")
    port = int(port)
    
    newsocket = socket.socket()
    newsocket.connect((address, port))
    print(f"You are now connected to {address}, by port {port}")
    startchatting(newsocket)

    
def hostnewchat():
    user = socket.gethostname()
    s = socket.socket()
    address = socket.gethostbyname(user)
    port = getport()
    
    s.bind((address, port))
    
    print(f"Tell your friend to connect to {address} with port number {port}")
    print("Now waiting for connection:")
    s.listen() 
    connection, peerport = s.accept()
    print(f"connected to {connection}")
    
    startchatting(connection)
    
if __name__ == "__main__":
    print("Welcome to the P2P terminal chat!")
    username = input("what's your name? \n ")
    print(f"okay {username}, now select an option:")
    print("1 : Host a new chat.   2 : Join an existing chat. ")
    option = input("")
    
    if option == '1' : 
        hostnewchat()
    else: chatconnect()