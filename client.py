import socket

BYTES_TO_READ = 4096

def get(host, port):
    # created our request
    request_data = b"GET / HTTP/1.1\nHost:" + host.encode('utf-8') + b'\n\n'

    #created our socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #sent some data to our socket
    s.connect((host, port))
    s.send(request_data)
    s.shutdown(socket.SHUT_WR)

    #listen for response
    response = s.recv(BYTES_TO_READ)
    while(len(response) > 0):
        print(response)
        response = s.recv(BYTES_TO_READ)
    
    s.close()

get("www.google.com", 80)