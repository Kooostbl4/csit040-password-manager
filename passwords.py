import bcrypt
from menu import start_menu
from database import get_user_id

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print(hashed_password)

    return hashed_password

def add_password(conn):
    name = input("Enter service name: ")
    password = input("Enter password: ")
    repeat = input("Repeat password: ")

    while password != repeat:
        print("Passwords do not match, please try again")
        password = input("Enter password: ")
        repeat = input("Repeat password: ")

    hashed_password = hash_password(password)
    user_id = get_user_id(conn)

    db = conn.cursor()
    query = "INSERT INTO passwords (name, password, owner) VALUES (%s, %s, %s)"
    values = (name, hashed_password, user_id)

    


    

def get_password():
    ...

def change_password():
    ...

def delete_password():
    ...