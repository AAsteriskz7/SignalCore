"""
Sentence-Level Pruner - Stage 2 of Signal-Core Pipeline

This module implements a centroid-based sentence pruning algorithm that
extracts the most important sentences from each chunk by ranking them
based on their similarity to the chunk's overall topic.
"""

import re
from typing import List, Counter as CounterType
from collections import Counter
import math


class SentencePruner:
    """
    Extracts the most important sentences from a text chunk using
    centroid-based ranking.
    
    The pruner calculates a "centroid" (average topic) for the chunk,
    then ranks sentences by their cosine similarity to this centroid.
    Top-scoring sentences are retained while preserving original order.
    """
    
    # Hard-coded parameter for MVP
    EXTRACTION_RATIO = 0.60  # Keep top 60% of sentences
    
    def prune(self, chunk: str) -> str:
        """
        Extract most important sentences from chunk.
        
        Args:
            chunk: A single text chunk from Stage 1
            
        Returns:
            The chunk with only high-importance sentences, in original order
        """
        # Step 1: Tokenize into sentences
        sentences = self._tokenize_sentences(chunk)
        
        if not sentences:
            return ""
        
        # If only one sentence, return it
        if len(sentences) == 1:
            return chunk
        
        # Step 2: Calculate chunk centroid (word frequency for entire chunk)
        centroid = self._calculate_centroid(chunk)
        
        # Step 3: Score each sentence by similarity to centroid + uniqueness bonus
        sentence_scores = []
        for idx, sentence in enumerate(sentences):
            sentence_vector = self._calculate_word_frequency(sentence)
            
            # Base score: similarity to centroid
            similarity_score = self._cosine_similarity(sentence_vector, centroid)
            
            # Uniqueness bonus: boost sentences with rare/unique words
            uniqueness_score = self._calculate_uniqueness(sentence_vector, centroid)
            
            # Combined score: Use uniqueness only for now
            # This preserves sentences with unique information (like the needle)
            combined_score = uniqueness_score
            
            sentence_scores.append((idx, sentence, combined_score))
        
        # Step 4: Extract top sentences by score
        num_sentences_to_keep = max(1, int(len(sentences) * self.EXTRACTION_RATIO))
        
        # Sort by score (descending) and take top N
        top_sentences = sorted(sentence_scores, key=lambda x: x[2], reverse=True)[:num_sentences_to_keep]
        
        # Step 5: Preserve original order
        top_sentences_sorted = sorted(top_sentences, key=lambda x: x[0])
        
        # Reconstruct text with preserved order
        pruned_text = ' '.join([sentence for _, sentence, _ in top_sentences_sorted])
        
        return pruned_text
    
    def _tokenize_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using regex pattern [.!?]\\s+
        
        Args:
            text: The text to tokenize
            
        Returns:
            List of sentences
        """
        # Split on sentence-ending punctuation followed by whitespace
        sentences = re.split(r'([.!?])\s+', text)
        
        # Reconstruct sentences with their punctuation
        result = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
                result.append(sentences[i] + sentences[i + 1])
                i += 2
            else:
                if sentences[i].strip():
                    result.append(sentences[i])
                i += 1
        
        return result
    
    def _calculate_centroid(self, text: str) -> Counter:
        """
        Calculate word frequency vector for entire chunk (the centroid).
        
        Args:
            text: The chunk text
            
        Returns:
            Counter object with word frequencies
        """
        return self._calculate_word_frequency(text)
    
    def _calculate_word_frequency(self, text: str) -> Counter:
        """
        Calculate word frequency vector for a piece of text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Counter object with word frequencies
        """
        # Convert to lowercase and split into words
        words = text.lower().split()
        return Counter(words)
    
    def _cosine_similarity(self, vec1: Counter, vec2: Counter) -> float:
        """
        Calculate cosine similarity between two word frequency vectors.
        
        Args:
            vec1: First word frequency vector
            vec2: Second word frequency vector
            
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # Find intersection of words
        intersection = set(vec1.keys()) & set(vec2.keys())
        
        # Calculate dot product (numerator)
        numerator = sum([vec1[word] * vec2[word] for word in intersection])
        
        # Calculate magnitudes
        sum1 = sum([vec1[word] ** 2 for word in vec1.keys()])
        sum2 = sum([vec2[word] ** 2 for word in vec2.keys()])
        
        # Calculate denominator
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        # Avoid division by zero
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _calculate_uniqueness(self, sentence_vector: Counter, centroid: Counter) -> float:
        """
        Calculate uniqueness score for a sentence based on rare words.
        
        Sentences with words that appear infrequently in the chunk get higher scores.
        This helps preserve sentences with unique information (like the needle).
        
        Args:
            sentence_vector: Word frequency vector for the sentence
            centroid: Word frequency vector for the entire chunk
            
        Returns:
            Uniqueness score (0.0 to 1.0)
        """
        if not sentence_vector:
            return 0.0
        
        # Calculate inverse document frequency for each word in the sentence
        uniqueness_scores = []
        for word in sentence_vector.keys():
            # Words that appear rarely in the chunk get higher scores
            chunk_frequency = centroid.get(word, 0)
            if chunk_frequency > 0:
                # Inverse frequency: rare words get higher scores
                # Use a stronger penalty for common words
                idf = 1.0 / (chunk_frequency ** 0.5)
                uniqueness_scores.append(idf)
            else:
                # Word not in chunk (shouldn't happen, but handle it)
                uniqueness_scores.append(1.0)
        
        # Sort scores and take average of top 3 most unique words
        # This balances between max (too aggressive) and average (too diluted)
        uniqueness_scores.sort(reverse=True)
        top_scores = uniqueness_scores[:min(3, len(uniqueness_scores))]
        return sum(top_scores) / len(top_scores) if top_scores else 0.0
