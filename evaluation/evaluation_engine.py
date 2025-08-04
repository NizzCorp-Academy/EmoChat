"""
Module: evaluation_engine
Author: Shuaib
Date: 03-08-2025
Purpose: To provide an engine for evaluating the chatbot's performance.
"""
from sqlalchemy import func
from db.models import Feedback, ChatLog

class EvaluationEngine:
    """
    Class: EvaluationEngine
    Author: Shuhaib
    Date: 04-08-2025
    Purpose: To provide an engine for evaluating the chatbot's performance.
    """
    def __init__(self, db_session):
        """
        Function: __init__
        Author: Shuhaib
        Date: 04-08-2025
        Purpose: To initialize the EvaluationEngine.
        Params: db_session
        Returns: None
        """
        self.db = db_session

    def get_average_feedback_rating(self):
        """
        Function: get_average_feedback_rating
        Author: Shuhaib
        Date: 04-08-2025
        Purpose: To calculate the average feedback rating from the feedback table.
        Params: None
        Returns: float
        """
        avg_rating = self.db.query(func.avg(Feedback.rating)).scalar()
        return avg_rating if avg_rating is not None else 0

    def get_risk_flag_count(self):
        """
        Function: get_risk_flag_count
        Author: Shuhaib
        Date: 04-08-2025
        Purpose: To count the number of interactions that triggered the safety guardrails.
        Params: None
        Returns: int
        """
        risk_count = self.db.query(func.count(ChatLog.id)).filter(ChatLog.risk_flag == True).scalar()
        return risk_count

    def get_total_interactions(self):
        """
        Function: get_total_interactions
        Author: Shuhaib
        Date: 04-08-2025
        Purpose: To count the total number of logged interactions.
        Params: None
        Returns: int
        """
        total_interactions = self.db.query(func.count(ChatLog.id)).scalar()
        return total_interactions

    def run_evaluation(self):
        """
        Function: run_evaluation
        Author: Shuhaib
        Date: 04-08-2025
        Purpose: To run all evaluation metrics and return a summary report.
        Params: None
        Returns: dict
        """
        avg_rating = self.get_average_feedback_rating()
        risk_count = self.get_risk_flag_count()
        total_interactions = self.get_total_interactions()

        report = {
            "average_feedback_rating": f"{avg_rating:.2f}",
            "total_interactions": total_interactions,
            "guardrail_triggered_count": risk_count,
            "guardrail_trigger_rate": f"{(risk_count / total_interactions * 100) if total_interactions > 0 else 0:.2f}%"
        }
        return report

# Example usage:
if __name__ == '__main__':
    from db.connector import get_db

    db = next(get_db())
    engine = EvaluationEngine(db)
    evaluation_report = engine.run_evaluation()

    print("--- Evaluation Report ---")
    for key, value in evaluation_report.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("-------------------------")
