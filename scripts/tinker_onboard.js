#!/usr/bin/env node
/**
 * Tinker onboarding via Playwright Node.js
 * Complete onboarding and extract API key
 */

const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const OUTPUT = '/tmp/tinker_result.json';

async function run() {
  const result = { success: false, api_key: null, error: null, step: 'start' };

  console.log('Launching headless Chromium...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();
  result.step = 'browser_ready';

  try {
    console.log('Navigating to Tinker /keys...');
    await page.goto('https://tinker-console.thinkingmachines.ai/keys', { timeout: 15000 });
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    
    let url = page.url();
    console.log(`Current URL: ${url}`);
    result.step = `navigated: ${url}`;

    // Need to auth?
    if (url.includes('auth.thinkingmachines.ai') || url.includes('sign')) {
      console.log('Need to auth, trying Google OAuth...');
      result.step = 'need_auth';

      // Trigger Google OAuth
      const oauthUrl = 'https://auth.thinkingmachines.ai/api/login?provider=GoogleOAuth' +
        '&redirect_uri=https%3A%2F%2Ftinker-console.thinkingmachines.ai%2Fcallback' +
        '&client_id=client_01JT41MFTDNYP0RYJ9MF318GDF&source=signin';
      
      await page.goto(oauthUrl, { timeout: 15000 });
      await page.waitForLoadState('networkidle', { timeout: 10000 });
      url = page.url();
      console.log(`OAuth redirect: ${url}`);

      if (url.includes('accounts.google.com')) {
        // Try to use existing account
        const accountLink = page.locator('text=muchammadizzuddin@gmail.com');
        const accountCount = await accountLink.count();
        
        if (accountCount > 0) {
          console.log('Found account in chooser, clicking...');
          await accountLink.click();
          await page.waitForLoadState('networkidle', { timeout: 15000 });
        } else {
          // Type email
          console.log('Typing email...');
          await page.fill('input[type="email"]', 'muchammadizzuddin@gmail.com');
          await page.click('button:has-text("Next"), #identifierNext');
          await page.waitForLoadState('networkidle', { timeout: 10000 });
          
          url = page.url();
          console.log(`After email: ${url}`);
          
          // Check if password needed
          const pwInput = page.locator('input[type="password"]');
          if (await pwInput.count() > 0) {
            result.error = 'NEED_GOOGLE_PASSWORD';
            result.step = 'blocked_need_password';
            console.log('BLOCKED: Google password required');
            await browser.close();
            fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
            return;
          }
        }
        
        // Google consent screen?
        url = page.url();
        console.log(`After Google: ${url}`);
        const continueBtn = page.locator('button:has-text("Continue")');
        if (await continueBtn.count() > 0) {
          await continueBtn.click();
          await page.waitForLoadState('networkidle', { timeout: 15000 });
        }
      }
    }

    url = page.url();
    console.log(`After auth: ${url}`);

    // Onboarding?
    if (url.includes('onboarding')) {
      console.log('On onboarding, completing...');
      result.step = 'onboarding';
      
      // Check ToS
      const checkbox = page.locator('input[type="checkbox"]');
      if (await checkbox.count() > 0) {
        const isChecked = await checkbox.isChecked();
        if (!isChecked) {
          await checkbox.check();
          console.log('ToS accepted');
        }
      }
      
      // Click Continue
      const btn = page.locator('button:has-text("Continue")');
      if (await btn.count() > 0 && await btn.isEnabled()) {
        await btn.click();
        await page.waitForLoadState('networkidle', { timeout: 15000 });
        console.log(`After onboarding: ${page.url()}`);
      }
    }

    url = page.url();
    console.log(`Final URL: ${url}`);

    // Navigate to keys if not there yet
    if (!url.includes('keys')) {
      await page.goto('https://tinker-console.thinkingmachines.ai/keys', { timeout: 15000 });
      await page.waitForLoadState('networkidle', { timeout: 10000 });
      url = page.url();
      console.log(`Keys URL: ${url}`);
    }

    // Extract API key from page
    const content = await page.content();
    result.final_url = url;
    result.page_title = await page.title();
    
    // Look for API key patterns (Tinker keys usually start with "tm_")
    const keyPatterns = [
      /tm_[a-zA-Z0-9_-]{20,}/g,
      /sk-[a-zA-Z0-9_-]{20,}/g,
      /"key":\s*"([^"]{20,})"/g,
      /"api_key":\s*"([^"]{20,})"/g,
    ];
    
    for (const pattern of keyPatterns) {
      const matches = content.match(pattern);
      if (matches && matches.length > 0) {
        result.api_key = matches[0];
        console.log(`Found API key: ${result.api_key.substring(0, 20)}...`);
        break;
      }
    }

    // Try clicking "Create" or "Generate" key button if no key found
    if (!result.api_key) {
      const createBtn = page.locator('button:has-text("Create"), button:has-text("Generate"), button:has-text("New"), button:has-text("+ ")');
      if (await createBtn.count() > 0) {
        console.log('Clicking create key button...');
        await createBtn.first().click();
        await page.waitForLoadState('networkidle', { timeout: 10000 });
        
        // Get new content
        const newContent = await page.content();
        for (const pattern of keyPatterns) {
          const matches = newContent.match(pattern);
          if (matches && matches.length > 0) {
            result.api_key = matches[0];
            console.log(`Found API key after create: ${result.api_key.substring(0, 20)}...`);
            break;
          }
        }
        
        // Also check text visible on page
        const keyText = await page.locator('[class*="key"], [class*="token"], [class*="api"]').allTextContents();
        console.log('Key elements text:', keyText.slice(0, 5));
        result.key_elements = keyText.slice(0, 5);
      }
    }

    result.success = !url.includes('auth') && !url.includes('sign');
    result.page_preview = content.substring(0, 3000);

  } catch (e) {
    result.error = e.message;
    console.error('Error:', e.message);
    try {
      result.final_url = page.url();
      result.page_preview = (await page.content()).substring(0, 2000);
    } catch {}
  }

  await browser.close();
  
  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== RESULT ===');
  console.log(JSON.stringify(result, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
