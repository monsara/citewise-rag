"""
Answer generation service with citations
"""
from typing import Dict, List, Tuple
import logging
import re

from models.llm import get_llm

logger = logging.getLogger(__name__)


class Generator:
    """Generate answers with citations"""
    
    def __init__(self):
        self.llm = None
    
    def _ensure_initialized(self):
        """Lazy initialization"""
        if self.llm is None:
            self.llm = get_llm()
    
    def generate_answer(
        self,
        query: str,
        chunks: List[Dict],
        llm_provider: str = None
    ) -> Dict:
        """
        Generate answer from query and retrieved chunks
        
        Args:
            query: User question
            chunks: Retrieved chunks with metadata
            llm_provider: Override default LLM provider
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        self._ensure_initialized()
        
        if not chunks:
            return {
                "answer": "Not found in sources",
                "citations": [],
                "context_used": False
            }
        
        # Format context with citations
        context, citation_map = self._format_context(chunks)
        
        # Generate answer
        if llm_provider:
            llm = get_llm(llm_provider)
        else:
            llm = self.llm
        
        logger.info(f"Generating answer for query: {query[:100]}...")
        answer_text = llm.generate(prompt=query, context=context)
        
        # Extract citations from answer
        citations = self._extract_citations(answer_text, citation_map)
        
        result = {
            "answer": answer_text,
            "citations": citations,
            "context_used": len(chunks),
            "chunks": chunks  # Include for trace
        }
        
        logger.info(f"Generated answer with {len(citations)} citations")
        return result
    
    @staticmethod
    def _format_context(chunks: List[Dict]) -> Tuple[str, Dict]:
        """
        Format chunks into context with citation markers
        
        Returns:
            Tuple of (formatted_context, citation_map)
        """
        context_parts = []
        citation_map = {}
        
        for idx, chunk in enumerate(chunks, start=1):
            citation_num = f"[{idx}]"
            context_parts.append(f"{citation_num} {chunk['text']}\n")
            
            citation_map[citation_num] = {
                "number": idx,
                "document_name": chunk["document_name"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                "similarity_score": chunk["similarity_score"]
            }
        
        context = "\n".join(context_parts)
        return context, citation_map
    
    @staticmethod
    def _extract_citations(answer: str, citation_map: Dict) -> List[Dict]:
        """
        Extract citation markers from answer and map to sources
        
        Args:
            answer: Generated answer text
            citation_map: Map of citation markers to chunk info
            
        Returns:
            List of citation objects
        """
        # Find all [N] patterns in answer
        citation_pattern = r'\[(\d+)\]'
        found_citations = set(re.findall(citation_pattern, answer))
        
        citations = []
        for num_str in sorted(found_citations, key=int):
            citation_marker = f"[{num_str}]"
            if citation_marker in citation_map:
                citations.append(citation_map[citation_marker])
        
        return citations


# Global instance
generator = Generator()
