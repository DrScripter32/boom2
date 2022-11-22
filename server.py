
from threading import Thread
import socket
import time
l=[]
def soo():
    
    from threading import Thread
    import logging , json
    from datetime import datetime
    logging.basicConfig( filename='logfile.log', filemode='a' )
# server's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5002 # port we want to use
    separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
    client_sockets = set()
# create a TCP socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    logging.info('socket set')
# make the port as reusable port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
    s.bind((SERVER_HOST, SERVER_PORT))
    logging.info('socket bind')
# listen for upcoming connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    def listen_for_client(cs):

        while True:
            try:
            # keep listening for a message from `cs` socket
                msg = cs.recv(1024).decode()

            except Exception as e:
            # client no longer connected
            # remove it from the set
                print(f"[!] Client closed")
                logging.error(e)
                client_sockets.remove(cs)
                logging.info('client removed')
            else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
                msg = msg.replace(separator_token, ": ")
        # iterate over all connected sockets
            for client_socket in client_sockets:
            # and send the message
                msgs = "["+ datetime.now().strftime('%H:%M:%S') +"] " +msg 
                jsons = {datetime.now().strftime('%Y-%m-%d | %H:%M:%S'):msgs}
                file = open("data.txt","a+")
                file.write((jsons)+"\n")
                file.close()
                client_socket.send(msgs.encode())


    while True:
    # we keep listening for new connections all the time
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        #////send 10 last mess
        p = open("data.txt")
        for client_socket in client_sockets:
        	for password in p:
        		password =password.strip("\n")
        		l.append(password)
        	l.reverse()
        	for client_socket in client_sockets:
        		for i in l:
        			msgs=i
        			client_socket.send(msgs.encode())
        
        
        
        
    # add the new connected client to connected sockets
        client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
        t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
        t.daemon = True
    # start the thread
        t.start()

# close client sockets
    for cs in client_sockets:
        cs.close()
# close server socket
    s.close()

#---
Thread(target=soo).start()
def udpserver():

    def T(data):
        try:
            ip = "127.0.0.1"
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((ip ,5002))
            client.send(data.encode())
            client.close()
        except Exception as e:
            print(e)
    UDPServerSocket = (socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM))

    UDPServerSocket.bind(("0.0.0.0", 1700))
    print("UDP server up")
    while True:
        RecvData = (UDPServerSocket.recvfrom(1024))
        print("-UDP-")
        print(RecvData)
        print("-e-UDP-")
        try:
            fil = open("O.txt","a+")
            fil.write(str(RecvData))
            fil.close()
            T(RecvData)
        except:
            pass



Thread(target=udpserver).start()
