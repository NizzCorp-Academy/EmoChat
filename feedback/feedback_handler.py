"""
Module: feedback_handler
Author: Arshad
Date: 29-07-2025
Purpose: To handle user feedback.
"""
from db.models import Feedback
class FeedbackHandler:
    """
    Class: FeedbackHandler
    Author: Arshad
    Date: 29-07-2025
    Purpose: To handle user feedback.
    """
    def __init__(self, db_session):
        """
        Function: __init__
        Author: Arshad
        Date: 029-07-2025
        Purpose: To initialize the FeedbackHandler.
        Params: db_session
        Returns: None
        """
        self.db = db_session
    def save_feedback(self, user_id, chat_log_id, rating, comment):
        """
        Function: save_feedback
        Author: Arshad
        Date: 29-07-2025
        Purpose: To save user feedback to the database.
        Params: int user_id, int chat_log_id, int rating, str comment
        Returns: Feedback
        """
        db_feedback = Feedback(
            user_id=user_id,
            chat_log_id=chat_log_id,
            rating=rating,
            comment=comment
        )
        self.db.add(db_feedback)
        self.db.commit()
        self.db.refresh(db_feedback)
        return db_feedback
# Example usage:
if __name__ == '__main__':
    from db.connector import get_db
    from db.models import User, ChatLog
    db = next(get_db())
    # Create a dummy user and chat log for testing
    if not db.query(User).first():
        test_user = User(name="Test User", email="test@example.com", hashed_password="test")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
    else:
        test_user = db.query(User).first()
    if not db.query(ChatLog).first():
        test_log = ChatLog(user_id=test_user.id, prompt="Hello", response="Hi there!")
        db.add(test_log)
        db.commit()
        db.refresh(test_log)
    else:
        test_log = db.query(ChatLog).first()
    handler = FeedbackHandler(db)
    feedback = handler.save_feedback(test_user.id, test_log.id, 5, "Very helpful!")
    print(f"Saved feedback with ID: {feedback.id}")
