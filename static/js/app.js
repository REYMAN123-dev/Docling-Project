const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const loading = document.getElementById('loading');
const result = document.getElementById('result');

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

async function handleFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    loading.style.display = 'block';
    result.style.display = 'none';
    
    try {
        const response = await fetch('/upload/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult('success', data.message, data);
        } else {
            showResult('error', data.detail || 'An error occurred');
        }
    } catch (error) {
        showResult('error', 'Network error: ' + error.message);
    } finally {
        loading.style.display = 'none';
    }
}

function showResult(type, message, data = null) {
    result.className = `result ${type}`;
    result.style.display = 'block';
    
    let content = `<h3>${message}</h3>`;
    
    if (data) {
        // Add status badge
        const statusClass = data.status === 'already_available' ? 'status-cached' : 'status-new';
        const statusText = data.status === 'already_available' ? '📋 Retrieved from Database' : '🆕 Newly Processed';
        content += `<div class="status-badge ${statusClass}">${statusText}</div>`;
        
        // Add file information
        if (data.filename) {
            content += `
                <div class="file-info">
                    <h4>📄 File Information</h4>
                    <p><strong>Filename:</strong> ${data.filename}</p>
                    <p><strong>File Type:</strong> ${data.file_type || 'Unknown'}</p>
                    <p><strong>File Hash:</strong> ${data.file_hash || 'N/A'}</p>
                    ${data.created_at ? `<p><strong>Processed:</strong> ${new Date(data.created_at).toLocaleString()}</p>` : ''}
                </div>
            `;
        }
        
        // Add JSON preview
        if (data.data) {
            content += `
                <div class="json-preview">
                    <strong>📊 Extracted JSON Data:</strong>
                    <pre>${JSON.stringify(data.data, null, 2)}</pre>
                </div>
            `;
        }
        
        // Add download button
        if (data.data) {
            const jsonBlob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
            const downloadUrl = URL.createObjectURL(jsonBlob);
            const downloadName = data.filename ? data.filename.replace(/\.[^/.]+$/, '.json') : 'extracted_data.json';
            
            content += `
                <div style="margin-top: 20px;">
                    <a href="${downloadUrl}" download="${downloadName}" class="btn btn-secondary">
                        📥 Download JSON File
                    </a>
                </div>
            `;
        }
    }
    
    result.innerHTML = content;
} 