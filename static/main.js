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
            displayUploadResults(data);
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
            displaySearchResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while searching.');
        }
    });

    function displayUploadResults(data) {
        resultsDiv.innerHTML = `
            <h3>Upload Results</h3>
            <p>${data.message}</p>
            <h4>Document Statistics:</h4>
            <ul>
                <li>Number of pages: ${data.num_pages}</li>
                <li>Number of chunks: ${data.stats.num_chunks}</li>
                <li>Total words: ${data.stats.total_words}</li>
                <li>Total characters: ${data.stats.total_characters}</li>
                <li>Average chunk size: ${data.stats.avg_chunk_size} characters</li>
            </ul>
            <h4>Sample Chunks:</h4>
            ${data.chunks.map((chunk, index) => `
                <div class="chunk-sample">
                    <h5>Chunk ${index + 1}</h5>
                    <pre>${chunk}</pre>
                </div>
            `).join('')}
        `;
    }

    function displaySearchResults(data) {
        resultsDiv.innerHTML = `
            <h3>Search Results</h3>
            <div class="answer">${data.answer}</div>
            <h4>Context:</h4>
            ${data.context.map((chunk, index) => `
                <div class="context-chunk">
                    <h5>Context ${index + 1}</h5>
                    <pre>${chunk}</pre>
                </div>
            `).join('')}
        `;
    }
});
