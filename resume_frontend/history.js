document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('historyGrid');
    const emptyState = document.getElementById('emptyState');
    const toastContainer = document.getElementById('toast-container');

    function showToast(message, type = 'error') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        let icon = type === 'error' ? '⚠️' : '✅';
        toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    try {
        // Fetch data from local backend API
        const response = await fetch('http://127.0.0.1:8000/history');
        
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
            const dateStr = new Date(item.created_at).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric'
            });

            // Determine the color of the score ring
            let scoreColor = 'var(--success)'; 
            if (item.ats_score < 50) scoreColor = 'var(--danger)'; 
            else if (item.ats_score < 75) scoreColor = '#eab308'; // Yellow

            const card = document.createElement('div');
            card.className = 'history-card';
            card.innerHTML = `
                <div class="history-header">
                    <div>
                        <div class="history-role">${item.job_role}</div>
                        <div class="history-filename">📄 ${item.filename}</div>
                    </div>
                    <div class="history-score-circle" style="color: ${scoreColor}; border-color: ${scoreColor};">
                        ${item.ats_score}
                    </div>
                </div>
                <div class="history-footer">
                    <span>${dateStr}</span>
                    <span>ID: #${item.id}</span>
                </div>
            `;
            
            grid.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        showToast('Connection error. Make sure your backend is running.', 'error');
        emptyState.classList.remove('hidden');
    }
});