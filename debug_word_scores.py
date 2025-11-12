"""
Debug word-level scores for the needle sentence.
"""

from backend.algorithms.pruner import SentencePruner
from backend.algorithms.chunker import SemanticChunker
from backend.utils import inject_needle
from collections import Counter

# Load the haystack document
with open('test_data/haystack.txt', 'r', encoding='utf-8') as f:
    haystack = f.read()

# Test parameters
needle = "The secret code is FJORD2024"
injection_depth = 50

# Inject needle
document = inject_needle(haystack, needle, injection_depth)

# Find the chunk with the needle
chunker = SemanticChunker()
chunks = chunker.chunk(document)

for i, chunk in enumerate(chunks):
    if needle in chunk:
        print(f"Found needle in chunk {i + 1}/{len(chunks)}")
        
        # Get centroid
        pruner = SentencePruner()
        centroid = pruner._calculate_centroid(chunk)
        
        # Find needle sentence
        sentences = pruner._tokenize_sentences(chunk)
        for sentence in sentences:
            if needle in sentence:
                print(f"\nNeedle sentence: {sentence}")
                
                # Get word frequencies
                sentence_vector = pruner._calculate_word_frequency(sentence)
                
                print(f"\nWord scores:")
                word_scores = []
                for word in sentence_vector.keys():
                    chunk_freq = centroid.get(word, 0)
                    if chunk_freq > 0:
                        idf = 1.0 / (chunk_freq ** 0.5)
                    else:
                        idf = 1.0
                    word_scores.append((word, chunk_freq, idf))
                    print(f"  {word}: chunk_freq={chunk_freq}, idf={idf:.4f}")
                
                # Show top 3
                word_scores.sort(key=lambda x: x[2], reverse=True)
                print(f"\nTop 3 unique words:")
                for word, freq, idf in word_scores[:3]:
                    print(f"  {word}: idf={idf:.4f}")
                
                uniqueness = sum([idf for _, _, idf in word_scores[:3]]) / 3
                print(f"\nUniqueness score (avg of top 3): {uniqueness:.4f}")
                
                break
        
        break
