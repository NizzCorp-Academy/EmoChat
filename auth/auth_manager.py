"""
Module: auth_manager
Author: Adhil
Date: 27-07-2025
Purpose: To manage user authentication.
"""
from passlib.context import CryptContext
from db.models import User
from db.connector import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthManager:
    """
    Class: AuthManager
    Author: Adhil
    Date: 27-07-2025
    Purpose: To manage user authentication.
    """
    def __init__(self, db_session):
        """
        Function: __init__
        Author: Adhil
        Date: 27-07-2025
        Purpose: To initialize the AuthManager.
        Params: db_session
        Returns: None
        """
        self.db = db_session

    def get_password_hash(self, password):
        """
        Function: get_password_hash
        Author: Adhil
        Date: 27-07-2025
        Purpose: To hash a password.
        Params: str password
        Returns: str
        """
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """
        Function: verify_password
        Author: Adhil
        Date: 27-07-2025
        Purpose: To verify a password.
        Params: str plain_password, str hashed_password
        Returns: bool
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_user(self, email: str):
        """
        Function: get_user
        Author: Adhil
        Date: 27-07-2025
        Purpose: To get a user by email.
        Params: str email
        Returns: User or None
        """
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, name, email, password):
        """
        Function: create_user
        Author: Adhil
        Date: 27-07-2025
        Purpose: To create a new user.
        Params: str name, str email, str password
        Returns: User or None
        """
        if self.get_user(email):
            return None # User already exists
        hashed_password = self.get_password_hash(password)
        db_user = User(name=name, email=email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, email, password):
        """
        Function: authenticate_user
        Author: Adhil
        Date: 27-07-2025
        Purpose: To authenticate a user.
        Params: str email, str password
        Returns: User or None
        """
        user = self.get_user(email)
        if not user:
            return None # User not found
        if not self.verify_password(password, user.hashed_password):
            return None # Invalid password
        return user
