document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('historyGrid');
    const emptyState = document.getElementById('emptyState');

    try {
        // Fetch data from our new FastAPI endpoint
        const response = await fetch('https://ats-resume-checker-00jy.onrender.com/history');
        
        if (!response.ok) {
            throw new Error('Failed to fetch history from the server.');
        }

        const data = await response.json();

        // Check if database is empty
        if (data.length === 0) {
            emptyState.classList.remove('hidden');
            return;
        }

        // Loop through the database results and build a card for each one
        data.forEach(item => {
            // Format the timestamp into a readable date (e.g., "May 25, 2026")
            const dateStr = new Date(item.created_at).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric'
            });

            // Determine the color of the score ring based on the result
            let scoreColor = '#22c55e'; // Green
            if (item.ats_score < 50) scoreColor = '#ef4444'; // Red
            else if (item.ats_score < 75) scoreColor = '#eab308'; // Yellow

            const card = document.createElement('div');
            card.className = 'history-card';
            card.innerHTML = `
                <div class="history-header">
                    <div>
                        <div class="history-role">${item.job_role}</div>
                        <div class="history-filename">📄 ${item.filename}</div>
                    </div>
                    <div class="history-score-circle" style="color: ${scoreColor}; border: 2px solid ${scoreColor};">
                        ${item.ats_score}
                    </div>
                </div>
                <div class="history-footer">
                    <span>${dateStr}</span>
                    <span style="color: var(--text-secondary);">ID: #${item.id}</span>
                </div>
            `;
            
            grid.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        grid.innerHTML = `<p class="error-message" style="grid-column: 1/-1;">Connection error. Make sure your FastAPI backend is running.</p>`;
    }
});