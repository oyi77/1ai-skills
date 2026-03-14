#!/usr/bin/env node
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const OUTPUT = '/tmp/tinker_result.json';
const TEMP_PROFILE = '/tmp/tinker_playwright_profile';

async function run() {
  const result = { success: false, api_key: null, error: null, step: 'start' };

  console.log('Launching Chromium with Vivaldi profile...');
  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await context.newPage();

  try {
    await page.goto('https://tinker-console.thinkingmachines.ai/onboarding', {
      timeout: 20000, waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(3000);

    const url = page.url();
    console.log('URL:', url);

    if (url.includes('onboarding')) {
      console.log('On onboarding page...');
      result.step = 'onboarding';

      // Click the Radix UI checkbox button
      const tosBtn = page.locator('button[role="checkbox"]');
      const tosBtnCount = await tosBtn.count();
      console.log('ToS button[role=checkbox] count:', tosBtnCount);

      if (tosBtnCount > 0) {
        const dataState = await tosBtn.getAttribute('data-state');
        console.log('ToS data-state:', dataState);

        if (dataState !== 'checked') {
          await tosBtn.click();
          await page.waitForTimeout(500);
          const newState = await tosBtn.getAttribute('data-state');
          console.log('ToS new data-state:', newState);
        }
      }

      // Wait for Continue button to be enabled
      await page.waitForTimeout(300);
      
      const continueBtn = page.locator('button[type="submit"]:has-text("Continue"), button:has-text("Continue")');
      const continueBtnDisabled = await continueBtn.getAttribute('disabled');
      console.log('Continue disabled:', continueBtnDisabled);

      if (continueBtnDisabled === null) {
        // Not disabled, click it
        console.log('Clicking Continue...');
        await continueBtn.click();
        await page.waitForLoadState('domcontentloaded', { timeout: 20000 });
        await page.waitForTimeout(4000);
        console.log('After onboarding:', page.url());
      } else {
        // Force JS submit
        console.log('Button still disabled, trying JS submit...');
        await page.evaluate(() => {
          const form = document.querySelector('form');
          if (form) {
            const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
            form.dispatchEvent(submitEvent);
          }
          // Also try clicking the button directly via JS
          const btn = document.querySelector('button[type="submit"]');
          if (btn) {
            btn.removeAttribute('disabled');
            btn.click();
          }
        });
        await page.waitForLoadState('domcontentloaded', { timeout: 20000 });
        await page.waitForTimeout(4000);
        console.log('After JS submit:', page.url());
      }
    }

    // Navigate to keys page
    const currentUrl = page.url();
    if (!currentUrl.includes('keys')) {
      await page.goto('https://tinker-console.thinkingmachines.ai/keys', {
        timeout: 20000, waitUntil: 'domcontentloaded'
      });
      await page.waitForTimeout(4000);
    }

    const finalUrl = page.url();
    console.log('Final URL:', finalUrl);
    result.final_url = finalUrl;
    result.page_title = await page.title();

    if (finalUrl.includes('keys')) {
      result.step = 'keys_page';
      const content = await page.content();
      const text = await page.locator('body').innerText();
      result.visible_text = text.substring(0, 3000);
      console.log('=== PAGE TEXT ===');
      console.log(text.substring(0, 1000));

      // Look for API keys
      const keyPatterns = [
        /tm_[a-zA-Z0-9_\-]{20,}/g,
        /sk-[a-zA-Z0-9_\-]{20,}/g,
      ];
      for (const p of keyPatterns) {
        const m = content.match(p);
        if (m) { result.api_key = m[0]; result.success = true; break; }
      }

      // Try creating a key if none found
      if (!result.api_key) {
        console.log('No key visible, looking for create button...');
        const createBtns = [
          'button:has-text("Create API Key")',
          'button:has-text("Create")',
          'button:has-text("Generate")',
          'button:has-text("New")',
          'button:has-text("Add")',
        ];
        for (const sel of createBtns) {
          const btn = page.locator(sel);
          if (await btn.count() > 0) {
            console.log('Clicking:', sel);
            await btn.first().click();
            await page.waitForTimeout(3000);

            const newContent = await page.content();
            const newText = await page.locator('body').innerText();
            console.log('After create:', newText.substring(0, 500));
            result.after_create_text = newText.substring(0, 2000);

            for (const p of keyPatterns) {
              const m = newContent.match(p);
              if (m) { result.api_key = m[0]; result.success = true; break; }
            }
            
            // Check modal
            const modalText = await page.locator('[role="dialog"]').allTextContents();
            if (modalText.length > 0) {
              console.log('Modal:', modalText);
              result.modal = modalText;
              // Grab key from modal
              for (const p of keyPatterns) {
                for (const t of modalText) {
                  const m = t.match(p);
                  if (m) { result.api_key = m[0]; result.success = true; break; }
                }
              }
            }
            break;
          }
        }
      }
    }

  } catch (e) {
    result.error = e.message;
    console.error('Error:', e.message);
    try { result.final_url = page.url(); } catch {}
  }

  await context.close();
  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== FINAL RESULT ===');
  const r = { ...result };
  delete r.visible_text;
  delete r.after_create_text;
  console.log(JSON.stringify(r, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e.message);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
