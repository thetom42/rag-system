document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const searchForm = document.getElementById('search-form');
    const resultsDiv = document.getElementById('results');

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(uploadForm);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            alert(data.message);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while uploading the file.');
        }
    });

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('search-input').value;
        
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while searching.');
        }
    });

    function displayResults(data) {
        resultsDiv.innerHTML = '';
        
        const answerDiv = document.createElement('div');
        answerDiv.className = 'result';
        answerDiv.innerHTML = `<strong>Answer:</strong> ${data.answer}`;
        resultsDiv.appendChild(answerDiv);

        const contextHeader = document.createElement('h3');
        contextHeader.textContent = 'Context:';
        resultsDiv.appendChild(contextHeader);

        data.context.forEach((chunk, index) => {
            const chunkDiv = document.createElement('div');
            chunkDiv.className = 'result';
            chunkDiv.innerHTML = `<strong>Chunk ${index + 1}:</strong> ${chunk}`;
            resultsDiv.appendChild(chunkDiv);
        });
    }
});
