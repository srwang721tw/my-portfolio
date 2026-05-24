'use strict';

// ---------------------------------------------------------------------------
// Elements
// ---------------------------------------------------------------------------
const hamburger      = document.getElementById('hamburger');
const sidebar        = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const modalBackdrop  = document.getElementById('modalBackdrop');
const modalClose     = document.getElementById('modalClose');
const modalBody      = document.getElementById('modalBody');
const navLinks       = document.querySelectorAll('.nav-link');
const sections       = document.querySelectorAll('.section');
const projectCards   = document.querySelectorAll('.project-card');

// ---------------------------------------------------------------------------
// Language
// ---------------------------------------------------------------------------
function setLang(lang) {
  const html = document.documentElement;
  html.setAttribute('lang', lang);
  html.className = 'lang-' + lang;
  localStorage.setItem('lang', lang);
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
}

function currentLang() {
  return localStorage.getItem('lang') || 'zh';
}

// Init language
setLang(currentLang());

// Wire all lang toggle buttons (sidebar + mobile header)
document.querySelectorAll('.lang-btn').forEach(btn => {
  btn.addEventListener('click', () => setLang(btn.dataset.lang));
});

// ---------------------------------------------------------------------------
// Section navigation
// ---------------------------------------------------------------------------
function showSection(id) {
  sections.forEach(s => s.classList.remove('active'));
  navLinks.forEach(l => l.classList.remove('active'));
  const section = document.getElementById(id);
  if (section) section.classList.add('active');
  const link = document.querySelector(`.nav-link[data-section="${id}"]`);
  if (link) link.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

navLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    showSection(link.dataset.section);
    closeSidebar();
  });
});

// Avatar → back to About
document.getElementById('avatarBtn').addEventListener('click', () => showSection('about'));
const mobileAvatar = document.getElementById('mobileAvatarBtn');
if (mobileAvatar) mobileAvatar.addEventListener('click', () => { showSection('about'); closeSidebar(); });

// ---------------------------------------------------------------------------
// Mobile sidebar
// ---------------------------------------------------------------------------
function openSidebar() {
  sidebar.classList.add('open');
  sidebarOverlay.classList.add('visible');
  hamburger.classList.add('open');
  hamburger.setAttribute('aria-expanded', 'true');
  hamburger.setAttribute('aria-label', '關閉選單');
}
function closeSidebar() {
  sidebar.classList.remove('open');
  sidebarOverlay.classList.remove('visible');
  hamburger.classList.remove('open');
  hamburger.setAttribute('aria-expanded', 'false');
  hamburger.setAttribute('aria-label', '開啟選單');
}
hamburger.addEventListener('click', () =>
  sidebar.classList.contains('open') ? closeSidebar() : openSidebar()
);
sidebarOverlay.addEventListener('click', closeSidebar);

