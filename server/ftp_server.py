from socket import *
from os import listdir, getcwd
from os.path import isfile, join

server_host = "127.0.0.1"
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)

while True:
    connection_socket = None
    connection_socket, addr = server_socket.accept()
    if connection_socket is not None:
        is_connected = True

    while is_connected == True:
        recv_cmd = connection_socket.recv(1024).decode()
        recv_cmd = recv_cmd.split(' ')
        #insert error handling at some point
        msg = ""


        if recv_cmd[0] == "CONNECT":
            msg = "Connected to server. Awaiting commands..."
            connection_socket.send(msg.encode())
        elif recv_cmd[0] == "LIST":
            # os.path
            file_list = listdir("./server/files")
            for filename in file_list:
                msg = msg + " " + filename
            # print(listdir("./server/files"))
            connection_socket.send(msg.encode())
            # connection_socket.send(fi)
            # connection_socket.sendfile(recv_cmd[1])
        elif recv_cmd[0] == "RETRIEVE":
            file_list = listdir("./server/files")
            for filename in file_list:
                #check if the file name matches what the user sent
                if filename == recv_cmd[1]:
                    file = open("./server/files/" + filename)
                    data = file.read()
                    file.close()
                else:
                    data = "File Not Found"

                connection_socket.send(data.encode())
                break

            print('')
            #logic stuff
        elif recv_cmd[0] == "STORE":
            file = open("./server/files/" + recv_cmd[1], 'wb')
            
            while True:
                data = connection_socket.recv(1024)
                if not data:
                    print("done")
                    file.close()
                    break
                file.write(data)
            # file.close()
            
            #logic stuff
        elif recv_cmd[0] == "QUIT":
            connection_socket.close()
            is_connected = False
        else:
            msg = "Invalid command. Please enter a valid command."

    
    


