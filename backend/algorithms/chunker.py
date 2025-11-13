"""
Semantic Chunker - Stage 1 of SignalCore Pipeline

This module implements a simple sentence-boundary based chunking algorithm
that splits documents into semantically coherent chunks while respecting
size constraints.
"""

import re
from typing import List


class SemanticChunker:
    """
    Splits long documents into chunks at sentence boundaries using a greedy
    sentence grouping algorithm.
    
    The chunker respects MIN_CHUNK_SIZE and MAX_CHUNK_SIZE constraints to
    avoid the "Lost in the Middle" problem while preserving semantic integrity.
    """
    
    # Hard-coded parameters for MVP
    MIN_CHUNK_SIZE = 200  # words
    MAX_CHUNK_SIZE = 1000  # words
    
    def chunk(self, text: str) -> List[str]:
        """
        Split text into semantically coherent chunks.
        
        Args:
            text: The full document text to be chunked
            
        Returns:
            List of text chunks with preserved semantic boundaries
        """
        # Step 1: Tokenize into sentences using regex pattern
        sentences = self._tokenize_sentences(text)
        
        if not sentences:
            return []
        
        # Step 2: Greedy sentence grouping
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            # Check if adding this sentence would exceed MAX_CHUNK_SIZE
            if current_word_count + sentence_words > self.MAX_CHUNK_SIZE:
                # If current chunk meets minimum size, save it and start new chunk
                if current_word_count >= self.MIN_CHUNK_SIZE:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_word_count = sentence_words
                else:
                    # Chunk too small, add sentence anyway to meet minimum
                    current_chunk.append(sentence)
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_word_count = 0
            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_word_count += sentence_words
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _tokenize_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using regex pattern [.!?]\\s+
        
        Args:
            text: The text to tokenize
            
        Returns:
            List of sentences
        """
        # Split on sentence-ending punctuation followed by whitespace
        # Keep the punctuation with the sentence
        sentences = re.split(r'([.!?])\s+', text)
        
        # Reconstruct sentences with their punctuation
        result = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
                # Combine text with its punctuation
                result.append(sentences[i] + sentences[i + 1])
                i += 2
            else:
                # Last sentence or sentence without punctuation
                if sentences[i].strip():
                    result.append(sentences[i])
                i += 1
        
        return result
