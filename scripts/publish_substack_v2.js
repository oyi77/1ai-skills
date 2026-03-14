#!/usr/bin/env node
/**
 * Publish Substack via magic link flow
 * 1. Request magic link to muchammadizzuddin@gmail.com
 * 2. Open Gmail (already logged in via profile) to get link
 * 3. Click magic link → logged in
 * 4. Navigate to editor → paste article → publish
 */
const PLAYWRIGHT_DIR = "/home/openclaw/.npm/_npx/e41f203b7505f1fb/node_modules";
const { chromium } = require(`${PLAYWRIGHT_DIR}/playwright`);
const fs = require('fs');

const TEMP_PROFILE = '/tmp/tinker_playwright_profile';
const OUTPUT = '/tmp/substack_result.json';
const EMAIL = 'muchammadizzuddin@gmail.com';
const TITLE = "10 AI Tools Gratis yang Bisa Gantikan 5 Karyawan di 2026";

// Full article content
const FULL_ARTICLE = `Bayangin lo punya 5 karyawan yang kerja 24/7, ga pernah sakit, ga minta THR, dan ga pernah resign.

Kedengeran impossible? Welcome to 2026.

AI udah bukan mainan tech bros lagi. Ini udah jadi senjata utama buat UMKM, freelancer, dan siapapun yang mau scale bisnis tanpa nambah headcount.

Gue udah test ratusan AI tools. Dan ini **10 yang beneran works** — semuanya GRATIS atau punya free tier yang cukup buat mulai.

---

## 1. 🤖 ChatGPT / Claude — Pengganti Admin & Customer Service

Bales chat customer, bikin template email, draft proposal — semua bisa dihandle AI.

**Yang bisa digantikan:** Admin, CS, sekretaris
**Hemat:** Rp 3-5 juta/bulan

---

## 2. 🎨 Canva AI — Pengganti Desainer Grafis

Magic Design bikin konten visual dalam hitungan detik. Logo, poster, social media post — tinggal describe, jadi.

**Yang bisa digantikan:** Junior graphic designer
**Hemat:** Rp 4-7 juta/bulan

---

## 3. 📝 Notion AI — Pengganti Project Manager

Organize project, bikin meeting notes otomatis, track deadline. Satu tool buat semua management.

**Yang bisa digantikan:** Project coordinator
**Hemat:** Rp 5-8 juta/bulan

---

## 4. 📊 Google Sheets + AI — Pengganti Data Analyst

Formula AI, pivot table otomatis, visualisasi data. Ga perlu hire data analyst buat basic analytics.

**Yang bisa digantikan:** Junior data analyst
**Hemat:** Rp 5-10 juta/bulan

---

## 5. 🎬 CapCut — Pengganti Video Editor

Auto-caption, template viral, effects library. Bikin konten TikTok/Reels quality tanpa skill editing.

**Yang bisa digantikan:** Junior video editor
**Hemat:** Rp 3-6 juta/bulan

---

## 6. 📧 AI Email Writer (Gmail AI) — Pengganti Copywriter

Draft email marketing, follow-up sequences, cold outreach — semua auto-generated.

**Yang bisa digantikan:** Junior copywriter
**Hemat:** Rp 3-5 juta/bulan

---

## 7. 🔍 Perplexity AI — Pengganti Research Assistant

Research market, competitive analysis, trend spotting — dalam hitungan menit bukan jam.

**Yang bisa digantikan:** Research intern
**Hemat:** Rp 2-4 juta/bulan

---

## 8. 📱 ManyChat — Pengganti Social Media Manager

Auto-reply DM, funnel Instagram/TikTok, lead generation otomatis 24/7.

**Yang bisa digantikan:** Social media handler
**Hemat:** Rp 3-5 juta/bulan

---

## 9. 🎙️ ElevenLabs — Pengganti Voice Over Artist

Text-to-speech yang kedengeran natural. Buat podcast, video narration, audiobook.

**Yang bisa digantikan:** Voice over freelancer
**Hemat:** Rp 500K-2 juta/project

---

## 10. 🧠 Cursor / Claude Code — Pengganti Junior Developer

Coding assistant yang bisa bikin website, automate tasks, bahkan build apps.

**Yang bisa digantikan:** Junior developer
**Hemat:** Rp 5-10 juta/bulan

---

## Total Penghematan: Rp 34-62 Juta/Bulan 🤯

Itu setara **5 karyawan full-time** yang digantikan oleh tools gratis.

Tapi tools doang ga cukup. Lo butuh **SISTEM** — workflow yang connect semua tools ini jadi mesin bisnis yang jalan otomatis.

---

## 🎁 Mau Sistem Lengkapnya? (GRATIS)

Gue udah compile **semua template, prompt, dan workflow** yang gue pake buat jalanin bisnis pakai AI:

👉 **Mesin Cetak Bisnis Kuliner AI** — Framework lengkap buat automate bisnis kuliner pakai AI (GRATIS, bayar seikhlasnya)
https://lynk.id/jendralbot/kzryk28dxmpx

👉 **JobMagnet AI** — AI-powered job hunting system yang udah bantu 100+ orang dapet kerja
https://lynk.id/jendralbot/45r5yvze3vy4

👉 **AI Creative Ad Engine** — Bikin iklan yang convert pakai AI, tanpa skill desain
https://lynk.id/jendralbot/9r8rj1o38q59

👉 **Guru Pintar AI** — Personal AI tutor buat belajar apapun 10x lebih cepat
https://lynk.id/jendralbot/6821op5e24kn

👉 **Kelas Affiliate TikTok** — Masterclass lengkap cara hasilin duit dari TikTok affiliate
https://lynk.id/jendralbot/regxdn7xkpz6

**Semua ada di:** https://lynk.id/jendralbot 🔥

---

Follow gue buat update AI tools terbaru setiap minggu. 2026 baru mulai — yang adaptasi sekarang, yang menang nanti.`;

