import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

# Initialize the connection pool globally
db_pool = None

def init_pool():
    global db_pool
    if db_pool is None:
        db_pool = pooling.MySQLConnectionPool(
            pool_name="dock_pool",
            pool_size=10,
            pool_reset_session=True,
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USERNAME"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_NAME")
        )

def get_db_connection():
    """Returns a connection from the connection pool.
    Caller must close the connection when done to return it to the pool.
    """
    global db_pool
    if db_pool is None:
        init_pool()
    return db_pool.get_connection()