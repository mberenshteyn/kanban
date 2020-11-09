import bcrypt
import flask
import secrets
from bson.objectid import ObjectId
from flask import jsonify, make_response, request, session

import database
import encoder

app = flask.Flask(__name__)
app.json_encoder = encoder.MongoEncoder
app.config['SECRET_KEY'] = secrets.token_bytes()

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    """
    Registers a new user in the database, if there is no account
    currently associated with the username.
    """
    if "username" not in request.args:
        return "ERROR: user did not supply a username"
    elif "password" not in request.args:
        return "ERROR: user did not supply a password"

    username = request.args["username"]
    password = request.args["password"]

    users = database.connect("users")

    print("Connected to users table.")
    if users.count_documents({"username": username}) != 0:
        return "ERROR: there is already an account registered under this username!"

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = {
        "username": username,
        "hashed_pwd": hashed,
        "board_ids": [],
        "board_names": []
    }

    result = users.insert_one(new_user)
    if not result.acknowledged:
        return "ERROR: failed to create new user"
    return "OK"

@app.route("/signin", methods = ["GET"])
def signin():
    """
    Signs user into the application, if they have already signed up.
    """
    if 'userID' in session:
        return "User is already logged in!"

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
    session['userID'] = current_user["_id"]
 
    return response

@app.route("/signout", methods = ["GET", "POST"])
def signout():
    """
    Signs user out of the application, if they are currently signed in.
    """
    pass

@app.route("/boards", methods = ["GET"])
def view_boards():
    """
    Loads all of a users' boards onto a single page to view.
    """
    userid = session["userID"]
    
    users = database.connect("users")
    boards = database.connect("boards")
    boards.create_index("userID")

    current_user = users.find_one({"_id": ObjectId(userid)})
    if not current_user:
        return "ERROR: there was an error finding the user"

    user_boards = []
    user_boardIDs = current_user["board_ids"]
    for boardID in user_boardIDs:
        board = boards.find_one({"_id": boardID})
        if not board:
            return "ERROR: there was an issue loading a users' board"
        user_boards.append(board)
    
    response = make_response(jsonify(user_boards), 200)
    return response

@app.route("/boards/new", methods = ["GET", "POST"])
def create_board():
    """
    Creates a new board for the logged in user. Fails if the given
    board name already exists for the user.
    """
    userid = session["userID"]
    board_name = request.args["board_name"]
    
    users = database.connect("users")
    boards = database.connect("boards")

    current_user = users.find_one({"_id": ObjectId(userid)})
    if not current_user:
        return "ERROR: there was an error finding the user"

    curr_board_names = current_user["board_names"]
    if board_name in curr_board_names:
        return "ERROR: user already has a board of the same name!"

    new_board = {
        "board_name": board_name,
        "userID": userid,
        "lists": {
            "todo": [],
            "in_progress": [],
            "done": []
        }
    }

    insert_result = boards.insert_one(new_board)
    if not insert_result.acknowledged:
        return "ERROR: failed to create new board"
    board_id = insert_result.inserted_id
    update_result = users.update_one({"_id": ObjectId(userid)}, 
        {"$push": {"board_ids": board_id, "board_names": board_name}})
    if not update_result.acknowledged:
        return "ERROR: failed to add new board to user directory"

    return "Successfully created new board"

@app.route("/boards/<board_name>", methods = ["GET"])
def get_board(board_name):
    """
    Loads a board for the logged in user. Fails if the given
    board name does not exist for the user.
    """
    userid = session["userID"]

    users = database.connect("users")
    boards = database.connect("boards")

    current_user = users.find_one({"_id": ObjectId(userid)})
    if not current_user:
        return "ERROR: there was an error finding the user"

    user_boardIDs = current_user["board_ids"]
    for boardID in user_boardIDs:
        board = boards.find_one({"_id": boardID})
        if not board:
            return "ERROR: there was an issue loading a users' board"
        if board["board_name"] == board_name:
            return make_response(jsonify(board), 200)
    
    return "ERROR: user does not have a board with the given name"

@app.route("/boards/<board_name>/new", methods = ["GET", "POST"])
def add_item(board_name):
    """
    Adds a new item to the specified board, if it exists. By default,
    adds the item to the todo board.
    """
    pass

@app.route("/boards/<board_name>/<item_id>", methods = ["GET"])
def view_item(board_name, item_id):
    """
    View the item with the provided item id in the specified board,
    if the board exists and the item id is present.
    """
    pass

@app.route("/boards/<board_name>/<item_id>/update")
def update_item(board_name, item_id):
    """
    Updates the item with the provided item id in the specified board,
    if the board exists and item id is present. Can update category, 
    title, or description.
    """
    pass


