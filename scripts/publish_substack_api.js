#!/usr/bin/env node
/**
 * Publish to Substack via undocumented API
 * Uses session cookie from browser profile
 */
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const https = require('https');
const fs = require('fs');

const TEMP_PROFILE = '/tmp/tinker_playwright_profile';
const OUTPUT = '/tmp/substack_result.json';

const TITLE = "10 AI Tools Gratis yang Bisa Gantikan 5 Karyawan di 2026";
const SUBTITLE = "Hemat Rp 34-62 Juta/Bulan dengan AI Tools yang Udah Terbukti Works";

// Convert markdown to Substack's TipTap JSON format
function markdownToSubstackBody(markdown) {
  // Substack uses a specific TipTap HTML format
  const lines = markdown.split('\n');
  let html = '';
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    
    if (trimmed.startsWith('## ')) {
      html += `<h2>${trimmed.substring(3)}</h2>`;
    } else if (trimmed.startsWith('# ')) {
      html += `<h3>${trimmed.substring(2)}</h3>`;
    } else if (trimmed === '---') {
      html += '<hr>';
    } else if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
      html += `<p><strong>${trimmed.slice(2, -2)}</strong></p>`;
    } else if (trimmed.startsWith('👉 ')) {
      // Links with emoji
      const linkMatch = trimmed.match(/👉 \*\*(.+?)\*\*[^(]*\(?(https?:\/\/[^\s)]+)\)?/);
      if (linkMatch) {
        html += `<p>👉 <a href="${linkMatch[2]}"><strong>${linkMatch[1]}</strong></a></p>`;
      } else {
        html += `<p>${trimmed}</p>`;
      }
    } else {
      // Replace markdown bold with HTML
      const formatted = trimmed
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\[(.+?)\]\((https?:\/\/[^\)]+)\)/g, '<a href="$2">$1</a>');
      html += `<p>${formatted}</p>`;
    }
  }
  return html;
}

function apiRequest(method, host, path, data, cookies) {
  return new Promise((resolve, reject) => {
    const body = data ? JSON.stringify(data) : null;
    const options = {
      hostname: host,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Referer': `https://${host}/publish/post/new`,
        'Origin': `https://${host}`,
      }
    };
    if (body) options.headers['Content-Length'] = Buffer.byteLength(body);

    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, data: data }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function run() {
  const result = { success: false, url: null, error: null, logs: [] };
  const log = msg => { console.log(msg); result.logs.push(msg); };

  // Step 1: Get session cookies from browser
  log('Getting session cookies...');
  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });
  
  await context.newPage().then(async p => {
    await p.goto('https://oyi77.substack.com', { timeout: 15000, waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(1000);
  });

  const allCookies = await context.cookies();
  await context.close();

  const substackCookies = allCookies.filter(c => 
    c.domain.includes('substack.com') || c.domain.includes('oyi77.substack.com')
  );
  
  const cookieStr = substackCookies.map(c => `${c.name}=${c.value}`).join('; ');
  log('Cookies: ' + substackCookies.map(c => c.name).join(', '));
  result.cookie_names = substackCookies.map(c => c.name);

  if (!substackCookies.length) {
    result.error = 'No Substack cookies found';
    fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
    return;
  }

  // Step 2: Get publication info
  log('\nGetting publication info...');
  const pubRes = await apiRequest('GET', 'oyi77.substack.com', '/api/v1/publication', null, cookieStr);
  log('Pub status: ' + pubRes.status);
  if (pubRes.status === 200) {
    log('Pub name: ' + pubRes.data?.name);
    result.publication = { id: pubRes.data?.id, name: pubRes.data?.name };
  } else {
    log('Pub response: ' + JSON.stringify(pubRes.data).substring(0, 200));
  }

  // Step 3: Create draft
  log('\nCreating draft...');
  const bodyHtml = markdownToSubstackBody(
    fs.readFileSync('/home/openclaw/.openclaw/workspace/temp/substack-article.md', 'utf8')
  );
  
  const draftData = {
    type: 'newsletter',
    draft_title: TITLE,
    draft_subtitle: SUBTITLE,
    draft_body: bodyHtml,
    audience: 'everyone',
    draft_section_id: null,
  };

  const draftRes = await apiRequest('POST', 'oyi77.substack.com', '/api/v1/drafts', draftData, cookieStr);
  log('Draft status: ' + draftRes.status);
  log('Draft response: ' + JSON.stringify(draftRes.data).substring(0, 300));
  
  if (draftRes.status !== 200 && draftRes.status !== 201) {
    // Try alternative endpoint
    log('Trying alternative draft endpoint...');
    const draftRes2 = await apiRequest('POST', 'substack.com', '/api/v1/drafts', draftData, cookieStr);
    log('Alt draft status: ' + draftRes2.status);
    log('Alt draft response: ' + JSON.stringify(draftRes2.data).substring(0, 300));
  }

  if (draftRes.data?.id) {
    const draftId = draftRes.data.id;
    log('\nDraft created! ID: ' + draftId);
    result.draft_id = draftId;
    result.draft_url = `https://oyi77.substack.com/publish/post/${draftId}`;

    // Step 4: Publish
    log('Publishing...');
    const publishData = {
      send: false, // don't send email blast initially
      share_automatically: false,
      audience: 'everyone',
    };
    
    const publishRes = await apiRequest('POST', 'oyi77.substack.com', 
      `/api/v1/posts/${draftId}/publish`, publishData, cookieStr);
    log('Publish status: ' + publishRes.status);
    log('Publish response: ' + JSON.stringify(publishRes.data).substring(0, 300));

    if (publishRes.status === 200 || publishRes.data?.slug) {
      const slug = publishRes.data?.slug || draftId;
      result.published_url = `https://oyi77.substack.com/p/${slug}`;
      result.success = true;
      result.step = 'published';
      log('\n✅ PUBLISHED: ' + result.published_url);
    } else {
      result.draft_url = `https://oyi77.substack.com/publish/post/${draftId}`;
      result.step = 'draft_created';
      log('\n📝 Draft saved: ' + result.draft_url);
    }
  } else {
    result.error = 'Failed to create draft';
    result.api_response = JSON.stringify(draftRes.data).substring(0, 500);
  }

  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== FINAL RESULT ===');
  console.log(JSON.stringify(result, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e.message);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
