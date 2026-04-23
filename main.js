/* ===== PURE CAPITAL — MAIN.JS ===== */

// ===== NAVBAR SCROLL EFFECT =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
}, { passive: true });

// ===== MOBILE HAMBURGER MENU =====
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('mobile-open');
  hamburger.classList.toggle('active', isOpen);
  hamburger.setAttribute('aria-expanded', isOpen);
});

// Close menu when a nav link is clicked
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('mobile-open');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', false);
  });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!navbar.contains(e.target) && navLinks.classList.contains('mobile-open')) {
    navLinks.classList.remove('mobile-open');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', false);
  }
});

// ===== FAQ ACCORDION =====
function toggleFaq(id) {
  const item = document.getElementById(id);
  if (!item) return;
  
  const isOpen = item.classList.contains('open');
  
  // Close all open items
  document.querySelectorAll('.faq-item.open').forEach(el => {
    el.classList.remove('open');
  });
  
  // Open clicked item if it was closed
  if (!isOpen) {
    item.classList.add('open');
  }
}

// ===== APPLY FORM HANDLER =====
function handleApply(e) {
  e.preventDefault();
  const form = document.getElementById('apply-form');
  const success = document.getElementById('apply-success');
  
  // Simple fade out / fade in
  form.style.opacity = '0';
  form.style.transform = 'translateY(8px)';
  form.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
  
  setTimeout(() => {
    form.style.display = 'none';
    success.style.display = 'block';
    success.style.opacity = '0';
    success.style.transform = 'translateY(8px)';
    success.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        success.style.opacity = '1';
        success.style.transform = 'none';
      });
    });
  }, 300);
}

// ===== SCROLL REVEAL ANIMATION =====
const revealElements = document.querySelectorAll(
  '.card, .step, .stat-card, .req-item, .testimonial-card, .faq-item, .hero-stats-bar'
);

revealElements.forEach((el, i) => {
  el.classList.add('reveal');
  // Stagger sibling elements
  const siblings = el.parentElement ? el.parentElement.children : [];
  const idx = Array.from(siblings).indexOf(el);
  if (idx > 0 && idx <= 4) {
    el.classList.add(`reveal-delay-${idx}`);
  }
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

revealElements.forEach(el => revealObserver.observe(el));

// ===== SMOOTH NAV LINK HIGHLIGHTING =====
const sections = document.querySelectorAll('section[id]');
const navLinkElems = document.querySelectorAll('.nav-links a');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navLinkElems.forEach(link => {
        link.style.color = '';
        if (link.getAttribute('href') === `#${id}`) {
          link.style.color = 'var(--text-primary)';
        }
      });
    }
  });
}, { threshold: 0.4 });

sections.forEach(s => sectionObserver.observe(s));

// ===== ANIMATED STAT COUNTER =====
function animateCounter(el, target, duration = 1800) {
  const isDecimal = target.toString().includes('.');
  const start = 0;
  const startTime = performance.now();
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease out cubic
    const value = start + (target - start) * eased;
    
    el.textContent = isDecimal
      ? value.toFixed(1)
      : Math.round(value).toLocaleString();
    
    if (progress < 1) requestAnimationFrame(update);
  }
  
  requestAnimationFrame(update);
}

// Observe stat numbers for counter animation
const statNumbers = document.querySelectorAll('.stat-num');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const text = el.textContent;
      
      // Extract numeric value
      const match = text.match(/[\d.]+/);
      if (match) {
        const num = parseFloat(match[0]);
        const prefix = text.split(match[0])[0];
        const suffix = text.slice(text.indexOf(match[0]) + match[0].length);
        
        animateCounter({ 
          set textContent(v) { el.textContent = prefix + v + suffix; }
        }, num);
      }
      
      counterObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

statNumbers.forEach(el => counterObserver.observe(el));

// ===== CONSOLE BRANDING =====
console.log('%c Pure Capital ', 'background: #1849D6; color: white; padding: 6px 14px; border-radius: 6px; font-size: 14px; font-weight: bold;');
console.log('%c Finance Solutions Built for Growth ', 'color: #4A5568; font-size: 12px;');
