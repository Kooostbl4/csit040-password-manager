import mysql.connector
import bcrypt
from passwords import hash_password, generate_strong_password, make_stronger_password, check_passwords

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

        if not check_passwords(password):
            print("\nYour password is too weak. There must have at least:\n8 characters\n1 capital letter\n1 digit\n1 special character\n")
            print("1. Randomly generate strong password")
            print("2. Make your password stronger autimatically")

            choice = input("Enter your choice: ")

            while choice not in ["1", "2"]:
                print("Invalid choice, please enter 1 or 2")
                choice = input("Enter your choice: ")

            if choice == "1":
                password = generate_strong_password()

                print(f"Your password is {password}")

            elif choice == "2":
                password = make_stronger_password(password)

                print(f"Your password is {password}")
            

        hashed_password = hash_password(password)

        db = conn.cursor()
        db.execute("UPDATE users SET status = 'out'")
        conn.commit()

        query = "INSERT INTO users (username, password, status) VALUES (%s, %s, %s)"
        values = (username, hashed_password, "in")

        db.execute(query, values)
        conn.commit()
        db = conn.cursor()
        return "success"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        


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

                user_id = user[0]
                db.execute("UPDATE users SET status = 'out'")
                conn.commit()   
                
                query = "UPDATE users SET status='in' WHERE id=%s"
                values = (user_id,)
                db.execute(query, values)
                conn.commit()

                return "success"
            else:
                print("Login failed: incorrect password")

        else:
            print("User not found")

    except Exception as e:
        print("Login failed:", str(e))


def logout(conn):
    try:
        choice = input("Are you sure you want to log out? (y/n): ")

        while choice not in ["y", "n"]:
            print("Invalid choice. Please enter 'y' or 'n': ")
            choice = input("Are you sure you want to log out? (y/n): ")

        if choice == "y":
            query = "UPDATE users SET status = 'out'"
            db = conn.cursor()
            db.execute(query)
            conn.commit()

            print("Successfully logged out")
            input("Press Enter to continue...")

            return "success"

    except:
        print("An error occurred while attempting to log out.")
        return
