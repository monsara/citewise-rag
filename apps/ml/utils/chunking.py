"""
Text chunking utilities
"""
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
import hashlib


class TextChunker:
    """Text chunking with configurable parameters"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_text(self, text: str, document_name: str = "") -> List[Dict]:
        """
        Split text into chunks with metadata
        
        Args:
            text: Text to chunk
            document_name: Name of source document
            
        Returns:
            List of chunk dictionaries with text, metadata, and hash
        """
        # Split text into chunks
        chunks = self.splitter.split_text(text)
        
        # Create chunk objects with metadata
        chunk_objects = []
        for idx, chunk_text in enumerate(chunks):
            chunk_hash = self._hash_text(chunk_text)
            chunk_objects.append({
                "text": chunk_text,
                "index": idx,
                "document_name": document_name,
                "char_count": len(chunk_text),
                "hash": chunk_hash
            })
        
        return chunk_objects
    
    @staticmethod
    def _hash_text(text: str) -> str:
        """Generate hash for deduplication"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Rough token count estimation (1 token ≈ 4 chars)"""
        return len(text) // 4


# Global instance
text_chunker = TextChunker()
