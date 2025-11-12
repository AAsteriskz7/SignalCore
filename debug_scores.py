"""
Debug script to see sentence scores.
"""

from backend.algorithms.pruner import SentencePruner
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
from backend.algorithms.chunker import SemanticChunker
chunker = SemanticChunker()
chunks = chunker.chunk(document)

needle_chunk_idx = None
for i, chunk in enumerate(chunks):
    if needle in chunk:
        needle_chunk_idx = i
        needle_chunk = chunk
        break

if needle_chunk_idx is not None:
    print(f"Found needle in chunk {needle_chunk_idx + 1}/{len(chunks)}")
    print(f"Chunk has {len(needle_chunk.split())} words")
    
    # Manually score sentences
    pruner = SentencePruner()
    sentences = pruner._tokenize_sentences(needle_chunk)
    centroid = pruner._calculate_centroid(needle_chunk)
    
    print(f"\nChunk has {len(sentences)} sentences")
    print("\nSentence scores:")
    print("-" * 80)
    
    for idx, sentence in enumerate(sentences):
        sentence_vector = pruner._calculate_word_frequency(sentence)
        similarity_score = pruner._cosine_similarity(sentence_vector, centroid)
        uniqueness_score = pruner._calculate_uniqueness(sentence_vector, centroid)
        combined_score = (0.5 * similarity_score) + (0.5 * uniqueness_score)
        
        is_needle = needle in sentence
        marker = " <-- NEEDLE" if is_needle else ""
        
        print(f"{idx+1}. Score: {combined_score:.4f} (sim: {similarity_score:.4f}, uniq: {uniqueness_score:.4f}){marker}")
        print(f"   {sentence[:100]}...")
        print()
    
    # Show which sentences would be kept
    num_to_keep = max(1, int(len(sentences) * pruner.EXTRACTION_RATIO))
    print(f"\nKeeping top {num_to_keep} out of {len(sentences)} sentences ({pruner.EXTRACTION_RATIO*100:.0f}%)")
