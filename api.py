import bcrypt
import flask
import secrets
from bson.objectid import ObjectId
from flask import jsonify, make_response, redirect, render_template, request, session
from functools import wraps

import encoder
from database import DatabaseClient

app = flask.Flask(__name__)
app.json_encoder = encoder.MongoEncoder
app.config['SECRET_KEY'] = secrets.token_bytes()
DatabaseClient.initialize_client()

def verify_login(f):
    """
    Decorator to verify that users are logged in before attempting 
    board operations.
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        if not session.get("userID"):
            flask.flash("You must be logged in to continue.")
            return flask.redirect(flask.url_for("signin"))
        return f(*args, **kwds)
    return wrapper

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/api/signup", methods = ["GET", "POST"])
def signup():
    """
    Registers a new user in the database, if there is no account
    currently associated with the username.
    """
    if "username" not in request.json:
        return make_response(
            jsonify({"message": "User did not supply a username", "authenticated": False}), 401
        )
    elif "password" not in request.json:
        return make_response(
            jsonify({"message": "User did not supply a username", "authenticated": False}), 401
        )

    username = request.json["username"]
    password = request.json["password"]

    users = DatabaseClient.connect("users")

    if users.count_documents({"username": username}) != 0:
        return make_response(
            jsonify({"message": "There is already an account registered under this username", "authenticated": False}), 401
        )

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = {
        "username": username,
        "hashed_pwd": hashed,
        "board_ids": [],
        "board_names": []
    }

    result = users.insert_one(new_user)
    if not result.acknowledged:
        return make_response(
            jsonify({"message": "Failed to initialize new user", "authenticated": False}), 401
        )

    current_user = users.find_one({"username": username})
    if not current_user:
        return make_response(
            jsonify({"message": "Incorrect username or password", "authenticated": False}), 401
        )

    session['userID'] = current_user["_id"]
    return make_response(jsonify({"message": "", "authenticated": True}), 200)

@app.route("/api/signin", methods = ["GET", "POST"])
def signin():
    """
    Signs user into the application, if they have already signed up.
    """
    if 'userID' in session:
        return make_response(
            jsonify({"message": "User is already logged in!", "authenticated": True}), 200
        )

    if "username" not in request.json:
        return make_response(
            jsonify({"message": "User did not supply a username", "authenticated": False}), 401
        )

    elif "password" not in request.json:
        return make_response(
            jsonify({"message": "User did not supply a password", "authenticated": False}), 401
        )

    username = request.json["username"]
    password = request.json["password"]

    users = DatabaseClient.connect("users")
    
    current_user = users.find_one({"username": username})
    if not current_user:
        return make_response(
            jsonify({"message": "Incorrect username or password", "authenticated": False}), 401
        )
    if not bcrypt.checkpw(password.encode("utf-8"), current_user.get("hashed_pwd")):
        return make_response(
            jsonify({"message": "Incorrect username or password", "authenticated": False}), 401
        )

    session['userID'] = current_user["_id"]
 
    return jsonify({"message": "OK", "authenticated": True})

@app.route("/api/signout", methods = ["GET", "POST"])
@verify_login
def signout():
    """
    Signs user out of the application, if they are currently signed in.
    """
    session.pop("session", None)
    session.pop("userID", None)
    return make_response(jsonify({"message": "You have been logged out successfully."}), 200)
    
@app.route("/api/boards", methods = ["GET"])
@verify_login
def view_boards():
    """
    Loads all of a users' boards onto a single page to view.
    """
    userid = session["userID"]
    
    users = DatabaseClient.connect("users")
    boards = DatabaseClient.connect("boards")
    boards.create_index("userID")

    current_user = users.find_one({"_id": ObjectId(userid)})
    if not current_user:
        return make_response(jsonify({"message": "ERROR: User does not exist"}), 500)

    user_boards = []
    user_boardIDs = current_user["board_ids"]
    for boardID in user_boardIDs:
        board = boards.find_one({"_id": boardID})
        if not board:
            return make_response(jsonify({"message": "ERROR: Board does not exist"}), 400)
        user_boards.append(board)
    
    response = make_response(jsonify(user_boards), 200)
    return response

@app.route("/api/boards/new", methods = ["GET", "POST"])
@verify_login
def create_board():
    """
    Creates a new board for the logged in user. Fails if the given
    board name already exists for the user.
    """
    userid = session["userID"]
    board_name = request.json["board_name"]
    info = request.json["info"]
    
    users = DatabaseClient.connect("users")
    boards = DatabaseClient.connect("boards")

    current_user = users.find_one({"_id": ObjectId(userid)})
    if not current_user:
        return make_response(
            jsonify({"message": "Error identifying the user"}), 401
        )

    curr_board_names = current_user["board_names"]
    if board_name in curr_board_names:
        return make_response(
            jsonify({"message": "User has board with same name"}), 400
        )

    new_board = {
        "board_name": board_name,
        "userID": userid,
        "info": info,
        "lists": {
            "todo": [],
            "in_progress": [],
            "done": []
        }
    }

    # To consider: possibly frame this as a single transaction to avoid being partially completed

    insert_result = boards.insert_one(new_board)
    if not insert_result.acknowledged:
        return make_response(
            jsonify({"message": "Error creating the board"}), 500
        )
    board_id = insert_result.inserted_id
    update_result = users.update_one({"_id": ObjectId(userid)}, 
        {"$push": {"board_ids": board_id, "board_names": board_name}})
    if not update_result.acknowledged:
        return make_response(
            jsonify({"message": "Error creating the board"}), 500
        )

    return make_response(jsonify({"message": "Successfully created new board"}), 201)

@app.route("/api/boards/<board_name>", methods = ["GET"])
@verify_login
def get_board(board_name):
    """
    Loads a board for the logged in user. Fails if the given
    board name does not exist for the user.
    """
    userid = session["userID"]

    users = DatabaseClient.connect("users")
    boards = DatabaseClient.connect("boards")

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

@app.route("/api/boards/<board_id>/new", methods = ["GET", "POST"])
@verify_login
def add_item(board_id):
    """
    Adds a new item to the specified board, if it exists. By default,
    adds the item to the todo board.
    """
    userid = session["userID"]

    title = request.args["title"]
    description = request.args["description"]

    boards = DatabaseClient.connect("boards")

    current_board = boards.find_one({"_id": ObjectId(board_id)})
    if current_board["userID"] != userid:
        return "ERROR: you do not have acccess to this board!"

    new_item = {
        "_id": ObjectId(),
        "title": title,
        "description": description,
        "status": "todo"
    }

    update_result = boards.update_one({"_id": ObjectId(board_id)}, 
        {"$push": {"lists.todo": new_item}})
    if not update_result.acknowledged:
        return "ERROR: failed to add new item to board"

    return "Successfully added new item"


@app.route("/api/boards/<board_id>/<category>/<item_id>", methods = ["GET"])
@verify_login
def view_item(board_id, category, item_id):
    """
    View the item with the provided item id in the specified board,
    if the board exists and the item id is present in the category.
    """
    userid = session["userID"]

    boards = DatabaseClient.connect("boards")

    current_board = boards.find_one({"_id": ObjectId(board_id)})
    if current_board["userID"] != userid:
        return "ERROR: you do not have acccess to this board!"

    for item in current_board["lists"][category]:
        if item["_id"] == ObjectId(item_id):
            response = make_response(jsonify(item))
            return response
    
    return "ERROR: the item was not present in the board"

@app.route("/api/boards/<board_id>/<category>/<item_id>/update")
@verify_login
def update_item(board_id, category, item_id):
    """
    Updates the item with the provided item id in the specified board,
    if the board exists and item id is present. Can update category, 
    title, or description.
    """
    pass

