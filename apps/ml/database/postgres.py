"""
PostgreSQL connection and operations
"""
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from contextlib import contextmanager
from typing import Any, Dict, List, Optional
import logging
from config import settings

logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = psycopg2.connect(settings.postgres_url)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[List[Dict]]:
    """Execute a SQL query and optionally fetch results"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return [dict(row) for row in cur.fetchall()]
            return None


def insert_document(filename: str, file_type: str, file_size: int, metadata: Dict = None) -> str:
    """Insert a new document and return its ID"""
    query = """
        INSERT INTO documents (filename, file_type, file_size, metadata, status)
        VALUES (%s, %s, %s, %s, 'processing')
        RETURNING id::text
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (filename, file_type, file_size, Json(metadata or {})))
            doc_id = cur.fetchone()[0]
            return doc_id


def update_document_status(doc_id: str, status: str):
    """Update document processing status"""
    query = "UPDATE documents SET status = %s WHERE id = %s"
    execute_query(query, (status, doc_id), fetch=False)


def insert_document_chunk(
    doc_id: str,
    chunk_index: int,
    weaviate_id: str,
    chunk_text: str,
    token_count: int,
    metadata: Dict = None
) -> str:
    """Insert a document chunk reference"""
    query = """
        INSERT INTO document_chunks 
        (document_id, chunk_index, weaviate_id, chunk_text, token_count, metadata)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id::text
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (doc_id, chunk_index, weaviate_id, chunk_text, token_count, Json(metadata or {}))
            )
            chunk_id = cur.fetchone()[0]
            return chunk_id


def get_documents() -> List[Dict]:
    """Get all documents"""
    query = """
        SELECT 
            id::text,
            filename,
            file_type,
            file_size,
            status,
            metadata,
            upload_date,
            (SELECT COUNT(*) FROM document_chunks WHERE document_id = documents.id) as chunk_count
        FROM documents
        ORDER BY upload_date DESC
    """
    return execute_query(query)


def get_document_by_id(doc_id: str) -> Optional[Dict]:
    """Get document by ID"""
    query = """
        SELECT 
            id::text,
            filename,
            file_type,
            file_size,
            status,
            metadata,
            upload_date
        FROM documents
        WHERE id = %s
    """
    results = execute_query(query, (doc_id,))
    return results[0] if results else None


def insert_query_trace(
    query_text: str,
    retrieved_chunk_ids: List[str],
    similarity_scores: List[float],
    answer_text: str,
    citations: List[Dict],
    llm_provider: str,
    embedding_provider: str,
    top_k: int,
    processing_time_ms: int
) -> str:
    """Insert a query trace for debugging"""
    query = """
        INSERT INTO query_traces
        (query_text, retrieved_chunk_ids, similarity_scores, answer_text, 
         citations, llm_provider, embedding_provider, top_k, processing_time_ms)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id::text
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    query_text,
                    Json(retrieved_chunk_ids),
                    Json(similarity_scores),
                    answer_text,
                    Json(citations),
                    llm_provider,
                    embedding_provider,
                    top_k,
                    processing_time_ms
                )
            )
            trace_id = cur.fetchone()[0]
            return trace_id


def get_query_trace(trace_id: str) -> Optional[Dict]:
    """Get query trace by ID"""
    query = """
        SELECT 
            id::text,
            query_text,
            retrieved_chunk_ids,
            similarity_scores,
            answer_text,
            citations,
            llm_provider,
            embedding_provider,
            top_k,
            processing_time_ms,
            created_at
        FROM query_traces
        WHERE id = %s
    """
    results = execute_query(query, (trace_id,))
    return results[0] if results else None


def get_query_traces(limit: int = 50) -> List[Dict]:
    """Get recent query traces"""
    query = """
        SELECT 
            id::text,
            query_text,
            answer_text,
            llm_provider,
            embedding_provider,
            top_k,
            processing_time_ms,
            created_at
        FROM query_traces
        ORDER BY created_at DESC
        LIMIT %s
    """
    return execute_query(query, (limit,))