// ---------------------------------------------------------------------------
// Modal
// ---------------------------------------------------------------------------
async function openProject(card) {
  const id = card.dataset.id;
  let project;
  try {
    const res = await fetch(`/api/projects/${encodeURIComponent(id)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    project = await res.json();
  } catch (err) {
    console.error('Failed to load project:', err);
    return;
  }
  renderModal(project);
  modalBackdrop.classList.add('open');
  modalBackdrop.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  modalBody.scrollTop = 0;
  modalClose.focus();
}

function renderModal(p) {
  const zh = currentLang() === 'zh';
  while (modalBody.firstChild) modalBody.removeChild(modalBody.firstChild);

  // Status
  const statusMap = {
    completed:    [zh ? '完成'   : 'Completed',  'status-completed'],
    'in-progress':[zh ? '進行中' : 'In Progress', 'status-in-progress'],
    planned:      [zh ? '計畫中' : 'Planned',     'status-planned'],
  };
  const [statusText, statusClass] = statusMap[p.status] ?? ['', ''];
  const mStatus = el('div', 'm-status');
  const badge   = el('span', `status-badge ${statusClass}`);
  badge.textContent = statusText;
  mStatus.appendChild(badge);
  modalBody.appendChild(mStatus);

  // Title
  const title = el('h2', 'm-title');
  title.id = 'modalTitle';
  title.textContent = zh ? p.title : (p.title_en || p.title);
  modalBody.appendChild(title);

  // Subtitle
  const subtitle = el('p', 'm-subtitle');
  subtitle.textContent = zh ? p.subtitle : (p.subtitle_en || p.subtitle);
  modalBody.appendChild(subtitle);

  // Tags
  const tags = el('div', 'm-tags');
  (p.tags ?? []).forEach(t => {
    const span = el('span', 'tag tag-purple');
    span.textContent = t;
    tags.appendChild(span);
  });
  modalBody.appendChild(tags);

  // Description
  const descLabel = el('p', 'm-label');
  descLabel.textContent = zh ? '專案介紹' : 'Project Overview';
  modalBody.appendChild(descLabel);

  const desc = el('p', 'm-desc');
  desc.textContent = zh ? p.details : (p.details_en || p.details);
  modalBody.appendChild(desc);

  // Highlights
  const hlList = zh ? p.highlights : (p.highlights_en || p.highlights);
  if (hlList?.length) {
    const section = el('div', 'm-highlights');
    const hlLabel = el('p', 'm-label');
    hlLabel.textContent = zh ? '技術亮點' : 'Highlights';
    section.appendChild(hlLabel);
    const list = el('ul', 'm-hl-list');
    hlList.forEach(h => {
      const li = el('li', 'm-hl-item');
      li.textContent = h;
      list.appendChild(li);
    });
    section.appendChild(list);
    modalBody.appendChild(section);
  }

  // Links
  const linksDiv = el('div', 'm-links');
  if (p.github && p.github !== '#') {
    const a = el('a', 'm-link m-link-primary');
    a.href = p.github; a.target = '_blank'; a.rel = 'noopener noreferrer';
    a.appendChild(githubIcon());
    a.appendChild(document.createTextNode(' GitHub'));
    linksDiv.appendChild(a);
  }
  if (p.demo && p.demo !== '#') {
    const a = el('a', 'm-link m-link-secondary');
    a.href = p.demo; a.target = '_blank'; a.rel = 'noopener noreferrer';
    a.appendChild(externalIcon());
    a.appendChild(document.createTextNode(zh ? ' 網站連結' : ' Live Demo'));
    linksDiv.appendChild(a);
  }
  if (linksDiv.children.length) modalBody.appendChild(linksDiv);
}

function closeModal() {
  modalBackdrop.classList.remove('open');
  modalBackdrop.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

modalClose.addEventListener('click', closeModal);
modalBackdrop.addEventListener('click', e => { if (e.target === modalBackdrop) closeModal(); });

// ---------------------------------------------------------------------------
// Project card events
// ---------------------------------------------------------------------------
projectCards.forEach(card => {
  card.addEventListener('click', () => openProject(card));
  card.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openProject(card); }
  });
});

// ---------------------------------------------------------------------------
// Keyboard
// ---------------------------------------------------------------------------
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) closeModal();
});

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function el(tag, className) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  return node;
}
function svgNS(tag) { return document.createElementNS('http://www.w3.org/2000/svg', tag); }

function githubIcon() {
  const svg = svgNS('svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('width', '14'); svg.setAttribute('height', '14');
  svg.setAttribute('fill', 'currentColor');
  const path = svgNS('path');
  path.setAttribute('d', 'M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z');
  svg.appendChild(path); return svg;
}

function externalIcon() {
  const svg = svgNS('svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('width', '14'); svg.setAttribute('height', '14');
  svg.setAttribute('fill', 'none'); svg.setAttribute('stroke', 'currentColor'); svg.setAttribute('stroke-width', '2');
  const p = svgNS('path'); p.setAttribute('d', 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6');
  const poly = svgNS('polyline'); poly.setAttribute('points', '15 3 21 3 21 9');
  const line = svgNS('line'); line.setAttribute('x1','10'); line.setAttribute('y1','14'); line.setAttribute('x2','21'); line.setAttribute('y2','3');
  svg.appendChild(p); svg.appendChild(poly); svg.appendChild(line); return svg;
}
