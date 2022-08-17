#!C:\Users\Anupam\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe
# shebang/SHArp bang line line

print("content-type: text/html\n\n")
# part of the HTTP Header sent to the client's browser

import cgi #for cgi handling
import cgitb #for getting runtime error details
import html #for script injection avoidance
import os # for file uploads

cgitb.enable()

# create an instance of FieldStorage class
form = cgi.FieldStorage()

# get the data from the fields
name = form.getvalue('name', 'No name')
email = form.getvalue('email', 'No email')
password = form.getvalue('pass', 'No password')
# Getting checklist values as a list
emotions_list = form.getlist('emotions')
satisfaction = form.getvalue('satisfaction')
comments = form.getvalue('comments')
location = form.getvalue('location')

# handling file upload
try:
    import msvcrt
    # set mode for stdin and stdout
    msvcrt.setmode(0, os.O_BINARY) # setting stdin to 0
    msvcrt.setmode(1, os.O_BINARY) # setting stdout to 1
except ImportError:
    pass

# to avoid script injetion and escape user input
import html
name = html.escape(name)
email = html.escape(email)
password = html.escape(password)
satisfaction = html.escape(satisfaction)
comments = html.escape(comments)
location = html.escape(location)

# The rest of the html part
print(f"""
<html>
    <head>
    <link type="text/css" rel="stylesheet" href="css/styles.css"/>
        <title>Feedback Submit</title>
    </head>
    <body>
        <div class="container output">""")
# get the file from the nested field storage instance
fileitem = form['bioimg']
# checking if a valid file was uploaded
if fileitem.filename: 
    # get rid of path and keep only the filename
    imagefilename = os.path.basename(fileitem.filename)
    open('files/'+imagefilename,'wb').write(fileitem.file.read())
    print(f"""<img src="{'files/'+imagefilename}" alt="Profile Picture">""")
else:
    print(f"""<p>No image was uploaded</p>""")
print(f"""<p><strong>Name:</strong> <span>{name}</span> </p>
            <p><strong>Email:</strong> <span>{email}</span> </p>
            <p><strong>Password:</strong> <span>{password}</span> </p>""")
print(f"<p><strong>Emotions:</strong> <span>")
for emotion in emotions_list:
    print(html.escape(emotion))
print(f"""</span></p>
            <p><strong>Satisfaction:</strong> <span>{satisfaction}</span></p>
            <p><strong>Comments:</strong> <span>{comments}</span> </p>
            <p><strong>Location visited:</strong> <span>{location}</span> </p>
        </div>
    </body>
</html>""")