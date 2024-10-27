import mysql.connector
import bcrypt
from menu import start_menu
from passwords import hash_password

def register(conn):
    print("Register:")

    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        password_confirmation = input("Repeat your password: ")

        while password != password_confirmation:
            print("Passwords do not match. Please try again.")
            password = input("Enter your password: ")
            password_confirmation = input("Repeat your password ")

        hashed_password = hash_password(password)

        query = "INSERT INTO users (username, password, status) VALUES (%s, %s, %s)"
        values = (username, hashed_password, "in")

        db = conn.cursor()

        db.execute(query, values)
        conn.commit()

        start_menu(conn, "logged_in")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        start_menu(conn, "logged_out")


def login(conn):
    print("Login:")

    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        query = "SELECT * FROM users WHERE username=%s"
        values = (username,)

        db = conn.cursor()
        db.execute(query, values)

        user = db.fetchone()

        if user is not None:
            stored_hash = bytes(user[2], 'utf-8')  

            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                start_menu(conn, "logged_in")
            else:
                print("Login failed: incorrect password")

        else:
            print("User not found")

    except Exception as e:
        print("Login failed:", str(e))