"""
Module: chat_logger
Author: Arshad
Date: 30-07-2025
Purpose: To log chat interactions to the database.
"""
from db.models import ChatLog
from sqlalchemy import desc

class ChatLogger:
    """
    Class: ChatLogger
    Author: Arshad
    Date: 30-07-2025
    Purpose: To log chat interactions to the database.
    """
    def __init__(self, db_session):
        """
        Function: __init__
        Author: Arshad
        Date: 30-07-2025
        Purpose: To initialize the ChatLogger.
        Params: db_session
        Returns: None
        """
        self.db = db_session
    def log_interaction(self, user_id, prompt, response, risk_flag=False):
        """
        Function: log_interaction
        Author: Arshad
        Date: 30-07-2025
        Purpose: To log a user-chatbot interaction to the database.
        Params: int user_id, str prompt, str response, bool risk_flag
        Returns: ChatLog
        """
        db_log = ChatLog(
            user_id=user_id,
            prompt=prompt,
            response=response,
            risk_flag=risk_flag
        )
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def get_chat_history(self, user_id):
        """
        Function: get_chat_history
        Author: Arshad
        Date: 30-07-2025
        Purpose: To retrieve the chat history for a given user.
        Params: int user_id
        Returns: list
        """
        return self.db.query(ChatLog).filter_by(user_id=user_id).order_by(ChatLog.timestamp.asc()).all()
# Example usage:
if __name__ == '__main__':
    from db.connector import get_db
    from db.models import User
    db = next(get_db())
    # Create a dummy user for testing
    if not db.query(User).first():
        test_user = User(name="Test User", email="test@example.com", hashed_password="test")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
    else:
        test_user = db.query(User).first()
    logger = ChatLogger(db)
    log = logger.log_interaction(test_user.id, "Hello there!", "General Kenobi!")
    print(f"Saved chat log with ID: {log.id}")
    risky_log = logger.log_interaction(test_user.id, "I want to die", "Fallback response...", risk_flag=True)
    print(f"Saved risky chat log with ID: {risky_log.id}")
