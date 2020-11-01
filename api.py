import database
import bcrypt
import uuid
import flask
from flask import request, jsonify, make_response

app = flask.Flask(__name__)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if "username" not in request.args:
        return "ERROR: user did not supply a username"
    elif "password" not in request.args:
        return "ERROR: user did not supply a password"

    username = request.args["username"]
    password = request.args["password"]

    users = database.connect("users")

    if users.count_documents({"username": username}) != 0:
        return "ERROR: there is already an account registered under this username!"

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    userid = uuid.uuid1()
    while users.count_documents({"uuid": userid}) != 0:
        userid = uuid.uuid1()

    new_user = {
        "uuid": userid,
        "username": username,
        "hashed_pwd": hashed
    }

    users.insert_one(new_user)

@app.route("/signin", methods = ["GET"])
def signin():
    if "username" not in request.args:
        return "ERROR: user did not supply a username"
    elif "password" not in request.args:
        return "ERROR: user did not supply a password"

    username = request.args["username"]
    password = request.args["password"]

    users = database.connect("users")
    
    current_user = users.find_one({"username": username})
    if not current_user:
        return "ERROR: there is not an account registered under this username!"
    if not bcrypt.checkpw(password.encode("utf-8"), current_user.get("hashed_pwd")):
        return "ERROR: username or password is not correct!"

    response = make_response("Generating user cookie")
    response.set_cookie("uuid", current_user.get("uuid").bytes)

    return response

def create_board(user, board_name):
    pass

def get_board(user, board_name):
    pass

def add_item(user, board, item_name):
    pass

def update_details(user, board, item_id, new_details):
    pass

def update_status(user, board, item_id, new_status): 
    pass

