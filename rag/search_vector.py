import faiss
import numpy as np
class VectorSearcher:
    def __init__(self, dimension):
        """
        Initializes the FAISS index.
        :param dimension: The dimensionality of the vectors.
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
    def create_index(self, embeddings):
        """
        Adds a list of embeddings to the FAISS index.
        """
        if not isinstance(embeddings, np.ndarray):
            embeddings = np.array(embeddings).astype('float32')
        self.index.add(embeddings)
    def search(self, query_embedding, top_k: int = 3):
        """
        Searches the index for the top_k most similar vectors.
        :return: A tuple of (distances, indices) of the nearest neighbors.
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