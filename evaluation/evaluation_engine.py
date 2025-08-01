from sqlalchemy import func
from db.models import Feedback, ChatLog

class EvaluationEngine:
    def __init__(self, db_session):
        self.db = db_session

    def get_average_feedback_rating(self):
        """
        Calculates the average feedback rating from the feedback table.
        """
        avg_rating = self.db.query(func.avg(Feedback.rating)).scalar()
        return avg_rating if avg_rating is not None else 0

    def get_risk_flag_count(self):
        """
        Counts the number of interactions that triggered the safety guardrails.
        """
        risk_count = self.db.query(func.count(ChatLog.id)).filter(ChatLog.risk_flag == True).scalar()
        return risk_count

    def get_total_interactions(self):
        """
        Counts the total number of logged interactions.
        """
        total_interactions = self.db.query(func.count(ChatLog.id)).scalar()
        return total_interactions

    def run_evaluation(self):
        """
        Runs all evaluation metrics and returns a summary report.
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
