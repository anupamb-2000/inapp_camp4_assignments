import socket # import the socket module

def server_program():
    host = socket.gethostname() # get the hostname
    port = 64435 # initiate port no above 1024 till 65535
    #HOST + "127.0.0.1" # standard loopback interace address (localhost)
    #PORT = 35432 # port to listen on (nonprivileged ports are > 1023)

    server_socket = socket.socket() # get instance of socket

    server_socket.bind((host, port))
    # bind host address and port together
    # the bind() function takes tuple as argument
    # configure how many clients the server can listen simultaneously
    server_socket.listen(2)
    # the accept() method will give back the conn obj and the
    # ip address of the incoming connection request
    conn, address = server_socket.accept() # accept new connection
    print(f"Connection accepted from {str(address)}")

    # now we can receive the messages
    # using a while loop, keep the connection active and 
    # receive messages until there is none
    while True:
        # infinite while loop to receive the data stream
        # receive the packets (max size of 1024 bytes)
        # decode the received data
        data = conn.recv(1024).decode()
        # if no data received, then terminate while loop
        if not data:
            break
        # if valid data, then print the data received
        print(f"Message from client {str(address)} : {str(data)}")
        # give provision to send reply back to the client
        data = input("Type reply here : ")
        # encode the data and send it to the client
        conn.send(data.encode())
    
    conn.close() # close the connection once the while loop breaks

# if the file is not imported, run the program directly, 
# else, just be there as an imported code and do not run 
# until the user calls the function (default  behaviour)
if __name__ == '__main__':
    server_program()