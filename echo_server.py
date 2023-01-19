import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" #or 0.0.0.0 which binds the socket to every single address on my computer
PORT = 8080

#call when we receive a connection
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by: {addr}")
        while True:

            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            conn.send(data) #send returns no. of bytes it sent. send_all returns an error if it doesnt send everything

def start_server():
    #with blocks help to autoclean code by closing stuff we might have overlooked. Don't close here cuz with will do that for you
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #1 is true. it lets us reuse the socket address. how to reuse the port? look at socket documentation
        #reusing sockets: cannot bind 2 sockets to the same address and port. can bind to same add or sam eport, but not both

        s.listen()

        conn, addr = s.accept() #returns clients IP address and port as a tuple
        handle_connection(conn, addr)
        
# Start multithreaded echo server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))

        '''
        setsockopt(level, option, value)
        https://manpages.debian.org/bullseye/manpages-dev/setsockopt.2.en.html
        '''
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2) # Allow backlog of up to 2 connections
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

start_server()
start_threaded_server()
