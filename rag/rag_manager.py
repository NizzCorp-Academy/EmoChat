"""
Module: rag_manager
Author: Shuaib
Date: 28-07-2025
Purpose: To manage the Retrieval-Augmented Generation (RAG) pipeline.
"""
import faiss
from rag.embedder import Embedder
from db.models import KnowledgeBase

class RAGManager:
    """
    Class: RAGManager
    Author: Shuaib
    Date: 28-07-2025
    Purpose: To manage the Retrieval-Augmented Generation (RAG) pipeline.
    """
    def __init__(self, db_session):
        """
        Function: __init__
        Author: Shuaib
        Date: 28-07-2025
        Purpose: To initialize the RAGManager.
        Params: db_session
        Returns: None
        """
        self.embedder = Embedder()
        
        # Load the FAISS index
        try:
            self.index = faiss.read_index("faiss_index.bin")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            print("Please run scripts/build_index.py to create the index.")
            self.index = None

        # Load all documents from the knowledge base
        self.docs = db_session.query(KnowledgeBase).all()
        self.doc_texts = [doc.content_chunk for doc in self.docs]

    def get_context(self, query: str, top_k: int = 2):
        """
        Function: get_context
        Author: Shuaib
        Date: 28-07-2025
        Purpose: To orchestrate the RAG pipeline to retrieve the most relevant context for a query.
        Params: str query, int top_k
        Returns: str
        """
        if not self.index:
            return None

        # 1. Embed the query
        query_embedding = self.embedder.embed([query])

        # 2. Search the FAISS index
        distances, indices = self.index.search(query_embedding, top_k)

        # 3. Compile the context from the top-k documents
        context = "\n".join([self.doc_texts[i] for i in indices[0]])
        return context
# Example usage:
if __name__ == '__main__':
    from db.connector import get_db
    db = next(get_db())
    rag_manager = RAGManager(db)
    # Make sure you've run retriever_sql.py to add sample data first
    query = "how can I deal with stress?"
    context = rag_manager.get_context(query)
    print(f"Query: '{query}'")
    print("\nRetrieved Context:")
    print(context)
