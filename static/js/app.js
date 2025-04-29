const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const processBtn = document.getElementById('process-btn');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const previewContainer = document.getElementById('preview-container');
const downloadZipBtn = document.getElementById('download-zip');

let files = [];
let processed = {};

// Drag & Drop handlers
['dragenter', 'dragover'].forEach(evt => {
  dropZone.addEventListener(evt, e => {
    e.preventDefault();
    dropZone.classList.add('bg-light');
  });
});
['dragleave', 'drop'].forEach(evt => {
  dropZone.addEventListener(evt, e => {
    e.preventDefault();
    dropZone.classList.remove('bg-light');
  });
});

dropZone.addEventListener('drop', e => {
  files = Array.from(e.dataTransfer.files);
  updateList();
});

dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', () => {
  files = Array.from(fileInput.files);
  updateList();
});

function updateList() {
  processBtn.disabled = files.length === 0;
  dropZone.querySelector('p').textContent = files.map(f => f.name).join(', ');
}

processBtn.addEventListener('click', async () => {
  progressContainer.classList.remove('d-none');
  previewContainer.innerHTML = '';
  const rules = JSON.parse(localStorage.getItem('rules') || '{}');
  const payload = [];

  for (let i = 0; i < files.length; i++) {
    const content = await files[i].text();
    payload.push({ name: files[i].name, content });
    const pct = ((i + 1) / files.length) * 100;
    progressBar.style.width = `${pct}%`;
    progressBar.textContent = `${Math.round(pct)}%`;
  }

  const res = await fetch('/api/remove', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ files: payload, rules })
  });
  const data = await res.json();
  processed = data.files;

  showPreview(payload);
  downloadZipBtn.classList.remove('d-none');
});

function showPreview(origList) {
  origList.forEach(f => {
    const clean = processed[f.name];
    const row = document.createElement('div');
    row.className = 'row g-2 mb-4';

    // Original column
    const ocol = document.createElement('div');
    ocol.className = 'col-md-6';
    const ocard = document.createElement('div');
    ocard.className = 'card';
    ocard.innerHTML = `
      <div class="card-header bg-light"><strong>Original: ${f.name}</strong></div>
      <pre class="language-${f.name.split('.').pop()}">${escapeHtml(f.content)}</pre>
    `;
    ocol.appendChild(ocard);

    // Cleaned column
    const ccol = document.createElement('div');
    ccol.className = 'col-md-6';
    const ccard = document.createElement('div');
    ccard.className = 'card';
    ccard.innerHTML = `
      <div class="card-header bg-light"><strong>Processed: ${f.name}</strong></div>
      <pre class="language-${f.name.split('.').pop()}">${escapeHtml(clean)}</pre>
    `;
    ccol.appendChild(ccard);

    row.appendChild(ocol);
    row.appendChild(ccol);
    previewContainer.appendChild(row);

    // Highlight code
    Prism.highlightElement(ocard.querySelector('pre'));
    Prism.highlightElement(ccard.querySelector('pre'));
  });

  downloadZipBtn.onclick = () => {
    const zip = new JSZip();
    Object.entries(processed).forEach(([name, txt]) => zip.file(name, txt));
    zip.generateAsync({ type: 'blob' }).then(blob => saveAs(blob, 'uncommented_files.zip'));
  };
}

// Utility to escape HTML in code blocks
function escapeHtml(str) {
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
}