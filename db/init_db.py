from .connector import initialize_database
def main():
    print("Initializing database...")
    initialize_database()
    # The success message is now printed inside initialize_database()
if __name__ == "__main__":
    main()