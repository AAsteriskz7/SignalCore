"""
Debug script to see needle ranking.
"""

from backend.algorithms.pruner import SentencePruner
from backend.algorithms.chunker import SemanticChunker
from backend.utils import inject_needle

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
        
        # Score sentences
        pruner = SentencePruner()
        sentences = pruner._tokenize_sentences(chunk)
        centroid = pruner._calculate_centroid(chunk)
        
        sentence_scores = []
        for idx, sentence in enumerate(sentences):
            sentence_vector = pruner._calculate_word_frequency(sentence)
            similarity_score = pruner._cosine_similarity(sentence_vector, centroid)
            uniqueness_score = pruner._calculate_uniqueness(sentence_vector, centroid)
            combined_score = uniqueness_score
            
            is_needle = needle in sentence
            sentence_scores.append((idx, sentence, combined_score, is_needle))
        
        # Sort by score
        sentence_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Find needle rank
        for rank, (idx, sentence, score, is_needle) in enumerate(sentence_scores, 1):
            if is_needle:
                print(f"\nNeedle rank: {rank} out of {len(sentences)}")
                print(f"Needle score: {score:.4f}")
                print(f"Keeping top {int(len(sentences) * pruner.EXTRACTION_RATIO)} sentences")
                print(f"Needle preserved: {rank <= int(len(sentences) * pruner.EXTRACTION_RATIO)}")
                break
        
        break
