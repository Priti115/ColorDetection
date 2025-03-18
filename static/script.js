const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const imageContainer = document.getElementById('image-container');
const uploadedImage = document.getElementById('uploaded-image');
const resultDiv = document.getElementById('result');

// Handle Drag and Drop Events
dropArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropArea.classList.add('active');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('active');
});

dropArea.addEventListener('drop', (e) => {
  e.preventDefault();
  dropArea.classList.remove('active');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFileUpload(files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFileUpload(e.target.files[0]);
  }
});

// Handle File Upload
function handleFileUpload(file) {
  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        resultDiv.innerHTML = `<p style='color:red;'>${data.error}</p>`;
      } else {
        uploadedImage.src = data.image_url;
        imageContainer.classList.remove('hidden');
        displayResults(data.results);
      }
    })
    .catch(error => console.error('Error:', error));
}

// Display Color Detection Results
function displayResults(results) {
  resultDiv.innerHTML = '<h3>Detected Colors:</h3>';
  results.forEach(res => {
    resultDiv.innerHTML += `<p>Color: ${res.color_name} | RGB: (${res.r}, ${res.g}, ${res.b}) at (${res.x}, ${res.y})</p>`;
  });
}
