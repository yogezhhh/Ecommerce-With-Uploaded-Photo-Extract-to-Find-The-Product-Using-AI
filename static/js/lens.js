(function () {
  const dropZone = document.getElementById('drop-zone');
  const input = document.getElementById('file-input');
  const preview = document.getElementById('preview');
  const placeholder = document.getElementById('placeholder');
  const submitBtn = document.getElementById('submit-btn');
  if (!dropZone) return;

  dropZone.addEventListener('click', () => input.click());

  dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('border-cyan-400'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('border-cyan-400'));
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-cyan-400');
    if (e.dataTransfer.files[0]) { input.files = e.dataTransfer.files; showPreview(e.dataTransfer.files[0]); }
  });

  input.addEventListener('change', () => { if (input.files[0]) showPreview(input.files[0]); });

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.classList.remove('hidden');
      placeholder.classList.add('hidden');
      submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }
})();