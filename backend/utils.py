"""
Utility functions for Signal-Core pipeline.
"""

def inject_needle(haystack: str, needle: str, depth_percentage: int) -> str:
    """
    Inject needle at specified depth (0-100%) in haystack.
    
    The needle is inserted as a complete sentence at a sentence boundary
    to avoid breaking the document structure.
    
    Args:
        haystack: The full document text
        needle: The fact to inject
        depth_percentage: Where to inject (0 = start, 100 = end)
    
    Returns:
        Document with needle injected at the specified position
    """
    import re
    
    # Split haystack into sentences
    sentences = re.split(r'([.!?])\s+', haystack)
    
    # Reconstruct sentences with their punctuation
    full_sentences = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
            full_sentences.append(sentences[i] + sentences[i + 1])
            i += 2
        else:
            if sentences[i].strip():
                full_sentences.append(sentences[i])
            i += 1
    
    # Calculate injection point based on depth percentage
    injection_point = int(len(full_sentences) * (depth_percentage / 100))
    
    # Ensure needle ends with punctuation
    if not needle.endswith(('.', '!', '?')):
        needle = needle + '.'
    
    # Insert needle at calculated position
    full_sentences.insert(injection_point, needle)
    
    # Return combined document
    return ' '.join(full_sentences)
