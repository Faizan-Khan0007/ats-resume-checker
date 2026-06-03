// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const jobRoleInput = document.getElementById('jobRole');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadForm = document.getElementById('uploadForm');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorMessage = document.getElementById('errorMessage');
// Clear any past results from memory so we start fresh
localStorage.removeItem('resumeAnalysisResult');

let selectedFile = null;

// --- 1. Drag and Drop UI Logic ---

// Highlight zone when dragging file over it
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
});

// Remove highlight when dragging leaves
['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });
});

// Handle the actual drop
dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    handleFile(files[0]);
});

// Handle click on "Browse" button
browseBtn.addEventListener('click', () => {
    fileInput.click();
});

// Handle file selection via browse window
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Validate and store the file
function handleFile(file) {
    errorMessage.textContent = ''; // Clear old errors
    
    if (!file) return;

    if (file.type !== 'application/pdf') {
        showError('Please upload a PDF file.');
        return;
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
        showError('File is too large. Maximum size is 5MB.');
        return;
    }

    selectedFile = file;
    fileNameDisplay.textContent = `✅ ${file.name} ready!`;
    checkFormReady();
}

// Enable button only if both file and text are present
jobRoleInput.addEventListener('input', checkFormReady);

function checkFormReady() {
    if (selectedFile && jobRoleInput.value.trim() !== '') {
        analyzeBtn.disabled = false;
    } else {
        analyzeBtn.disabled = true;
    }
}

function showError(msg) {
    errorMessage.textContent = msg;
    selectedFile = null;
    fileNameDisplay.textContent = '';
    analyzeBtn.disabled = true;
}

// --- 2. API Communication Logic ---

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!selectedFile || !jobRoleInput.value.trim()) return;

    // Show loading screen
    loadingOverlay.classList.remove('hidden');
    errorMessage.textContent = '';

    // Prepare the data exactly how FastAPI expects it (FormData)
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('job_role', jobRoleInput.value.trim());

    try {
        // Call your local backend API!
        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed on the server.');
        }

        const resultData = await response.json();
        
        // Success! Save the data to local storage so the next page can read it
        localStorage.setItem('resumeAnalysisResult', JSON.stringify(resultData));
        
        // Redirect to the results page (which we will build tomorrow!)
        window.location.href = 'results.html';

    } catch (error) {
        console.error(error);
        showError(`Error: ${error.message}`);
        loadingOverlay.classList.add('hidden');
    }
});