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

    # Create a cursor object
    cursor = conn.cursor()

    # SQL statements to create tables
    create_table_queries = [
       """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS posts (
            post_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            user_id INT,
            category_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS likes (
            like_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            post_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (post_id) REFERENCES posts(post_id)
        )
        """
    ]

    # Execute the create table queries
    for query in create_table_queries:
        cursor.execute(query)
        print("Table created successfully!")

    # SQL statements to insert dummy data
    insert_data_queries = [
        "INSERT INTO categories (name) VALUES ('Cats')",
        "INSERT INTO categories (name) VALUES ('Dogs')",
        "INSERT INTO categories (name) VALUES ('Bears')",
        "INSERT INTO users (username, email, password) VALUES ('john_doe', 'john@example.com', 'password123')",
        "INSERT INTO users (username, email, password) VALUES ('jane_smith', 'jane@example.com', 'securepassword')",
        "INSERT INTO posts (title, content, user_id, category_id) VALUES ('Introduction to Cats', 'Cats is a are really cute', 1, 1)",
        "INSERT INTO posts (title, content, user_id, category_id) VALUES ('Introduction to dogs', 'Dogs are cuter than cats', 2, 2)",
        "INSERT INTO likes (user_id, post_id) VALUES (1, 1)",
        "INSERT INTO likes (user_id, post_id) VALUES (2, 2)"
    ]

    # Execute the insert data queries
    for query in insert_data_queries:
        cursor.execute(query)
        print("Data inserted successfully!")

    # Commit the transaction
    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    # Rollback the transaction in case of error
    conn.rollback()

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
    backend/
