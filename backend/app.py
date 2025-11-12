"""
Signal-Core Flask API Server

This module provides HTTP endpoints for the Signal-Core demo UI.
It exposes two endpoints:
- /api/test-naive: Tests LLM with full unprocessed document
- /api/test-optimized: Tests LLM with Signal-Core optimized document
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
load_dotenv(project_root / '.env')

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.pipeline import SignalCorePipeline
from backend.llm_client import LLMClient
from backend.utils import inject_needle


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize Signal-Core components
pipeline = SignalCorePipeline()

# Load API key from environment and initialize LLM client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

llm_client = LLMClient(api_key=api_key)


def count_tokens(text: str) -> int:
    """
    Approximate token count using word-based estimation.
    
    Rule of thumb: 1 token ≈ 0.75 words
    
    Args:
        text: The text to count tokens for
        
    Returns:
        Estimated token count
    """
    words = len(text.split())
    return int(words / 0.75)


@app.route('/api/test-naive', methods=['POST'])
def test_naive():
    """
    Test Naive RAG approach with full unprocessed document.
    
    Request JSON:
        - haystack: The full document text
        - needle: The fact to inject
        - injection_depth: Percentage (0-100) where to inject needle
        - query: The question to ask the LLM
    
    Response JSON:
        - response: LLM's answer
        - tokens: Token count of the full document
    """
    try:
        # Parse request JSON
        data = request.json
        haystack = data.get('haystack', '')
        needle = data.get('needle', '')
        injection_depth = data.get('injection_depth', 50)
        query = data.get('query', '')
        
        # Validate inputs
        if not haystack or not needle or not query:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Inject needle into haystack
        document = inject_needle(haystack, needle, injection_depth)
        
        # Count tokens in full document
        tokens = count_tokens(document)
        
        # Query LLM with full document
        response = llm_client.query(document, query)
        
        # Return response with token count
        return jsonify({
            "response": response,
            "tokens": tokens
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/test-optimized', methods=['POST'])
def test_optimized():
    """
    Test Optimized RAG approach with Signal-Core processed document.
    
    Request JSON:
        - haystack: The full document text
        - needle: The fact to inject
        - injection_depth: Percentage (0-100) where to inject needle
        - query: The question to ask the LLM
    
    Response JSON:
        - response: LLM's answer
        - original_tokens: Token count of original document
        - optimized_tokens: Token count of optimized document
        - reduction_percentage: Percentage reduction in tokens
    """
    try:
        # Parse request JSON
        data = request.json
        haystack = data.get('haystack', '')
        needle = data.get('needle', '')
        injection_depth = data.get('injection_depth', 50)
        query = data.get('query', '')
        
        # Validate inputs
        if not haystack or not needle or not query:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Inject needle into haystack
        document = inject_needle(haystack, needle, injection_depth)
        
        # Process document through Signal-Core pipeline
        optimized_context, metrics = pipeline.process(document)
        
        # Query LLM with optimized context
        response = llm_client.query(optimized_context, query)
        
        # Return response with metrics
        return jsonify({
            "response": response,
            "original_tokens": metrics["original_tokens"],
            "optimized_tokens": metrics["optimized_tokens"],
            "reduction_percentage": metrics["reduction_percentage"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
