(function () {
  const dropZone = document.getElementById('drop-zone');
  const input = document.getElementById('file-input');
  const preview = document.getElementById('preview');
  const placeholder = document.getElementById('placeholder');
  const submitBtn = document.getElementById('submit-btn');
  const form = document.getElementById('lens-form');
  const scanOverlay = document.getElementById('scan-overlay');
  const scanLine = document.getElementById('scan-line');
  if (!dropZone) return;

  dropZone.addEventListener('click', () => input.click());

  ['dragenter', 'dragover'].forEach(ev =>
    dropZone.addEventListener(ev, e => { e.preventDefault(); dropZone.classList.add('border-cyan-400'); })
  );
  ['dragleave', 'drop'].forEach(ev =>
    dropZone.addEventListener(ev, e => { e.preventDefault(); dropZone.classList.remove('border-cyan-400'); })
  );

  dropZone.addEventListener('drop', e => {
    const file = e.dataTransfer.files[0];
    if (file) { input.files = e.dataTransfer.files; showPreview(file); }
  });

  input.addEventListener('change', () => { if (input.files[0]) showPreview(input.files[0]); });

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.classList.remove('hidden');
      placeholder.classList.add('hidden');
      submitBtn.disabled = false;
      submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    };
    reader.readAsDataURL(file);
  }

  form.addEventListener('submit', () => {
    submitBtn.innerHTML = '⏳ Analyzing...';
    submitBtn.disabled = true;
    scanOverlay.classList.remove('hidden');
    let pos = 0;
    setInterval(() => { pos = (pos + 2) % 100; scanLine.style.top = pos + '%'; }, 12);
  });
})();