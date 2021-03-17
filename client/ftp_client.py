from socket import *
import os.path
from os import listdir
is_connected = False

print("Welcome to your custom FTP client!")

while True:
    user_command = input("Enter command: ")
    command_args = user_command.split(' ')
    payload = ""

    #user command to connect to the server
    if command_args[0] == "CONNECT":
        if is_connected == True:
            print("Cannot connect to another server while already connected to a server.")
        elif len(command_args) == 3 and (command_args[1] is not None or command_args[2] is not None):
            #set up connection with the server and port the user specified
            server_name = command_args[1]
            server_port = command_args[2]
            client_socket = socket(AF_INET, SOCK_STREAM)
            
            #try to connect to server and if the connection fails report the error to the user
            try:
                client_socket.connect((server_name, int(server_port)))
            except OSError as error_msg:
                print("Couldn't connect to Server " + command_args[1] + " Port " + command_args[2] + ".  Error: " + str(error_msg))
                client_socket.close()
                continue

            is_connected = True
            print("Connection to Server " + command_args[1] + " Port " + command_args[2] + " Established Successfully")
        else:
            print("Invalid arguments for \'CONNECT\'")
    
    #ensure that the user can't execute any command other thatn "CONNECT" if no connection is set up yet
    elif is_connected == False:
        print("Cannot make any other commands besides \'CONNECT\' until client is connected to a server.")

    #user command to list all files stored on the server
    elif command_args[0] == "LIST":
        #check if the user supplied more than 1 argument
        if len(command_args) != 1:
            print("Invalid arguments for \'LIST\'")
            continue
        
        client_socket.send(command_args[0].encode())
        payload = client_socket.recv(1024)
        print("Files on server are: ", payload.decode())

    #user command to retrieve a file from the server
    elif command_args[0] == "RETRIEVE":
        #check if the user supplied the right number of arguments
        if len(command_args) == 2:

            #if the user already has this file, ask if they want to replace it
            file_list = listdir("./client/downloads")
            if command_args[1] in file_list:
                user_command = input("This file already exists on this client. Want to replace the existing file? (Y/N): ")
                
                while True:
                    if user_command == 'Y' or user_command == 'N':
                        break
                    else:
                        user_command = input("Please enter Y or N: ")

            #if the file already exists and the user doesn't want to replace it, just get the next command
            if user_command == 'N':
                print("RETRIEVE Command Cancelled")
                continue

            #put the commands together in one string to be sent to the server
            msg = command_args[0] + " " + command_args[1]
            client_socket.send(msg.encode())
            payload = client_socket.recv(1024)
            payload = payload.decode()

            if payload == "File Not Found":
                #if the file wasn't found, just print the return message from the server
                print(payload)
            else:
                print(payload)
                #create a new file to store the data in recieved from the server
                file = open("./client/downloads/" + command_args[1], "wb")

                #loop and recieve the requested data until the server is done sending 
                while True:
                    payload = client_socket.recv(1024)
                    file.write(payload)

                    if len(payload) < 1024:
                        print("Done")
                        file.close()
                        break

                print(command_args[1] + " Retrieved Successfully")
        else:
            print("Invalid arguments for \'RETRIEVE\'")
    
    #user command to store a file from the client onto the server
    elif command_args[0] == "STORE":
        #check if the user supplied the right number of arguments
        if len(command_args) == 2:

            #catch exception if the file being opened doesn't exist
            try:
                file = open(command_args[1], 'rb')
            except IOError:
                print("File does not exist on the client")
                continue

            msg = command_args[0] + " " + os.path.split(command_args[1])[1]
            client_socket.send(msg.encode())

            #continuously read from the file and send the data to the server until there is no more to send
            while True:
                payload = file.read(1024)
                if not payload:
                    print("File Stored Successfully")
                    file.close()
                    break
                client_socket.send(payload)
            
        else:
            print("Invalid arguments for \'STORE\'")

    #user command to quit the FTP session
    elif command_args[0] == "QUIT":
        #check if the user supplied the right number of arguments
        if len(command_args) == 1:
            client_socket.send(command_args[0].encode())
            client_socket.close()
            is_connected = False
            print("Client disconnected from server")
        else:
            print("Invalid arguments for \'QUIT\'")
    else:
        print("Invalid command. Valid commands are \'CONNECT\', \'LIST\', \'RETRIEVE\', \'STORE\', and \'QUIT\'")
