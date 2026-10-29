/* Khan Mebel: общие скрипты всех страниц: шапка, ползунки, отзывы, заявка, галерея, видео. */
(function () {
  var WA = '77001116291';
  function $(id) { return document.getElementById(id); }
  function all(sel) { return [].slice.call(document.querySelectorAll(sel)); }

  // Шапка: фон после прокрутки и белый текст над тёмными блоками
  var bar = $('top-bar');
  if (bar) {
    var darks = all('.dark');
    var onScroll = function () {
      bar.classList.toggle('scrolled', scrollY > 10);
      var y = bar.offsetHeight / 2;
      bar.classList.toggle('on-dark', darks.some(function (d) {
        var r = d.getBoundingClientRect(); return r.top <= y && r.bottom > y;
      }));
    };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Заливка ползунков калькулятора
  function fill(r) { r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%'); }
  all('.qc input[type=range]').forEach(function (r) { fill(r); r.addEventListener('input', function () { fill(r); }); });

  // Карусель отзывов
  var track = $('rev-track');
  if (track) {
    all('[data-rev]').forEach(function (b) {
      b.addEventListener('click', function () {
        var c = track.querySelector('.rev');
        track.scrollBy({ left: (c ? c.getBoundingClientRect().width + 16 : 400) * (+b.dataset.rev), behavior: 'smooth' });
      });
    });
  }

  // Заявка на замер → WhatsApp
  var form = $('cta_form');
  if (form) {
    var nm = $('cta_name'), ph = $('cta_phone'), wh = $('cta_what'), go = $('cta_send');
    var upd = function () {
      go.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(
        'Здравствуйте! Меня зовут ' + (nm.value || '…') + '. Интересует: ' + wh.value +
        '. Телефон: ' + (ph.value || 'не указан') + '. Хочу записаться на замер.');
    };
    [nm, ph, wh].forEach(function (el) { el.addEventListener('input', upd); });
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    upd();
  }

  // Галерея проектов: фильтр и просмотр на весь экран
  var g = $('gallery');
  if (g) {
    var shots = [].slice.call(g.querySelectorAll('.shot'));
    all('.filters button').forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.dataset.f;
        all('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        shots.forEach(function (s) { s.hidden = !(f === 'all' || s.dataset.cat === f); });
      });
    });
    var lb = null, cur = 0;
    var vis = function () { return shots.filter(function (s) { return !s.hidden; }); };
    var show = function (i) {
      var v = vis(); cur = (i + v.length) % v.length; var s = v[cur];
      lb.querySelector('img').src = s.dataset.full; lb.querySelector('img').alt = s.dataset.cap;
      lb.querySelector('p').textContent = s.dataset.cap;
      lb.querySelector('.lb-count').textContent = (cur + 1) + ' / ' + v.length;
    };
    var close = function () { lb.hidden = true; document.body.style.overflow = ''; var v = vis()[cur]; if (v) v.focus(); };
    var open = function (s) {
      if (!lb) {
        lb = document.createElement('div'); lb.className = 'lb';
        lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Фото проекта');
        lb.innerHTML = '<div class="lb-stage"><img alt=""></div><div class="lb-bar"><p></p><span class="lb-count"></span>' +
          '<button class="arrow" type="button" data-d="-1" aria-label="Предыдущее фото">←</button>' +
          '<button class="arrow" type="button" data-d="1" aria-label="Следующее фото">→</button>' +
          '<button class="arrow" type="button" data-x aria-label="Закрыть">✕</button></div>';
        lb.addEventListener('click', function (e) {
          var t = e.target.closest('button');
          if (t && t.dataset.d) show(cur + (+t.dataset.d));
          else if ((t && t.hasAttribute('data-x')) || e.target === lb || e.target.classList.contains('lb-stage')) close();
        });
        document.body.appendChild(lb);
      }
      lb.hidden = false; show(vis().indexOf(s)); document.body.style.overflow = 'hidden'; lb.querySelector('[data-x]').focus();
    };
    shots.forEach(function (s) { s.addEventListener('click', function () { open(s); }); });
    document.addEventListener('keydown', function (e) {
      if (!lb || lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(cur + 1);
      if (e.key === 'ArrowLeft') show(cur - 1);
    });
  }

  // Видео: играют без звука, когда видны; кнопка «Со звуком»
  var vids = all('.reel video');
  if (vids.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting && e.intersectionRatio > .45) { if (v.preload === 'none') v.preload = 'auto'; var p = v.play(); if (p) p.catch(function () {}); }
        else if (!v.dataset.sound) v.pause();
      });
    }, { threshold: [0, .5] });
    vids.forEach(function (v) { io.observe(v); });
  }
  all('.reel-sound').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.parentElement.querySelector('video');
      vids.forEach(function (o) { if (o !== v) { o.muted = true; delete o.dataset.sound; } });
      v.dataset.sound = '1'; v.muted = false; v.currentTime = 0; v.controls = true;
      var p = v.play(); if (p) p.catch(function () {}); b.hidden = true;
    });
  });

  // Яндекс Метрика: цели «whatsapp» (клик по любой ссылке на WhatsApp) и «phone» (клик по телефону)
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || typeof window.ym !== 'function') return;
    var h = a.getAttribute('href');
    if (/wa\.me|whatsapp/i.test(h)) window.ym(113868698, 'reachGoal', 'whatsapp');
    else if (/^tel:/i.test(h)) window.ym(113868698, 'reachGoal', 'phone');
  });
})();
