import { readFile, access } from 'node:fs/promises';
import assert from 'node:assert/strict';
const html = await readFile('index.html', 'utf8');
const css = await readFile('style.css', 'utf8');
const js = await readFile('script.js', 'utf8');
assert(!/<\/?div(?:\s|>)/i.test(html + js), 'The lab guide disallows div content containers');
assert(css.includes('box-sizing:border-box;margin:0;padding:0'), 'Missing full universal reset');
await access('images/portrait.svg');
for (const tag of ['header', 'nav', 'main', 'section', 'article', 'footer']) assert(html.includes(`<${tag}`), `Missing ${tag}`);
for (const type of ['email', 'tel', 'url']) assert(html.includes(`type="${type}"`), `Missing ${type} input`);
assert(html.includes('required'), 'Missing HTML validation');
assert(css.includes('@media (min-width: 1024px)'), 'Missing required desktop breakpoint');
assert(css.includes('repeat(12,') && css.includes('repeat(4,'), 'Missing 12 / 4 column grids');
assert(!/<table[\s>]/i.test(html), 'Table layout is not allowed');
assert(!/\bfloat\s*:/.test(css), 'Float layout is not allowed');
const withoutMedia = css.replace(/@media[^\{]+/g, '');
assert(!/\d+(?:\.\d+)?px\b/.test(withoutMedia), 'Fixed px content geometry is not allowed');
for (const match of html.matchAll(/(?:src|href)="([^"#][^"]*)"/g)) {
  if (/^(?:https?:|data:)/.test(match[1])) continue;
  await access(match[1]);
}
for (const file of ['portrait', 'noma', 'moneta', 'forma', 'dala', 'mark']) {
  const svg = await readFile(`images/${file}.svg`, 'utf8');
  assert(!svg.includes('<text'), `${file} SVG contains unoutlined text`);
  await access(`images/${file}.webp`);
}
console.log('PASS: semantic structure, form fields, relative CSS units, breakpoints, grids, local assets, SVG outlines and WebP exports.');
