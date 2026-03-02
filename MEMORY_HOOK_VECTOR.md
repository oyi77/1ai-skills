# Memory Hook Integration for Vector DB Plugin

## Problem
User wants: Just say "cara optimasi iklan" → automatically search vector DB
Not: "ruvector_search_indonesian('cara optimasi iklan')"

## Solution
Need to integrate with OpenClaw's memory_search hook

## How it works
1. User says natural query: "cara optimasi iklan"
2. System detects query intent
3. Routes to appropriate vector engine:
   - Indonesian query → ruvector
   - Technical/structured → pageindex
   - General → zvec
4. Returns results

## Implementation
Add to ~/.openclaw/openclaw.json:

```json
"tools": {
  "memory": {
    "enhanced": true,
    "vectorDb": {
      "enabled": true,
      "defaultEngine": "ruvector",
      "fallbackEngines": ["zvec", "pageindex"],
      "autoLanguageDetection": true
    }
  }
}
```

## Auto-routing rules
1. Detect language (EN/ID/Mixed)
2. Detect content type (code, article, pdf, general)
3. Route to best engine:
   - ID text → ruvector
   - Structured docs → pageindex  
   - General → zvec

## Testing
User: "cara optimasi iklan"
System: Auto-detects ID → ruvector → returns results

User: "trading strategy Asia breakout"
System: Auto-detects EN + technical → zvec/pageindex → returns results