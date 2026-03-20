// Holink Bulk Add Script - Run in browser console at app.holink.com/links
// This script adds all products automatically

const products = [
  { t: '#9 CARLTON Oven LUNA 12L - Rp17RB', u: 'https://s.shopee.co.id/50UIZT8wJ4' },
  { t: '#10 Panci Presto Alumunium - Rp16RB', u: 'https://s.shopee.co.id/8fNawCuysP' },
  { t: '#11 Clarice Ceramic Dinnerware - Rp18RB', u: 'https://s.shopee.co.id/6Kzg9j0KAM' },
  { t: '#12 Rantang Susun Stainless - Rp13RB', u: 'https://s.shopee.co.id/8V4AjkFwnm' },
  { t: '#13 Mug Enamel Jadul - Rp11RB', u: 'https://s.shopee.co.id/6pvwkfAs7C' },
  { t: '#14 Cherie Ceramic Plate - Rp10RB', u: 'https://s.shopee.co.id/5fjzMV2rWI' },
  { t: '#15 Piring Kaca Oval - Rp9RB', u: 'https://s.shopee.co.id/5L78xuGaB4' },
  { t: '#17 Pisau Pengupas Nanas - Rp1RB', u: 'https://s.shopee.co.id/8fNaw0rRQ3' },
  { t: '#18 Amplop Lebaran Isi 50 - Rp4RB', u: 'https://s.shopee.co.id/900RKuiYcf' },
  { t: '#19 Amplop Lebaran Box Premium - Rp3RB', u: 'https://s.shopee.co.id/1gDqbTrs2F' },
  { t: '#20 Amplop Lebaran Premium 50 - Rp3RB', u: 'https://s.shopee.co.id/6Kzg9xak22' },
  { t: '#22 Amplop Lebaran Idul Fitri - Rp3RB', u: 'https://s.shopee.co.id/2Vmxay7IoH' },
  { t: '#23 Sepeda Listrik Kingkong Max - Rp629RB', u: 'https://s.shopee.co.id/2LTXOVCJus' },
  { t: '#24 LEKA Air Purifier AP8000 - Rp159RB', u: 'https://s.shopee.co.id/9fG8805zv8' },
  { t: '#25 LEKA Dehumidifier DH6223 - Rp139RB', u: 'https://s.shopee.co.id/3LM4aNtgox' },
  { t: '#26 Water Heater Listrik 10-30L - Rp103RB', u: 'https://s.shopee.co.id/2qPnzNMpmV' },
  { t: '#27 Paket PLTS Mini 500W - Rp54RB', u: 'https://s.shopee.co.id/4VY1yRGUOf' },
  { t: '#28 Hamra Vacuum Karpet Masjid - Rp2JT', u: 'https://s.shopee.co.id/8fNawBZNzT' },
  { t: '#29 Hiasan Dinding Besi Modern - Rp35RB', u: 'https://s.shopee.co.id/5Anila4lWy' },
  { t: '#30 Hiasan Dinding Walldecor - Rp30RB', u: 'https://s.shopee.co.id/5AnilbHDW5' },
  { t: '#31 Hiasan Dinding Import - Rp24RB', u: 'https://s.shopee.co.id/9zsyWRQuLt' },
  { t: '#32 Tikar Karpet Ruang Tamu - Rp23RB', u: 'https://s.shopee.co.id/4VY1yM7Isu' },
  { t: '#33 NIIMBOT B21Pro Label Printer - Rp64RB', u: 'https://s.shopee.co.id/qejbuDeBr' },
  { t: '#34 NIIMBOT D101 Label Printer - Rp20RB', u: 'https://s.shopee.co.id/4VY1ycGij4' },
  { t: '#35 NIIMBOT B1 Label Printer - Rp20RB', u: 'https://s.shopee.co.id/900RKszabO' },
  { t: '#36 Waffle Mini Maker - Rp7RB', u: 'https://s.shopee.co.id/7poTwfy9Ys' },
  { t: '#37 Stiker Dinding Dapur Aluminium - Rp7RB', u: 'https://s.shopee.co.id/6Kzg9kCm89' },
  { t: '#38 Paket Couple Botol Minum - Rp10RB', u: 'https://s.shopee.co.id/70FMwvcKRX' },
  { t: '#39 Tumbler STARBUCKS - Rp9RB', u: 'https://s.shopee.co.id/4frSAf6fWs' },
  { t: '#40 Tumbler Thermos SUS316 - Rp7RB', u: 'https://s.shopee.co.id/6pvwkccxnV' },
  { t: '#41 Tumbler Termos Change 600ml - Rp6RB', u: 'https://s.shopee.co.id/6fcWYMBVTC' },
  { t: '#42 Tumbler Tifale Ciele - Rp6RB', u: 'https://s.shopee.co.id/2qPnzKbWI8' },
  { t: '#43 Crayon Set Anak 150pc - Rp9RB', u: 'https://s.shopee.co.id/9pZYKONPuy' },
  { t: '#44 Stiker Kartun Shiny 200pcs - Rp7RB', u: 'https://s.shopee.co.id/3LM4aRmA7A' },
  { t: '#45 Free Ongkir Mainan Anak - Rp6RB', u: 'https://s.shopee.co.id/8KkkXdT7xZ' },
  { t: '#46 Kuromi Tempat Pensil - Rp5RB', u: 'https://s.shopee.co.id/2qPnzWo481' },
  { t: '#47 Crayon Colorful 12-48 Warna - Rp5RB', u: 'https://s.shopee.co.id/1Lb0CltmAa' },
  { t: '#48 Rak Sangkar Burung Gold - Rp18RB', u: 'https://s.shopee.co.id/10y9nvKcyn' },
  { t: '#49 Lemari Pakaian Plastik Besar - Rp17RB', u: 'https://s.shopee.co.id/3VfUmUpeY0' },
  { t: '#50 Rak Tempat Aqua Botol - Rp17RB', u: 'https://s.shopee.co.id/1VuQOoxGbw' },
  { t: '#51 Dispenser Kaca Kristal 1.8-4L - Rp14RB', u: 'https://s.shopee.co.id/AACOixpGoX' },
  { t: '#52 IORA Dispenser 5-10 Liter - Rp14RB', u: 'https://s.shopee.co.id/AUpF7Zo09e' },
  { t: '#53 Termos Stainless Double Layer - Rp260RB', u: 'https://s.shopee.co.id/8fNaw3FJSj' },
  { t: '#54 Pom Mini Pertamini Digital - Rp247RB', u: 'https://s.shopee.co.id/7poTwZ3nd7' },
  { t: '#55 Box Parcel Silinder Bulat - Rp17RB', u: 'https://s.shopee.co.id/7KsDLnWvzL' },
  { t: '#56 Hampers Kado Pernikahan - Rp13RB', u: 'https://s.shopee.co.id/40blNSLesw' },
  { t: '#57 Cobek Keramik Sultan - Rp8RB', u: 'https://s.shopee.co.id/4VY1yNJkqy' },
  { t: '#58 Sarung Bantal Anak Cushion - Rp19RB', u: 'https://s.shopee.co.id/2g6Nn1c9d7' },
  { t: '#59 Sprei Kasur Beludru Bulu - Rp13RB', u: 'https://s.shopee.co.id/8ARKL4Xt5N' },
  { t: '#60 Bed Cover Set Valentine - Rp12RB', u: 'https://s.shopee.co.id/7KsDLa8y6F' },
  { t: '#61 Sprei Waterproof Anti Air - Rp10RB', u: 'https://s.shopee.co.id/8ARKL37PaU' },
  { t: '#62 Kursi Lesehan Lipat Sandaran - Rp9RB', u: 'https://s.shopee.co.id/gLJPI0RIj' },
  { t: '#63 Jemuran Baju Tempel Dinding - Rp15RB', u: 'https://s.shopee.co.id/5fjzMV2rVF' },
  { t: '#64 Glimzy Cermin Tempel Dinding - Rp15RB', u: 'https://s.shopee.co.id/4LEbm1mTrH' },
  { t: '#65 Sprei Rumbai Premium 180x200 - Rp11RB', u: 'https://s.shopee.co.id/qejbaznxk' },
  { t: '#66 Unewell Humidifier Ultrasonic - Rp10RB', u: 'https://s.shopee.co.id/2qPnzRW0lO' },
  { t: '#67 UPUPIN Humidifier Diffuser - Rp8RB', u: 'https://s.shopee.co.id/1VuQOzb5TG' }
];

