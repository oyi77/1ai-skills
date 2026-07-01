#!/usr/bin/env node
/**
 * Postinstall: check if a newer version of 1ai-skills is available.
 * Runs silently — prints only if an update exists. Never blocks or errors.
 */

const https = require("https");
const path = require("path");

const PKG_PATH = path.join(__dirname, "..", "package.json");
let pkg;
try {
  pkg = require(PKG_PATH);
} catch {
  process.exit(0);
}

const CURRENT = pkg.version;
const NAME = pkg.name;

function fetch(url) {
  return new Promise((resolve) => {
    https
      .get(url, { headers: { "User-Agent": `${NAME}/${CURRENT}` } }, (res) => {
        if (res.statusCode === 301 || res.statusCode === 302) {
          return fetch(res.headers.location).then(resolve);
        }
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => resolve(data));
        res.on("error", () => resolve(null));
      })
      .on("error", () => resolve(null));
  });
}

function cmp(a, b) {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    if (pa[i] > pb[i]) return 1;
    if (pa[i] < pb[i]) return -1;
  }
  return 0;
}

(async () => {
  try {
    const data = await fetch(`https://registry.npmjs.org/${NAME}/latest`);
    if (!data) return;
    const latest = JSON.parse(data).version;
    if (cmp(latest, CURRENT) > 0) {
      console.log(`\n  📦 1ai-skills v${latest} available (installed: v${CURRENT})`);
      console.log(`     Run: npm install -g ${NAME}@latest\n`);
    }
  } catch {
    // Silent — never break install
  }
})();
