"""
Retrieval service for RAG pipeline
"""
from typing import List, Dict
import logging
from collections import defaultdict

from models.embeddings import get_embedder
from services.vector_store import get_vector_store
from config import settings

logger = logging.getLogger(__name__)


class Retriever:
    """Retrieve relevant chunks for queries"""
    
    def __init__(self):
        self.embedder = None
        self.vector_store = None
    
    def _ensure_initialized(self):
        """Lazy initialization"""
        if self.embedder is None:
            self.embedder = get_embedder()
        if self.vector_store is None:
            self.vector_store = get_vector_store()
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        embedding_provider: str = None
    ) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User question
            top_k: Number of chunks to retrieve
            embedding_provider: Override default embedding provider
            
        Returns:
            List of relevant chunks with metadata
        """
        self._ensure_initialized()
        
        top_k = top_k or settings.default_top_k
        
        # Generate query embedding
        if embedding_provider:
            embedder = get_embedder(embedding_provider)
        else:
            embedder = self.embedder
        
        query_embedding = embedder.embed_text(query)
        logger.info(f"Generated query embedding for: {query[:100]}...")
        
        # Search in vector store
        # Request more than top_k to allow for deduplication
        raw_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k * 2
        )
        
        logger.info(f"Retrieved {len(raw_results)} raw results")
        
        # Deduplicate and limit chunks per document
        filtered_results = self._deduplicate_and_limit(
            raw_results,
            max_per_document=settings.max_chunks_per_document
        )
        
        # Take top_k after filtering
        final_results = filtered_results[:top_k]
        
        logger.info(f"After filtering: {len(final_results)} chunks")
        
        return final_results
    
    @staticmethod
    def _deduplicate_and_limit(
        results: List[Dict],
        max_per_document: int = 3
    ) -> List[Dict]:
        """
        Deduplicate results and limit chunks per document
        
        Ensures diversity by limiting how many chunks come from one document
        """
        seen_hashes = set()
        doc_chunk_counts = defaultdict(int)
        filtered = []
        
        for result in results:
            # Skip if we've seen this exact text
            chunk_hash = result.get("chunk_hash")
            if chunk_hash and chunk_hash in seen_hashes:
                continue
            
            # Skip if we already have enough chunks from this document
            doc_id = result["document_id"]
            if doc_chunk_counts[doc_id] >= max_per_document:
                continue
            
            # Add to results
            filtered.append(result)
            if chunk_hash:
                seen_hashes.add(chunk_hash)
            doc_chunk_counts[doc_id] += 1
        
        return filtered


# Global instance
retriever = Retriever()
