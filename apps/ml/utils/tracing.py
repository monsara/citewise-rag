"""
Query tracing utilities for debugging RAG pipeline
"""
from typing import List, Dict
import logging
from database import postgres

logger = logging.getLogger(__name__)


def save_trace(
    query_text: str,
    chunks: List[Dict],
    answer: str,
    citations: List[Dict],
    llm_provider: str,
    embedding_provider: str,
    top_k: int,
    processing_time_ms: int
) -> str:
    """
    Save query trace to database
    
    Args:
        query_text: Original user query
        chunks: Retrieved chunks
        answer: Generated answer
        citations: Extracted citations
        llm_provider: LLM provider used
        embedding_provider: Embedding provider used
        top_k: Number of chunks requested
        processing_time_ms: Total processing time
        
    Returns:
        Trace ID
    """
    try:
        # Extract chunk IDs and scores
        chunk_ids = [chunk.get("weaviate_id", "") for chunk in chunks]
        similarity_scores = [chunk.get("similarity_score", 0.0) for chunk in chunks]
        
        trace_id = postgres.insert_query_trace(
            query_text=query_text,
            retrieved_chunk_ids=chunk_ids,
            similarity_scores=similarity_scores,
            answer_text=answer,
            citations=citations,
            llm_provider=llm_provider,
            embedding_provider=embedding_provider,
            top_k=top_k,
            processing_time_ms=processing_time_ms
        )
        
        logger.info(f"Saved trace: {trace_id}")
        return trace_id
    
    except Exception as e:
        logger.error(f"Error saving trace: {e}")
        # Don't fail the request if trace fails
        return ""


def get_trace(trace_id: str) -> Dict:
    """Get trace by ID"""
    trace = postgres.get_query_trace(trace_id)
    if not trace:
        raise ValueError(f"Trace not found: {trace_id}")
    return trace


def get_traces(limit: int = 50) -> List[Dict]:
    """Get recent traces"""
    return postgres.get_query_traces(limit=limit)
