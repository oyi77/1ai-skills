#!/usr/bin/env node
/**
 * Publish Substack article via Playwright headless
 * Using Vivaldi profile cookies (already logged in)
 */
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const TEMP_PROFILE = '/tmp/tinker_playwright_profile'; // reuse same profile - has Google session
const OUTPUT = '/tmp/substack_result.json';

// Article content
const TITLE = "10 AI Tools Gratis yang Bisa Gantikan 5 Karyawan di 2026";
const SUBTITLE = "Hemat Rp 34-62 Juta/Bulan dengan AI Tools yang Udah Terbukti Works";

// Full article as plain text with structure hints for Substack editor
const ARTICLE_PARAGRAPHS = [
  "Bayangin lo punya 5 karyawan yang kerja 24/7, ga pernah sakit, ga minta THR, dan ga pernah resign.",
  "Kedengeran impossible? Welcome to 2026.",
  "AI udah bukan mainan tech bros lagi. Ini udah jadi senjata utama buat UMKM, freelancer, dan siapapun yang mau scale bisnis tanpa nambah headcount.",
  "Gue udah test ratusan AI tools. Dan ini 10 yang beneran works — semuanya GRATIS atau punya free tier yang cukup buat mulai.",
];

async function run() {
  const result = { success: false, url: null, error: null, step: 'start' };

  console.log('Launching browser...');
  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await context.newPage();

  try {
    // Navigate to Substack new post
    console.log('Navigating to Substack...');
    await page.goto('https://substack.com/sign-in', { timeout: 20000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);

    let url = page.url();
    console.log('Substack URL:', url);

    // Need to sign in?
    if (url.includes('sign-in') || url.includes('login')) {
      console.log('Need to sign in to Substack...');
      result.step = 'need_signin';

      // Try Google sign in
      const googleBtn = page.locator('button:has-text("Sign in with Google"), a:has-text("Continue with Google"), button:has-text("Google")');
      if (await googleBtn.count() > 0) {
        console.log('Clicking Google sign in...');
        await googleBtn.first().click();
        await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
        await page.waitForTimeout(2000);

        url = page.url();
        console.log('After Google btn:', url);

        // Google account chooser
        if (url.includes('accounts.google.com')) {
          const accountEl = page.locator('text=muchammadizzuddin@gmail.com');
          if (await accountEl.count() > 0) {
            await accountEl.click();
            await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
            await page.waitForTimeout(3000);
            console.log('After account select:', page.url());
          } else {
            // Try typing email
            const emailInput = page.locator('input[type="email"]');
            if (await emailInput.count() > 0) {
              await emailInput.fill('muchammadizzuddin@gmail.com');
              await page.click('#identifierNext, button:has-text("Next")');
              await page.waitForLoadState('domcontentloaded', { timeout: 10000 });
              await page.waitForTimeout(2000);
              
              if (await page.locator('input[type="password"]').count() > 0) {
                result.error = 'NEED_GOOGLE_PASSWORD';
                result.step = 'blocked';
                await context.close();
                fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
                return;
              }
            }
          }
        }
      } else {
        // Try email sign in
        const emailInput = page.locator('input[type="email"], input[name="email"]');
        if (await emailInput.count() > 0) {
          result.error = 'NEED_EMAIL_PASSWORD';
          result.step = 'need_credentials';
          await context.close();
          fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
          return;
        }
      }
    }

    // Check if logged in now
    await page.waitForTimeout(2000);
    url = page.url();
    console.log('Current URL:', url);

    // Navigate to new post editor
    console.log('Going to new post editor...');
    await page.goto('https://substack.com/publish/post/new', { timeout: 20000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);
    url = page.url();
    console.log('Editor URL:', url);

    // Check if redirected to sign-in
    if (url.includes('sign-in') || url.includes('login')) {
      result.error = 'NOT_LOGGED_IN';
      result.step = 'auth_failed';
      result.final_url = url;
      const text = await page.locator('body').innerText();
      result.page_text = text.substring(0, 500);
      await context.close();
      fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
      return;
    }

    // Check if we're in the editor
    const pageText = await page.locator('body').innerText();
    console.log('Page preview:', pageText.substring(0, 300));
    result.page_preview = pageText.substring(0, 1000);
    result.final_url = url;

    // Try to find the title field
    const titleField = page.locator('[data-testid="post-title"], [placeholder*="Title"], h1[contenteditable], .post-title-input');
    if (await titleField.count() > 0) {
      console.log('Found title field, typing title...');
      await titleField.click();
      await titleField.fill(TITLE);
      await page.waitForTimeout(500);
      result.step = 'typing_title';
    } else {
      console.log('Title field not found, saving page state...');
      result.step = 'no_title_field';
      result.html_preview = (await page.content()).substring(0, 3000);
    }

    result.success = !url.includes('sign-in');

  } catch (e) {
    result.error = e.message;
    console.error('Error:', e.message);
    try { result.final_url = page.url(); } catch {}
  }

  await context.close();
  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== RESULT ===');
  const r = { ...result };
  delete r.html_preview;
  console.log(JSON.stringify(r, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e.message);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
