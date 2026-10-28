#!/usr/bin/env node
/* Regression check for mip-drafts-console.html.

   Loads the console's own JavaScript (no browser needed), feeds it the synthetic fixtures,
   runs three settings configurations, and compares every outcome with tests/baseline/*.json:
     - the Step 04 summary tiles
     - where every manuscript went, and why
     - the subject and text of every editor, triage, EA and reviewer draft
     - Step 05b delayed editors

   Usage (from the repo root, Node 18+):
     node tests/run.js            compare with the baseline (exit code 1 on any difference)
     node tests/run.js --update   accept the current behaviour as the new baseline

   Only run --update when a difference is an intended change, and say so in CHANGELOG.md.
*/
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CONSOLE = path.join(ROOT, 'mip-drafts-console.html');
const FIX = path.join(__dirname, 'fixtures');
const BASE_DIR = path.join(__dirname, 'baseline');
const RUN_DATE = '2026-10-01T12:00:00Z';   // must match RUN_DATE in tests/make_fixtures.py
const UPDATE = process.argv.includes('--update');

const CONFIGS = {
  'v2-defaults':        {grouping: 'journal', allOverdue: true,  healthSkip: false},
  'like-original':      {grouping: 'editor',  allOverdue: false, healthSkip: false},
  'health-check-rule':  {grouping: 'journal', allOverdue: true,  healthSkip: true},
};

/* ---------- minimal DOM stand-in: enough for the console's logic to run ---------- */
function makeDom(jsonTags){
  const els = {};
  function el(id){
    const classes = new Set();
    const node = {
      id, value: '', checked: false, disabled: false, style: {}, dataset: {}, children: [],
      textContent: jsonTags[id] || '', _html: '',
      classList: { add: c => classes.add(c), remove: c => classes.delete(c), contains: c => classes.has(c),
                   toggle: (c, f) => { const on = f === undefined ? !classes.has(c) : f; on ? classes.add(c) : classes.delete(c); return on; } },
      addEventListener(){}, removeEventListener(){}, remove(){}, before(){}, after(){}, prepend(){}, append(){},
      insertBefore(){}, replaceWith(){}, getAttribute(){ return null; }, setAttribute(){}, focus(){}, select(){}, click(){},
      scrollIntoView(){}, insertAdjacentHTML(){}, appendChild(c){ this.children.push(c); return c; }, removeChild(){},
      querySelector(){ return el('_q'); }, querySelectorAll(){ return []; }, closest(){ return el('_c'); }, parentNode: null,
    };
    return new Proxy(node, {
      get(t, p){ return p === 'innerHTML' ? t._html : t[p]; },
      set(t, p, v){ if (p === 'innerHTML') t._html = v; else t[p] = v; return true; },
    });
  }
  return {
    getElementById: id => els[id] || (els[id] = el(id)),
    querySelector: () => el('_x'), querySelectorAll: () => [], createElement: t => el(t),
    addEventListener(){}, body: el('body'),
  };
}

