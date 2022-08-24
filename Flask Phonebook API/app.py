from flask import Flask, render_template, redirect,url_for, request, abort, jsonify # convert list/dict to json
import requests
import pyodbc

#create a connection string
myConString = 'Driver={SQL Server};Server=DESKTOP-517KMB6\SQLEXPRESS;Database=phonebook_db;Trusted_Connection=yes;'

# creating an application instance
# the argument for the constructor is the main module name
# main module will be  there in the dunder __name__
app = Flask(__name__)

# defining a route in flask using the app.route
# app is out flask application obj
# / is the root of the website, like the default index.html
# greet() functiion will be executed when accessing defalt reoute

# list all contacts in the phonebook
@app.route("/contacts", methods=['GET'])
def listContacts():
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        #get the contents 
        mycursor.execute("SELECT * FROM phonebook ORDER BY name")
    except Exception as e:
        return(f"{type(e).__name__}")
    else:
        #saving the result into a dictionary
        phoneBook = [{'Name': row[0], 'Number': row[1]} for row in mycursor.fetchall()]
        return render_template('index.html', phoneBook=phoneBook)
        # return f"<h1>{phoneBook}</h1>"
    finally: 
        myconn.commit()
        myconn.close()

# Add contact
@app.route("/contacts", methods=['POST'])
def addContact():
    #create a connection with the connection string
    myconn = pyodbc.connect(myConString)
    try: 
        #get the cursor object
        mycursor = myconn.cursor()
        # create a new contact as a dictionary item
        contact = {
            'Name': request.form.get('Name'),
            'Number': request.form.get('Number')
        }
        name = contact['Name']
        number = contact['Number']
        #insert into the table
        mycursor.execute("INSERT INTO phonebook VALUES (?, ?)", (name, number))
    except Exception as e:
        return(f"{type(e).__name__}")
    else:
        # jsonify will convert list/dict to json format
        return redirect(url_for('listContacts'))
    finally:
        myconn.commit()
        myconn.close()

# Search contact by name
@app.route("/contacts/<name>", methods=['GET'])
def searchByName(name):
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
                return(f"{type(e).__name__}")
            else:
                #saving the result into a dictionary
                phoneBook = [{'Name': row[0], 'Number': row[1]} for row in mycursor.fetchall()]
                # jsonify will convert list/dict to json format
                return jsonify({'contacts': phoneBook})              
        else:
            abort(404)
    except Exception as e:
        abort(404)
    finally: 
        myconn.commit()
        myconn.close()

# Search contact by number
@app.route("/contacts/<int:number>", methods=['GET'])
def searchByNumber(number):
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
                return(f"{type(e).__name__}")
            else:
                #saving the result into a dictionary
                phoneBook = [{'Name': row[0], 'Number': row[1]} for row in mycursor.fetchall()]
                return jsonify({'contacts': phoneBook})              
        else:
            abort(404)
    except Exception as e:
        abort(404)
    finally: 
        myconn.commit()
        myconn.close()

# Delete contact
@app.route("/contacts/<name>", methods=['DELETE'])
def delete_book(name):
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
                return(f"{type(e).__name__}")
            else:
                return redirect(url_for('listContacts'))
        else:
            abort(404)
    except Exception as e:
        abort(404)
    finally: 
        myconn.commit()
        myconn.close()

# check if it's the main module, then run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 