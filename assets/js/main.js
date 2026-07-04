// 데이터 인사이트랩 — 헤더 상태·모바일 메뉴·리빌 애니메이션 (바닐라 JS)
(function () {
  'use strict';

  document.body.classList.add('js');

  var header = document.querySelector('.site-header');
  var hero = document.querySelector('.hero');
  var isHome = document.body.classList.contains('page-home');

  // 헤더: 홈은 hero 지나면 솔리드, 서브페이지는 항상 솔리드
  function updateHeader() {
    if (!header) return;
    var solid = !isHome ||
      document.body.classList.contains('menu-open') ||
      window.pageYOffset > (hero ? hero.offsetHeight - 90 : 420);
    header.classList.toggle('is-solid', solid);
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      updateHeader();
      ticking = false;
    });
  }, { passive: true });
  window.addEventListener('resize', updateHeader);
  updateHeader();

  // 모바일 메뉴
  var burger = document.querySelector('.hamburger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      updateHeader();
    });
  }

  // 리빌 애니메이션 (reduced-motion 시 전체 표시)
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  els.forEach(function (el) { obs.observe(el); });
})();

// 문의 폼: ?service= 자동 선택 + 제목 갱신 + fetch 제출 (실패 시 일반 POST 폴백 유지)
(function () {
  'use strict';

  var form = document.querySelector('.contact-form');
  if (!form) return;

  var select = form.querySelector('#f-service');
  var subject = form.querySelector('input[name="subject"]');

  function syncSubject() {
    if (select && subject) subject.value = '[사이트 문의] ' + select.value;
  }

  // /contact/?service=01 → 해당 서비스 자동 선택 (실패해도 무해)
  try {
    var num = new URLSearchParams(location.search).get('service');
    if (num && select) {
      var opt = select.querySelector('option[data-num="' + num + '"]');
      if (opt) select.value = opt.value;
    }
  } catch (e) { /* 미지원 브라우저는 기본값 유지 */ }
  syncSubject();
  if (select) select.addEventListener('change', syncSubject);

  if (!window.fetch || !window.FormData) return;

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (!form.reportValidity()) return;
    var body = form.querySelector('.form-body');
    var success = form.querySelector('.form-success');
    var error = form.querySelector('.form-error');
    var btn = form.querySelector('button[type="submit"]');
    error.hidden = true;
    btn.disabled = true;
    var data = new FormData(form);
    data.delete('redirect'); // fetch 경로에서는 인라인 메시지 사용
    fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.success) {
          body.hidden = true;
          success.hidden = false;
          success.setAttribute('tabindex', '-1');
          success.focus();
        } else {
          error.hidden = false;
          btn.disabled = false;
        }
      })
      .catch(function () {
        error.hidden = false;
        btn.disabled = false;
      });
  });
})();
