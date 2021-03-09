from socket import *

server_name = "127.0.0.1"
serverPort = 12000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, serverPort))
sentence = input("Input lowercase sentence:")
client_socket.send(sentence.encode())
modifiedSentence = client_socket.recv(1024)
print('From Server: ', modifiedSentence.decode())
client_socket.close()