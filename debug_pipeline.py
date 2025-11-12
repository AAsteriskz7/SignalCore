"""
Debug script to understand what's happening in the pipeline.
"""

from backend.pipeline import SignalCorePipeline
from backend.utils import inject_needle

# Load the haystack document
with open('test_data/haystack.txt', 'r', encoding='utf-8') as f:
    haystack = f.read()

# Test parameters
needle = "The secret code is FJORD2024"
injection_depth = 50

# Inject needle
document = inject_needle(haystack, needle, injection_depth)

# Check if needle is in the document
print(f"Needle in original document: {needle in document}")
print(f"Original document word count: {len(document.split())}")

# Process through pipeline
pipeline = SignalCorePipeline()
optimized_context, metrics = pipeline.process(document)

# Check if needle is in optimized context
print(f"\nNeedle in optimized context: {needle in optimized_context}")
print(f"Optimized document word count: {len(optimized_context.split())}")
print(f"\nMetrics:")
print(f"  Original tokens: {metrics['original_tokens']:,}")
print(f"  Optimized tokens: {metrics['optimized_tokens']:,}")
print(f"  Reduction: {metrics['reduction_percentage']:.1f}%")

# Find where the needle should be
words = document.split()
injection_point = int(len(words) * (injection_depth / 100))
context_start = max(0, injection_point - 50)
context_end = min(len(words), injection_point + 50)
context = ' '.join(words[context_start:context_end])

print(f"\nContext around injection point (words {context_start}-{context_end}):")
print(context)

# Check if this context is in the optimized version
if needle in optimized_context:
    print("\n✓ Needle preserved in optimized context!")
else:
    print("\n✗ Needle was removed during optimization!")
    
    # Find which chunk contained the needle
    chunks = pipeline.chunker.chunk(document)
    for i, chunk in enumerate(chunks):
        if needle in chunk:
            print(f"\nNeedle was in chunk {i+1}/{len(chunks)}")
            print(f"Chunk word count: {len(chunk.split())}")
            
            # Prune this chunk
            pruned = pipeline.pruner.prune(chunk)
            print(f"Pruned chunk word count: {len(pruned.split())}")
            print(f"Needle in pruned chunk: {needle in pruned}")
            
            if needle not in pruned:
                print("\n✗ The needle was removed during sentence pruning!")
                print("This is the problem - the pruner is removing the needle sentence.")
            break
