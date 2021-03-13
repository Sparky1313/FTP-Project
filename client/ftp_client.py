from socket import *
import os.path
is_connected = False

print("Welcome to your custom FTP client!")

while True:
    user_command = input("Enter command: ")
    command_args = user_command.split(' ')
    payload = None

    if command_args[0] == "CONNECT":
        if is_connected == True:
            print("Cannot connect to another server while already connected one server.")
        elif len(command_args) == 3 and (command_args[1] is not None or command_args[2] is not None):
            server_name = command_args[1]
            server_port = command_args[2]
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((server_name, int(server_port)))
            is_connected = True
            print("Connection to Server " + command_args[1] + " Port " + command_args[2] + " Established Successfully")
        else:
            print("Invalid arguments for \'CONNECT\'")
    elif is_connected == False:
        print("Cannot make any other commands besides \'CONNECT\' until client is connected to a server.")
    elif command_args[0] == "LIST":
        client_socket.send(command_args[0].encode())
        payload = client_socket.recv(1024)
        print("Files on server are: ", payload.decode())
    elif command_args[0] == "RETRIEVE":
        if command_args[1] is not None:
            # logic
            #put the commands together in one string to be sent to the server
            msg = command_args[0] + " " + command_args[1]
            client_socket.send(msg.encode())
            payload = client_socket.recv(1024)
            data = payload.decode()
            if(data == "File Not Found"):
                #if the file wasn't found, just print the return message from the server
                print(data)
            else:
                #create a new file to store the data in recieved from the server
                file = open("./client/files/" + command_args[1], "w")
                file.write(data)
                file.close()
                print(command_args[1] + " Retrieved Successfully")
        else:
            print("Invalid arguments for \'RETRIEVE\'")
    elif command_args[0] == "STORE":
        if command_args[1] is not None:
            print(command_args[1])
            msg = command_args[0] + " " + os.path.split(command_args[1])[1]
            client_socket.send(msg.encode())
            file = open(command_args[1], 'rb')

            while True:
                payload = file.read(1024)
                if not payload:
                    print("Done")
                    file.close()
                    break
                client_socket.send(payload)
                print(payload)
            # payload = file.read()
            # file.close()
            # filename = os.path.split(command_args[1])
           
            print(os.path.split(command_args[1]))
            
            # client_socket.send(payload)
            
            # print(data)
            # file_list = listdir("./client/files")
            # for filename in file_list:
            #     #check if the file name matches what the user sent
            #     if filename == recv_cmd[1]:
            #         file = open("./client/files/" + filename)
            #         data = file.read()
            #     else:
            #         data = "File Not Found"

            #     connection_socket.send(data.encode())
            #     break
        else:
            print("Invalid arguments for \'STORE\'")
    elif command_args[0] == "QUIT":
        client_socket.send(command_args[0].encode())
        client_socket.close()
        is_connected = False
        print("Client disconnected from server")
    else:
        print("Invalid command. Valid commands are \'CONNECT\', \'LIST\', \'RETRIEVE\', \'STORE\', and \'EXIT\'")

# server_name = "127.0.0.1"
# server_port = 12000

# sentence = input("Input lowercase sentence:")
# client_socket.send(sentence.encode())
# modifiedSentence = client_socket.recv(1024)
# print('From Server: ', modifiedSentence.decode())
