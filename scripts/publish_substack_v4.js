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
    // Step 1: Check cookies & auth state for substack
    log('Checking Substack session...');
    await page.goto('https://oyi77.substack.com', { timeout: 20000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
    log('oyi77 URL: ' + page.url());
    
    const cookies = await context.cookies('https://substack.com');
    const substackCookies = cookies.filter(c => c.name.includes('substack') || c.name.includes('connect') || c.name === 'token' || c.name === 'user');
    log('Substack cookies: ' + substackCookies.map(c => c.name).join(', '));

    // Step 2: Try writer dashboard directly
    const writerUrls = [
      'https://oyi77.substack.com/publish/post/new',
      'https://substack.com/publish/post/new?pub=oyi77',
    ];

    let editorFound = false;
    for (const url of writerUrls) {
      log('Trying: ' + url);
      await page.goto(url, { timeout: 20000, waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
      log('Result URL: ' + page.url());

      const editables = await page.evaluate(() => 
        [...document.querySelectorAll('[contenteditable]')].map(el => ({
          tag: el.tagName, 
          placeholder: el.getAttribute('data-placeholder') || el.getAttribute('placeholder') || '',
          text: el.textContent.substring(0, 30)
        }))
      );
      log('Editables: ' + JSON.stringify(editables));

      if (editables.some(e => e.placeholder.toLowerCase().includes('title') || e.placeholder.toLowerCase().includes('story'))) {
        log('Editor found!');
        editorFound = true;
        result.editor_url = page.url();
        break;
      }

      // Check page buttons
      const btns = await page.locator('button').allTextContents();
      log('Buttons: ' + btns.join(', '));
      
      if (page.url().includes('/publish/')) {
        editorFound = true;
        break;
      }
    }

    if (!editorFound) {
      // Dump full page state for diagnosis
      const allText = await page.locator('body').innerText();
      result.page_state = allText.substring(0, 2000);
      result.final_url = page.url();
      log('Editor not found. Page: ' + allText.substring(0, 300));
      
      // Try clicking any "Create" or "New" button via JS
      const clickResult = await page.evaluate(() => {
        const links = [...document.querySelectorAll('a, button')];
        const createLink = links.find(el => 
          el.textContent.includes('New post') || 
          el.textContent.includes('Create') ||
          el.href?.includes('/publish/post/new')
        );
        if (createLink) {
          const href = createLink.href || 'button';
          createLink.click();
          return href;
        }
        return null;
      });
      log('JS click result: ' + clickResult);
      if (clickResult) {
        await page.waitForTimeout(3000);
        log('After JS click: ' + page.url());
        result.final_url = page.url();
      }
    }

    // If we're in editor, type title + body + publish
    const editables = await page.evaluate(() => 
      [...document.querySelectorAll('[contenteditable]')].map(el => ({
        tag: el.tagName, 
        placeholder: el.getAttribute('data-placeholder') || '',
        text: el.textContent.substring(0, 30)
      }))
    );
    log('Final editables: ' + JSON.stringify(editables));

    const titleEl = page.locator('[data-placeholder="Title"], [data-placeholder*="title" i], h1[contenteditable]').first();
    if (await titleEl.count() > 0) {
      log('Typing title...');
      await titleEl.click();
      await page.keyboard.type(TITLE, { delay: 10 });
      await page.keyboard.press('Tab');
      await page.waitForTimeout(500);

      // Subtitle
      const subEl = page.locator('[data-placeholder*="ubtitle" i], [data-placeholder*="Subtitle"]');
      if (await subEl.count() > 0) {
        await subEl.click();
        await page.keyboard.type(SUBTITLE, { delay: 10 });
        await page.keyboard.press('Tab');
        await page.waitForTimeout(300);
      }

      // Body - click inside editor and type
      const bodyEl = page.locator('[data-placeholder*="story" i], [data-placeholder*="Start writing" i], .ProseMirror').first();
      if (await bodyEl.count() > 0) {
        await bodyEl.click();
      } else {
        await page.keyboard.press('Tab');
      }
      await page.waitForTimeout(300);

      // Type article in chunks
      const lines = ARTICLE.split('\n');
      for (const line of lines) {
        if (line.trim()) {
          await page.keyboard.type(line, { delay: 5 });
        }
        await page.keyboard.press('Enter');
      }
      log('Article typed!');
      result.step = 'article_typed';
      await page.waitForTimeout(2000);

      // Publish
      const publishBtn = page.locator('button:has-text("Publish"), button:has-text("Continue to publish")').first();
      if (await publishBtn.count() > 0) {
        log('Clicking Publish...');
        await publishBtn.click();
        await page.waitForTimeout(3000);
        
        // Confirm dialog
        const confirmBtn = page.locator('button:has-text("Publish now"), button:has-text("Publish post")').first();
        if (await confirmBtn.count() > 0) {
          await confirmBtn.click();
          await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
          await page.waitForTimeout(3000);
        }
        log('Published URL: ' + page.url());
        result.published_url = page.url();
        result.success = true;
      } else {
        log('Publish button not found');
        const allBtns = await page.locator('button').allTextContents();
        log('Available buttons: ' + allBtns.join(', '));
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
  console.log(JSON.stringify({ ...result, page_state: result.page_state?.substring(0,200) }, null, 2));
}

run().catch(e => {
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
