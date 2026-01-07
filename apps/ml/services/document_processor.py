"""
Document processing service: upload, chunking, embedding
"""
from typing import Dict, List
import logging
from pathlib import Path
import time

from models.embeddings import get_embedder
from utils.chunking import text_chunker
from services.vector_store import get_vector_store
from database import postgres
from config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process documents for RAG pipeline"""
    
    def __init__(self):
        self.embedder = None
        self.vector_store = None
    
    def _ensure_initialized(self):
        """Lazy initialization of heavy components"""
        if self.embedder is None:
            self.embedder = get_embedder()
        if self.vector_store is None:
            self.vector_store = get_vector_store()
    
    async def process_document(
        self,
        file_content: bytes,
        filename: str,
        embedding_provider: str = None
    ) -> Dict:
        """
        Process a document: chunk, embed, store
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            embedding_provider: Override default embedding provider
            
        Returns:
            Processing result with document ID and stats
        """
        self._ensure_initialized()
        
        start_time = time.time()
        
        # Determine file type
        file_ext = Path(filename).suffix.lower()
        if file_ext not in ['.txt', '.md']:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Decode text
        try:
            text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("File must be UTF-8 encoded text")
        
        file_size = len(file_content)
        
        logger.info(f"Processing document: {filename} ({file_size} bytes)")
        
        # Insert document metadata
        doc_id = postgres.insert_document(
            filename=filename,
            file_type=file_ext.replace('.', ''),
            file_size=file_size,
            metadata={"char_count": len(text)}
        )
        
        try:
            # Chunk the text
            chunks = text_chunker.chunk_text(text, document_name=filename)
            logger.info(f"Created {len(chunks)} chunks")
            
            # Generate embeddings
            if embedding_provider:
                embedder = get_embedder(embedding_provider)
            else:
                embedder = self.embedder
            
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = embedder.embed_batch(chunk_texts)
            logger.info(f"Generated {len(embeddings)} embeddings")
            
            # Store in Weaviate
            weaviate_ids = self.vector_store.add_chunks(
                chunks=chunks,
                embeddings=embeddings,
                document_id=doc_id,
                document_name=filename
            )
            
            # Store chunk references in PostgreSQL
            for chunk, weaviate_id in zip(chunks, weaviate_ids):
                token_count = text_chunker.estimate_tokens(chunk["text"])
                postgres.insert_document_chunk(
                    doc_id=doc_id,
                    chunk_index=chunk["index"],
                    weaviate_id=weaviate_id,
                    chunk_text=chunk["text"],
                    token_count=token_count,
                    metadata={"hash": chunk["hash"]}
                )
            
            # Update document status
            postgres.update_document_status(doc_id, "completed")
            
            processing_time = time.time() - start_time
            
            result = {
                "document_id": doc_id,
                "filename": filename,
                "chunk_count": len(chunks),
                "processing_time_seconds": round(processing_time, 2),
                "status": "completed"
            }
            
            logger.info(f"Document processed successfully: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            postgres.update_document_status(doc_id, "failed")
            raise
    
    def get_documents(self) -> List[Dict]:
        """Get all documents"""
        return postgres.get_documents()
    
    def get_document(self, doc_id: str) -> Dict:
        """Get document by ID"""
        doc = postgres.get_document_by_id(doc_id)
        if not doc:
            raise ValueError(f"Document not found: {doc_id}")
        return doc


# Global instance
document_processor = DocumentProcessor()
