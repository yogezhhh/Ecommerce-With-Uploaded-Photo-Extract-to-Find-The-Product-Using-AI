window.addEventListener('load', () => {
  if (typeof gsap === 'undefined') return;
  gsap.registerPlugin(ScrollTrigger);

  gsap.utils.toArray('section').forEach((section) => {
    gsap.from(section.querySelectorAll('h2, p, .glass'), {
      y: 40, opacity: 0, duration: 1, stagger: 0.06, ease: 'power3.out',
      scrollTrigger: { trigger: section, start: 'top 85%' }
    });
  });

  document.querySelectorAll('.tilt-card').forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const r = card.getBoundingClientRect();
      const rx = ((e.clientY - r.top) / r.height - 0.5) * -12;
      const ry = ((e.clientX - r.left) / r.width - 0.5) * 12;
      card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateZ(10px)`;
    });
    card.addEventListener('mouseleave', () => card.style.transform = '');
  });
});