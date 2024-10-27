from users import register, login
from passwords import *

def start_menu(conn, status="logged_out"):
    try:
        print("-"*100)
        print("Welcome to Password Manager!")
        print("-"*100)

        if status == "logged_in":
            print("What do you want to do?\n")
            print("1. Add new password")
            print("2. Look up the password")
            print("3. Delete password")
            print("4. Change password")
            print("5. Log out")
            print("6. Exit") 

            choice = input("Enter your choice: ")

            if choice == "1":
                status = add_password(conn)

                if status == "success":
                    print("\nPassword added successfully!\n")
                    start_menu(conn, "logged_in")

                else:
                    print("\nFailed to add password\n")
                    start_menu(conn, "logged_in")

        elif status == "logged_out":
            print("You are not logged in\n")
            print("1. Log in")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                status = login(conn)

                if status == "success":
                    print("\nLogged in successfully!\n")
                    start_menu(conn, "logged_in")

            elif choice == "2":
                status = register(conn)

                if status == "success":
                    print("\nRegistration successful!\n")
                    start_menu(conn, "logged_in")

    except:
        print("An error occurred")
        start_menu(conn, "logged_out")