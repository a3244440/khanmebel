/* Khan Mebel — анимации по прокрутке (GSAP + ScrollTrigger). Без библиотеки страница работает как обычно. */
(function () {
  if (!window.gsap || !window.ScrollTrigger) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  function has(sel) { return document.querySelector(sel); }
  var mm = gsap.matchMedia();

  // Веер фото на первом экране
  if (has('.fan')) {
    var cards = gsap.utils.toArray('.fan .card');
    gsap.from(cards, { '--x': '0%', '--y': '40%', '--r0': '0deg', duration: 1.3, ease: 'expo.out', stagger: .07, delay: .15 });
    gsap.to(cards, { '--s': 1.45, ease: 'none', scrollTrigger: { trigger: '.fan', start: 'top 70%', end: 'bottom top', scrub: true } });
  }

  // Заголовки разделов выезжают снизу
  gsap.utils.toArray('.sec-title h2, .calc-intro h2').forEach(function (h) {
    gsap.from(h, { y: 70, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: h, start: 'top 88%' } });
  });

  mm.add('(min-width: 821px)', function () {
    // Чёрная сцена «Ханское качество»: закрепление, видео растёт, карточки вылетают
    if (has('.stage-pin')) {
      var v = has('.stage-video');
      gsap.set(v, { xPercent: -50, yPercent: -50, x: 0, y: 0 });
      gsap.timeline({ scrollTrigger: { trigger: '.stage-pin', start: 'top top', end: '+=130%', pin: true, scrub: .6 } })
        .from('.giant', { scale: 1.35, ease: 'none' }, 0)
        .from(v, { scale: .35, rotation: -8, ease: 'none' }, 0)
        .from('.stat', { y: 520, rotation: function (i) { return [-26, 18, -18, 26][i]; }, stagger: .06, ease: 'power2.out' }, .1);
    }
    // Цветные карточки вокруг заголовка услуг
    if (has('.float-sec')) {
      gsap.utils.toArray('.fcard').forEach(function (c, i) {
        gsap.from(c, { y: i % 2 ? 260 : -200, rotation: '+=' + (i % 2 ? 24 : -24), ease: 'none',
          scrollTrigger: { trigger: '.float-sec', start: 'top bottom', end: 'bottom top', scrub: true } });
      });
    }
  });

  // Карточки цен и принципов
  gsap.utils.toArray('.plan, .pillar').forEach(function (c, i) {
    gsap.from(c, { y: 60, rotation: i % 2 ? 2 : -2, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: c, start: 'top 92%' } });
  });

  addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
