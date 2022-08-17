import socket # import the socket module

def client_program():
    print("inside client program")
    host = socket.gethostname() # get the hostname
    # as both codes are running in the same comuputer, we can 
    # get the loopback address as the server address
    port = 64435 # initiate port no above 1024 till 65535

    client_socket = socket.socket() # get instance of socket

    # instead of binding, we are connecting to the server
    client_socket.connect((host, port))
    # the connect() function takes tuple as argument

    # getting the message to send to the server
    message = input("Enter the message to send to the server: ")

    while message.lower().strip() != "exit":
        # if the message is not 'exit', send it to server
        client_socket.send(message.encode())
        # receive any reply data from the server
        data = client_socket.recv(1024).decode()
        # print the received data
        print(f"Received from server: {data}")
        message = input("Enter the message to send to the server: ")

    # close the socket connection once the while lopp is exited
    client_socket.close()

# if the file is not imported, run the program directly, 
# else, just be there as an imported code and do not run 
# until the user calls the function (default  behaviour)
if __name__ == '__main__':
    client_program()