/* ---------- normalise HTML so harmless markup differences don't fail the test ---------- */
const ENT = {amp:'&', lt:'<', gt:'>', quot:'"', '#39':"'", nbsp:' ', ndash:'–', mdash:'—', middot:'·', rarr:'→', hellip:'…'};
function norm(html){
  return String(html)
    .replace(/&#(\d+);/g, (m, n) => String.fromCodePoint(+n))
    .replace(/&([a-z0-9#]+);/gi, (m, n) => ENT[n] !== undefined ? ENT[n] : m)
    .replace(/ target="_blank" rel="noopener noreferrer"/g, '')
    .replace(/\s+/g, ' ').trim();
}

function runConfig(name, cfg){
  const html = fs.readFileSync(CONSOLE, 'utf8');
  const jsonTags = {};
  for (const m of html.matchAll(/<script type="application\/json" id="([^"]+)">([\s\S]*?)<\/script>/g)) jsonTags[m[1]] = m[2];
  const start = html.indexOf('<script>', html.indexOf('xlsx.full.min.js'));
  const code = html.slice(start + 8, html.lastIndexOf('</script>'));

  const RealDate = Date;
  const sandbox = {
    document: makeDom(jsonTags),
    navigator: {clipboard: {}}, alert(){}, console: {log(){}, warn(){}, error: (...a) => console.error('[console]', ...a)},
    URL: {createObjectURL: () => 'blob:test', revokeObjectURL(){}},
    Blob: class { constructor(p){ this.parts = p; } }, XLSX: {}, FileReader: class {},
    TextEncoder, setTimeout: () => 0, clearTimeout(){},
    Date: class extends RealDate { constructor(...a){ a.length ? super(...a) : super(RUN_DATE); } static now(){ return new RealDate(RUN_DATE).getTime(); } },
    MIP: JSON.parse(fs.readFileSync(path.join(FIX, 'synthetic-mip.json'), 'utf8')),
    REVIEWERS: JSON.parse(fs.readFileSync(path.join(FIX, 'synthetic-reviewers.json'), 'utf8')),
    CFG: cfg, OUT: {},
  };
  sandbox.window = sandbox;
  const driver = `
    const CAPTURE = {};
    const _rrRender = rrRenderDrafts; rrRenderDrafts = function(d){ CAPTURE.rr = d; return _rrRender(d); };
    const $ = id => document.getElementById(id);
    $('inviteGraceDays').value = '10'; $('staleInviteCount').value = '60';
    $('inactivityThresholdDays').value = '30'; $('longPendingThreshold').value = '365';
    $('eaEmail').value = 'ea.mailbox@example.org'; $('signOff').value = '';
    $('editorGroupingMode').value = CFG.grouping;
    $('allOverdueToInvite').checked = CFG.allOverdue;
    $('healthOnTrackSkip').checked = CFG.healthSkip;
    $('rrYourName').value = 'Test Sender';
    loadRows(MIP, 'synthetic-mip.json');
    generateAll();
    rrLoadPerf(REVIEWERS, 'synthetic-reviewers.json');
    rrGenerateAll();
    const tiles = [...$('statRow').innerHTML.matchAll(/<div class="n">([\\s\\S]*?)<\\/div>\\s*<div class="label">([\\s\\S]*?)<\\/div>/g)]
      .map(m => (m[2].replace(/<[^>]+>/g, '').trim() + ': ' + m[1].replace(/<[^>]+>/g, '').trim()));
    const rows = ROWS.map(r => { const a = ANNOTATIONS[r._rawIndex] || {}; return {id: String(r.id), inDraft: !!a.inDraft, to: a.draftedTo || '', action: a.draftedAction || '', reason: a.reason || '', category: rowHighlightFor(a).category}; });
    const drafts = {};
    Object.entries(LAST_EDITORS_DICT).forEach(([k, p]) => { const e = buildPersonEmail(p.displayName, p, '', 'editor'); drafts['editor | ' + k] = {to: p.email, subject: e.subject, text: e.html}; });
    Object.entries(LAST_TRIAGE_DICT).forEach(([k, p]) => { const e = buildPersonEmail(p.displayName, p, '', 'triage'); drafts['triage | ' + k] = {to: p.email, subject: e.subject, text: e.html}; });
    LAST_EA_DRAFTS.forEach(d => { drafts['ea | ' + d.nameForFile] = {to: d.to, subject: d.subject, text: d.html}; });
    (CAPTURE.rr || []).forEach(d => { drafts['reviewer | ' + d.manuscriptId + ' | ' + d.reviewerEmail] = {to: d.reviewerEmail, subject: d.subject, text: d.html}; });
    const delayed = Object.values(DELAY_GROUPS).filter(e => e.delayed > 0).map(e => ({editor: e.name, journal: e.journal, needsAction: e.delayed, current: e.total}))
      .sort((a, b) => (a.editor + a.journal).localeCompare(b.editor + b.journal));
    OUT.result = {tiles, rows, drafts, delayed, templateVersion: MIP_TEMPLATES.version};
  `;
  const fn = new Function(...Object.keys(sandbox), code + '\n' + driver);
  fn(...Object.values(sandbox));
  const r = sandbox.OUT.result;
  Object.values(r.drafts).forEach(d => { d.subject = norm(d.subject); d.text = norm(d.text); });
  return r;
}

function diff(a, b, where, out){
  if (JSON.stringify(a) === JSON.stringify(b)) return;
  if (a && b && typeof a === 'object' && typeof b === 'object' && !Array.isArray(a)){
    new Set([...Object.keys(a), ...Object.keys(b)]).forEach(k => diff(a[k], b[k], `${where}.${k}`, out));
    return;
  }
  if (Array.isArray(a) && Array.isArray(b) && a.length === b.length){
    a.forEach((x, i) => diff(x, b[i], `${where}[${i}]`, out));
    return;
  }
  if (typeof a === 'string' && typeof b === 'string'){
    // Show the text around the first character that differs, not the start of a long email.
    let i = 0; while (i < a.length && a[i] === b[i]) i++;
    const from = Math.max(0, i - 60);
    out.push(`  ${where}\n    expected: …${a.slice(from, i + 140)}…\n    actual:   …${b.slice(from, i + 140)}…`);
    return;
  }
  const show = v => v === undefined ? '(missing)' : JSON.stringify(v).slice(0, 300);
  out.push(`  ${where}\n    expected: ${show(a)}\n    actual:   ${show(b)}`);
}

fs.mkdirSync(BASE_DIR, {recursive: true});
let failed = 0;
for (const [name, cfg] of Object.entries(CONFIGS)){
  const actual = runConfig(name, cfg);
  const file = path.join(BASE_DIR, `${name}.json`);
  if (UPDATE || !fs.existsSync(file)){
    fs.writeFileSync(file, JSON.stringify(actual, null, 1) + '\n');
    console.log(`✔ ${name}: baseline ${UPDATE ? 'updated' : 'created'} (${Object.keys(actual.drafts).length} drafts, ${actual.rows.length} rows)`);
    continue;
  }
  const expected = JSON.parse(fs.readFileSync(file, 'utf8'));
  const problems = [];
  diff(expected, actual, name, problems);
  if (problems.length){
    failed++;
    console.log(`✘ ${name}: ${problems.length} difference(s)`);
    problems.slice(0, 25).forEach(p => console.log(p));
    if (problems.length > 25) console.log(`  … and ${problems.length - 25} more`);
  } else {
    console.log(`✔ ${name}: matches baseline (${Object.keys(actual.drafts).length} drafts, ${actual.rows.length} rows)`);
  }
}
if (failed){
  console.log(`\n${failed} configuration(s) differ from the baseline. If every difference is intended, run: node tests/run.js --update`);
  process.exit(1);
}
