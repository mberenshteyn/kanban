from pymongo import MongoClient
import configparser

def initialize_client():
    """
    Initializes a MongoClient based on the username, password, and database
    name stored in the config.ini file.
    """

    config = configparser.ConfigParser()
    config.read("config.ini")

    username = config["mongodb"]["user"]
    password = config["mongodb"]["password"]
    dbname = config["mongodb"]["dbname"]

    print("Attempting to initialize client ...")
    client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.kcedc.mongodb.net/{dbname}?retryWrites=true&w=majority")
    print("Successfully initialized client")

    return client

def connect(collection: str, db = "test"):
    """
    Initializes the MongoDB client and connects to a specific collection in the client.
    """
    return client[db][collection]

client = initialize_client()