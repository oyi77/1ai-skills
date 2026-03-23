# NotebookLM Automation

> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

**Automate Google NotebookLM for content research, podcast generation, and study materials.**

---

## Description

Automate Google NotebookLM — create notebooks, import sources (URL/YouTube/PDF/text), generate Audio Overview (podcast MP3), Video overview, Slide decks (PPTX), Infographics, Quizzes, Mind maps, Reports. Download all artifacts locally.

## Use Cases (BerkahKarya)

- **Content Research**: Import competitor URLs and YouTube channels, generate summarized reports
- **Podcast Generation**: Turn blog posts / articles into podcast-style audio overviews
- **Trading Education**: Import trading strategy docs, generate quizzes and mind maps
- **Competitor Analysis**: Feed competitor landing pages, get structured analysis
- **Course Material**: Import PDFs/articles, generate slide decks and study guides

---

## Setup

### 1. Install

```bash
pip install notebooklm-py
```

### 2. Authentication

NotebookLM requires Google cookies for auth. Export cookies from your browser:

1. Log into NotebookLM (notebooklm.google.com) in your browser
2. Use a cookie export extension to get cookies
3. Set environment variable:

```bash
export NOTEBOOKLM_COOKIES='<your_cookies_json>'
# OR save to file:
export NOTEBOOKLM_COOKIES_FILE=~/.notebooklm_cookies.json
```

If auth fails, the script will print setup instructions.

---

## Usage

### CLI Tool

```bash
# Create a new notebook
python scripts/notebooklm_helper.py --action create --title "XAUUSD Research"

# Import sources
python scripts/notebooklm_helper.py --action import --notebook-id <ID> --source-url "https://example.com/article"

# Import YouTube video
python scripts/notebooklm_helper.py --action import --notebook-id <ID> --source-url "https://youtube.com/watch?v=xxx"

# Generate audio overview (podcast)
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type audio

# Generate video overview
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type video

# Generate slides
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type slides

# Generate quiz
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type quiz

# Generate mind map
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type mindmap

# Generate report
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type report

# Download all artifacts
python scripts/notebooklm_helper.py --action download --notebook-id <ID>
```

### Output

All artifacts saved to `skills/notebooklm/output/<notebook_id>/`

---

## BerkahKarya Workflow Examples

### Research Competitor Product
```bash
# Create notebook for competitor
python scripts/notebooklm_helper.py --action create --title "Competitor: PostAI"
# Import their landing page
python scripts/notebooklm_helper.py --action import --notebook-id <ID> --source-url "https://postai.com"
# Generate analysis report
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type report
```

### Generate Trading Podcast
```bash
python scripts/notebooklm_helper.py --action create --title "XAUUSD Weekly"
python scripts/notebooklm_helper.py --action import --notebook-id <ID> --source-url "https://tradingview.com/..."
python scripts/notebooklm_helper.py --action generate --notebook-id <ID> --output-type audio
python scripts/notebooklm_helper.py --action download --notebook-id <ID>
```

---

## Dependencies

- `notebooklm-py` (pip)
- Google account with NotebookLM access
- Valid browser cookies for authentication

**Author:** Veris (BerkahKarya)
**Version:** 1.0.0
