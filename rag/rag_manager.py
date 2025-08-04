"""
Module: rag_manager
Author: Shuaib
Date: 28-07-2025
Purpose: To manage the Retrieval-Augmented Generation (RAG) pipeline.
"""
from rag.retriever_sql import SQLRetriever
from rag.embedder import Embedder
from rag.search_vector import VectorSearcher
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
        self.retriever = SQLRetriever(db_session)
        self.embedder = Embedder()
    def get_context(self, query: str, top_k: int = 2):
        """
        Function: get_context
        Author: Shuaib
        Date: 28-07-2025
        Purpose: To orchestrate the RAG pipeline to retrieve the most relevant context for a query.
        Params: str query, int top_k
        Returns: str
        """
        # 1. Retrieve initial candidates from SQL
        retrieved_docs = self.retriever.retrieve(query, top_k=10) # Get a larger pool first
        if not retrieved_docs:
            return None
        # 2. Embed the retrieved documents and the query
        doc_texts = [doc.content_chunk for doc in retrieved_docs]
        doc_embeddings = self.embedder.embed(doc_texts)
        query_embedding = self.embedder.embed([query])
        # 3. Perform vector search to find the best matches
        searcher = VectorSearcher(dimension=doc_embeddings.shape[1])
        searcher.create_index(doc_embeddings)
        distances, indices = searcher.search(query_embedding, top_k=top_k)
        # 4. Compile the context from the top-k documents
        context = "\n".join([doc_texts[i] for i in indices[0]])
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
