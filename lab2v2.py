from flask import Flask, render_template, make_response, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo

'''
Implementation Details:
Concept of this implementation is an announcement board where the admin can send and delete announcements. The announcements
are stored on a MongoDB using PyMongo

localhost:5000/
The first page is a login page which requires the admin to login with the credentials "admin" for both
Username and Password using the POST API. Trying to access other pages without login in results in automatically redirecting
back to the login page
The GET API returns the instructions on the login page
The POST API is used for logging in. It only takes in a json type with keys "user" for username and "pass" for password
Commands to run:
$ curl -X GET localhost:5000
$ curl -X POST -d '{"user":"admin", "pass":"admin"}' -H "Content-Type: application/json" localhost:5000

localhost:5000/msgboard/ and localhost:5000/msgboard/<int value>
After logging in, the user will then be able to access a list of commands that allows the user to add/delete notes,
namely using the API NOTE and DELETE. The user will also be able to see the number of post that is up by using the
SIZE API. The NOTE call supports 2 content types, namely application/json and text/plain.
The GET API returns the instruction on the msgboard page, which teaches the user what commands can be ran
The NOTE API submits a new announcement on whichever int value at the end of the path. NOTE API accepts application/json type
with key "message" as well as text/plain
The SIZE API returns the number of post on the announcement channel
Commands to run:
$ curl -X GET localhost:5000/msgboard/
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X NOTE -d '{"message":"welcome to messageboard"}'  -H "Content-Type: application/json" localhost:5000/msgboard/1
$ curl -X GET localhost:5000/msgboard/1
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X DELETE localhost:5000/msgboard/1
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X NOTE -d "New Message" -H "Content-Type: text/plain" localhost:5000/msgboard/1
$ curl -X GET localhost:5000/msgboard/1
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X DELETE localhost:5000/msgboard/1

localhost:5000/logoutpage/
This is the page for the user to logout and only has the EXIT call
The EXIT API logs the user out of the account
Commands to run:
$ curl -X EXIT localhost:5000/logoutpage
'''

app = Flask(__name__, template_folder='templates')
app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)

credentials = {"admin":"admin"}
global login_status
login_status = False

@app.route('/', methods=["GET", "POST"])
def AnnouncementSpace():
    global login_status
    if (request.method == "GET"):
        if(login_status):
            return redirect("/msgboard")
        else:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'),200,headers)
    elif(request.method == "POST"):
        if (login_status):
            return "Already Logged in\n"
        data = request.get_json()
        if("user" not in data or "pass" not in data):
            return "Invalid curl command\n"
        if(data["user"] in credentials):
            if(data["pass"] == credentials[data["user"]]):
                login_status = True
                return "Successful Login\n"
            else:
                return "Login Failed\n"
        else:
            return "Login Failed\n"

@app.route('/msgboard/', methods=["GET","POST","SIZE"])
def MessageBoard():
    global login_status
    if(login_status):
        if (request.method == "GET"):
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('msg.html'),200,headers)
        elif (request.method == "POST"):
            if(request.form["button"] == "User Settings"):
                return redirect("/user")
        elif (request.method == "SIZE"):
            note = mongo.db.note
            allnotes = note.find()
            return "Total Number of Post {number}\n".format(number=allnotes.count())
    else:
        return redirect("/")

@app.route('/msgboard/<int:postID>', methods=["GET","POST","NOTE", "DELETE"])
def MessageContent(postID):
    global login_status
    if(login_status):
        if(postID <= 0):
            return "Invalid Post Number\n", 404
        if(request.method == "GET"):
            note = mongo.db.note
            n = note.find_one({'post' : postID})
            if n:
                output = {'post' : n['post'], 'message' : n['message']}
            else:
                output = "No such post"
            return jsonify({'result' : output})
        elif(request.method == "NOTE"):
            note = mongo.db.note
            try:
                data = request.get_json()
                newdata = data["message"]
                noteid = note.insert({'post': postID, 'message': newdata})
                new_note = note.find_one({'_id': noteid })
                output = {'post' : new_note['post'], 'message' : new_note['message']}
                return jsonify({'result' : output})
            except:
                data = str(request.data)
                noteid = note.insert({'post': postID, 'message': data})
                new_note = note.find_one({'_id': noteid })
                output = {'post' : new_note['post'], 'message' : new_note['message']}
                return jsonify({'result' : output})
        elif(request.method == "DELETE"):
            note = mongo.db.note
            myquery = {'post' : postID}
            note.delete_one(myquery)
            return "Deleted post {number}\n".format(number=postID)

    else:
        return redirect("/")

@app.route('/logoutpage', methods=["GET", "EXIT"])
def Logout():
    global login_status
    if(login_status):
        if (request.method == "GET"):
            return "Type curl -X EXIT localhost:5000/logoutpage\n"
        elif (request.method == "EXIT"):
            login_status = False
            return redirect('/')
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)