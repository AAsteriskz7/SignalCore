# Signal-Core

**Smart AI Cost Reduction**: Cut LLM token usage by ~38% while maintaining answer quality.

Signal-Core is a two-stage pipeline that intelligently filters out redundant content from long documents. It reads your document, removes the "fluff" and repetitive sentences, and produces a shorter, "high-signal" version - getting you the same quality answers while using significantly fewer tokens.

## What It Does

When you feed a long document to an LLM, you're paying for every token - including redundant sentences, repetitive explanations, and low-value content. Signal-Core solves this by:

1. **Semantic Chunking**: Splits documents at optimal sentence boundaries
2. **Smart Filtering**: Removes redundant sentences while preserving key information  
3. **Cost Savings**: Reduces tokens by ~38% on average

**Result**: Same quality answers, lower AI costs.

## Demo Results

Using a 10,000-word technical document:
- **Full Document**: 13,398 tokens → Answer: ✓ Correct
- **Optimized Document**: 8,213 tokens → Answer: ✓ Correct  
- **Savings**: 38.7% reduction in AI costs

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

### Installation

1. Clone the repository and navigate to the project directory:
```bash
cd SignalCore
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
- Copy `.env.example` to `.env`
- Get your Gemini API key from https://makersuite.google.com/app/apikey
- Add your API key to the `.env` file:
  ```
  GEMINI_API_KEY=your_actual_api_key_here
  ```

### Running the Application

1. Start the Flask backend server:
```bash
python backend/app.py
```

2. Open the frontend in your browser:
```bash
# Open frontend/index.html in your browser
```

3. Try the demo:
- Paste a long document (e.g., a Wikipedia article, research paper, or technical documentation)
- Enter a question about the content
- Click "Query Full Document" to see the baseline
- Click "Query Optimized Document" to see Signal-Core in action
- Compare the answers and token savings!

### Quick Test

Run the automated test to verify everything works:
```bash
python test_new_demo.py
```

## Project Structure

```
SignalCore/
├── backend/
│   ├── algorithms/
│   │   ├── chunker.py       # Semantic Chunker implementation
│   │   └── pruner.py        # Sentence-Level Pruner implementation
│   ├── app.py               # Flask API server
│   ├── pipeline.py          # Signal-Core Pipeline orchestration
│   ├── llm_client.py        # LLM API client (Gemini)
│   └── utils.py             # Utility functions (needle injection)
├── frontend/
│   ├── index.html           # Web UI
│   ├── styles.css           # Styling
│   └── script.js            # Frontend logic
├── test_data/
│   └── haystack.txt         # Sample test document
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # This file
```

## How It Works

Signal-Core uses a two-stage pipeline:

1. **Stage 1: Semantic Chunker** - Splits documents at optimal sentence boundaries (200-1000 words per chunk)
2. **Stage 2: Sentence-Level Pruner** - Extracts high-signal sentences using centroid-based ranking with uniqueness scoring

The pruner keeps the most important sentences (those most relevant to the document's main topics and containing unique information) while filtering out redundant content. This maintains answer quality while reducing token costs.

## License

MIT
