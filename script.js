'use strict';
const storage = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); return true; } catch { return false; } },
  remove(key) { try { localStorage.removeItem(key); return true; } catch { return false; } }
};
const themeButton = document.querySelector('#theme-toggle');
const preference = storage.get('azamat-theme');
const previewTheme = new URLSearchParams(location.search).get('theme');
if (new URLSearchParams(location.search).get('design') === '1') document.documentElement.dataset.design = 'true';
const systemDark = window.matchMedia('(prefers-color-scheme: dark)');
function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeButton.setAttribute('aria-checked', String(theme === 'dark'));
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#191a18' : '#f5f3ee';
}
setTheme(previewTheme === 'light' || previewTheme === 'dark' ? previewTheme : preference === 'light' || preference === 'dark' ? preference : systemDark.matches ? 'dark' : 'light');
themeButton.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  setTheme(theme); storage.set('azamat-theme', theme);
});
systemDark.addEventListener('change', event => {
  if (!storage.get('azamat-theme')) setTheme(event.matches ? 'dark' : 'light');
});

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Open navigation'); nav.classList.remove('is-open'); }
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  nav.classList.toggle('is-open', open);
});
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); menuButton.focus(); } });
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
window.matchMedia('(min-width: 1024px)').addEventListener('change', closeMenu);

const caseStudies = {
  noma: { title: 'Noma', category: 'E-commerce / UI & UX concept', image: 'noma', intro: 'A calm homeware shopping experience that gives products room to breathe.', challenge: 'Shopping interfaces often compete for attention. This concept explores how to make browsing and product comparison feel more focused.', approach: 'Group products by purpose, use clear product information, and keep one main action visible at each step.', deliverables: ['Homepage and collection concept', 'Responsive card system', 'Olive and warm-neutral visual palette', 'Clear product hierarchy'], learning: 'Whitespace and consistent typography can make a busy catalog easier to scan.' },
  moneta: { title: 'Moneta', category: 'Mobile finance / Product concept', image: 'moneta', intro: 'An approachable finance app concept, designed around one question: where is my money going?', challenge: 'Balances, transactions, and savings goals can become overwhelming when every number has the same visual weight.', approach: 'Prioritize the balance, group recent activity, and make savings progress readable at a glance.', deliverables: ['Dashboard screen concept', 'Savings goal screen concept', 'Reusable mobile cards', 'High-contrast primary actions'], learning: 'Financial information needs clear labels and predictable structure. The screens use illustrative balances only.' },
  forma: { title: 'Forma', category: 'Architecture / Website concept', image: 'forma', intro: 'An editorial website concept for an imagined architecture studio.', challenge: 'Let visual projects lead while keeping project details and contact actions easy to find.', approach: 'Combine generous imagery with a restrained type system, a simple navigation, and compact project metadata.', deliverables: ['Editorial homepage concept', 'Architecture project preview', 'Desktop-to-mobile layout rules', 'Minimal visual identity'], learning: 'Strong visual rhythm can connect a large image with a small amount of meaningful text.' },
  dala: { title: 'Dala', category: 'Travel / Web design concept', image: 'dala', intro: 'A travel discovery concept inspired by open landscapes and simpler choices.', challenge: 'Travel pages can show too many options before helping people decide what kind of trip they want.', approach: 'Start with a clear destination prompt, use a small set of meaningful categories, and present the next action consistently.', deliverables: ['Destination discovery homepage', 'Trip preview cards', 'Landscape illustration system', 'Responsive search concept'], learning: 'Useful filters and a clear starting point are often more helpful than a long list of destinations.' }
};
const caseDialog = document.querySelector('#case-dialog');
document.querySelectorAll('[data-case]').forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  const entry = caseStudies[link.dataset.case];
  document.querySelector('#case-content').innerHTML = `<img class="dialog-image" src="images/${entry.image}.svg" alt="${entry.title} interface concept"><p class="eyebrow">${entry.category}</p><h2 id="case-title">${entry.title}</h2><p>${entry.intro}</p><section class="case-detail-grid" aria-label="Case study details"><section><h3>The challenge</h3><p>${entry.challenge}</p></section><section><h3>The approach</h3><p>${entry.approach}</p></section><section><h3>Concept deliverables</h3><ul>${entry.deliverables.map(item => `<li>${item}</li>`).join('')}</ul></section><section><h3>What I learned</h3><p>${entry.learning}</p></section></section><p class="concept-note">Independent student concept. These are design explorations, not launched client products.</p><a href="#contact" class="button button-dark" id="case-contact">Discuss a similar idea <span aria-hidden="true">↗</span></a>`;
  caseDialog.showModal();
  caseDialog.scrollTop = 0;
  document.querySelector('#case-contact').addEventListener('click', () => caseDialog.close());
}));
const legalDialog = document.querySelector('#legal-dialog');
document.querySelectorAll('[data-legal]').forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  const privacy = link.dataset.legal === 'privacy';
  document.querySelector('#legal-content').innerHTML = privacy ? `<h2 id="legal-title">Privacy information</h2><p>This student portfolio has no analytics, advertising cookies, or remote form endpoint. Submitting the form does not email the designer.</p><p>If you give consent, one project brief is saved in this browser's local storage. It contains the name, email, optional phone, specification link, service, details, and creation date you enter. Saving another brief replaces it.</p><p>Use “Download brief” to export a text copy, or “Delete saved brief” to remove it. Theme preference is also saved on this device. If browser storage is unavailable, you can still download the current brief.</p><p>Do not enter confidential or sensitive information into this educational demonstration. External design-platform links lead to separate websites with their own privacy practices.</p>` : `<h2 id="legal-title">Portfolio terms</h2><p>This is an educational UI/UX portfolio by Azamat Abduraupov for ICT6001. Noma, Moneta, Forma, and Dala are independent fictional design concepts, with no client affiliation.</p><p>All prices are illustrative starting prices in Kazakhstani tenge. They do not create a service contract or a promise of availability.</p><p>The illustrated avatar is a placeholder for a personal photograph. Behance and Dribbble links lead to platform homepages, not verified personal profiles.</p><p>© 2026 Azamat Abduraupov. Original concept illustrations and source code are provided with this coursework. Brand names of external platforms belong to their respective owners.</p>`;
  legalDialog.showModal();
}));
document.querySelectorAll('dialog').forEach(dialog => {
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
});