const utm = '?utm_source=griyadalaman&utm_medium=social&utm_campaign=shopee_affiliate_2026';

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function addProduct(title, url) {
  // Click Add button
  const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Add' && !b.disabled);
  if (!addBtn) return false;
  addBtn.click();
  await sleep(400);
  
  // Click Web link in dropdown
  const lis = document.querySelectorAll('li');
  for (const li of lis) {
    if (li.textContent.includes('Web link') && li.textContent.includes('Custom URL')) {
      li.click();
      break;
    }
  }
  await sleep(400);
  
  // Fill empty inputs
  const titles = document.querySelectorAll('input[placeholder="Add your link now"]');
  const urls = document.querySelectorAll('input[placeholder="Please paste your URL website here"]');
  
  for (let i = 0; i < titles.length; i++) {
    if (!titles[i].value || titles[i].value.length < 3) {
      titles[i].value = title;
      titles[i].dispatchEvent(new Event('input', { bubbles: true }));
      if (urls[i]) {
        urls[i].value = url + utm;
        urls[i].dispatchEvent(new Event('input', { bubbles: true }));
      }
      return true;
    }
  }
  return false;
}

async function runBulkAdd() {
  console.log('Starting bulk add...');
  let added = 0;
  
  for (const p of products) {
    const success = await addProduct(p.t, p.u);
    if (success) {
      added++;
      console.log(`Added ${added}: ${p.t}`);
    }
    await sleep(200);
  }
  
  console.log(`Done! Added ${added} products`);
  return added;
}

// Run it
runBulkAdd();
