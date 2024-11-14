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
    

def verify_password(service_name, password, conn):
    try:
        user_id = get_user_id(conn)

        db = conn.cursor()
        query = "SELECT password FROM passwords WHERE name = %s AND owner = %s"
        values = (service_name, user_id)

        db.execute(query, values)
        result = db.fetchone()

        if password == decrypt_password(result[0]):
            return True

    except:
        print("An error occurred while verifying the password")
        return False

def add_password(conn):
    try:
        user_id = get_user_id(conn)
        service_name = input("Enter service name: ")

        db = conn.cursor()
        query = "SELECT name FROM passwords WHERE name = %s AND owner = %s"
        values = (service_name, user_id)
        db.execute(query, values)

        existance = db.fetchone()
        # db.commit()

        if existance:
            print("\nService name already exists for the current user.\n")
            choice = input("\nDo you want to change this password? (y/n): ")

            while choice not in ["y", "n"]:
                print("Invalid choice, please enter 'y' or 'n'")
                choice = input("Do you want to change this password? (y/n): ")

            if choice == "y":
                change_password(conn)

            else:
                return "cancel"

        password = input("Enter password: ")
        repeat = input("Repeat password: ")

        while password != repeat:
            print("Passwords do not match, please try again")
            password = input("Enter password: ")
            repeat = input("Repeat password: ")

        encrypted_password = encrypt_password(password)

        query = "INSERT INTO passwords (name, password, owner) VALUES (%s, %s, %s)"
        values = (service_name, encrypted_password, user_id)

        db.execute(query, values)
        conn.commit()

        print("\nPassword added successfully!\n")
        input("Press enter to continue...")

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
            input("Press Enter to continue...")

    except:
        print("An error occurred while retrieving the password")
        input("Press Enter to continue...")
        return


def change_password(conn):
    try:
        service_name = input("Enter service name: ")
        user_id = get_user_id(conn)

        old_password = input("Enter your old password: ")
        
        if verify_password(service_name, old_password, conn):
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
            


def delete_password(conn):
    try:
        service_name = input("Enter service name: ")
        password = input("Enter password: ")

        if verify_password(service_name, password, conn):
            choice = input("Are you sure? (y/n): ")

            while choice not in ["y", "n"]:
                print("Invalid choice, please enter 'y' or 'n'")
                choice = input("Are you sure? (y/n): ")

            if choice == "y":
                user_id = get_user_id(conn)
                
                db = conn.cursor()
                query = "DELETE FROM passwords WHERE name = %s AND owner = %s"

                values = (service_name, user_id)
                db.execute(query, values)
                conn.commit()

                print("\nPassword deleted successfully\n")
                input("Press Enter to continue...")

                return "success"
            
            elif choice == "n":
                return

        else:
            print("Incorrect password")
            return

    except:
        print("An error occurred while deleting the password")
        return