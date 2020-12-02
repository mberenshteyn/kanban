from pymongo import MongoClient
import configparser

class DatabaseClient:
    client = None

    @classmethod
    def initialize_client(cls, db = "test"):
        """
        Initializes a MongoClient based on the supplied database and the 
        username, password, and database name stored in the config.ini file.
        """

        config = configparser.ConfigParser()
        config.read("config.ini")

        username = config["mongodb"]["user"]
        password = config["mongodb"]["password"]
        dbname = config["mongodb"]["dbname"]

        print("Attempting to initialize client ...")
        DatabaseClient.client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.kcedc.mongodb.net/{dbname}?retryWrites=true&w=majority")[db]
        print("Successfully initialized client")

    @classmethod
    def connect(cls, collection: str):
        """
        Initializes the MongoDB client and connects to a specific collection in the client.
        """
        if DatabaseClient.client is None:
            DatabaseClient.client = DatabaseClient.initialize_client()
        return DatabaseClient.client[collection]