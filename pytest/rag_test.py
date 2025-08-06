import pytest
from rag.embedder import Embedder
from rag.rag_manager import RAGManager
from unittest.mock import MagicMock, patch
import numpy as np
from rag.search_vector import VectorSearcher
from rag.retriever_sql import SQLRetriever
from db.models import KnowledgeBase

def test_embedder_embedding_output():
    embedder = Embedder()
    texts = ["Hello world", "Test sentence"]
    embeddings = embedder.embed(texts)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 2
    assert all(isinstance(e, list) or hasattr(e, '__len__') for e in embeddings)

import numpy as np
from rag.search_vector import VectorSearcher
from rag.embedder import Embedder

def test_vector_search_basic_functionality():
    embedder = Embedder()
    texts = ["One", "Two", "Three"]
    embeddings = np.array(embedder.embed(texts)).astype("float32")

    searcher = VectorSearcher(dimension=embeddings.shape[1])
    searcher.create_index(embeddings)

    query_embedding = np.array(embedder.embed(["Two"])).astype("float32")
    distances, indices = searcher.search(query_embedding, top_k=2)

    assert distances.shape == (1, 2)
    assert indices.shape == (1, 2)

from rag.retriever_sql import SQLRetriever
from db.models import KnowledgeBase
from unittest.mock import MagicMock

def test_sql_retriever_returns_expected_results():
    mock_session = MagicMock()
    retriever = SQLRetriever(mock_session)
    retriever.retrieve("stress")

    assert mock_session.query.called

from rag.rag_manager import RAGManager
from rag.embedder import Embedder
from unittest.mock import MagicMock, patch

@patch("rag.rag_manager.faiss.read_index")
def test_rag_manager_context_retrieval(mock_read_index):
    mock_index = MagicMock()
    mock_index.search.return_value = ([0.1], [[0]])
    mock_read_index.return_value = mock_index

    mock_db = MagicMock()
    mock_doc = MagicMock()
    mock_doc.content_chunk = "This is a test chunk."
    mock_db.query.return_value.all.return_value = [mock_doc]

    manager = RAGManager(mock_db)
    context = manager.get_context("test")

    assert isinstance(context, str)
    assert "test chunk" in context

