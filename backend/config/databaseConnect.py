import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DB_HOST = os.getenv('MYSQLHOST')
DB_PORT = int(os.getenv('MYSQLPORT'))  # convert to int because it's a port number
DB_USER = os.getenv('MYSQLUSER')
DB_PASSWORD = os.getenv('MYSQLPASSWORD')
DB_NAME = os.getenv('MYSQLDATABASE')

# Establish a connection to the database
try:
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    print("Connected to the database!")
except Exception as e:
    print(f"Error connecting to the database: {e}")