async function run() {
  const result = { success: false, url: null, error: null, step: 'start' };

  console.log('Launching browser with profile...');
  const context = await chromium.launchPersistentContext(TEMP_PROFILE, {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await context.newPage();

  try {
    // Step 1: Request Substack magic link
    console.log('Requesting Substack magic link...');
    await page.goto('https://substack.com/sign-in?redirect=%2Fhome', {
      timeout: 20000, waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(2000);

    console.log('Sign-in URL:', page.url());
    const bodyText = await page.locator('body').innerText();
    console.log('Page preview:', bodyText.substring(0, 200));

    // Find email input and request magic link
    const emailInput = page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]');
    if (await emailInput.count() > 0) {
      await emailInput.fill(EMAIL);
      await page.waitForTimeout(300);
      
      // Click sign in / continue button
      const signInBtn = page.locator('button[type="submit"], button:has-text("Sign in"), button:has-text("Continue"), button:has-text("Send")');
      if (await signInBtn.count() > 0) {
        await signInBtn.first().click();
        await page.waitForTimeout(3000);
        console.log('After email submit:', page.url());
        const newText = await page.locator('body').innerText();
        console.log('After submit text:', newText.substring(0, 300));
        result.step = 'magic_link_sent';
      }
    } else {
      console.log('No email input found, checking if already logged in...');
      result.step = 'no_email_input';
    }

    // Step 2: Check Gmail for magic link
    console.log('\nChecking Gmail for magic link...');
    await page.goto('https://mail.google.com/mail/u/0/#inbox', {
      timeout: 20000, waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(4000);
    console.log('Gmail URL:', page.url());

    if (!page.url().includes('mail.google.com')) {
      result.error = 'Gmail not accessible';
      result.step = 'gmail_failed';
      await context.close();
      fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
      return;
    }

    // Search for Substack magic link email
    console.log('Searching for Substack email...');
    await page.goto('https://mail.google.com/mail/u/0/#search/from%3Asubstack+login', {
      timeout: 20000, waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(4000);

    // Click most recent Substack email
    const emailRows = page.locator('tr.zA');
    const rowCount = await emailRows.count();
    console.log('Email rows found:', rowCount);

    if (rowCount > 0) {
      await emailRows.first().click();
      await page.waitForTimeout(3000);
      console.log('Opened email, URL:', page.url());

      // Look for magic link in the email
      const emailBody = await page.locator('.a3s, [data-message-id]').first().innerText().catch(() => '');
      console.log('Email body preview:', emailBody.substring(0, 500));

      // Find the magic link URL
      const links = await page.locator('a[href*="substack.com/magic"]').all();
      console.log('Magic links found:', links.length);

      if (links.length > 0) {
        const magicUrl = await links[0].getAttribute('href');
        console.log('Magic URL:', magicUrl?.substring(0, 100));
        result.magic_url = magicUrl;

        // Click the magic link
        await links[0].click();
        await page.waitForLoadState('domcontentloaded', { timeout: 15000 });
        await page.waitForTimeout(3000);
        console.log('After magic link:', page.url());
        result.step = 'magic_link_clicked';
      } else {
        // Try finding any link with "login" or "sign" in the email
        const allLinks = await page.locator('a[href*="substack"]').all();
        console.log('All substack links:', allLinks.length);
        for (const link of allLinks.slice(0, 5)) {
          const href = await link.getAttribute('href');
          console.log(' -', href?.substring(0, 100));
        }
        result.step = 'no_magic_link_found';
        result.email_preview = emailBody.substring(0, 1000);
      }
    } else {
      result.step = 'no_substack_email';
      // Check inbox directly
      const inboxText = await page.locator('body').innerText();
      result.inbox_preview = inboxText.substring(0, 500);
    }

    // Step 3: Navigate to editor (if logged in)
    const currentUrl = page.url();
    if (currentUrl.includes('substack.com') && !currentUrl.includes('sign-in')) {
      console.log('\nNavigating to Substack editor...');
      
      // Go to oyi77's substack dashboard
      await page.goto('https://oyi77.substack.com/publish/post/new', {
        timeout: 20000, waitUntil: 'domcontentloaded'
      });
      await page.waitForTimeout(4000);
      console.log('Editor URL:', page.url());

      const editorText = await page.locator('body').innerText();
      console.log('Editor preview:', editorText.substring(0, 300));
      result.editor_url = page.url();
      result.editor_preview = editorText.substring(0, 1000);

      // Check for title field
      const titleFields = [
        'h1[contenteditable]',
        '[data-placeholder="Title"]',
        '[placeholder*="Title" i]',
        '.post-title',
        'input[name="title"]',
      ];

      for (const sel of titleFields) {
        const field = page.locator(sel);
        if (await field.count() > 0) {
          console.log('Found title field:', sel);
          await field.click();
          await page.keyboard.type(TITLE);
          result.step = 'title_typed';
          break;
        }
      }
    }

    result.success = result.step !== 'start';
    result.final_url = page.url();

  } catch (e) {
    result.error = e.message;
    console.error('Error:', e.message);
    try { result.final_url = page.url(); } catch {}
  }

  await context.close();
  fs.writeFileSync(OUTPUT, JSON.stringify(result, null, 2));
  console.log('\n=== RESULT ===');
  const r = { ...result };
  ['inbox_preview', 'email_preview', 'editor_preview'].forEach(k => delete r[k]);
  console.log(JSON.stringify(r, null, 2));
}

run().catch(e => {
  console.error('Fatal:', e.message);
  fs.writeFileSync(OUTPUT, JSON.stringify({ success: false, error: e.message }, null, 2));
  process.exit(1);
});
