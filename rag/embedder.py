"""
Module: embedder
Author: Shuaib
Date: 27-07-2025
Purpose: To provide an embedder for converting text to embeddings.
"""
from sentence_transformers import SentenceTransformer
class Embedder:
    """
    Class: Embedder
    Author: Shuaib
    Date: 27-07-2025
    Purpose: To provide an embedder for converting text to embeddings.
    """
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Function: __init__
        Author: Shuaib
        Date: 27-07-2025
        Purpose: To initialize the embedder with a pre-trained sentence-transformer model.
        Params: str model_name
        Returns: None
        """
        self.model = SentenceTransformer(model_name)
    def embed(self, texts):
        """
        Function: embed
        Author: Shuaib
        Date: 27-07-2025
        Purpose: To convert a list of texts into a list of embeddings.
        Params: list texts
        Returns: list
        """
        return self.model.encode(texts, convert_to_tensor=False)
# Example usage:
if __name__ == '__main__':
    embedder = Embedder()
    sample_texts = [
        "This is a sample sentence.",
        "Embeddings are numerical representations of text."
    ]
    embeddings = embedder.embed(sample_texts)
    print("Generated embeddings:")
    print(embeddings)
    print(f"Shape of embeddings: {embeddings.shape}")
