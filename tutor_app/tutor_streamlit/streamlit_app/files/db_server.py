from pymongo import MongoClient
import os
import mysql.connector



def create_connection(database_name):
    """
    Creates a connection to a MongoDB database.

    Args:
        database_name (str): The name of the database to connect to.

    Returns:
        pymongo.MongoClient: A MongoClient object representing the connection to the database.

    Raises:
        Exception: If an error occurs while creating the connection.
    """

    host = "replace_endpoint"
    port = 27017
    username = os.environ["db_username"]
    password = os.environ["db_password"] 

    mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/{database_name}"

    try:
        client = MongoClient(mongo_uri)
    except Exception:
        print("ERROR")

    return client


def create_connection_sql(db_name):
    """
    Creates a connection to a MySQL database.

    Args:
        db_name (str): The name of the database to connect to.

    Returns:
        tuple: A tuple containing the connection object and the cursor object.

    Raises:
        Exception: If an error occurs while creating the connection.
    """
    try:
        rds_endpoint = os.environ["rds_endpoint"]
        username = os.environ["sql_username"]
        password = os.environ["sql_password"]
    except Exception:
       print('CREDENTIALS ERROR') 
       return 0

    connection = mysql.connector.connect(
            host=rds_endpoint,
            user=username,
            password=password,
            port=3306,
            connect_timeout=10,
            database=db_name
        )

    return connection, connection.cursor()


def make_request(req, db_name):
    connection, cursor = create_connection_sql(db_name)
    cursor.execute(req)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return res