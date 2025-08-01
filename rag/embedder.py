from sentence_transformers import SentenceTransformer
class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initializes the embedder with a pre-trained sentence-transformer model.
        """
        self.model = SentenceTransformer(model_name)
    def embed(self, texts):
        """
        Converts a list of texts into a list of embeddings.
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
