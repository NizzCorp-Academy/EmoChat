"""
Module: search_vector
Author: Shuaib
Date: 01-08-2025
Purpose: To provide a vector searcher for finding similar vectors.
"""
import faiss
import numpy as np
class VectorSearcher:
    """
    Class: VectorSearcher
    Author: Shuaib
    Date: 01-08-2025
    Purpose: To provide a vector searcher for finding similar vectors.
    """
    def __init__(self, dimension):
        """
        Function: __init__
        Author: Shuaib
        Date: 01-08-2025
        Purpose: To initialize the FAISS index.
        Params: int dimension
        Returns: None
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
    def create_index(self, embeddings):
        """
        Function: create_index
        Author: Shuaib
        Date: 01-08-2025
        Purpose: To add a list of embeddings to the FAISS index.
        Params: list embeddings
        Returns: None
        """
        if not isinstance(embeddings, np.ndarray):
            embeddings = np.array(embeddings).astype('float32')
        self.index.add(embeddings)
    def search(self, query_embedding, top_k: int = 3):
        """
        Function: search
        Author: Shuaib
        Date: 01-08-2025
        Purpose: To search the index for the top_k most similar vectors.
        Params: list query_embedding, int top_k
        Returns: tuple
        """
        if not isinstance(query_embedding, np.ndarray):
            query_embedding = np.array([query_embedding]).astype('float32')
        elif len(query_embedding.shape) == 1:
            query_embedding = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        return distances, indices
# Example usage:
if __name__ == '__main__':
    from embedder import Embedder
    embedder = Embedder()
    sample_texts = [
        "Anxiety is a common mental health concern.",
        "Mindfulness can help reduce stress.",
        "Depression can affect people in different ways.",
        "It's important to get enough sleep for your well-being."
    ]
    embeddings = embedder.embed(sample_texts)
    searcher = VectorSearcher(dimension=embeddings.shape[1])
    searcher.create_index(embeddings)
    query_text = "I'm feeling anxious and stressed."
    query_embedding = embedder.embed([query_text])
    distances, indices = searcher.search(query_embedding, top_k=2)
    print(f"Query: '{query_text}'")
    print("Top matching documents:")
    for i in indices[0]:
        print(f"- {sample_texts[i]}")
