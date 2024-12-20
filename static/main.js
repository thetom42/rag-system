document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const suggestionsContainer = document.getElementById('suggestions-container');
    const resultsDiv = document.getElementById('results');
    const documentList = document.getElementById('document-list');

    function toggleLoading(elementId, isLoading) {
        const element = document.getElementById(elementId);
        if (isLoading) {
            element.classList.add('loading');
            element.disabled = true;
        } else {
            element.classList.remove('loading');
            element.disabled = false;
        }
    }

    function displaySelectedFiles() {
        const fileInput = document.querySelector('input[type="file"]');
        const fileList = document.getElementById('selected-files');
        fileList.innerHTML = '';
        for (const file of fileInput.files) {
            const li = document.createElement('li');
            li.textContent = file.name;
            fileList.appendChild(li);
        }
    }

    document.querySelector('input[type="file"]').addEventListener('change', displaySelectedFiles);

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        toggleLoading('upload-button', true);
        const formData = new FormData(uploadForm);
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                displayUploadResults(data);
                updateDocumentList();
            } else {
                throw new Error(data.error || 'An error occurred while uploading the file(s).');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        } finally {
            toggleLoading('upload-button', false);
        }
    });

    let debounceTimer;
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(getSuggestions, 300);
    });

    async function getSuggestions() {
        const query = searchInput.value;
        console.log('Getting suggestions for query:', query);
        if (query.length < 2) {
            suggestionsContainer.innerHTML = '';
            return;
        }

        try {
            console.log('Sending request to /suggestions with query:', query);
            const response = await fetch('/suggestions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });
            console.log('Received response:', response);
            const data = await response.json();
            console.log('Received data:', data);
            if (response.ok) {
                console.log('Suggestions received:', data.suggestions);
                displaySuggestions(data.suggestions);
            } else {
                console.error('Error in response:', data.error);
                throw new Error(data.error || 'An error occurred while fetching suggestions.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function displaySuggestions(suggestions) {
        console.log('Displaying suggestions:', suggestions);
        suggestionsContainer.innerHTML = '';
        if (suggestions.length === 0) {
            console.log('No suggestions to display');
            return;
        }
        suggestions.forEach(suggestion => {
            const div = document.createElement('div');
            div.classList.add('suggestion');
            div.textContent = suggestion;
            div.addEventListener('click', () => {
                searchInput.value = suggestion;
                suggestionsContainer.innerHTML = '';
                searchForm.dispatchEvent(new Event('submit'));
            });
            suggestionsContainer.appendChild(div);
        });
    }

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        toggleLoading('search-button', true);
        const query = searchInput.value;
        suggestionsContainer.innerHTML = '';
        
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });
            const data = await response.json();
            if (response.ok) {
                displaySearchResults(data, query);
            } else {
                throw new Error(data.error || 'An error occurred while searching.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        } finally {
            toggleLoading('search-button', false);
        }
    });

    function displayUploadResults(data) {
        resultsDiv.innerHTML = `
            <h3>Upload Results</h3>
            <p>${data.message}</p>
            <h4>Document Statistics:</h4>
            <ul>
                ${data.documents.map(doc => `
                    <li>
                        <strong>${doc.filename}</strong>
                        <ul>
                            <li>Number of pages: ${doc.num_pages}</li>
                            <li>Number of chunks: ${doc.stats.num_chunks}</li>
                            <li>Total words: ${doc.stats.total_words}</li>
                            <li>Total characters: ${doc.stats.total_characters}</li>
                            <li>Average chunk size: ${doc.stats.avg_chunk_size} characters</li>
                        </ul>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    function displaySearchResults(data, query) {
        const highlightText = (text, query) => {
            const regex = new RegExp(`(${query})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        };

        resultsDiv.innerHTML = `
            <h3>Search Results</h3>
            <div class="answer">${data.answer}</div>
            <h4>Context:</h4>
            ${data.context.map((chunk, index) => `
                <div class="context-chunk">
                    <h5>Context ${index + 1}</h5>
                    <pre>${highlightText(chunk, query)}</pre>
                </div>
            `).join('')}
        `;
    }

    async function updateDocumentList() {
        try {
            const response = await fetch('/documents');
            if (response.ok) {
                const documents = await response.json();
                documentList.innerHTML = documents.map(doc => `
                    <li>
                        <strong>${doc.filename}</strong>
                        <ul>
                            <li>Pages: ${doc.num_pages}</li>
                            <li>Chunks: ${doc.stats.num_chunks}</li>
                        </ul>
                        <button onclick="deleteDocument('${doc.id}')">Delete</button>
                    </li>
                `).join('');
            } else {
                throw new Error('Failed to fetch the document list.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    }

    window.deleteDocument = async (documentId) => {
        if (confirm('Are you sure you want to delete this document?')) {
            try {
                const response = await fetch(`/documents/${documentId}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    updateDocumentList();
                } else {
                    throw new Error('Failed to delete the document.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            }
        }
    };

    updateDocumentList();
});