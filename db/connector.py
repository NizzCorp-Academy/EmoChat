"""
Module: connector
Author: Shuaib
Date: 26-07-2025
Purpose: To provide a connector to the database.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
# --- Configuration Loading ---
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
# --- Database Engine and Session ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# --- Database Initialization and Dependency ---
def initialize_database():
    """
    Function: initialize_database
    Author: Shuaib
    Date: 26-07-2025
    Purpose: To ensure the database and all tables exist before the app starts.
    Params: None
    Returns: None
    """
    try:
        # 1. Connect to the server, not a specific database
        server_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"
        server_engine = create_engine(server_url)
        # 2. Create the database if it doesn't exist
        with server_engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}"))
        # 3. Now, connect to the specific database and create all tables
        #    This uses the main 'engine' which is bound to our DB.
        #    The models that inherit from 'Base' will be registered here.
        from . import models # Important: ensures models are registered with Base
        Base.metadata.create_all(bind=engine)
        print("Database and tables initialized successfully.")
    except OperationalError as e:
        print(f"DB connection error: {e}. Please check MySQL server and .env config.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during DB initialization: {e}")
        raise
def get_db():
    """
    Function: get_db
    Author: Shuaib
    Date: 26-07-2025
    Purpose: Dependency to get a DB session for each request.
    Params: None
    Returns: Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
