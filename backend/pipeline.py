"""
SignalCore Pipeline - Orchestrates the two-stage optimization process

This module combines the Semantic Chunker (Stage 1) and Sentence-Level Pruner
(Stage 2) to create an optimized context for LLM consumption. It also calculates
token reduction metrics.
"""

from typing import Tuple, Dict
from backend.algorithms.chunker import SemanticChunker
from backend.algorithms.pruner import SentencePruner


class SignalCorePipeline:
    """
    Orchestrates the two-stage text optimization pipeline.
    
    Stage 1: Semantic Chunker splits document at optimal boundaries
    Stage 2: Sentence-Level Pruner extracts important sentences from each chunk
    
    The pipeline also calculates token reduction metrics to demonstrate
    efficiency gains.
    """
    
    def __init__(self):
        """Initialize the pipeline with chunker and pruner instances."""
        self.chunker = SemanticChunker()
        self.pruner = SentencePruner()
    
    def process(self, document: str) -> Tuple[str, Dict[str, float]]:
        """
        Run full two-stage optimization on the document.
        
        Args:
            document: Full document text with injected needle
            
        Returns:
            Tuple containing:
                - optimized_context: Processed text ready for LLM
                - metrics: Dictionary with token counts and reduction percentage
        """
        # Calculate original token count
        original_tokens = self._count_tokens(document)
        
        # Stage 1: Chunk the document
        chunks = self.chunker.chunk(document)
        
        # Stage 2: Prune each chunk
        pruned_chunks = [self.pruner.prune(chunk) for chunk in chunks]
        
        # Combine pruned chunks
        optimized_context = "\n\n".join(pruned_chunks)
        
        # Calculate optimized token count
        optimized_tokens = self._count_tokens(optimized_context)
        
        # Calculate reduction percentage
        reduction_percentage = 0.0
        if original_tokens > 0:
            reduction_percentage = ((original_tokens - optimized_tokens) / original_tokens) * 100
        
        # Build metrics dictionary
        metrics = {
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "reduction_percentage": reduction_percentage
        }
        
        return optimized_context, metrics
    
    def _count_tokens(self, text: str) -> int:
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
