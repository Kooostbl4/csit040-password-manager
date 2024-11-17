import bcrypt
from database import get_user_id
from cryptography.fernet import Fernet
from dotenv import load_dotenv 
import os
import re
import random
import string

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
    
def check_passwords(password):
    # Check if password has at least 8 characters
    if len(password) < 8:
        return False
    # Check if password has at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    # Check if password has at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    # Check if password has at least one digit
    if not re.search(r'[0-9]', password):
        return False
    # Check if password has at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def generate_strong_password(length=20):
    if length < 12:
        raise ValueError("Password length should be at least 12 characters for strong security.")
    
    # Character sets for different password requirements
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    
    # Ensure the password has at least one of each required character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_characters)
    ]
    
    # Fill the rest of the password length with a random choice of all character types
    all_characters = lowercase + uppercase + digits + special_characters
    password += random.choices(all_characters, k=length - 4)
    
    # Shuffle the password list to make the pattern unpredictable
    random.shuffle(password)
    
    # Join the list into a string
    return ''.join(password)

def make_stronger_password(password):
    # Dictionary to map letters to "stronger" characters
    substitutions = {
        'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'
    }
    
    # List to hold the transformed password characters
    stronger_password = []
    
    # Apply substitutions and random capitalization
    for char in password:
        # Substitute some characters
        if char.lower() in substitutions:
            char = substitutions[char.lower()]
        
        # Randomly capitalize some letters
        if char.isalpha() and random.choice([True, False]):
            char = char.upper()
        
        # Append the modified character to the list
        stronger_password.append(char)
    
    # Ensure the modified password has at least one digit and one special character
    if not any(char.isdigit() for char in stronger_password):
        stronger_password.append(random.choice(string.digits))
    if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in stronger_password):
        stronger_password.append(random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?/"))

    # If the password is still too short, add random characters until it reaches 10 characters
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    while len(stronger_password) < 10:
        stronger_password.append(random.choice(all_characters))
    
    return ''.join(stronger_password)


def add_password(conn):
    try:
        user_id = get_user_id(conn)
        service_name = input("Enter service name: ")

        db = conn.cursor()
        query = "SELECT name FROM passwords WHERE name = %s AND owner = %s"
        values = (service_name, user_id)
        db.execute(query, values)

        existance = db.fetchone()

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

        if not check_passwords(password):
            print("\nYour password is too weak, are you sure?\n")
            print("1. Generate strong password")
            print("2. Make your password stronger autimatically")
            print("3. Keep this password")

            choice = input("Enter your choice: ")

            while choice not in ["1", "2", "3"]:
                print("Invalid choice, please enter 1, 2, or 3")
                choice = input("Enter your choice: ")

            if choice == "1":
                password = generate_strong_password()
                
                print(f"Your password is {password}")

            elif choice == "2":
                password = make_stronger_password(password)

                print(f"Your password is {password}")

            elif choice == "3":
                pass

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
        db = conn.cursor()

        old_password = input("Enter your old password: ")
        
        if verify_password(service_name, old_password, conn):
            new_password = input("Enter your new password: ")
            repeat_password = input("Repeat your new password: ")
            
            while new_password != repeat_password:
                print("Passwords do not match, please try again")
                new_password = input("Enter your new password: ")
                repeat_password = input("Repeat your new password: ")

            if not check_passwords(new_password):
                print("\nYour password is too weak, are you sure?\n")
                print("1. Generate strong password")
                print("2. Make your password stronger autimatically")
                print("3. Keep this password")

                choice = input("Enter your choice: ")

                while choice not in ["1", "2", "3"]:
                    print("Invalid choice, please enter 1, 2, or 3")
                    choice = input("Enter your choice: ")

                if choice == "1":
                    new_password = generate_strong_password()
                    
                    print(f"Your password is {new_password}")

                elif choice == "2":
                    new_password = make_stronger_password(new_password)

                    print(f"Your password is {new_password}")

                elif choice == "3":
                    pass

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

def all_passwords(conn):
    try:
        user_id = get_user_id(conn)

        db = conn.cursor()
        query = "SELECT name, password FROM passwords WHERE owner = %s"
        values = (user_id,)
        db.execute(query, values)

        passwords = list(db.fetchall())
        # print(passwords)
        print()
        for password in passwords:
            print(f"{password[0]: <20} {decrypt_password(password[1]): >40}")

        input("\nPress Enter to continue...")

        return "success"

    except:
        print("An error occured while getting all passwords")
        return