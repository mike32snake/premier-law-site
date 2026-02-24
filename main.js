(function() {
  'use strict';

  // ---- Header scroll behavior ----
  // On sub-pages (no .hero element), force scrolled state immediately
  var header = document.getElementById('header');
  var heroExists = document.querySelector('.hero');

  function handleScroll() {
    if (!heroExists) {
      header.classList.add('scrolled');
      return;
    }
    if (window.pageYOffset > 60) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  // ---- Active nav link highlighting ----
  var currentPage = window.location.pathname.split('/').pop() || 'index.html';
  if (currentPage === '' || currentPage === '/') currentPage = 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-menu a[href]').forEach(function(link) {
    var href = link.getAttribute('href');
    if (!href) return;
    var linkPage = href.split('#')[0].split('?')[0];
    if (linkPage === currentPage) {
      link.classList.add('active');
    }
  });

  // ---- Mobile menu ----
  var hamburger = document.getElementById('hamburger');
  var mobileMenu = document.getElementById('mobileMenu');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function() {
      var isOpen = mobileMenu.classList.contains('open');
      mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', String(!isOpen));
      mobileMenu.setAttribute('aria-hidden', String(isOpen));
      document.body.style.overflow = isOpen ? '' : 'hidden';
    });

    mobileMenu.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('active');
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      });
    });
  }

  // ---- Intersection Observer for reveal animations ----
  var revealElements = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
    revealElements.forEach(function(el) { observer.observe(el); });
  } else {
    revealElements.forEach(function(el) { el.classList.add('revealed'); });
  }

  // ---- FAQ Accordion ----
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = this.closest('.faq-item');
      var answer = item.querySelector('.faq-answer');
      var wasOpen = item.classList.contains('open');

      // Close all others in same FAQ list
      var parent = item.parentElement;
      parent.querySelectorAll('.faq-item.open').forEach(function(openItem) {
        openItem.classList.remove('open');
        openItem.querySelector('.faq-answer').style.maxHeight = null;
      });

      if (!wasOpen) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  // ---- Form validation ----
  var contactForm = document.getElementById('contactForm');
  var formSuccess = document.getElementById('formSuccess');

  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      var isValid = true;
      contactForm.querySelectorAll('.form-group').forEach(function(g) {
        g.classList.remove('has-error');
      });

      var nameField = document.getElementById('name');
      if (nameField && !nameField.value.trim()) {
        nameField.closest('.form-group').classList.add('has-error');
        isValid = false;
      }

      var emailField = document.getElementById('email');
      if (emailField && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value.trim())) {
        emailField.closest('.form-group').classList.add('has-error');
        isValid = false;
      }

      var messageField = document.getElementById('message');
      if (messageField && !messageField.value.trim()) {
        messageField.closest('.form-group').classList.add('has-error');
        isValid = false;
      }

      if (isValid && formSuccess) {
        contactForm.style.display = 'none';
        formSuccess.style.display = 'block';
      } else {
        var firstError = contactForm.querySelector('.has-error input, .has-error textarea');
        if (firstError) firstError.focus();
      }
    });

    contactForm.querySelectorAll('input, textarea, select').forEach(function(field) {
      field.addEventListener('input', function() {
        this.closest('.form-group').classList.remove('has-error');
      });
    });
  }

  // ---- Smooth scroll for same-page anchor links only ----
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var headerHeight = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-height'));
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.pageYOffset - headerHeight,
          behavior: 'smooth'
        });
      }
    });
  });

  // ---- Parallax on hero orbs (homepage only) ----
  var orb1 = document.querySelector('.hero-orb--1');
  var orb2 = document.querySelector('.hero-orb--2');
  if (orb1 && orb2 && window.matchMedia('(min-width: 768px)').matches) {
    window.addEventListener('scroll', function() {
      var scrollY = window.pageYOffset;
      if (scrollY < window.innerHeight) {
        var f = scrollY * 0.15;
        orb1.style.transform = 'translate(' + (f * 0.3) + 'px, ' + (f * 0.5) + 'px)';
        orb2.style.transform = 'translate(' + (-f * 0.2) + 'px, ' + (-f * 0.4) + 'px)';
      }
    }, { passive: true });
  }

})();
