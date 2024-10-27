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
                status = logout(conn)

                if status == "success":
                    print("\nLogged out successfully!\n")
                    start_menu(conn, "logged_out")

                else:
                    start_menu(conn, "logged_in")

            elif choice == "6":
                print("\nExiting...\n")
                exit()

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