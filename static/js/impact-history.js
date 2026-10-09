/* Native details remain usable without JavaScript. Enhancement adds hover/focus,
   one-panel-at-a-time behavior and viewport-aware desktop positioning. */
(() => {
  const figure = document.querySelector('.fm-history');
  if (!figure) return;
  const items = [...figure.querySelectorAll('.history-item')];
  const desktop = matchMedia('(min-width: 65.001rem)');
  let active = null, pinned = false, timer = null, suppressFocus = false;
  function position() {
    if (!active || !desktop.matches) return;
    const panel = active.querySelector('.history-panel');
    const anchor = active.querySelector('summary').getBoundingClientRect();
    const pad = 12, gap = 8, width = Math.min(400, innerWidth - pad * 2);
    panel.style.width = `${width}px`;
    panel.style.maxHeight = `${innerHeight - pad * 2}px`;
    const height = panel.getBoundingClientRect().height;
    let left = anchor.right + gap;
    if (left + width > innerWidth - pad) left = anchor.left - width - gap;
    left = Math.max(pad, Math.min(left, innerWidth - width - pad));
    let top = Math.max(pad, Math.min(anchor.top, innerHeight - height - pad));
    panel.style.left = `${left}px`;
    panel.style.top = `${top}px`;
  }
  function close(restore = false) {
    clearTimeout(timer);
    if (!active) return;
    const old = active;
    active = null; pinned = false;
    old.open = false;
    old.querySelector('summary').setAttribute('aria-expanded', 'false');
    if (restore) {
      suppressFocus = true;
      old.querySelector('summary').focus({preventScroll:true});
      suppressFocus = false;
    }
  }
  function open(item, pin = false) {
    clearTimeout(timer);
    if (active !== item) { close(); active = item; }
    pinned = pinned || pin;
    item.open = true;
    item.querySelector('summary').setAttribute('aria-expanded', 'true');
    position();
  }
  function leave(item) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (active === item && !pinned && !item.contains(document.activeElement)) close();
    }, 350);
  }
  items.forEach(item => {
    const trigger = item.querySelector('summary');
    const panel = item.querySelector('.history-panel');
    trigger.setAttribute('aria-expanded', 'false');
    item.addEventListener('pointerenter', e => {
      if (e.pointerType === 'mouse' && desktop.matches) open(item);
    });
    item.addEventListener('pointerleave', () => leave(item));
    panel.addEventListener('pointerenter', () => clearTimeout(timer));
    panel.addEventListener('pointerleave', () => leave(item));
    trigger.addEventListener('focus', () => { if (!suppressFocus && desktop.matches) open(item); });
    trigger.addEventListener('click', event => {
      event.preventDefault();
      if (active === item && pinned) close(); else open(item, true);
    });
    item.addEventListener('focusout', () => {
      setTimeout(() => {
        if (desktop.matches && active === item && !item.contains(document.activeElement) && !item.matches(':hover')) close();
      }, 0);
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && active) { event.preventDefault(); close(true); }
  });
  document.addEventListener('pointerdown', event => { if (desktop.matches && active && !active.contains(event.target)) close(); });
  document.addEventListener('click', event => { if (!desktop.matches && active && !active.contains(event.target)) close(); });
  window.addEventListener('resize', position);
  window.addEventListener('scroll', position, {passive:true});
  desktop.addEventListener('change', () => close());
  figure.classList.add('history-enhanced');
})();
