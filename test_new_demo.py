"""
Test the new simplified demo (no needle injection).
"""

import requests

# API endpoint
API_BASE = 'http://localhost:5000'

# Load a sample document
with open('test_data/haystack.txt', 'r', encoding='utf-8') as f:
    document = f.read()

# Test query
query = "What is machine learning?"

print("=" * 80)
print("SIGNAL-CORE DEMO TEST (No Needle)")
print("=" * 80)
print(f"\nDocument size: {len(document.split())} words")
print(f"Query: {query}")
print("\n" + "=" * 80)

# Test Full Document
print("\n[1/2] Testing Full Document...")
print("-" * 80)

try:
    response = requests.post(
        f'{API_BASE}/api/test-naive',
        json={
            'document': document,
            'query': query
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: SUCCESS")
        print(f"\nAnswer:")
        print(f"  {data['response'][:200]}...")
        print(f"\nTokens Used: {data['tokens']:,}")
        
    else:
        print(f"✗ Status: FAILED (HTTP {response.status_code})")
        
except Exception as e:
    print(f"✗ Status: ERROR - {str(e)}")

# Test Optimized Document
print("\n" + "=" * 80)
print("\n[2/2] Testing Optimized Document...")
print("-" * 80)

try:
    response = requests.post(
        f'{API_BASE}/api/test-optimized',
        json={
            'document': document,
            'query': query
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: SUCCESS")
        print(f"\nAnswer:")
        print(f"  {data['response'][:200]}...")
        print(f"\nMetrics:")
        print(f"  Original Tokens: {data['original_tokens']:,}")
        print(f"  Optimized Tokens: {data['optimized_tokens']:,}")
        print(f"  Reduction: {data['reduction_percentage']:.1f}%")
        print(f"\n✓ Saved {data['reduction_percentage']:.1f}% in AI costs!")
        
    else:
        print(f"✗ Status: FAILED (HTTP {response.status_code})")
        
except Exception as e:
    print(f"✗ Status: ERROR - {str(e)}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
