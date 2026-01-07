"""
Embedding providers: Local (Sentence Transformers) and OpenAI
"""
from abc import ABC, abstractmethod
from typing import List
import logging
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from config import settings

logger = logging.getLogger(__name__)


class AbstractEmbedder(ABC):
    """Base class for embedding providers"""
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        pass


class LocalEmbedder(AbstractEmbedder):
    """Local embeddings using Sentence Transformers"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.local_embedding_model
        logger.info(f"Loading local embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded successfully. Dimension: {self._dimension}")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings.tolist()
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self._dimension


class OpenAIEmbedder(AbstractEmbedder):
    """OpenAI embeddings API"""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        self.model_name = model_name or settings.openai_embedding_model
        api_key = api_key or settings.openai_api_key
        
        if not api_key:
            raise ValueError("OpenAI API key is required for OpenAI embeddings")
        
        self.client = OpenAI(api_key=api_key)
        # text-embedding-3-small has 1536 dimensions
        self._dimension = 1536
        logger.info(f"OpenAI embedder initialized with model: {self.model_name}")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text
        )
        return response.data[0].embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        # OpenAI API accepts batch requests
        response = self.client.embeddings.create(
            model=self.model_name,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self._dimension


# Factory function
def get_embedder(provider: str = None) -> AbstractEmbedder:
    """
    Get embedder instance based on provider
    
    Args:
        provider: "local" or "openai". If None, uses settings.embedding_provider
    
    Returns:
        AbstractEmbedder instance
    """
    provider = provider or settings.embedding_provider
    
    if provider == "local":
        return LocalEmbedder()
    elif provider == "openai":
        return OpenAIEmbedder()
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")
