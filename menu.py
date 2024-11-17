from users import register, login, logout
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
            print("3. Change password")
            print("4. Delete password")
            print("5. List of your passwords")
            print("6. Log out")
            print("7. Exit") 

            choice = input("Enter your choice: ")

            while choice not in ["1", "2", "3", "4", "5", "6", "7"]:
                print("Invalid choice, please enter 1-7")
                choice = input("Enter your choice: ")

            if choice == "1":
                status = add_password(conn)

                if status == "success":
                    print("\nPassword added successfully!\n")
                    start_menu(conn, "logged_in")

                elif status == "cancel":
                    start_menu(conn, "logged_in")

                else:
                    print("\nFailed to add password\n")
                    start_menu(conn, "logged_in")

            elif choice == "2":
                status = get_password(conn)

                if status == "success":
                    start_menu(conn, "logged_in")

                else:
                    print("\nFailed to find password\n")
                    start_menu(conn, "logged_in")

            elif choice == "3":
                status = change_password(conn)

                if status == "success":
                    start_menu(conn, "logged_in")

                else:
                    print("\nFailed to change password\n")
                    start_menu(conn, "logged_in")

            elif choice == "4":
                status = delete_password(conn)

                if status == "success":
                    start_menu(conn, "logged_in")

                else:
                    print("\nFailed to delete password\n")
                    start_menu(conn, "logged_in")

            elif choice == "5":
                status = all_passwords(conn)

                if status == "success":
                    start_menu(conn, "logged_in")

                else:
                    print("\nFailed to get the list of passwords\n")
                    start_menu(conn, "logged_in")

            elif choice == "6":
                status = logout(conn)

                if status == "success":
                    print("\nLogged out successfully!\n")
                    start_menu(conn, "logged_out")

                else:
                    start_menu(conn, "logged_in")

            elif choice == "7":
                print("\nExiting...\n")
                return

        elif status == "logged_out":
            print("You are not logged in\n")
            print("1. Log in")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice: ")

            while choice not in ["1", "2", "3", "4", "5", "6"]:
                print("Invalid choice, please enter 1-3")
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

            elif choice == "3":
                print("\nExiting...\n")
                return

    except:
        print("An error occurred")
        start_menu(conn, "logged_out")