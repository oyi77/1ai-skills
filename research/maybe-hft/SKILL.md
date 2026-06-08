---
name: maybe-hft
description: Hedging EA dengan sistem trailing stop dan pending order otomatis. Converted
  dari MQL5, cross-platform (Windows/Linux/Mac). Compatible dengan mt5linux Docker.
metadata:
  openclaw:
    emoji: 🛡️
    requires:
      python: true
      pyEnv: trading-venv
  parameters:
    lots:
      type: float
      default: 0.1
      desc: Ukuran lot per transaksi
    stoploss:
      type: int
      default: 1500
      desc: StopLoss dalam point
    trailing:
      type: int
      default: 500
      desc: Jarak trailing dalam point
    trail_start:
      type: int
      default: 1000
      desc: Profit minimal sebelum trailing aktif
    x_distance:
      type: int
      default: 300
      desc: Jarak pending dari SL
    start_direction:
      type: int
      default: 0
      desc: 0=BUY dulu, 1=SELL dulu
      choices:
      - 0
      - 1
    broker:
      type: str
      default: auto
      desc: 'Broker: mt5, simulated, auto'
      choices:
      - mt5
      - simulated
      - auto
    mode:
      type: str
      default: paper
      desc: 'Mode: paper, live'
      choices:
      - paper
      - live
    once:
      type: bool
      default: false
      desc: Jalan sekali aja, tidak loop
domain: research
---

# Maybe HFT Hedging EA

> *"The way to build long-term returns is through preservation of capital and home runs."* — **Paul Tudor Jones**

Expert Advisor cross-platform berbasis Python untuk trading hedging dengan sistem trailing stop dan pending order otomatis.

## Fitur Utama

- **Main Order** — Buka posisi BUY/SELL pertama sesuai konfigurasi
- **Hedging System** — Otomatis buat pending order opposite saat SL kena (locking strategy)
- **Trailing Stop** — Geser SL secara otomatis ketika profit mencapai threshold
- **Cross-Platform** — Jalan di Windows, Linux, Mac (pake mt5linux Docker atau simulated broker)

## Penggunaan

Panduan penggunaan skill ini untuk analisis dan riset.


### Jalankan dari OpenClaw

Setelah skill ter-register, elo bisa panggil dari OpenClaw:

```
# Paper trading dengan parameter default
run maybe-hft --broker mt5 --mode paper

# Custom parameters
run maybe-hft --lots 0.05 --stoploss 1000 --trailing 300 --start-direction 0

# Jalankan sekali aja (testing)
run maybe-hft --once

# Live trading (RISIKO TINGGI!)
run maybe-hft --broker mt5 --mode live --lots 0.01
```

### Jalankan Manual (CLI)

```bash
# Dari folder trading
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading/

# Jalankan dengan parameter default
PYTHONPATH=. ~/.trading-venv/bin/python EA/maybe_hft.py

# Jalankan dengan parameter kustom
PYTHONPATH=. ~/.trading-venv/bin/python EA/maybe_hft.py --lots 0.05 --stoploss 1000 --trailing 300 --start-direction 0
```

### Parameter Command Line

| Parameter | Default | Deskripsi |
|-----------|---------|-----------|
| `--lots` | 0.10 | Lot size per transaksi |
| `--stoploss` | 1500 | StopLoss dalam point |
| `--trailing` | 500 | Jarak trailing dalam point |
| `--trail-start` | 1000 | Minimal profit (point) sebelum trailing aktif |
| `--x-distance` | 300 | Jarak pending dari SL |
| `--slippage` | 30 | Slippage dalam point |
| `--magic` | 12345 | Magic number untuk identifikasi order |
| `--start-direction` | 0 | 0=BUYa dulu, 1=SELL dulu |
| `--symbol` | GC=X | Pair yang ditrading (default: XAUUSD) |
| `--broker` | auto | Broker: mt5, simulated, auto |
| `--mode` | paper | Mode: paper, live |
| `--once` | - | Jalan sekali saja (tidak loop) |

### Mode Broker

- **mt5** — Pakai mt5linux Docker container (`5.189.138.144:18812`)
- **simulated** — Pakai yfinance (paper trading tanpa koneksi MT5)
- **auto** — Coba mt5, fallback ke simulated kalau gagal

### Mode Trading

- **paper** — Simulasi dengan balance virtual (rekomen untuk testing)
- **live** — Trading beneran (pake uang nyata, RISIKO TINGGI!)

### Contoh Penggunaan

