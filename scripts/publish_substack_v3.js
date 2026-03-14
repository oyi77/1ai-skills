#!/usr/bin/env node
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const TEMP_PROFILE = '/tmp/tinker_playwright_profile';
const OUTPUT = '/tmp/substack_result.json';

const TITLE = "10 AI Tools Gratis yang Bisa Gantikan 5 Karyawan di 2026";
const SUBTITLE = "Hemat Rp 34-62 Juta/Bulan dengan AI Tools yang Udah Terbukti Works";
const FULL_ARTICLE = fs.readFileSync('/home/openclaw/.openclaw/workspace/temp/substack-article.md', 'utf8');

async function run() {
  const result = { success: false, url: null, error: null, step: 'start', logs: [] };
  const log = (msg) => { console.log(msg); result.logs.push(msg); };

  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await context.newPage();

  try {
    // Already logged in — go directly to writer dashboard
    log('Going to Substack dashboard...');
    await page.goto('https://substack.com/dashboard', { timeout: 20000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);
    log('Dashboard URL: ' + page.url());

    // Try writer subdomain  
    if (!page.url().includes('substack.com/dashboard') && !page.url().includes('oyi77')) {
      log('Trying oyi77 substack...');
      await page.goto('https://oyi77.substack.com/publish', { timeout: 20000, waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
      log('oyi77 URL: ' + page.url());
    }

    let bodyText = await page.locator('body').innerText();
    log('Page text: ' + bodyText.substring(0, 200));

    // Find "New post" button or look for editor
    const newPostSelectors = [
      'a:has-text("New post")', 'button:has-text("New post")',
      'a:has-text("New Post")', 'button:has-text("New Post")',
      'a[href*="/publish/post/new"]',
      'button:has-text("Write")', 'a:has-text("Write")',
    ];

    let clickedNew = false;
    for (const sel of newPostSelectors) {
      const el = page.locator(sel);
      if (await el.count() > 0) {
        log('Clicking: ' + sel);
        await el.first().click();
        await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
        await page.waitForTimeout(3000);
        log('After new post click: ' + page.url());
        clickedNew = true;
        break;
      }
    }

    if (!clickedNew) {
      // Try direct URL with subdomain
      log('Direct to editor...');
      await page.goto('https://oyi77.substack.com/publish/post/new', { timeout: 20000, waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(4000);
      log('Editor URL: ' + page.url());
    }

    // Check current state
    bodyText = await page.locator('body').innerText();
    log('Editor page text: ' + bodyText.substring(0, 400));
    result.editor_url = page.url();

    // Look for title field - try many selectors
    const titleSelectors = [
      'h1[contenteditable="true"]',
      '[data-placeholder="Title"]',
      '[data-testid="post-title"]',
      '.post-title',
      'div[contenteditable][class*="title"]',
      'p[data-placeholder="Title"]',
    ];

    let titleTyped = false;
    for (const sel of titleSelectors) {
      const el = page.locator(sel);
      if (await el.count() > 0) {
        log('Found title with: ' + sel);
        await el.click();
        await page.keyboard.selectAll();
        await page.keyboard.type(TITLE);
        log('Title typed!');
        titleTyped = true;
        result.step = 'title_typed';
        break;
      }
    }

    if (!titleTyped) {
      // Dump all contenteditable elements
      const editables = await page.evaluate(() => {
        return [...document.querySelectorAll('[contenteditable]')].map(el => ({
          tag: el.tagName,
          class: el.className.substring(0, 60),
          placeholder: el.getAttribute('data-placeholder') || '',
          text: el.textContent.substring(0, 50),
        }));
      });
      log('Contenteditable elements: ' + JSON.stringify(editables));
      result.editables = editables;
    }

    if (titleTyped) {
      // Press Tab or Enter to move to subtitle/body
      await page.keyboard.press('Tab');
      await page.waitForTimeout(500);

      // Type subtitle if there's a subtitle field
      const subtitleEl = page.locator('[data-placeholder="Subtitle"], [data-placeholder*="subtitle" i]');
      if (await subtitleEl.count() > 0) {
        await subtitleEl.click();
        await page.keyboard.type(SUBTITLE);
        log('Subtitle typed!');
      }
      await page.keyboard.press('Tab');
      await page.waitForTimeout(500);

      // Type body - find body editor
      const bodySelectors = [
        'div[contenteditable="true"]:not([data-placeholder="Title"]):not([data-placeholder*="ubtitle"])',
        '.ProseMirror',
        '[data-placeholder="Tell your story..."]',
        '[data-placeholder*="story"]',
        '[data-placeholder*="Start writing"]',
      ];

      let bodyTyped = false;
      for (const sel of bodySelectors) {
        const el = page.locator(sel);
        if (await el.count() > 0) {
          log('Found body with: ' + sel);
          await el.click();
          // Type the article in chunks to avoid timeout
          const chunks = FULL_ARTICLE.split('\n\n');
          for (const chunk of chunks) {
            await page.keyboard.type(chunk);
            await page.keyboard.press('Enter');
            await page.keyboard.press('Enter');
            await page.waitForTimeout(100);
          }
          log('Body typed! ' + chunks.length + ' paragraphs');
          bodyTyped = true;
          result.step = 'body_typed';
          break;
        }
      }

      if (!bodyTyped) {
        log('Body field not found, trying keyboard focus...');
        // Just tab again and try typing
        await page.keyboard.press('Tab');
        await page.waitForTimeout(300);
        await page.keyboard.type('Test paragraph');
        result.step = 'body_attempt';
      }

      // Wait a bit for autosave
      await page.waitForTimeout(2000);

      // Publish - find publish button
      const publishSelectors = [
        'button:has-text("Publish")',
        'button:has-text("Publish now")', 
        'button:has-text("Continue")',
        '[data-testid="publish-button"]',
      ];

      for (const sel of publishSelectors) {
        const btn = page.locator(sel);
        if (await btn.count() > 0) {
          log('Found publish btn: ' + sel);
          await btn.first().click();
          await page.waitForTimeout(3000);
          log('After publish click: ' + page.url());

          // Confirm publish in dialog if shown
          const confirmBtn = page.locator('button:has-text("Publish now"), button:has-text("Publish post"), button:has-text("Confirm")');
          if (await confirmBtn.count() > 0) {
            await confirmBtn.first().click();
            await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
            await page.waitForTimeout(3000);
            log('Published! URL: ' + page.url());
            result.published_url = page.url();
            result.success = true;
            result.step = 'published';
          }
          break;
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
  console.log(JSON.stringify(r, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e.message);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
