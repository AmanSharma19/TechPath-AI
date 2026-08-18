document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictor-form');
    const resultsContainer = document.getElementById('results-container');
    const predictionsDiv = document.getElementById('predictions');
    const resetBtn = document.getElementById('reset-btn');

    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const skills = document.getElementById('skills').value;
        const qualification = document.getElementById('qualification').value;
        const experience = document.getElementById('experience_level').value;

        // Show loader
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');

        try {
            const response = await fetch('http://localhost:5000/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    skills: skills,
                    qualification: qualification,
                    experience_level: experience
                })
            });

            const data = await response.json();

            if (data.success && data.predictions) {
                renderPredictions(data.predictions);

                // Hide form, show results
                form.classList.add('hidden');
                resultsContainer.classList.remove('hidden');
            } else {
                alert('Error predicting career path: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('API Error:', error);
            alert('Failed to connect to the backend server. Make sure it is running on port 5000.');
        } finally {
            // Revert button state
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    function renderPredictions(predictions) {
        predictionsDiv.innerHTML = '';

        predictions.forEach((pred, index) => {
            const card = document.createElement('div');
            card.className = `card ${index === 0 ? 'rank-1' : ''}`;

            card.innerHTML = `
                <div class="role-title">${pred.role}</div>
                <div class="confidence">${pred.confidence}% Match</div>
            `;

            predictionsDiv.appendChild(card);
        });
    }

    resetBtn.addEventListener('click', () => {
        resultsContainer.classList.add('hidden');
        form.classList.remove('hidden');
        form.reset();
    });
});
