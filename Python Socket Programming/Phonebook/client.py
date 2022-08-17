import json
import socket # import the socket module

def display(phoneBook):
    #Displaying the results
    for record in phoneBook:
        print(f"\tName : {record['Name']}, Number : {record['Number']} ")

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
    message = "y"

    while message.lower().strip() != "n":
        # if the message is not 'exit', send it to server
        print("Menu :")
        print("\t1. List all contacts")
        print("\t2. Add a new contact")
        print("\t3. Search by name")
        print("\t4. Search by number")
        print("\t5. Delete")
        print("\t6. Exit")
        choice = input("Enter your choice:")
        match int(choice):
            case 1:
                msg = json.dumps({
                    'choice' : choice
                })
                client_socket.send(msg.encode())
            case 2:
                name = input("Enter the name : ").capitalize()
                number = int(input("Enter number : "))
                msg = json.dumps({
                    'choice' : choice,
                    'name' : name,
                    'number' : number
                })
                client_socket.send(msg.encode())
            case 3:
                name = input("Enter name of contact to search : ")
                # msg = "" + choice + " " + name
                msg = json.dumps({
                    'choice' : choice,
                    'name' : name
                })
                client_socket.send(msg.encode())
            case 4:
                number = int(input("Enter number of contact to search : "))
                # msg = str((choice, number))
                msg = json.dumps({
                    'choice' : choice,
                    'number' : number
                })
                client_socket.send(msg.encode())
            case 5: 
                name = input("Enter name of contact to delete : ")
                msg = json.dumps({
                    'choice' : choice,
                    'name' : name
                })
                client_socket.send(msg.encode())
            case 6:
                message = "n"
                continue
            case _:
                print("Invalid Input!")
        
        # receive any reply data from the server
        data = json.loads(client_socket.recv(1024).decode())
        # print the received data
        if data['status'] != 0:
            display(data['result'])
        else :
            print(data['result'])

    # close the socket connection once the while lopp is exited
    client_socket.close()

# if the file is not imported, run the program directly, 
# else, just be there as an imported code and do not run 
# until the user calls the function (default  behaviour)
if __name__ == '__main__':
    client_program()