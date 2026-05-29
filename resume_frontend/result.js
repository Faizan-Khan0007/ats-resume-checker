document.addEventListener('DOMContentLoaded', () => {
    // 1. Pull the data from local storage
    const rawData = localStorage.getItem('resumeAnalysisResult');

    // If someone tries to visit results.html directly without uploading, kick them back
    if (!rawData) {
        window.location.href = 'analyze.html';
        return;
    }

    const response = JSON.parse(rawData);
    const aiData = response.data; // This matches our Pydantic schema!

    // 2. Display Cache Badge if it was instant
    if (response.cached) {
        document.getElementById('cacheBadge').classList.remove('hidden');
    }

    // 3. Render the Chart.js Doughnut
    renderScoreChart(aiData.ats_score);
    
    // 4. Update basic text fields
    document.getElementById('keywordMatchDisplay').textContent = `${aiData.keyword_match_percentage}%`;

    // 5. Populate Skills Pills
    populatePills('skillsFoundContainer', aiData.skills_found, 'success-pill');
    populatePills('skillsMissingContainer', aiData.skills_missing, 'danger-pill');

    // 6. Populate AI Suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    aiData.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });

    // 7. Render Exotic Feature: Line Rewrites
    renderRewrites(aiData.line_rewrites);

    // 8. Render Exotic Feature: Keyword Strategy
    renderStrategies(aiData.keyword_strategies);
});

// --- Helper Functions ---

function renderScoreChart(score) {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    
    // Determine color based on score
    let chartColor = '#ef4444'; // Red
    if (score >= 50) chartColor = '#eab308'; // Yellow
    if (score >= 75) chartColor = '#22c55e'; // Green

    // Animate the number counting up
    animateValue("atsScoreDisplay", 0, score, 1500);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [chartColor, 'rgba(255, 255, 255, 0.05)'],
                borderWidth: 0,
                borderRadius: 20
            }]
        },
        options: {
            cutout: '80%',
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                animateScale: true,
                animateRotate: true,
                duration: 1500
            },
            plugins: { tooltip: { enabled: false } }
        }
    });
}

function animateValue(id, start, end, duration) {
    let obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function populatePills(containerId, items, className) {
    const container = document.getElementById(containerId);
    if (!items || items.length === 0) {
        container.innerHTML = '<span style="color: #94a3b8; font-size: 0.9rem;">None detected</span>';
        return;
    }
    items.forEach(item => {
        const span = document.createElement('span');
        span.className = `skill-pill ${className}`;
        span.textContent = item;
        container.appendChild(span);
    });
}

function renderRewrites(rewrites) {
    const container = document.getElementById('rewritesContainer');
    if (!rewrites || rewrites.length === 0) {
        container.innerHTML = '<p style="color: #94a3b8;">Your bullet points look solid!</p>';
        return;
    }
    
    rewrites.forEach(item => {
        const div = document.createElement('div');
        div.className = 'rewrite-block';
        div.innerHTML = `
            <div class="weak-line">"${item.original_line}"</div>
            <p style="color: var(--text-secondary); font-size: 0.9rem;"><strong>Why it's weak:</strong> ${item.why_its_weak}</p>
            <div class="strong-line">Try this instead: <br>➔ "${item.rewritten_options[0]}"</div>
        `;
        container.appendChild(div);
    });
}

function renderStrategies(strategies) {
    const container = document.getElementById('strategyContainer');
    if (!strategies || strategies.length === 0) {
        container.innerHTML = '<p style="color: #94a3b8;">No specific strategies needed.</p>';
        return;
    }

    strategies.forEach(item => {
        const div = document.createElement('div');
        div.className = 'strategy-block';
        div.innerHTML = `
            <strong style="color: white;">Missing: ${item.missing_keyword}</strong>
            <p style="color: var(--text-secondary); margin: 8px 0; font-size: 0.95rem;"><strong>Where to put it:</strong> ${item.where_to_add}</p>
            <div style="background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 6px; font-style: italic; color: #a1a1aa;">
                " ${item.example_sentence} "
            </div>
        `;
        container.appendChild(div);
    });
}