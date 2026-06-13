/* ============================================
   PRINCESS TRACKER — main.js
   Animations, Checklist, Dashboard, Mood
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── CURRENT DATE ──────────────────────────
  const dateEl = document.getElementById('current-date');
  if (dateEl) {
    const opts = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateEl.textContent = new Date().toLocaleDateString('en-ZA', opts);
  }

  // ── DAY-OF-WEEK AUTO BADGE ─────────────────
  const day = new Date().getDay(); // 0=Sun, 5=Fri
  const dayBadge = document.getElementById('day-badge');
  if (dayBadge) {
    const labels = { 5: '⛪ Friday — Church Day', 0: '⛪ Sunday — Church & Planning' };
    if (labels[day]) { dayBadge.textContent = labels[day]; dayBadge.style.display = 'inline-flex'; }
  }

  // ── CHECKLIST PROGRESS BAR ─────────────────
  const checkboxes = document.querySelectorAll('.check-item input[type="checkbox"]');
  const progressFill = document.querySelector('.progress-bar-fill');
  const progressLabel = document.getElementById('progress-label');

  function updateProgress() {
    if (!checkboxes.length || !progressFill) return;
    const checked = [...checkboxes].filter(c => c.checked).length;
    const pct = Math.round((checked / checkboxes.length) * 100);
    progressFill.style.width = pct + '%';
    if (progressLabel) progressLabel.textContent = `${checked} / ${checkboxes.length} completed (${pct}%)`;
    // celebrate at 100%
    if (pct === 100) showConfetti();
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', updateProgress);
  });
  updateProgress();

  // ── MOOD SELECTOR ──────────────────────────
  const moodBtns = document.querySelectorAll('.mood-btn');
  const moodInput = document.getElementById('mood-value');
  moodBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      moodBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      if (moodInput) moodInput.value = btn.dataset.mood;
    });
  });

  // ── ANIMATED COUNTER (dashboard) ──────────
  function animateCounter(el, target, suffix = '') {
    let start = 0;
    const duration = 1400;
    const step = (timestamp) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(ease * target) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  // ── RING CHART ANIMATION ───────────────────
  function animateRing(svgEl, percentage) {
    const fg = svgEl.querySelector('.ring-fg');
    if (!fg) return;
    const circumference = 220;
    const offset = circumference - (circumference * percentage / 100);
    setTimeout(() => { fg.style.strokeDashoffset = offset; }, 200);
  }

  // ── INTERSECTION OBSERVER for Dashboard ───
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      // KPI counter
      const counterEl = entry.target.querySelector('[data-count]');
      if (counterEl) {
        const val    = parseFloat(counterEl.dataset.count);
        const suffix = counterEl.dataset.suffix || '';
        animateCounter(counterEl, val, suffix);
        counterEl.removeAttribute('data-count');
      }

      // Ring chart
      const ring = entry.target.querySelector('.ring-fg[data-pct]');
      if (ring) {
        animateRing(entry.target.querySelector('.ring-chart'), parseFloat(ring.dataset.pct));
        ring.removeAttribute('data-pct');
      }

      // Bar chart
      const bars = entry.target.querySelectorAll('.bar-fill[data-h]');
      bars.forEach((bar, i) => {
        setTimeout(() => {
          bar.style.height = bar.dataset.h + '%';
          bar.removeAttribute('data-h');
        }, i * 100);
      });

      observer.unobserve(entry.target);
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.kpi-card, .chart-card').forEach(el => observer.observe(el));

  // ── INSIGHTS SLIDER ────────────────────────
  const slides = document.querySelectorAll('.insight-slide');
  const dots   = document.querySelectorAll('.slider-dots span');
  let current  = 0;
  let sliderTimer;

  function goSlide(n) {
    slides[current]?.classList.remove('active');
    dots[current]?.classList.remove('active');
    current = (n + slides.length) % slides.length;
    slides[current]?.classList.add('active');
    dots[current]?.classList.add('active');
  }

  if (slides.length) {
    goSlide(0);
    sliderTimer = setInterval(() => goSlide(current + 1), 4500);
    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        clearInterval(sliderTimer);
        goSlide(i);
        sliderTimer = setInterval(() => goSlide(current + 1), 4500);
      });
    });
  }

  // ── BAR CHART (trend) already handled by observer ─

  // ── CONFETTI on 100% ─────────────────────
  function showConfetti() {
    const colors = ['#f78fb3', '#9b59b6', '#74b9ff', '#ffd6e8', '#c77ddb'];
    for (let i = 0; i < 60; i++) {
      const dot = document.createElement('div');
      dot.style.cssText = `
        position:fixed;
        width:8px;height:8px;border-radius:50%;
        background:${colors[Math.floor(Math.random()*colors.length)]};
        left:${Math.random()*100}vw;
        top:-10px;
        z-index:9999;
        animation:confettiFall ${1.5+Math.random()*2}s linear forwards;
        opacity:0.85;
      `;
      document.body.appendChild(dot);
      setTimeout(() => dot.remove(), 3500);
    }
  }
  const style = document.createElement('style');
  style.textContent = `
    @keyframes confettiFall {
      to { transform: translateY(110vh) rotate(${Math.random()*360}deg); opacity:0; }
    }`;
  document.head.appendChild(style);

  // ── FLASH MESSAGES AUTO-HIDE ──────────────
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity 0.5s'; setTimeout(() => el.remove(), 500); }, 4000);
  });

  // ── FORM SUBMISSION LOADING STATE ─────────
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('.btn-submit');
      if (btn) { btn.textContent = 'Saving…'; btn.style.opacity = '0.7'; }
    });
  });

});
