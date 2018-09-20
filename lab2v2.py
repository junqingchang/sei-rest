from flask import Flask, render_template, make_response, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo

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
            data = request.get_json()
            newdata = data["message"]
            noteid = note.insert({'post': postID, 'message': newdata})
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

@app.route('/logout', methods=["GET", "EXIT"])
def Logout():
    global login_status
    if(login_status):
        if (request.method == "GET"):
            return "Type curl -X EXIT localhost:5000/logout\n"
        elif (request.method == "EXIT"):
            login_status = False
            return redirect('/')
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)