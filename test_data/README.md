# NIAH Test Data

This directory contains test data for the Needle in a Haystack (NIAH) test used to demonstrate Signal-Core's effectiveness.

## Test Document

**File:** `haystack.txt`

**Description:** A 10,000+ word document created by concatenating content about various technology topics including:
- Artificial Intelligence and Machine Learning
- Climate Change and Environmental Science
- Space Exploration and Astronomy
- Quantum Computing and Physics
- Biotechnology and Genetic Engineering
- Blockchain and Cryptocurrency
- Neuroscience and Brain Research
- Robotics and Automation
- Cybersecurity and Information Security
- Internet of Things and Smart Devices
- Virtual Reality and Augmented Reality

## Test Parameters

### Needle
```
The secret code is FJORD2024
```

### Query
```
What is the secret code?
```

### Injection Depth
**Recommended:** 50% (the "dead zone" where LLMs typically fail)

This depth is chosen because it represents the middle of the document where the "Lost in the Middle" problem is most pronounced.

## Expected Behavior

### Naive RAG (Full Document)
- **Expected Result:** FAILS to retrieve the correct answer at 50% depth
- **Reason:** The needle gets lost in the middle of the long context
- **Token Count:** ~13,000+ tokens

### Optimized RAG (Signal-Core Processed)
- **Expected Result:** SUCCEEDS in retrieving the correct answer at 50% depth
- **Reason:** Signal-Core removes noise while preserving the needle
- **Token Count:** ~2,600-3,900 tokens (70-80% reduction)
- **Reduction:** 70%+ token reduction expected

## Usage

1. Load `haystack.txt` into the demo UI
2. Enter the needle: "The secret code is FJORD2024"
3. Set injection depth to 50%
4. Enter the query: "What is the secret code?"
5. Click "Test Naive RAG" - observe failure
6. Click "Test Optimized RAG" - observe success with significant token reduction

## Notes

- The document is designed to be semantically diverse to test the chunking algorithm
- Each section contains dense, technical content to challenge the pruning algorithm
- The 50% injection depth is the optimal demonstration point for the "Lost in the Middle" problem
