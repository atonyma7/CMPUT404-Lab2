#!/usr/bin/env python3
import socket, time, sys

HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    extern_host = 'www.google.com'
    extern_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('starting proxy server')
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True: 
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print('connecting to google')
                remote_ip = get_remote_ip(extern_host)
                proxy_end.connect((remote_ip, extern_port))

                send_full_data = conn.recv(BUFFER_SIZE)
                print (f"sending recieved data {send_full_data} to google")
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                
                print (f"sending recieved data {data} to client")

                conn.send(data)
            conn.close()
if __name__ == "__main__":
    main()