// Laver færdige plakat-PDF'er fra docs/plakat.html. Kør: node site/make_pdfs.js (kræver playwright)
const { chromium } = require('playwright');
const path = require('path');
const root = path.resolve(__dirname, '..');
const JOBS = [
  ['plakat-A2-5-generationer.pdf', 'g5', 'A2'],
  ['plakat-A1-alle-aner.pdf', 'g99', 'A1'],
  ['plakat-A3-fars-side.pdf', 'g6-far', 'A3'],
  ['plakat-A3-mors-side.pdf', 'g6-mor', 'A3'],
];
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  for (const [out, hash, paper] of JOBS) {
    const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
    await p.goto('file://' + path.join(root, 'docs', 'plakat.html') + '#' + hash.replace('g99', 'g' + 99));
    await p.waitForFunction(() => window.__posterReady);
    if (hash === 'g99') await p.evaluate(() => { const s = document.getElementById('gens'); s.value = s.options[s.options.length - 1].value; s.dispatchEvent(new Event('change')); });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(500);
    await p.pdf({ path: path.join(root, 'docs', out), format: paper, landscape: true, printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
    console.log('wrote', out);
    await p.close();
  }
  await b.close();
})();
