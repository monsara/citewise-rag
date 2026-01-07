"""
CiteWise RAG - FastAPI Application
Main entry point for the RAG service
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import time

from config import settings
from services.document_processor import document_processor
from services.retriever import retriever
from services.generator import generator
from utils import tracing
from database import postgres

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CiteWise RAG API",
    description="Learning-focused RAG system with source citations",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = None
    llm_provider: Optional[str] = None
    embedding_provider: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]
    trace_id: str
    processing_time_ms: int
    context_used: int


# Endpoints
@app.get("/")
async def root():
    """API root"""
    return {
        "name": "CiteWise RAG API",
        "version": "0.1.0",
        "status": "running",
        "philosophy": "Learning > Features | Clarity > Abstraction"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        postgres.execute_query("SELECT 1", fetch=True)
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    embedding_provider: Optional[str] = Query(None)
):
    """
    Upload and process a document
    
    Accepts .txt and .md files
    """
    logger.info(f"Uploading document: {file.filename}")
    
    try:
        content = await file.read()
        result = await document_processor.process_document(
            file_content=content,
            filename=file.filename,
            embedding_provider=embedding_provider
        )
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Document processing failed")


@app.get("/documents")
async def get_documents():
    """Get all documents"""
    try:
        documents = document_processor.get_documents()
        return {"documents": documents}
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve documents")


@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get document by ID"""
    try:
        document = document_processor.get_document(doc_id)
        return document
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve document")


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Main RAG endpoint: retrieve and generate answer
    
    This is the core of the RAG pipeline:
    1. Retrieve relevant chunks
    2. Generate answer with citations
    3. Save trace for debugging
    """
    start_time = time.time()
    
    logger.info(f"Query received: {request.query[:100]}...")
    
    try:
        # Retrieve relevant chunks
        chunks = retriever.retrieve(
            query=request.query,
            top_k=request.top_k,
            embedding_provider=request.embedding_provider
        )
        
        # Generate answer
        generation_result = generator.generate_answer(
            query=request.query,
            chunks=chunks,
            llm_provider=request.llm_provider
        )
        
        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Save trace
        trace_id = tracing.save_trace(
            query_text=request.query,
            chunks=generation_result.get("chunks", []),
            answer=generation_result["answer"],
            citations=generation_result["citations"],
            llm_provider=request.llm_provider or settings.llm_provider,
            embedding_provider=request.embedding_provider or settings.embedding_provider,
            top_k=request.top_k or settings.default_top_k,
            processing_time_ms=processing_time_ms
        )
        
        return QueryResponse(
            answer=generation_result["answer"],
            citations=generation_result["citations"],
            trace_id=trace_id,
            processing_time_ms=processing_time_ms,
            context_used=generation_result.get("context_used", 0)
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Query processing failed")


@app.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    """Get query trace by ID"""
    try:
        trace = tracing.get_trace(trace_id)
        return trace
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting trace: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trace")


@app.get("/traces")
async def get_traces(limit: int = Query(50, le=100)):
    """Get recent query traces"""
    try:
        traces = tracing.get_traces(limit=limit)
        return {"traces": traces}
    except Exception as e:
        logger.error(f"Error getting traces: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve traces")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
