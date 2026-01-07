"""
LLM providers: Ollama (local), OpenAI, and Groq
"""
from abc import ABC, abstractmethod
from typing import Optional
import logging
import ollama
from openai import OpenAI
from groq import Groq
from config import settings

logger = logging.getLogger(__name__)


class AbstractLLM(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, context: str) -> str:
        """
        Generate answer given prompt and context
        
        Args:
            prompt: User query
            context: Retrieved context from documents
            
        Returns:
            Generated answer text
        """
        pass


class OllamaLLM(AbstractLLM):
    """Local LLM using Ollama"""
    
    def __init__(self, model_name: str = None, base_url: str = None):
        self.model_name = model_name or settings.ollama_model
        self.base_url = base_url or settings.ollama_base_url
        logger.info(f"Ollama LLM initialized with model: {self.model_name}")
    
    def generate(self, prompt: str, context: str) -> str:
        """Generate answer using Ollama"""
        
        # Construct system message with RAG instructions
        system_message = """You are a helpful assistant that answers questions based ONLY on the provided context.

CRITICAL RULES:
1. Answer ONLY using information from the provided context
2. Use inline citations like [1], [2] for each fact
3. If the answer cannot be found in the context, respond with: "Not found in sources"
4. Do not use your own knowledge or make assumptions
5. Be concise and accurate"""
        
        # Construct user message with context and query
        user_message = f"""Context:
{context}

Question: {prompt}

Please answer the question using ONLY the context above. Include citations [1], [2], etc."""
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ]
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise


class OpenAILLM(AbstractLLM):
    """OpenAI GPT models"""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        self.model_name = model_name or settings.openai_model
        api_key = api_key or settings.openai_api_key
        
        if not api_key:
            raise ValueError("OpenAI API key is required for OpenAI LLM")
        
        self.client = OpenAI(api_key=api_key)
        logger.info(f"OpenAI LLM initialized with model: {self.model_name}")
    
    def generate(self, prompt: str, context: str) -> str:
        """Generate answer using OpenAI API"""
        
        # Construct system message with RAG instructions
        system_message = """You are a helpful assistant that answers questions based ONLY on the provided context.

CRITICAL RULES:
1. Answer ONLY using information from the provided context
2. Use inline citations like [1], [2] for each fact
3. If the answer cannot be found in the context, respond with: "Not found in sources"
4. Do not use your own knowledge or make assumptions
5. Be concise and accurate"""
        
        # Construct user message with context and query
        user_message = f"""Context:
{context}

Question: {prompt}

Please answer the question using ONLY the context above. Include citations [1], [2], etc."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise


class GroqLLM(AbstractLLM):
    """Groq API with fast inference"""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        self.model_name = model_name or settings.groq_model
        api_key = api_key or settings.groq_api_key
        
        if not api_key:
            raise ValueError("Groq API key is required for Groq LLM")
        
        self.client = Groq(api_key=api_key)
        logger.info(f"Groq LLM initialized with model: {self.model_name}")
    
    def generate(self, prompt: str, context: str) -> str:
        """Generate answer using Groq API"""
        
        # Construct system message with RAG instructions
        system_message = """You are a helpful assistant that answers questions based ONLY on the provided context.

CRITICAL RULES:
1. Answer ONLY using information from the provided context
2. Use inline citations like [1], [2] for each fact
3. If the answer cannot be found in the context, respond with: "Not found in sources"
4. Do not use your own knowledge or make assumptions
5. Provide detailed, comprehensive answers with examples when available"""
        
        # Construct user message with context and query
        user_message = f"""Context:
{context}

Question: {prompt}

Please answer the question using ONLY the context above. Include citations [1], [2], etc."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=2000  # Groq supports longer outputs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise


# Factory function
def get_llm(provider: str = None) -> AbstractLLM:
    """
    Get LLM instance based on provider
    
    Args:
        provider: "ollama", "openai", or "groq". If None, uses settings.llm_provider
    
    Returns:
        AbstractLLM instance
    """
    provider = provider or settings.llm_provider
    
    if provider == "ollama":
        return OllamaLLM()
    elif provider == "openai":
        return OpenAILLM()
    elif provider == "groq":
        return GroqLLM()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Choose from: ollama, openai, groq")
