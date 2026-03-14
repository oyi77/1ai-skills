#!/usr/bin/env node
/**
 * Tinker onboarding using Vivaldi profile directly
 * Uses persistent context with existing user data
 */

const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');
const path = require('path');

const OUTPUT = '/tmp/tinker_result.json';
const VIVALDI_PROFILE = '/home/openclaw/.openclaw/browser/openclaw/user-data';
const TEMP_PROFILE = '/tmp/tinker_playwright_profile';

async function run() {
  const result = { success: false, api_key: null, error: null, step: 'start' };

  // Copy Vivaldi profile to temp dir (can't use live profile directly)
  console.log('Copying browser profile...');
  try {
    if (fs.existsSync(TEMP_PROFILE)) {
      fs.rmSync(TEMP_PROFILE, { recursive: true });
    }
    // Only copy Default folder (has cookies, local storage)
    fs.mkdirSync(TEMP_PROFILE, { recursive: true });
    fs.mkdirSync(`${TEMP_PROFILE}/Default`, { recursive: true });
    
    // Copy key files
    const files = ['Cookies', 'Local Storage', 'Session Storage', 'Local State'];
    for (const f of files) {
      const src = `${VIVALDI_PROFILE}/Default/${f}`;
      const dst = `${TEMP_PROFILE}/Default/${f}`;
      if (fs.existsSync(src)) {
        const stat = fs.statSync(src);
        if (stat.isDirectory()) {
          fs.cpSync(src, dst, { recursive: true });
        } else {
          fs.copyFileSync(src, dst);
        }
        console.log(`Copied: ${f}`);
      }
    }
    // Copy Local State (needed for Chrome Safe Storage)
    const localState = `${VIVALDI_PROFILE}/Local State`;
    if (fs.existsSync(localState)) {
      fs.copyFileSync(localState, `${TEMP_PROFILE}/Local State`);
      console.log('Copied: Local State');
    }
  } catch (e) {
    console.log('Profile copy error:', e.message);
  }

  console.log('Launching Chromium with profile...');
  
  let browser;
  try {
    // Try persistent context with copied profile
    const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
      ignoreHTTPSErrors: true,
    });

    const page = await context.newPage();
    result.step = 'browser_ready';

    console.log('Navigating to Tinker /onboarding...');
    await page.goto('https://tinker-console.thinkingmachines.ai/keys', { 
      timeout: 20000,
      waitUntil: 'domcontentloaded'
    });
    
    // Wait a bit for JS to run
    await page.waitForTimeout(3000);
    
    let url = page.url();
    console.log(`URL: ${url}`);
    result.step = `at: ${url}`;

    // Handle each state
    if (url.includes('sign') || url.includes('auth.thinkingmachines')) {
      console.log('On sign-in page, trying Google OAuth...');
      
      // Click "Continue with Google"  
      const googleBtn = page.locator('a:has-text("Continue with Google"), button:has-text("Continue with Google")');
      if (await googleBtn.count() > 0) {
        await googleBtn.click();
        await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
        await page.waitForTimeout(2000);
        url = page.url();
        console.log(`After Google click: ${url}`);
        
        if (url.includes('accounts.google.com')) {
          // Account chooser
          const accountEl = page.locator('[data-email="muchammadizzuddin@gmail.com"], li:has-text("muchammadizzuddin@gmail.com")');
          if (await accountEl.count() > 0) {
            console.log('Clicking account in chooser...');
            await accountEl.click();
          } else {
            // Try link with email text
            const emailLink = page.locator(`a:has-text("muchammadizzuddin"), [data-identifier="muchammadizzuddin@gmail.com"]`);
            if (await emailLink.count() > 0) {
              await emailLink.click();
            } else {
              console.log('Account not found in chooser, checking page...');
              const html = await page.content();
              const emailPos = html.indexOf('muchammadizzuddin');
              console.log('Email in page:', emailPos !== -1 ? 'YES at pos ' + emailPos : 'NO');
              
              if (emailPos !== -1) {
                // Try clicking nearby element
                await page.locator('text=muchammadizzuddin').first().click();
              }
            }
          }
          
          await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
          await page.waitForTimeout(2000);
          url = page.url();
          console.log(`After account select: ${url}`);
          
          // Consent screen
          if (url.includes('consent') || url.includes('oauth/id')) {
            const continueBtn = page.locator('button:has-text("Continue")');
            if (await continueBtn.count() > 0) {
              await continueBtn.click();
              await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
              await page.waitForTimeout(2000);
              url = page.url();
              console.log(`After consent: ${url}`);
            }
          }
        }
      }
    }

    // On sign-up/onboarding?
    url = page.url();
    if (url.includes('onboarding') || url.includes('sign-up')) {
      console.log('On onboarding/signup page...');
      result.step = 'onboarding';
      
      await page.waitForTimeout(1000);
      
      // Check ToS - use JS click to bypass custom component overlay
      const checked = await page.evaluate(() => {
        // Find checkbox and check its state
        const cb = document.querySelector('input[name="tos"], input[type="checkbox"]');
        return cb ? cb.checked : false;
      });
      console.log('ToS checked:', checked);
      
      if (!checked) {
        // Use JS to click the label/wrapper div (bypasses pointer-events intercept)
        const clicked = await page.evaluate(() => {
          // Try label first
          const label = document.querySelector('label[for], button[role="checkbox"], [data-state]');
          if (label) { label.click(); return 'label'; }
          // Try clicking near the checkbox
          const cb = document.querySelector('input[name="tos"], input[type="checkbox"]');
          if (cb) {
            cb.checked = true;
            cb.dispatchEvent(new Event('change', { bubbles: true }));
            cb.dispatchEvent(new Event('input', { bubbles: true }));
            cb.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            return 'direct';
          }
          return 'not found';
        });
        console.log('ToS click method:', clicked);
        await page.waitForTimeout(1000);
        
        // Verify
        const nowChecked = await page.evaluate(() => {
          const cb = document.querySelector('input[name="tos"], input[type="checkbox"]');
          return cb ? cb.checked : false;
        });
        console.log('ToS now checked:', nowChecked);
      }
      
      // Wait for Continue button to be enabled
      await page.waitForTimeout(500);
      
      // Click Continue - try multiple approaches
      const allBtns = await page.locator('button').allTextContents();
      console.log('All buttons:', allBtns);
      
      const btn = page.locator('button:has-text("Continue")');
      if (await btn.count() > 0) {
        console.log('Clicking Continue on onboarding...');
        // Force click via JS to bypass any overlays
        await page.evaluate(() => {
          const btn = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Continue'));
          if (btn) btn.click();
        });
        await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
        await page.waitForTimeout(3000);
        url = page.url();
        console.log(`After onboarding submit: ${url}`);
      } else {
        console.log('Continue button not found');
      }
    }

    // Navigate to keys
    url = page.url();
    if (!url.includes('keys') && !url.includes('auth') && !url.includes('sign')) {
      console.log('Navigating to /keys...');
      await page.goto('https://tinker-console.thinkingmachines.ai/keys', {
        timeout: 20000,
        waitUntil: 'domcontentloaded'
      });
      await page.waitForTimeout(3000);
      url = page.url();
      console.log(`Keys page URL: ${url}`);
    }

    result.final_url = url;
    result.page_title = await page.title();
    const content = await page.content();
    result.page_preview = content.substring(0, 3000);

    // Extract API keys
    const keyPatterns = [
      /tm_[a-zA-Z0-9_\-]{20,}/g,
      /sk-[a-zA-Z0-9_\-]{20,}/g,
    ];
    
    for (const pattern of keyPatterns) {
      const matches = content.match(pattern);
      if (matches) {
        result.api_key = matches[0];
        console.log(`FOUND KEY: ${matches[0].substring(0, 25)}...`);
        result.success = true;
        break;
      }
    }

    // Check for "Create" / "Generate" button on keys page
    if (!result.api_key && url.includes('keys')) {
      console.log('Looking for create key button...');
      const createSelectors = [
        'button:has-text("Create")', 
        'button:has-text("Generate")',
        'button:has-text("New API")',
        'button:has-text("Add")',
        'button[class*="primary"]'
      ];
      
      for (const sel of createSelectors) {
        const btn = page.locator(sel);
        if (await btn.count() > 0) {
          console.log(`Clicking: ${sel}`);
          await btn.first().click();
          await page.waitForTimeout(3000);
          
          const newContent = await page.content();
          for (const pattern of keyPatterns) {
            const matches = newContent.match(pattern);
            if (matches) {
              result.api_key = matches[0];
              result.success = true;
              console.log(`KEY AFTER CREATE: ${matches[0].substring(0, 25)}...`);
              break;
            }
          }
          
          // Check modal/dialog for key
          const modalText = await page.locator('[role="dialog"], [class*="modal"], [class*="dialog"]').allTextContents();
          console.log('Modal text:', modalText.slice(0, 3));
          result.modal_text = modalText.slice(0, 3);
          break;
        }
      }
    }

    // Get all visible text on keys page
    if (url.includes('keys')) {
      const visibleText = await page.locator('body').innerText();
      result.visible_text = visibleText.substring(0, 2000);
      console.log('Page text:', visibleText.substring(0, 500));
    }

    await context.close();

  } catch (e) {
    result.error = e.message;
    console.error('Error:', e.message);
    if (browser) await browser.close().catch(() => {});
  }

  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== RESULT ===');
  const r = { ...result };
  delete r.page_preview;
  delete r.visible_text;
  console.log(JSON.stringify(r, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e.message);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
