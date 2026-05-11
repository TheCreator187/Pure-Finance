document.addEventListener('DOMContentLoaded', () => {

  // Reveal Animations on Scroll
  const revealElements = document.querySelectorAll('.reveal');
  
  const revealCallback = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  };
  
  const revealOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };
  
  const revealObserver = new IntersectionObserver(revealCallback, revealOptions);
  
  revealElements.forEach(el => {
    revealObserver.observe(el);
  });

  // Counter Animation
  const counters = document.querySelectorAll('.counter');
  
  const animateCounter = (el) => {
    const target = +el.getAttribute('data-target');
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 2000; // ms
    const stepTime = 20; // ms
    const steps = duration / stepTime;
    const increment = target / steps;
    
    const hasDecimal = target % 1 !== 0;
    
    let current = 0;
    
    const updateCounter = () => {
      current += increment;
      if (current < target) {
        let displayValue;
        if (target > 999) {
          displayValue = Math.ceil(current).toLocaleString();
        } else if (hasDecimal) {
          displayValue = current.toFixed(1);
        } else {
          displayValue = Math.ceil(current);
        }
          
        el.innerText = `${prefix}${displayValue}${suffix}`;
        setTimeout(updateCounter, stepTime);
      } else {
        const displayValue = target > 999 
          ? target.toLocaleString() 
          : target;
        el.innerText = `${prefix}${displayValue}${suffix}`;
      }
    };
    
    updateCounter();
  };

  const counterCallback = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  };

  const counterObserver = new IntersectionObserver(counterCallback, { threshold: 0.5 });
  
  counters.forEach(counter => {
    counterObserver.observe(counter);
  });

  // Smooth Scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });

  // Handle hero form submit
  const loanForm = document.getElementById('loan-application');
  if (loanForm) {
    loanForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const amount = document.getElementById('funding-amount').value;
      if (amount) {
        // Since we don't have a multi-step wizard anymore, 
        // we simulate redirecting to the full application portal.
        alert(`Great! Starting your application for ${amount}. You will now be redirected to our secure portal.`);
      }
    });
  }

});
