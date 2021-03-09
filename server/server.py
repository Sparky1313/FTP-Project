from socket import *
from os import listdir, getcwd
from os.path import isfile, join

server_port = 12000
sever_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
sever_socket.listen(1)

while True:
    connection_socket, addr = sever_socket.accept()
    recv_cmd = connection_socket.recv(1024).decode()
    recv_cmd = recv_cmd.split(' ')
    #insert error handling at some point


    if recv_cmd[0] == "LIST":
        os.path
        files = []
        listdir(getcwd)