document.querySelectorAll('[data-service]').forEach(link => link.addEventListener('click', () => { document.querySelector('#service').value = link.dataset.service; }));
const briefKey = 'azamat-project-brief-v1';
let currentBrief = null;
try { currentBrief = JSON.parse(storage.get(briefKey)); } catch { currentBrief = null; }
if (!currentBrief || typeof currentBrief.name !== 'string' || typeof currentBrief.email !== 'string') currentBrief = null;
const actions = document.querySelector('#brief-actions');
const status = document.querySelector('#form-status');
if (currentBrief) { actions.hidden = false; status.textContent = 'A previous project brief is saved on this device. Download it or delete it below.'; }
document.querySelector('#project-form').addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const url = new URL(data.get('specifications'));
  const urlInput = document.querySelector('#client-spec');
  if (!['https:', 'http:'].includes(url.protocol)) { urlInput.setCustomValidity('Use an https:// or http:// link.'); urlInput.reportValidity(); return; }
  urlInput.setCustomValidity('');
  currentBrief = { name: data.get('name').trim(), email: data.get('email').trim(), phone: data.get('phone').trim(), specifications: url.href, service: data.get('service'), details: data.get('details').trim(), createdAt: new Date().toISOString() };
  const saved = storage.set(briefKey, JSON.stringify(currentBrief));
  status.textContent = saved ? 'Your project brief is saved on this device. You can download a copy below. Nothing has been sent.' : 'This browser could not save the brief. You can download the current copy below before closing this page.';
  actions.hidden = false;
});
document.querySelector('#client-spec').addEventListener('input', event => event.target.setCustomValidity(''));
document.querySelector('#download-brief').addEventListener('click', () => {
  if (!currentBrief) return;
  const text = `PROJECT BRIEF\nAzamat Abduraupov / UI/UX student portfolio\n\nName: ${currentBrief.name}\nEmail: ${currentBrief.email}\nPhone: ${currentBrief.phone || 'Not provided'}\nTechnical specifications: ${currentBrief.specifications}\nService: ${currentBrief.service}\n\nProject details:\n${currentBrief.details || 'Not provided'}\n\nCreated: ${currentBrief.createdAt}\n\nEducational demo. This brief has not been sent to a server.\n`;
  const objectUrl = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }));
  const anchor = document.createElement('a'); anchor.href = objectUrl; anchor.download = 'project-brief.txt'; anchor.click(); setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
});
document.querySelector('#delete-brief').addEventListener('click', () => {
  if (!storage.remove(briefKey)) { status.textContent = 'The browser could not remove its saved brief. Clear site data in your browser settings.'; return; }
  currentBrief = null; actions.hidden = true; status.textContent = 'The saved brief has been deleted from this browser.';
});
