#!/usr/bin/env node
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const TEMP_PROFILE = '/tmp/tinker_playwright_profile';

async function run() {
  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await context.newPage();
  await page.goto('https://tinker-console.thinkingmachines.ai/onboarding', {
    timeout: 20000, waitUntil: 'domcontentloaded'
  });
  await page.waitForTimeout(3000);

  // Get full HTML of the form area
  const formHtml = await page.evaluate(() => {
    const main = document.querySelector('main') || document.body;
    return main.innerHTML.substring(0, 8000);
  });
  
  fs.writeFileSync('/tmp/tinker_form.html', formHtml);
  console.log('Form HTML saved to /tmp/tinker_form.html');
  
  // Get all interactive elements
  const elements = await page.evaluate(() => {
    const result = [];
    document.querySelectorAll('button, input, label, [role], [data-state], [onclick]').forEach(el => {
      result.push({
        tag: el.tagName,
        type: el.type || '',
        id: el.id || '',
        name: el.name || '',
        class: el.className.substring(0, 80),
        text: el.textContent.trim().substring(0, 50),
        role: el.getAttribute('role') || '',
        dataState: el.getAttribute('data-state') || '',
        ariaHidden: el.getAttribute('aria-hidden') || '',
        forAttr: el.getAttribute('for') || '',
        disabled: el.disabled || false,
      });
    });
    return result;
  });
  
  console.log('\n=== INTERACTIVE ELEMENTS ===');
  elements.forEach(e => console.log(JSON.stringify(e)));
  
  // Try to find the ToS element
  console.log('\n=== TOS SPECIFIC ===');
  const tosInfo = await page.evaluate(() => {
    const cb = document.querySelector('input[name="tos"]');
    if (!cb) return 'no tos input found';
    const parent = cb.parentElement;
    const grandparent = parent ? parent.parentElement : null;
    return {
      input: { html: cb.outerHTML, checked: cb.checked },
      parent: parent ? { html: parent.outerHTML.substring(0, 300), tag: parent.tagName } : null,
      grandparent: grandparent ? { html: grandparent.outerHTML.substring(0, 300), tag: grandparent.tagName } : null,
    };
  });
  console.log(JSON.stringify(tosInfo, null, 2));

  await context.close();
}

run().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
