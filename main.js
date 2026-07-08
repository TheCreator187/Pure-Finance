document.addEventListener('DOMContentLoaded', () => {

  // Mobile navigation
  const menuToggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      const isOpen = mobileNav.classList.toggle('open');
      menuToggle.classList.toggle('active', isOpen);
      menuToggle.setAttribute('aria-expanded', isOpen);
    });

    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Scroll reveal
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  revealElements.forEach(el => revealObserver.observe(el));

  // Counter animation
  const animateCounter = (el) => {
    const target = +el.getAttribute('data-target');
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 2000;
    const steps = duration / 20;
    const increment = target / steps;
    const hasDecimal = target % 1 !== 0;
    let current = 0;

    const update = () => {
      current += increment;
      if (current < target) {
        let val;
        if (target > 999) val = Math.ceil(current).toLocaleString();
        else if (hasDecimal) val = current.toFixed(1);
        else val = Math.ceil(current);
        el.textContent = `${prefix}${val}${suffix}`;
        setTimeout(update, 20);
      } else {
        const val = target > 999 ? target.toLocaleString() : target;
        el.textContent = `${prefix}${val}${suffix}`;
      }
    };
    update();
  };

  const counterObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.counter').forEach(c => counterObserver.observe(c));

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Pre-fill loan type from URL (?type=Small+Business+Loan)
  const params = new URLSearchParams(window.location.search);
  const loanType = params.get('type');
  if (loanType) {
    document.querySelectorAll('[name="loan_type"]').forEach(field => {
      field.value = loanType;
    });
  }

  // Application form submission
  document.querySelectorAll('.application-form:not(.prequal-form)').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const submitBtn = form.querySelector('[type="submit"]');
      const messageEl = form.querySelector('.form-message');
      const originalText = submitBtn.innerHTML;

      if (messageEl) {
        messageEl.className = 'form-message';
        messageEl.textContent = '';
      }

      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Submitting…';

      const formData = new FormData(form);
      if (!formData.get('source_page')) {
        formData.set('source_page', window.location.pathname.split('/').pop() || 'index.html');
      }

      try {
        const response = await fetch('process.php', {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        const result = await response.json();

        if (result.success) {
          window.location.href = 'thank-you.html';
          return;
        }

        if (messageEl) {
          messageEl.className = 'form-message error';
          messageEl.textContent = result.message || 'Something went wrong. Please try again.';
        }
      } catch {
        if (messageEl) {
          messageEl.className = 'form-message error';
          messageEl.textContent = 'Unable to submit. Please call us or try again later.';
        }
      }

      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    });
  });

  // SSN formatting (XXX-XX-XXXX)
  document.querySelectorAll('input[name="ssn"]').forEach(input => {
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

  // Phone formatting
  document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('input', () => {
      let digits = input.value.replace(/\D/g, '').slice(0, 10);
      if (digits.length >= 7) {
        input.value = `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
      } else if (digits.length >= 4) {
        input.value = `(${digits.slice(0, 3)}) ${digits.slice(3)}`;
      } else if (digits.length > 0) {
        input.value = `(${digits}`;
      }
    });
  });

});
