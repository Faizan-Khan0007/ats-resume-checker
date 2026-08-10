// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const jobRoleInput = document.getElementById('jobRole');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadForm = document.getElementById('uploadForm');
const loadingOverlay = document.getElementById('loadingOverlay');
const toastContainer = document.getElementById('toast-container');

// Clear any past results from memory so we start fresh
localStorage.removeItem('resumeAnalysisResult');

let selectedFile = null;

// --- 1. Toast Notification System ---
function showToast(message, type = 'error') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = type === 'error' ? '⚠️' : '✅';
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    
    toastContainer.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// --- 2. Drag and Drop UI Logic ---

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
    if (!file) return;

    if (file.type !== 'application/pdf') {
        showToast('Please upload a PDF file.', 'error');
        selectedFile = null;
        fileNameDisplay.classList.add('hidden');
        checkFormReady();
        return;
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
        showToast('File is too large. Maximum size is 5MB.', 'error');
        selectedFile = null;
        fileNameDisplay.classList.add('hidden');
        checkFormReady();
        return;
    }

    selectedFile = file;
    fileNameDisplay.textContent = `✅ ${file.name}`;
    fileNameDisplay.classList.remove('hidden');
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

// --- 3. API Communication Logic ---

let progressIntervals = [];

function resetProgressUI() {
    // Clear any running timers
    progressIntervals.forEach(clearInterval);
    progressIntervals = [];
    
    // Reset all steps to default
    for (let i = 1; i <= 4; i++) {
        const step = document.getElementById(`step-${i}`);
        if(step) {
            step.classList.remove('active', 'completed');
        }
    }
}

function startProgressSimulation() {
    resetProgressUI();
    let currentStep = 1;
    
    // Immediately set step 1 active
    document.getElementById(`step-1`).classList.add('active');
    
    // Move to next steps every 1.8 seconds
    const interval = setInterval(() => {
        if (currentStep < 4) {
            document.getElementById(`step-${currentStep}`).classList.replace('active', 'completed');
            currentStep++;
            document.getElementById(`step-${currentStep}`).classList.add('active');
        } else {
            // Once we hit the end, just pulse on the last step until API responds
            clearInterval(interval);
        }
    }, 1800);
    
    progressIntervals.push(interval);
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!selectedFile || !jobRoleInput.value.trim()) return;

    // Show loading screen and start sequential progress
    loadingOverlay.classList.remove('hidden');
    startProgressSimulation();

    // Prepare the data exactly how FastAPI expects it (FormData)
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('job_role', jobRoleInput.value.trim());

    try {
        // Call local backend API
        const response = await fetch('https://ats-resume-checker-00jy.onrender.com/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed on the server.');
        }

        const resultData = await response.json();
        
        // Success! Fast-forward UI to 100% completed
        resetProgressUI();
        for (let i = 1; i <= 4; i++) {
            document.getElementById(`step-${i}`).classList.add('completed');
        }
        
        // Save the data to local storage so the next page can read it
        localStorage.setItem('resumeAnalysisResult', JSON.stringify(resultData));
        
        // Small delay so user sees the 100% completion before redirect
        setTimeout(() => {
            window.location.href = 'results.html';
        }, 500);

    } catch (error) {
        console.error(error);
        showToast(error.message, 'error');
        resetProgressUI();
        loadingOverlay.classList.add('hidden');
    }
});