### Dari OpenClaw

```
# Paper trading dengan mt5linux
run maybe-hft --broker mt5 --mode paper --lots 0.01 --stoploss 1000

# Paper trading simulated
run maybe-hft --broker simulated --mode paper --once

# Live trading
run maybe-hft --broker mt5 --mode live --lots 0.05 --trailing 300 --start-direction 1
```

### Manual (CLI)

```bash
# Paper trading dengan mt5linux
PYTHONPATH=. ~/.trading-venv/bin/python EA/maybe_hft.py --broker mt5 --mode paper --lots 0.01 --stoploss 1000

# Paper trading simulated (tanpa mt5linux)
PYTHONPATH=. ~/.trading-venv/bin/python EA/maybe_hft.py --broker simulated --mode paper --once

# Live trading dengan parameter custom
PYTHONPATH=. ~/.trading-venv/bin/python EA/maybe_hft.py --broker mt5 --mode live --lots 0.05 --trailing 300 --start-direction 1
```

## Konfigurasi via config.yaml

Bisa juga atur parameter di `config.yaml`:

```yaml
# EA Maybe HFT Configuration
symbol: "GC=X"
lots: 0.10
stoploss: 1500
trailing: 500
trail_start: 1000
x_distance: 300
slippage: 30
magic: 12345
start_direction: 0  # 0=BUYa dulu, 1=SELL dulu
broker: "auto"
mode: "paper"
```

Jalankan dengan konfigurasi:
```bash
PYTHONPATH=. ~/.trading-venv/bin/python EA/maybe_hft.py --config config.yaml
```

## Cara Kerja

Alur kerja dan metodologi yang digunakan.


### 1. Open Main Order
Pada awal (kalau tidak ada posisi), EA buka order utama sesuai `StartDirection`:
- `StartDirection=0` → BUY dulu
- `StartDirection=1` → SELL dulu

### 2. Handle Pending (Hedging)
EA terus memantau posisi utama. Kalau:
- Ada posisi main dan SL sudah ditentukan
- Belum ada pending order untuk hedge
- Maka EA buat **pending order opposite** di jarak `XDistance` dari SL

Contoh:
- BUY di 5200, SL di 5185
- EA buat SELL STOP di 5185 + 300 = 5215
- Kalau SL BUY kena, SELL STOP kepicu dan jadi posisi hedge

### 3. Trailing Orders
EA cek profit posisi:
- BUY: Profit > `TrailStart` point → Geser SL ke `Bid - Trailing`
- SELL: Profit > `TrailStart` point → Geser SL ke `Ask + Trailing`

### 4. Modify Pending
Kalau pending order sudah ada tapi harga berubah, EA otomatis modify agar tetap di posisi optimal.

## Struktur Folder

```
EA/
├── SKILL.md           # Dokumentasi ini
├── maybe_hft.py       # Main EA script
├── config.yaml        # Konfigurasi default
└── requirements.txt   # Dependencies
```

## Integrasi dengan Automated Trader

EA ini juga bisa dipanggil dari `automated_trader.py`:

```bash
# Pakai EA Maybe HFT sebagai strategy
PYTHONPATH=. ~/.trading-venv/bin/python automated_trader.py --strategy maybe_hft --broker mt5 --mode paper --symbol GC=X
```

## Catatan Penting

⚠️ **RISIKO TINGGI!**
- Strategy hedging berisiko tinggi jika tidak dimanage dengan benar
- Selalu testing di paper mode dulu sebelum live trading
- Gunakan lot kecil (0.01-0.05) untuk awal
- Monitor posisi secara berkala

⚙️ **Parameter Tuning:**
- `Stoploss` dan `Trailing` harus disesuaikan dengan volatilitas pair
- `XDistance` menentukan seberapa agresif hedging
- `TrailStart` menentukan kapan trailing mulai aktif

## Dependencies

- `mt5linux` (jika pakai broker mt5)
- `rpyc` (sudah include di mt5linux)
- `PyYAML` (untuk config)
- `argparse` (sudah include di Python stdlib)

## Author

Mas Imam - wa.me/6289679369219

## When NOT to Use

- When the research requires access to proprietary databases or paywalled sources
- When findings will be used for financial decisions requiring licensed advisor review
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Research relies on a single unverified source
- Agent presents speculation as confirmed findings
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Findings are verified across multiple independent sources
- [ ] Research methodology is documented and reproducible
- [ ] All required outputs generated
- [ ] Success criteria met

