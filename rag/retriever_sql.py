"""
Module: retriever_sql
Author: Shuaib
Date: 29-07-2025
Purpose: To retrieve knowledge base articles from the database.
"""
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import or_
from db.models import KnowledgeBase
class SQLRetriever:
    """
    Class: SQLRetriever
    Author: Shuaib
    Date: 29-07-2025
    Purpose: To retrieve knowledge base articles from the database.
    """
    def __init__(self, db_session):
        """
        Function: __init__
        Author: Shuaib
        Date: 29-07-2025
        Purpose: To initialize the SQLRetriever.
        Params: db_session
        Returns: None
        """
        self.db = db_session
    def retrieve(self, query: str, top_k: int = 5):
        """
        Function: retrieve
        Author: Shuaib
        Date: 29-07-2025
        Purpose: To retrieve knowledge base articles by searching for keywords in the title or tags.
        Params: str query, int top_k
        Returns: list
        """
        search_term = f"%{query}%"
        results = (
            self.db.query(KnowledgeBase)
            .filter(
                or_(
                    KnowledgeBase.title.ilike(search_term),
                    KnowledgeBase.tags.ilike(search_term),
                    KnowledgeBase.content_chunk.ilike(search_term)
                )
            )
            .limit(top_k)
            .all()
        )
        return results
# Example usage:
if __name__ == '__main__':
    from db.connector import get_db
    # Add some sample data
    db = next(get_db())
    if db.query(KnowledgeBase).count() == 0:
        print("Adding sample knowledge base data...")
        sample_data = [
            KnowledgeBase(title="Understanding Anxiety", content_chunk="Anxiety is a feeling of unease, such as worry or fear, that can be mild or severe.", tags="anxiety, worry, fear"),
            KnowledgeBase(title="Coping with Stress", content_chunk="Deep breathing exercises and mindfulness can help manage stress.", tags="stress, coping, mindfulness"),
            KnowledgeBase(title="The Importance of Sleep", content_chunk="Getting enough quality sleep is vital for mental and physical health.", tags="sleep, health, wellness")
        ]
        db.add_all(sample_data)
        db.commit()
        print("Sample data added.")
    retriever = SQLRetriever(db)
    retrieved_docs = retriever.retrieve("anxiety")
    print(f"Found {len(retrieved_docs)} documents for 'anxiety':")
    for doc in retrieved_docs:
        print(f"- {doc.title}")
