"""
LLM API Client for Signal-Core

This module provides integration with Google Gemini API for querying
the LLM with context and questions.
"""

import os
import google.generativeai as genai


class LLMClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the LLM client with Google Gemini API.
        
        Args:
            api_key: Google Gemini API key. If None, reads from environment.
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def query(self, context: str, question: str) -> str:
        """
        Query the LLM with context and a question.
        
        Args:
            context: The document context (naive or optimized)
            question: The user's question
        
        Returns:
            The LLM's response text, or "API Error" on failure
        """
        prompt = f"""Context: {context}

Question: {question}

Answer:"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"LLM API Error: {e}")
            return "API Error"
