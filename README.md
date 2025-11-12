# Signal-Core

A two-stage algorithmic pipeline designed to optimize long-context inputs for Large Language Models (LLMs). Signal-Core addresses the "Lost in the Middle" problem by removing noise and preserving signal, increasing LLM accuracy while reducing token costs.

## Features

- **Semantic Chunker**: Splits documents at optimal semantic boundaries
- **Sentence-Level Pruner**: Extracts the most important sentences from each chunk
- **NIAH Demo**: Interactive demonstration comparing Naive RAG vs Optimized RAG

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
- Paste a long document (10,000+ words) in the haystack field
- Enter a needle fact to inject
- Set the injection depth (0-100%)
- Enter a query question
- Compare Naive RAG vs Optimized RAG results

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

1. **Stage 1: Semantic Chunker** - Splits documents at optimal semantic boundaries using Dynamic Programming
2. **Stage 2: Sentence-Level Pruner** - Extracts the most important sentences using TextRank algorithm

This approach maintains semantic coherence while reducing token count by up to 80%.

## License

MIT
