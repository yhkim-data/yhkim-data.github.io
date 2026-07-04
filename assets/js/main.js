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
