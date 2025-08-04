"""
Module: init_db
Author: Shuaib
Date: 27-07-2025
Purpose: To initialize the database.
"""
from .connector import initialize_database
def main():
    """
    Function: main
    Author: Shuhaib
    Date: 04-08-2025
    Purpose: Main function to initialize the database.
    Params: None
    Returns: None
    """
    print("Initializing database...")
    initialize_database()
    # The success message is now printed inside initialize_database()
if __name__ == "__main__":
    main()
