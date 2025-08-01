from .connector import create_tables
if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Tables created successfully.")