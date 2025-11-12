"""
End-to-end integration test for Signal-Core demo.
This script tests both Naive RAG and Optimized RAG endpoints.
"""

import requests
import json

# API endpoint
API_BASE = 'http://localhost:5000'

# Load the haystack document
with open('test_data/haystack.txt', 'r', encoding='utf-8') as f:
    haystack = f.read()

# Test parameters
needle = "The secret code is FJORD2024"
injection_depth = 50
query = "What is the secret code?"

print("=" * 80)
print("SIGNAL-CORE END-TO-END INTEGRATION TEST")
print("=" * 80)
print(f"\nTest Configuration:")
print(f"  Haystack size: {len(haystack.split())} words")
print(f"  Needle: {needle}")
print(f"  Injection depth: {injection_depth}%")
print(f"  Query: {query}")
print("\n" + "=" * 80)

# Test Naive RAG
print("\n[1/2] Testing Naive RAG...")
print("-" * 80)

try:
    response = requests.post(
        f'{API_BASE}/api/test-naive',
        json={
            'haystack': haystack,
            'needle': needle,
            'injection_depth': injection_depth,
            'query': query
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: SUCCESS")
        print(f"\nLLM Response:")
        print(f"  {data['response']}")
        print(f"\nMetrics:")
        print(f"  Total Tokens: {data['tokens']:,}")
        
        # Check if the answer contains the secret code
        naive_found_answer = "FJORD2024" in data['response'].upper()
        print(f"\nAnswer Found: {'YES ✓' if naive_found_answer else 'NO ✗'}")
        
    else:
        print(f"✗ Status: FAILED (HTTP {response.status_code})")
        print(f"  Error: {response.text}")
        
except Exception as e:
    print(f"✗ Status: ERROR")
    print(f"  Exception: {str(e)}")

# Test Optimized RAG
print("\n" + "=" * 80)
print("\n[2/2] Testing Optimized RAG...")
print("-" * 80)

try:
    response = requests.post(
        f'{API_BASE}/api/test-optimized',
        json={
            'haystack': haystack,
            'needle': needle,
            'injection_depth': injection_depth,
            'query': query
        },
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: SUCCESS")
        print(f"\nLLM Response:")
        print(f"  {data['response']}")
        print(f"\nMetrics:")
        print(f"  Original Tokens: {data['original_tokens']:,}")
        print(f"  Optimized Tokens: {data['optimized_tokens']:,}")
        print(f"  Reduction: {data['reduction_percentage']:.1f}%")
        
        # Check if the answer contains the secret code
        optimized_found_answer = "FJORD2024" in data['response'].upper()
        print(f"\nAnswer Found: {'YES ✓' if optimized_found_answer else 'NO ✗'}")
        
        # Check if reduction meets target (70%+)
        meets_target = data['reduction_percentage'] >= 70.0
        print(f"Meets 70% Reduction Target: {'YES ✓' if meets_target else 'NO ✗'}")
        
    else:
        print(f"✗ Status: FAILED (HTTP {response.status_code})")
        print(f"  Error: {response.text}")
        
except Exception as e:
    print(f"✗ Status: ERROR")
    print(f"  Exception: {str(e)}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
