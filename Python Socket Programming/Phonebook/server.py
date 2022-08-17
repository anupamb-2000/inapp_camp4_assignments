import socket # import the socket module
import pyodbc
import json

#create a connection string
myConString = 'Driver={SQL Server};Server=DESKTOP-517KMB6\SQLEXPRESS;Database=phonebook_db;Trusted_Connection=yes;'

#create a connection with the connection string
myconn = pyodbc.connect(myConString)
try: 
    #get the cursor object
    mycursor = myconn.cursor()
    #create a new table for storing the records
    mycursor.execute('''CREATE TABLE phonebook(
	  name varchar(50),
	  number int
  );''')
except:
    try:    
        mycursor.execute("SELECT * FROM phonebook")
    except:
        print("Failed to create table")
        exit()

myconn.commit()
myconn.close()

# defining the fucntion for various operations
def sort():
    #create a connection with the connection string
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        #get the contents 
        mycursor.execute("SELECT * FROM phonebook ORDER BY name")
    except Exception as e:
        print(f"{type(e).__name__}")
    else:
        #saving the result into a dictionary
        phoneBook = [{'Name': row[0], 'Number': row[1]} for row in mycursor.fetchall()]
        return {'status' : 1, 'result' :  phoneBook}
    finally:
        myconn.commit()
        myconn.close()

def add(name, number):
    #create a connection with the connection string
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        #insert into the table
        mycursor.execute("INSERT INTO phonebook VALUES (?, ?)", (name, number))
    except Exception as e:
        print(f"{type(e).__name__}")
    else:
        return {'status' : 0, 'result' :  "Record added to phonebook"}
    finally:
        myconn.commit()
        myconn.close()

def delete(name):
    #create a connection with the connection string
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        #check if present in the table
        mycursor.execute(f"SELECT COUNT(*) FROM phonebook WHERE name = '{name}'")
        if mycursor.fetchall()[0][0] > 0:
            try:
                mycursor.execute(f"DELETE FROM phonebook WHERE name = '{name}'")
            except Exception as e:
                print(f"{type(e).__name__}")
            else:
                return {'status' : 0, 'result' :  "Record deleted from phonebook"}
        else:
            return {'status' : 0, 'result' :  "No such record found!"}
    except Exception as e:
        print(f"{type(e).__name__}")
    finally:
        myconn.commit()
        myconn.close()

def searchname(name):
    #create a connection with the connection string
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        #check if present in the table
        mycursor.execute(f"SELECT COUNT(*) FROM phonebook WHERE name = '{name}'")
        if mycursor.fetchall()[0][0] > 0:
            try:
                mycursor.execute(f"SELECT * FROM phonebook WHERE name = '{name}'")
            except Exception as e:
                print(f"{type(e).__name__}")
            else:
                #saving the result into a dictionary
                phoneBook = [{'Name': row[0], 'Number': row[1]} for row in mycursor.fetchall()]
                return {'status' : 1, 'result' :  phoneBook}
        else:
            return {'status' : 0, 'result' :  "No such record found!"}
    except Exception as e:
        print(f"{type(e).__name__}")
    finally:
        myconn.commit()
        myconn.close()

def searchno(number):
    #create a connection with the connection string
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        #check if present in the table
        mycursor.execute(f"SELECT COUNT(*) FROM phonebook WHERE number = '{number}'")
        if mycursor.fetchall()[0][0] > 0:
            try:
                mycursor.execute(f"SELECT * FROM phonebook WHERE number = '{number}'")
            except Exception as e:
                print(f"{type(e).__name__}")
            else:
                #saving the result into a dictionary
                phoneBook = [{'Name': row[0], 'Number': row[1]} for row in mycursor.fetchall()]
                return {'status' : 1, 'result' :  phoneBook}
        else:
            return {'status' : 0, 'result' :  "No such record found!"}
    except Exception as e:
        print(f"{type(e).__name__}")
    finally:
        myconn.commit()
        myconn.close()

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
        # data = conn.recv(1024).decode().split()
        data = json.loads(conn.recv(1024).decode())
        # if no data received, then terminate while loop
        if not data:
            break
        # if valid data
        match int(data['choice']):
            case 1:
                result = sort()
            case 2:
                result = add(data['name'], data['number'])
            case 3:
                result = searchname(data['name'])
            case 4:
                result = searchno(data['number'])
            case 5: 
                result = delete(data['name'])
            case 6:
                exit()
            case _:
                print("Invalid Input!")
        print(f"Message from client {str(address)} : {str(data['choice'])}")
        # give provision to send reply back to the client
        # encode the data and send it to the client
        conn.send(json.dumps(result).encode())
    conn.close() # close the connection once the while loop breaks

# if the file is not imported, run the program directly, 
# else, just be there as an imported code and do not run 
# until the user calls the function (default  behaviour)
if __name__ == '__main__':
    server_program()