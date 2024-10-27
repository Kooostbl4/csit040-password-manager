from database import connect_to_database    
from menu import start_menu

def main():
    conn = connect_to_database()
    start_menu(conn)

if __name__ == "__main__":
    main()