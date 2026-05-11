/* ===== PURE CAPITAL — APP WIZARD JS ===== */

// Total number of steps in the wizard (excluding success step)
const TOTAL_STEPS = 3;

/**
 * Validates the current step before allowing navigation to the next step.
 */
function validateStep(stepNumber) {
  const stepEl = document.getElementById(`step-${stepNumber}`);
  if (!stepEl) return false;

  const inputs = stepEl.querySelectorAll('input[required], select[required], textarea[required]');
  let isValid = true;

  // Clear previous error styles
  inputs.forEach(input => {
    input.style.borderColor = '';
    
    // Check validity
    if (!input.checkValidity()) {
      isValid = false;
      input.style.borderColor = '#ef4444'; // Red border for error
      
      // Add a shake animation to the first invalid input
      if (isValid === false && input === inputs[0]) {
        input.classList.add('error-shake');
        setTimeout(() => input.classList.remove('error-shake'), 400);
      }
    }
  });

  // Special check for radio buttons (Funding amount)
  const radios = stepEl.querySelectorAll('input[type="radio"][required]');
  if (radios.length > 0) {
    const radioName = radios[0].name;
    const isRadioChecked = stepEl.querySelector(`input[name="${radioName}"]:checked`);
    if (!isRadioChecked) {
      isValid = false;
      const radioContainer = radios[0].closest('.amount-options');
      if (radioContainer) {
        radioContainer.style.border = '1px solid #ef4444';
        radioContainer.style.padding = '8px';
        radioContainer.style.borderRadius = 'var(--radius-lg)';
        setTimeout(() => {
          radioContainer.style.border = '';
          radioContainer.style.padding = '';
        }, 2000);
      }
    }
  }

  return isValid;
}

/**
 * Navigates to the next step if validation passes.
 */
function nextStep(nextStepNumber) {
  const currentStepNumber = nextStepNumber - 1;
  
  if (!validateStep(currentStepNumber)) {
    // Optionally alert the user or let the red borders do the talking
    return;
  }

  goToStep(nextStepNumber);
}

/**
 * Navigates to the previous step.
 */
function prevStep(prevStepNumber) {
  goToStep(prevStepNumber);
}

/**
 * Handles DOM updates to show the requested step.
 */
function goToStep(stepNumber) {
  // Hide all steps
  document.querySelectorAll('.wizard-step').forEach(step => {
    step.classList.remove('active');
  });

  // Show the target step
  const targetStep = document.getElementById(`step-${stepNumber}`);
  if (targetStep) {
    targetStep.classList.add('active');
  }

  // Update progress bar & text (if not success step)
  if (stepNumber <= TOTAL_STEPS) {
    const progressPercent = (stepNumber / TOTAL_STEPS) * 100;
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
      progressBar.style.width = `${progressPercent}%`;
    }

    const stepIndicator = document.getElementById('step-indicator');
    if (stepIndicator) {
      stepIndicator.textContent = `Step ${stepNumber} of ${TOTAL_STEPS}`;
    }
    
    // Ensure header is visible
    document.getElementById('wizard-header').style.display = 'block';
  } else {
    // Hide progress header on success step
    document.getElementById('wizard-header').style.display = 'none';
  }
}

/**
 * Handles the final form submission.
 */
function handleWizardSubmit(e) {
  e.preventDefault();
  
  // Validate final step
  if (!validateStep(TOTAL_STEPS)) return;

  const form = document.getElementById('loan-application');
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  // Show processing state on button
  const submitBtn = document.getElementById('submit-btn');
  const originalText = submitBtn.innerHTML;
  submitBtn.innerHTML = 'Processing...';
  submitBtn.disabled = true;

  // SIMULATED API CALL OR MAILTO LOGIC
  setTimeout(() => {
    console.log('Form Data Submitted:', data);
    
    // To implement the email requirement:
    // Option A: API integration (like Formspree, EmailJS, Zapier)
    // fetch('https://api.yourmailer.com/submit', {
    //   method: 'POST',
    //   body: JSON.stringify(data),
    //   headers: { 'Content-Type': 'application/json' }
    // });
    
    // Option B: Mailto fallback
    // const subject = encodeURIComponent(`New Loan Application - ${data.business_name}`);
    // const body = encodeURIComponent(
    //   `Name: ${data.first_name} ${data.last_name}\n` +
    //   `Business: ${data.business_name}\n` +
    //   `Email: ${data.email}\n` +
    //   `Phone: ${data.phone}\n` +
    //   `Amount Needed: ${data.funding_amount}\n` +
    //   `Purpose: ${data.funding_purpose}\n` +
    //   `Time in Biz: ${data.time_in_business}\n` +
    //   `Revenue: ${data.annual_revenue}`
    // );
    // window.location.href = `mailto:${data.target_email}?subject=${subject}&body=${body}`;

    // Move to success step
    goToStep(TOTAL_STEPS + 1);
  }, 1200);
}

// Add a quick shake animation class via JS if not in CSS
document.head.insertAdjacentHTML('beforeend', `
  <style>
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      25% { transform: translateX(-4px); }
      75% { transform: translateX(4px); }
    }
    .error-shake {
      animation: shake 0.4s ease-in-out;
    }
  </style>
`);

// ===== SCROLL REVEAL ANIMATIONS =====
document.addEventListener('DOMContentLoaded', () => {
  const revealElements = document.querySelectorAll('.reveal');

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  revealElements.forEach(el => {
    revealObserver.observe(el);
  });
});
