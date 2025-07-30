from passlib.context import CryptContext
from db.models import User
from db.connector import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthManager:
    def __init__(self, db_session):
        self.db = db_session

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_user(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, name, email, password):
        if self.get_user(email):
            return None # User already exists
        hashed_password = self.get_password_hash(password)
        db_user = User(name=name, email=email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, email, password):
        user = self.get_user(email)
        if not user:
            return None # User not found
        if not self.verify_password(password, user.hashed_password):
            return None # Invalid password
        return user
