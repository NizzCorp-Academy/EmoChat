from db.models import Feedback
class FeedbackHandler:
    def __init__(self, db_session):
        self.db = db_session
    def save_feedback(self, user_id, chat_log_id, rating, comment):
        """
        Saves user feedback to the database.
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