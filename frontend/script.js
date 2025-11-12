// API endpoint base URL
const API_BASE = 'http://localhost:5000';

// Get DOM elements
const haystackInput = document.getElementById('haystack');
const needleInput = document.getElementById('needle');
const depthInput = document.getElementById('depth');
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
    const haystack = haystackInput.value.trim();
    const needle = needleInput.value.trim();
    const depth = depthInput.value.trim();
    const query = queryInput.value.trim();

    if (!haystack) {
        alert('Please enter a haystack document');
        return false;
    }

    if (!needle) {
        alert('Please enter a needle');
        return false;
    }

    if (!depth || depth < 0 || depth > 100) {
        alert('Please enter a valid injection depth (0-100)');
        return false;
    }

    if (!query) {
        alert('Please enter a query');
        return false;
    }

    return true;
}

// Display naive RAG result
function displayNaiveResult(data) {
    const resultContent = naiveResultDiv.querySelector('.result-content');
    
    resultContent.innerHTML = `
        <div class="response">
            <h3>LLM Response:</h3>
            <p>${escapeHtml(data.response)}</p>
        </div>
        <div class="metrics">
            <h3>Metrics:</h3>
            <p><strong>Total Tokens:</strong> ${data.tokens.toLocaleString()}</p>
        </div>
    `;
}

// Display optimized RAG result
function displayOptimizedResult(data) {
    const resultContent = optimizedResultDiv.querySelector('.result-content');
    
    resultContent.innerHTML = `
        <div class="response">
            <h3>LLM Response:</h3>
            <p>${escapeHtml(data.response)}</p>
        </div>
        <div class="metrics">
            <h3>Metrics:</h3>
            <p><strong>Original Tokens:</strong> ${data.original_tokens.toLocaleString()}</p>
            <p><strong>Optimized Tokens:</strong> ${data.optimized_tokens.toLocaleString()}</p>
            <p><strong>Reduction:</strong> ${data.reduction_percentage.toFixed(1)}%</p>
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
                haystack: haystackInput.value,
                needle: needleInput.value,
                injection_depth: parseInt(depthInput.value),
                query: queryInput.value
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayNaiveResult(data);
    } catch (error) {
        console.error('Error testing naive RAG:', error);
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
                haystack: haystackInput.value,
                needle: needleInput.value,
                injection_depth: parseInt(depthInput.value),
                query: queryInput.value
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayOptimizedResult(data);
    } catch (error) {
        console.error('Error testing optimized RAG:', error);
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

// Clamp depth input to 0-100 range
depthInput.addEventListener('input', function() {
    const value = parseInt(this.value);
    if (value < 0) this.value = 0;
    if (value > 100) this.value = 100;
});
