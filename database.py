import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("PASSWORD"),
            database='password_manager',
            port=3306
        )
        
        return conn
    
    except mysql.connector.Error as err:
        print(f"Error while connecting to database: {err}")

def get_user_id(conn):
    try:
        db = conn.cursor();
        db.execute("SELECT id FROM users WHERE status='in'")
        user_id = db.fetchone();

        return list(user_id)[0]
    
    except mysql.connector.Error as err:
        print(f"Error while getting user id: {err}")