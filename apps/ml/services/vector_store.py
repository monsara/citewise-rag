"""
Weaviate vector store operations
"""
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Optional
import logging
from config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Weaviate vector store for RAG"""
    
    COLLECTION_NAME = "DocumentChunk"
    
    def __init__(self, weaviate_url: str = None):
        self.weaviate_url = weaviate_url or settings.weaviate_url
        self.client = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Connect to Weaviate and initialize schema"""
        try:
            self.client = weaviate.connect_to_local(
                host=self.weaviate_url.replace("http://", "").replace(":8080", "")
            )
            logger.info(f"Connected to Weaviate at {self.weaviate_url}")
            self._initialize_schema()
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {e}")
            raise
    
    def _initialize_schema(self):
        """Create collection if it doesn't exist"""
        try:
            # Check if collection exists
            if self.client.collections.exists(self.COLLECTION_NAME):
                self.collection = self.client.collections.get(self.COLLECTION_NAME)
                logger.info(f"Using existing collection: {self.COLLECTION_NAME}")
            else:
                # Create collection
                self.collection = self.client.collections.create(
                    name=self.COLLECTION_NAME,
                    properties=[
                        Property(name="text", data_type=DataType.TEXT),
                        Property(name="document_id", data_type=DataType.TEXT),
                        Property(name="document_name", data_type=DataType.TEXT),
                        Property(name="chunk_index", data_type=DataType.INT),
                        Property(name="char_count", data_type=DataType.INT),
                        Property(name="chunk_hash", data_type=DataType.TEXT),
                    ],
                    vectorizer_config=Configure.Vectorizer.none(),  # We provide embeddings
                )
                logger.info(f"Created new collection: {self.COLLECTION_NAME}")
        except Exception as e:
            logger.error(f"Schema initialization error: {e}")
            raise
    
    def add_chunks(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
        document_id: str,
        document_name: str
    ) -> List[str]:
        """
        Add document chunks with embeddings to Weaviate
        
        Args:
            chunks: List of chunk dictionaries from TextChunker
            embeddings: List of embedding vectors
            document_id: UUID of parent document
            document_name: Name of parent document
            
        Returns:
            List of Weaviate UUIDs
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match")
        
        weaviate_ids = []
        
        try:
            with self.collection.batch.dynamic() as batch:
                for chunk, embedding in zip(chunks, embeddings):
                    properties = {
                        "text": chunk["text"],
                        "document_id": document_id,
                        "document_name": document_name,
                        "chunk_index": chunk["index"],
                        "char_count": chunk["char_count"],
                        "chunk_hash": chunk["hash"],
                    }
                    
                    uuid = batch.add_object(
                        properties=properties,
                        vector=embedding
                    )
                    weaviate_ids.append(str(uuid))
            
            logger.info(f"Added {len(weaviate_ids)} chunks to Weaviate")
            return weaviate_ids
        
        except Exception as e:
            logger.error(f"Error adding chunks to Weaviate: {e}")
            raise
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for similar chunks
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            document_id: Optional filter by document ID
            
        Returns:
            List of chunk results with metadata and scores
        """
        try:
            # Build query
            query = self.collection.query.near_vector(
                near_vector=query_embedding,
                limit=top_k,
                return_metadata=MetadataQuery(distance=True)
            )
            
            # Apply document filter if provided
            if document_id:
                query = query.where(f"document_id == '{document_id}'")
            
            response = query
            
            # Format results
            results = []
            for obj in response.objects:
                # Convert distance to similarity score (0-1)
                distance = obj.metadata.distance if obj.metadata.distance else 0
                similarity_score = 1 / (1 + distance)  # Simple transformation
                
                results.append({
                    "weaviate_id": str(obj.uuid),
                    "text": obj.properties["text"],
                    "document_id": obj.properties["document_id"],
                    "document_name": obj.properties["document_name"],
                    "chunk_index": obj.properties["chunk_index"],
                    "similarity_score": round(similarity_score, 4),
                    "distance": round(distance, 4)
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            raise
    
    def delete_by_document(self, document_id: str):
        """Delete all chunks for a document"""
        try:
            self.collection.data.delete_many(
                where={"path": ["document_id"], "operator": "Equal", "valueText": document_id}
            )
            logger.info(f"Deleted chunks for document {document_id}")
        except Exception as e:
            logger.error(f"Delete error: {e}")
            raise
    
    def close(self):
        """Close Weaviate connection"""
        if self.client:
            self.client.close()
            logger.info("Weaviate connection closed")


# Global instance
_vector_store = None


def get_vector_store() -> VectorStore:
    """Get or create global VectorStore instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
