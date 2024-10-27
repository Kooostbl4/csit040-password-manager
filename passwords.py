import bcrypt
from database import get_user_id
from cryptography.fernet import Fernet
from dotenv import load_dotenv 
import os

load_dotenv()

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def encrypt_password(password):
    try:
        key = bytes(os.getenv("ENCRYPTION_KEY"), 'utf-8')
        f = Fernet(key)

        password = bytes(password, 'utf-8')
        encrypted_password = f.encrypt(password)
        
        return encrypted_password
    
    except Exception as e:
        print("An error occurred while encrypting the password:", str(e))
        return

def decrypt_password(encrypted_password):
    try:
        key = bytes(os.getenv("ENCRYPTION_KEY"), 'utf-8')
        f = Fernet(key)
        decrypted_password = f.decrypt(encrypted_password)
        
        return decrypted_password.decode()
    
    except Exception as e:
        print("An error occurred while decrypting the password:", str(e))
        return

def add_password(conn):
    try:
        service_name = input("Enter service name: ")
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
        values = (service_name, encrypted_password, user_id)
        print(values)

        db.execute(query, values)
        conn.commit()

        return "success"

    except:
        print("An error occurred while adding the password")
        return

def get_password(conn):
    try:
        service_name = input("Enter service name: ")
        user_id = get_user_id(conn)

        db = conn.cursor()
        query = "SELECT password FROM passwords WHERE name = %s AND owner = %s"
        values = (service_name, user_id)

        db.execute(query, values)
        result = db.fetchone()

        if result:
            decrypted_password = decrypt_password(result[0])
            print(f"\nPassword for {service_name}: {decrypted_password}\n")

            input("Press Enter to continue...")

            return "success"
        else:
            print("No matching service found")

    except:
        print("An error occurred while retrieving the password")
        return


def change_password(conn):
    try:
        service_name = input("Enter service name: ")
        user_id = get_user_id(conn)

        old_password = input("Enter your old password: ")

        db = conn.cursor()
        query = "SELECT password FROM passwords WHERE name = %s AND owner = %s"
        values = (service_name, user_id)

        db.execute(query, values)
        result = db.fetchone()

        if old_password == decrypt_password(result[0]):
            new_password = input("Enter your new password: ")
            repeat_password = input("Repeat your new password: ")
            
            while new_password != repeat_password:
                print("Passwords do not match, please try again")
                new_password = input("Enter your new password: ")
                repeat_password = input("Repeat your new password: ")

            encrypted_password = encrypt_password(new_password)

            query = "UPDATE passwords SET password = %s WHERE name = %s AND owner = %s"
            values = (encrypted_password, service_name, user_id)
            db.execute(query, values)
            conn.commit()

            print("\nPassword changed successfully\n")
            input("Press Enter to continue...")
            
            return "success"

        else:
            print("Incorrect old password")
            return

    except:
        print("An error occurred while changing the password")
        return
            


def delete_password():
    ...