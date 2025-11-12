"""
Utility functions for Signal-Core pipeline.
"""

def inject_needle(haystack: str, needle: str, depth_percentage: int) -> str:
    """
    Inject needle at specified depth (0-100%) in haystack.
    
    Args:
        haystack: The full document text
        needle: The fact to inject
        depth_percentage: Where to inject (0 = start, 100 = end)
    
    Returns:
        Document with needle injected at the specified position
    """
    # Split haystack into words
    words = haystack.split()
    
    # Calculate injection point based on depth percentage
    injection_point = int(len(words) * (depth_percentage / 100))
    
    # Insert needle at calculated position
    words.insert(injection_point, needle)
    
    # Return combined document
    return ' '.join(words)
