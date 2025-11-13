// API endpoint base URL
const API_BASE = 'http://localhost:5000';

// Get DOM elements
const documentInput = document.getElementById('document');
const queryInput = document.getElementById('query');
const btnNaive = document.getElementById('btn-naive');
const btnOptimized = document.getElementById('btn-optimized');
const loadingDiv = document.getElementById('loading');
const naiveResultDiv = document.getElementById('naive-result');
const optimizedResultDiv = document.getElementById('optimized-result');

// Loading indicator functions
function showLoading() {
    loadingDiv.style.display = 'block';
}

function hideLoading() {
    loadingDiv.style.display = 'none';
}

// Input validation
function validateInputs() {
    const document = documentInput.value.trim();
    const query = queryInput.value.trim();

    if (!document) {
        alert('Please enter a document');
        return false;
    }

    if (!query) {
        alert('Please enter a question');
        return false;
    }

    return true;
}

// Display naive RAG result
function displayNaiveResult(data) {
    const resultContent = naiveResultDiv.querySelector('.result-content');
    
    resultContent.innerHTML = `
        <div class="response">
            <h3>Answer:</h3>
            <p>${escapeHtml(data.response)}</p>
        </div>
        <div class="metrics">
            <h3>Cost:</h3>
            <p><strong>Tokens Used:</strong> ${data.tokens.toLocaleString()}</p>
            <p class="note">Using the full document without optimization</p>
        </div>
    `;
}

// Display optimized RAG result
function displayOptimizedResult(data) {
    const resultContent = optimizedResultDiv.querySelector('.result-content');
    
    const savings = ((data.original_tokens - data.optimized_tokens) / data.original_tokens * 100).toFixed(1);
    
    resultContent.innerHTML = `
        <div class="response">
            <h3>Answer:</h3>
            <p>${escapeHtml(data.response)}</p>
        </div>
        <div class="metrics">
            <h3>Cost Savings:</h3>
            <p><strong>Original:</strong> ${data.original_tokens.toLocaleString()} tokens</p>
            <p><strong>Optimized:</strong> ${data.optimized_tokens.toLocaleString()} tokens</p>
            <p class="savings"><strong>Saved ${savings}% in AI costs!</strong></p>
            <p class="note">SignalCore filtered out redundant content while preserving the answer</p>
        </div>
    `;
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Test Naive RAG
async function testNaive() {
    if (!validateInputs()) {
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/api/test-naive`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document: documentInput.value,
                query: queryInput.value
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayNaiveResult(data);
    } catch (error) {
        console.error('Error querying full document:', error);
        const resultContent = naiveResultDiv.querySelector('.result-content');
        resultContent.innerHTML = `
            <div class="error">
                <p><strong>Error:</strong> Failed to process request. Please check if the backend server is running.</p>
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// Test Optimized RAG
async function testOptimized() {
    if (!validateInputs()) {
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/api/test-optimized`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document: documentInput.value,
                query: queryInput.value
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayOptimizedResult(data);
    } catch (error) {
        console.error('Error querying optimized document:', error);
        const resultContent = optimizedResultDiv.querySelector('.result-content');
        resultContent.innerHTML = `
            <div class="error">
                <p><strong>Error:</strong> Failed to process request. Please check if the backend server is running.</p>
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// Add event listeners
btnNaive.addEventListener('click', testNaive);
btnOptimized.addEventListener('click', testOptimized);
