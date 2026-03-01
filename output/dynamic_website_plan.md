# Dynamic Website Plan - Partial HTML + Content Sections

**Last Updated**: 2026-02-28 03:20

---

## 🎯 Konsep: Single Page Application (SPA)

### Struktur Files:

**1. Main HTML (Dynamic Loader)**
- File: `index.html` (utama)
- Fitur: 
  - Dynamic content loader
  - Smooth transitions/animations
  - URL hash routing (#portfolio, #pricing, dll)
  - Lazy loading content sections
  - SPA navigation

**2. Content Sections (Partial HTML)**
- Folder: `sections/`
- Files:
  - `home-section.html` - Hero + features
  - `services-section.html` - Services detail
  - `portfolio-section.html` - Portfolio videos
  - `pricing-section.html` - Pricing tables
  - `contact-section.html` - Contact form
  - `footer-section.html` - Footer

**3. JavaScript (Dynamic Core)**
- File: `js/app.js`
- Fitur:
  - Content section loader
  - Route handler (hash-based)
  - Transition animations
  - Lazy loading
  - History management

**4. CSS (Transitions)**
- File: `css/dynamic.css`
- Fitur:
  - Smooth fade transitions
  - Slide animations
  - Page transition effects
  - Loading animations

---

## 🔄 Workflow

### 1. User Opens Website
- `index.html` loads
- JavaScript app.js inisialisasi
- Check URL hash (#home, #portfolio, #pricing, dll)

### 2. Content Loading
- App.js load content section berdasarkan hash
- Contoh: `#portfolio` → load `sections/portfolio-section.html`
- Smooth transition: Fade out → Load content → Fade in

### 3. Navigation
- User klik nav link
- Update URL hash
- Load new content section
- Smooth transition

### 4. Dynamic Updates
- Content sections dapat di-update tanpa reload full page
- JavaScript akan re-load section yang berubah saja
- Smooth transition antar sections

---

## 💡 Keuntungan

**Sebelumnya (Static):**
- Halaman terpisah: index.html, tiktok-agency.html, dll
- Full reload untuk setiap navigasi
- Tidak smooth transitions
- Duplikasi kode (header, footer, nav)

**Sekarang (Dynamic):**
- 1 file HTML utama (SPA)
- Content sections terpisah
- Partial loading (hanya section yang berubah)
- Smooth transitions/animations
- Tidak ada duplikasi kode
- Lebih cepat (hanya load section yang perlu)
- Lebih modern UX

---

## 📁 File Structure

```
berkahkarya-compro/
├── index.html (Dynamic SPA)
├── css/
│   ├── main.css (Core styles)
│   ├── dynamic.css (Transitions)
│   └── animations.css (Animation keyframes)
├── js/
│   ├── app.js (Dynamic loader)
│   └── transitions.js (Transition effects)
├── sections/
│   ├── home-section.html
│   ├── services-section.html
│   ├── portfolio-section.html (TikTok Agency)
│   ├── pricing-section.html
│   ├── contact-section.html
│   └── footer-section.html
└── assets/
    ├── images/
    ├── videos/
    └── fonts/
```

---

## 🎨 Smooth Transitions

### 1. Fade Transition
```css
.fade-out {
  opacity: 0;
  transition: opacity 0.3s ease-out;
}
.fade-in {
  opacity: 0;
  transition: opacity 0.3s ease-in;
}
.fade-in.active {
  opacity: 1;
}
```

### 2. Slide Transition
```css
.slide-out {
  transform: translateX(100%);
  transition: transform 0.4s ease-in-out;
}
.slide-in {
  transform: translateX(-100%);
  transition: transform 0.4s ease-in-out;
}
.slide-in.active {
  transform: translateX(0);
}
```

### 3. Scale Transition
```css
.scale-out {
  transform: scale(0.95);
  opacity: 0;
  transition: all 0.3s ease-out;
}
.scale-in {
  transform: scale(1.05);
  opacity: 0;
  transition: all 0.3s ease-in;
}
.scale-in.active {
  transform: scale(1);
  opacity: 1;
}
```

---

## 🔄 JavaScript Core (app.js)

### Features:

**1. Router (Hash-based):**
```javascript
function router() {
  const hash = window.location.hash || '#home';
  loadSection(hash.replace('#', ''));
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router);
```

**2. Content Loader:**
```javascript
async function loadSection(sectionName) {
  // Fade out current section
  await fadeOutCurrent();
  
  // Load new section
  const content = await fetch(`sections/${sectionName}.html`);
  const html = await content.text();
  
  // Update DOM
  document.getElementById('content').innerHTML = html;
  
  // Fade in new section
  await fadeInNew();
}
```

**3. Smooth Transitions:**
```javascript
function fadeOutCurrent() {
  return new Promise(resolve => {
    const content = document.getElementById('content');
    content.classList.add('fade-out');
    
    setTimeout(() => {
      content.style.display = 'none';
      resolve();
    }, 300);
  });
}

function fadeInNew() {
  return new Promise(resolve => {
    const content = document.getElementById('content');
    content.style.display = 'block';
    
    // Force reflow
    content.offsetHeight;
    
    content.classList.add('fade-in');
    content.classList.add('active');
    
    setTimeout(() => {
      content.classList.remove('fade-in');
      resolve();
    }, 300);
  });
}
```

**4. Lazy Loading:**
```javascript
function lazyLoadSection(sectionName) {
  // Load section only when needed
  const cache = new Map();
  
  if (cache.has(sectionName)) {
    return Promise.resolve(cache.get(sectionName));
  }
  
  return fetch(`sections/${sectionName}.html`)
    .then(response => response.text())
    .then(html => {
      cache.set(sectionName, html);
      return html;
    });
}
```

---

## 📄 Content Sections (Partial HTML)

### 1. home-section.html
```html
<section id="home" class="content-section">
  <div class="container">
    <h1>Berkah Karya</h1>
    <p>Digital Growth Agency</p>
    <!-- Hero content -->
  </div>
</section>
```

### 2. portfolio-section.html (TikTok Agency)
```html
<section id="portfolio" class="content-section">
  <div class="container">
    <h2>Portfolio</h2>
    <div class="portfolio-grid">
      <!-- 3 Sample Videos -->
    </div>
  </div>
</section>
```

### 3. pricing-section.html
```html
<section id="pricing" class="content-section">
  <div class="container">
    <h2>Pricing</h2>
    <div class="pricing-grid">
      <!-- 3 Pricing Tables -->
    </div>
  </div>
</section>
```

---

## 🚀 Implementation Steps

### Phase 1: Create Dynamic Structure
1. Buat `index.html` baru (SPA architecture)
2. Buat `sections/` folder
3. Buat `js/app.js` (dynamic loader)
4. Buat `css/dynamic.css` (transitions)

### Phase 2: Move Content to Sections
1. Pindah Hero + Features ke `sections/home-section.html`
2. Pindah Portfolio ke `sections/portfolio-section.html`
3. Pindah Pricing ke `sections/pricing-section.html`
4. Pindah Contact ke `sections/contact-section.html`
5. Pindah Footer ke `sections/footer-section.html`

### Phase 3: Implement Transitions
1. Tambah fade transition ke `css/dynamic.css`
2. Implement `fadeOutCurrent()` di `js/app.js`
3. Implement `fadeInNew()` di `js/app.js`
4. Test smooth transitions

### Phase 4: Add Advanced Features
1. Lazy loading untuk content sections
2. Caching untuk performa
3. History management (back button support)
4. SEO optimization (meta tags dynamic)

---

## 📊 Comparison: Static vs Dynamic

| Feature | Static | Dynamic (SPA) |
|---------|--------|----------------|
| Files | 7+ HTML files | 1 HTML + sections |
| Duplikasi | High | Low |
| Full reload | Setiap navigasi | Partial (section only) |
| Smooth transitions | Tidak | Ya |
| Load time | Lama | Cepat (lazy loading) |
| UX | Basic | Modern |
| Maintenance | Sulit | Mudah |

---

## 🎯 Next Steps

### Sekarang (Immediate):
1. Buat `index.html` baru (SPA architecture)
2. Buat `sections/` folder
3. Buat `js/app.js` (dynamic loader)
4. Buat `css/dynamic.css` (transitions)

### Lalu (Next Hour):
1. Pindah content ke `sections/` folder
2. Implement router di `js/app.js`
3. Implement smooth transitions
4. Test navigasi

### Terakhir (Next 2 Hours):
1. Add lazy loading
2. Add caching
3. Optimize performa
4. Test all transitions
5. Deploy ke Netlify

---

## 💡 Technical Notes

### SEO Optimization:
```javascript
// Update meta tags based on current section
function updateMetaTags(section) {
  const meta = {
    title: `Berkah Karya - ${section.charAt(0).toUpperCase() + section.slice(1)}`,
    description: getSectionDescription(section)
  };
  
  document.title = meta.title;
  document.querySelector('meta[name="description"]').content = meta.description;
}
```

### History Management:
```javascript
// Support back button
window.addEventListener('popstate', (event) => {
  const section = event.state || 'home';
  loadSection(section);
});

// Save state when navigating
function navigateTo(section) {
  window.history.pushState(section, '', `#${section}`);
  loadSection(section);
}
```

### Performance Optimization:
```javascript
// Lazy load images
function lazyLoadImages() {
  const images = document.querySelectorAll('img[data-src]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.getAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });
  
  images.forEach(img => observer.observe(img));
}
```

---

*Plan Created: 2026-02-28 03:20*
*Status: Ready for implementation*
*Priority: Create dynamic structure → Move content to sections → Implement transitions*
