#!/usr/bin/env node
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const TEMP_PROFILE = '/tmp/tinker_playwright_profile';
const OUTPUT = '/tmp/substack_result.json';
const TITLE = "10 AI Tools Gratis yang Bisa Gantikan 5 Karyawan di 2026";
const SUBTITLE = "Hemat Rp 34-62 Juta/Bulan dengan AI Tools yang Udah Terbukti Works";
const ARTICLE = fs.readFileSync('/home/openclaw/.openclaw/workspace/temp/substack-article.md', 'utf8');

async function run() {
  const result = { success: false, url: null, error: null, logs: [] };
  const log = msg => { console.log(msg); result.logs.push(msg); };

  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await context.newPage();

  try {
    log('Opening editor...');
    await page.goto('https://oyi77.substack.com/publish/post/new', {
      timeout: 20000, waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(3000);
    log('URL: ' + page.url());

    // Dump all contenteditable elements with full detail
    const allEditables = await page.evaluate(() => {
      const els = [...document.querySelectorAll('[contenteditable="true"], [contenteditable=""]')];
      return els.map((el, i) => ({
        index: i,
        tag: el.tagName,
        className: el.className.substring(0, 80),
        placeholder: el.getAttribute('data-placeholder') || el.getAttribute('placeholder') || '',
        ariaLabel: el.getAttribute('aria-label') || '',
        id: el.id || '',
        text: el.textContent.substring(0, 50),
        rect: (() => { const r = el.getBoundingClientRect(); return {top: r.top, left: r.left, w: r.width, h: r.height}; })(),
      }));
    });
    log('All editables: ' + JSON.stringify(allEditables, null, 2));

    // Find title by position (usually top element) or class name
    const titleIndex = allEditables.findIndex(e => 
      e.rect.top < 200 && e.rect.top > 0 && e.rect.w > 400
    );
    log('Title likely at index: ' + titleIndex);

    // Click title field - the topmost wide contenteditable
    if (titleIndex >= 0 || allEditables.length > 0) {
      const idx = titleIndex >= 0 ? titleIndex : 0;
      const titleEl = allEditables[idx];
      log('Using title element: ' + JSON.stringify(titleEl));

      // Click by index
      await page.evaluate((index) => {
        const els = [...document.querySelectorAll('[contenteditable="true"], [contenteditable=""]')];
        if (els[index]) els[index].click();
      }, idx);
      await page.waitForTimeout(300);

      // Clear and type title
      await page.keyboard.press('Control+a');
      await page.keyboard.type(TITLE, { delay: 10 });
      log('Title typed!');
      await page.waitForTimeout(500);

      // Tab to subtitle if exists
      await page.keyboard.press('Tab');
      await page.waitForTimeout(300);
      
      // Check if subtitle field appeared
      const afterTab = await page.evaluate(() => 
        document.activeElement ? {
          tag: document.activeElement.tagName,
          placeholder: document.activeElement.getAttribute('data-placeholder') || '',
          class: document.activeElement.className.substring(0, 60)
        } : null
      );
      log('After Tab focus: ' + JSON.stringify(afterTab));

      if (afterTab?.placeholder?.toLowerCase().includes('subtitle')) {
        await page.keyboard.type(SUBTITLE, { delay: 10 });
        await page.keyboard.press('Tab');
        await page.waitForTimeout(300);
      }

      // Click the body field (Start writing...)
      const bodyEl = page.locator('[data-placeholder="Start writing..."]').first();
      await bodyEl.click();
      await page.waitForTimeout(300);

      // Type article - line by line
      log('Typing article...');
      const lines = ARTICLE.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.trim()) {
          await page.keyboard.type(line, { delay: 3 });
        }
        await page.keyboard.press('Enter');
        if (i % 20 === 0) await page.waitForTimeout(100); // occasional pause
      }
      log('Article done! Lines: ' + lines.length);
      result.step = 'article_typed';
      await page.waitForTimeout(2000);

      // Click Continue (Substack's publish flow button)
      const continueBtn = page.locator('button:has-text("Continue")').first();
      if (await continueBtn.count() > 0) {
        log('Clicking Continue...');
        await continueBtn.click();
        await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
        await page.waitForTimeout(3000);
        log('After Continue: ' + page.url());

        // On publish settings page - click Publish
        const publishBtn = page.locator('button:has-text("Publish"), button:has-text("Publish now"), button:has-text("Send")').first();
        if (await publishBtn.count() > 0) {
          log('Found Publish button, clicking...');
          await publishBtn.click();
          await page.waitForLoadState('domcontentloaded', { timeout: 20000 });
          await page.waitForTimeout(4000);
          log('Published! URL: ' + page.url());
          result.published_url = page.url();
          result.success = page.url().includes('oyi77.substack.com/p/');
          result.step = 'published';
        } else {
          const allBtns = await page.locator('button').allTextContents();
          log('Buttons on publish page: ' + allBtns.join(', '));
          result.step = 'on_publish_page';
          result.final_url = page.url();
          
          // Save screenshot content for diagnosis
          result.publish_page_text = (await page.locator('body').innerText()).substring(0, 1000);
        }
      }
    }

    result.final_url = page.url();

  } catch (e) {
    result.error = e.message;
    log('ERROR: ' + e.message);
    try { result.final_url = page.url(); } catch {}
  }

  await context.close();
  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== RESULT ===');
  const r = { ...result };
  delete r.publish_page_text;
  console.log(JSON.stringify(r, null, 2));
}

run().catch(e => {
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
