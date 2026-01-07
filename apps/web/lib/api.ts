/**
 * API client for FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface QueryOptions {
  top_k?: number;
  llm_provider?: 'ollama' | 'openai' | 'groq';
  embedding_provider?: 'local' | 'openai';
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  trace_id: string;
  processing_time_ms: number;
  context_used: number;
}

export interface Citation {
  number: number;
  document_name: string;
  chunk_index: number;
  text: string;
  similarity_score: number;
}

export interface Document {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: string;
  upload_date: string;
  chunk_count?: number;
}

export interface Trace {
  id: string;
  query_text: string;
  answer_text: string;
  llm_provider: string;
  embedding_provider: string;
  top_k: number;
  processing_time_ms: number;
  created_at: string;
}

/**
 * Upload a document
 */
export async function uploadDocument(
  file: File,
  embeddingProvider?: string
): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);

  const url = new URL('/documents/upload', API_BASE_URL);
  if (embeddingProvider) {
    url.searchParams.append('embedding_provider', embeddingProvider);
  }

  const response = await fetch(url.toString(), {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }

  return response.json();
}

/**
 * Query RAG system
 */
export async function queryRAG(
  query: string,
  options: QueryOptions = {}
): Promise<QueryResponse> {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      ...options,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Query failed');
  }

  return response.json();
}

/**
 * Get all documents
 */
export async function getDocuments(): Promise<Document[]> {
  const response = await fetch(`${API_BASE_URL}/documents`);

  if (!response.ok) {
    throw new Error('Failed to fetch documents');
  }

  const data = await response.json();
  return data.documents;
}

/**
 * Get trace by ID
 */
export async function getTrace(traceId: string): Promise<Trace> {
  const response = await fetch(`${API_BASE_URL}/traces/${traceId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch trace');
  }

  return response.json();
}

/**
 * Get recent traces
 */
export async function getTraces(limit: number = 50): Promise<Trace[]> {
  const response = await fetch(`${API_BASE_URL}/traces?limit=${limit}`);

  if (!response.ok) {
    throw new Error('Failed to fetch traces');
  }

  const data = await response.json();
  return data.traces;
}
