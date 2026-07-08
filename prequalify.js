document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('prequal-form');
  if (!form) return;

  const TOTAL_STEPS = 4;
  let currentStep = 1;

  const panels = form.querySelectorAll('.prequal-step-panel');
  const progressSteps = document.querySelectorAll('.prequal-progress-step');
  const prevBtn = form.querySelector('.prequal-prev');
  const nextBtn = form.querySelector('.prequal-next');
  const submitBtn = form.querySelector('.prequal-submit');
  const messageEl = form.querySelector('.form-message');

  const MAX_FILE_SIZE = 10 * 1024 * 1024;

  const signaturePads = {};

  function showMessage(text, isError = true) {
    if (!messageEl) return;
    messageEl.className = isError ? 'form-message error' : 'form-message success';
    messageEl.textContent = text;
    messageEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function clearMessage() {
    if (!messageEl) return;
    messageEl.className = 'form-message';
    messageEl.textContent = '';
  }

  function goToStep(step) {
    currentStep = step;
    panels.forEach(panel => {
      const n = +panel.dataset.step;
      const active = n === step;
      panel.classList.toggle('active', active);
      panel.hidden = !active;
    });
    progressSteps.forEach(el => {
      const n = +el.dataset.step;
      el.classList.toggle('active', n === step);
      el.classList.toggle('completed', n < step);
    });
    prevBtn.hidden = step === 1;
    nextBtn.hidden = step === TOTAL_STEPS;
    submitBtn.hidden = step !== TOTAL_STEPS;
    clearMessage();
    form.querySelector('.prequal-step-panel.active')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function toggleOther(selectId, otherGroupId, otherInputId) {
    const select = document.getElementById(selectId);
    const group = document.getElementById(otherGroupId);
    const other = document.getElementById(otherInputId);
    if (!select || !group || !other) return;
    const show = select.value === 'Other';
    group.classList.toggle('hidden', !show);
    other.required = show;
    if (!show) other.value = '';
  }

  document.getElementById('industry')?.addEventListener('change', () =>
    toggleOther('industry', 'industry-other-group', 'industry_other'));
  document.getElementById('legal_entity')?.addEventListener('change', () =>
    toggleOther('legal_entity', 'legal-entity-other-group', 'legal_entity_other'));

  toggleOther('industry', 'industry-other-group', 'industry_other');
  toggleOther('legal_entity', 'legal-entity-other-group', 'legal_entity_other');

  form.querySelectorAll('.ssn-input').forEach(input => {
    input.addEventListener('input', () => {
      const digits = input.value.replace(/\D/g, '').slice(0, 9);
      if (digits.length > 5) {
        input.value = `${digits.slice(0, 3)}-${digits.slice(3, 5)}-${digits.slice(5)}`;
      } else if (digits.length > 3) {
        input.value = `${digits.slice(0, 3)}-${digits.slice(3)}`;
      } else {
        input.value = digits;
      }
    });
  });

  form.querySelectorAll('.phone-input, #business_phone').forEach(input => {
    input.addEventListener('input', () => {
      let digits = input.value.replace(/\D/g, '').slice(0, 10);
      if (digits.length >= 7) {
        input.value = `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
      } else if (digits.length >= 4) {
        input.value = `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
      } else if (digits.length > 0) {
        input.value = `(${digits}`;
      } else {
        input.value = '';
      }
    });
  });

  function initSignaturePad(canvasId, key) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = '#0c1a2e';
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    let drawing = false;
    let hasStroke = false;

    function pos(e) {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const touch = e.touches ? e.touches[0] : e;
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY,
      };
    }

    function start(e) {
      e.preventDefault();
      drawing = true;
      const p = pos(e);
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
    }

    function draw(e) {
      if (!drawing) return;
      e.preventDefault();
      const p = pos(e);
      ctx.lineTo(p.x, p.y);
      ctx.stroke();
      hasStroke = true;
    }

    function stop() { drawing = false; }

    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stop);
    canvas.addEventListener('mouseleave', stop);
    canvas.addEventListener('touchstart', start, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stop);

    return {
      clear() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        hasStroke = false;
      },
      isEmpty() { return !hasStroke; },
      toDataURL() { return hasStroke ? canvas.toDataURL('image/png') : ''; },
    };
  }

  signaturePads.owner = initSignaturePad('owner-signature-pad', 'owner');
  signaturePads['co-owner'] = initSignaturePad('co-owner-signature-pad', 'co-owner');

  form.querySelectorAll('.signature-clear').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.dataset.pad;
      signaturePads[key]?.clear();
    });
  });

  form.querySelectorAll('.file-input').forEach(input => {
    input.addEventListener('change', () => {
      const file = input.files?.[0];
      if (file && file.size > MAX_FILE_SIZE) {
        showMessage(`"${file.name}" exceeds the 10 MB limit. Please choose a smaller file.`);
        input.value = '';
      }
    });
  });

  function validateStep(step) {
    const panel = form.querySelector(`.prequal-step-panel[data-step="${step}"]`);
    if (!panel) return true;

    const fields = panel.querySelectorAll('input, select, textarea');
    for (const field of fields) {
      if (field.closest('.hidden')) continue;
      if (field.type === 'file' && !field.required) continue;
      if (!field.checkValidity()) {
        field.reportValidity();
        field.focus();
        return false;
      }
    }

    if (step === 1) {
      const industry = document.getElementById('industry');
      if (industry?.value === 'Other' && !document.getElementById('industry_other')?.value.trim()) {
        showMessage('Please specify your industry.');
        document.getElementById('industry_other')?.focus();
        return false;
      }
      const legal = document.getElementById('legal_entity');
      if (legal?.value === 'Other' && !document.getElementById('legal_entity_other')?.value.trim()) {
        showMessage('Please specify your legal entity type.');
        document.getElementById('legal_entity_other')?.focus();
        return false;
      }
      const contact = form.querySelector('input[name="contact_method"]:checked');
      if (!contact) {
        showMessage('Please select a preferred contact method.');
        return false;
      }
    }

    if (step === 2) {
      const ssn = document.getElementById('owner_ssn');
      const digits = ssn?.value.replace(/\D/g, '') || '';
      if (digits.length !== 9) {
        showMessage('Please enter a valid 9-digit Social Security Number.');
        ssn?.focus();
        return false;
      }
    }

    if (step === 4) {
      for (const input of panel.querySelectorAll('.file-input[required]')) {
        if (!input.files?.length) {
          showMessage('Please upload all required documents.');
          input.focus();
          return false;
        }
        if (input.files[0].size > MAX_FILE_SIZE) {
          showMessage(`"${input.files[0].name}" exceeds the 10 MB limit.`);
          return false;
        }
      }
      for (const input of panel.querySelectorAll('.file-input:not([required])')) {
        const file = input.files?.[0];
        if (file && file.size > MAX_FILE_SIZE) {
          showMessage(`"${file.name}" exceeds the 10 MB limit.`);
          return false;
        }
      }
      const terms = document.getElementById('terms_accepted');
      if (!terms?.checked) {
        showMessage('Please accept the terms and authorization to continue.');
        terms?.focus();
        return false;
      }
      const ownerSig = signaturePads.owner;
      const ownerName = document.getElementById('owner_signature_name')?.value.trim();
      if (ownerSig?.isEmpty() && !ownerName) {
        showMessage('Please provide your signature or type your full legal name.');
        return false;
      }
    }

    return true;
  }

  prevBtn?.addEventListener('click', () => {
    if (currentStep > 1) goToStep(currentStep - 1);
  });

  nextBtn?.addEventListener('click', () => {
    if (!validateStep(currentStep)) return;
    if (currentStep < TOTAL_STEPS) goToStep(currentStep + 1);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopImmediatePropagation();

    if (!validateStep(TOTAL_STEPS)) return;

    const ownerData = signaturePads.owner?.toDataURL() || '';
    const coOwnerData = signaturePads['co-owner']?.toDataURL() || '';
    document.getElementById('owner_signature_data').value = ownerData;
    document.getElementById('co_owner_signature_data').value = coOwnerData;

    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Submitting…';
    clearMessage();

    const formData = new FormData(form);

    try {
      const response = await fetch('process_prequalify.php', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });

      const result = await response.json();

      if (result.success) {
        window.location.href = 'thank-you.html?type=prequalify';
        return;
      }

      showMessage(result.message || 'Something went wrong. Please try again.');
    } catch {
      showMessage('Unable to submit. Please call us at (347) 201-2166 or try again later.');
    }

    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
  }, true);

  goToStep(1);
});
