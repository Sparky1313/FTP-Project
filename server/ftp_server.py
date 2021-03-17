from socket import *
from os import listdir, getcwd
from os.path import isfile, join

server_host = "127.0.0.1"
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)

#listen for a connection request from a client
while True:
    connection_socket = None
    connection_socket, addr = server_socket.accept()
    if connection_socket is not None:
        is_connected = True

    #constantly listen for new client commands
    while is_connected == True:
        #read command sent by the client
        recv_cmd = connection_socket.recv(1024).decode()
        recv_cmd = recv_cmd.split(' ')
        payload = ""

        #client command to list the files currently on the server
        if recv_cmd[0] == "LIST":
            file_list = listdir("./server/files")
            if len(file_list) == 0:
                payload = "No Files On Server"
            else:
                for filename in file_list:
                    payload = payload + filename + " "
                
            connection_socket.send(payload.encode())

        #client command to retrieve a file on the server
        elif recv_cmd[0] == "RETRIEVE":
            file_list = listdir("./server/files")

            #check if the requested file exists
            if recv_cmd[1] in file_list:
                payload = "File found.\nBeginning transfer..."
                connection_socket.send(payload.encode())
                file = open("./server/files/" + recv_cmd[1], "rb")

                #continuously send the file data until there is no more data to send
                while True:
                    payload = file.read(1024)

                    if not payload:
                        file.close()
                        break

                    connection_socket.send(payload)
                #file.close()
                payload = "File transfer completed."

            else:
                #let client know the file wasn't found
                payload = "File Not Found"
                connection_socket.send(payload.encode())

        #client command to store a file on the server
        elif recv_cmd[0] == "STORE":
            file = open("./server/files/" + recv_cmd[1], 'wb')
            
            #constantly recieve the file data from the client until there is no more to recieve
            while True:
                data = connection_socket.recv(1024)
                file.write(data)

                if len(data) < 1024:
                    file.close()
                    break
            
        #client command to end the FTP session
        elif recv_cmd[0] == "QUIT":
            connection_socket.close()
            is_connected = False
        else:
            payload = "Invalid command. Please enter a valid command."
            connection_socket.send(payload)

    
    


