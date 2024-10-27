import mysql.connector
import bcrypt
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from database import get_user_id

load_dotenv()

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def encrypt_password(password):
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())

    return encrypted_password

def decrypt_password(encrypted_password):
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)

    return decrypted_password

def add_password(conn):
    try:
        name = input("Enter service name: ")
        password = input("Enter password: ")
        repeat = input("Repeat password: ")

        while password != repeat:
            print("Passwords do not match, please try again")
            password = input("Enter password: ")
            repeat = input("Repeat password: ")

        encrypted_password = encrypt_password(password)
        user_id = get_user_id(conn)

        db = conn.cursor()
        query = "INSERT INTO passwords (name, password, owner) VALUES (%s, %s, %s)"
        values = (name, encrypt_password, user_id)

        db.execute(query, values)
        conn.commit()

        return "success"

    except mysql.connector.Error as err:
        print(f"Error while adding password: {err}")
    

def get_password():
    ...

def change_password():
    ...

def delete_password():
    ...