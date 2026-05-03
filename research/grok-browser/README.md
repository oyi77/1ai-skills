# Grok Browser

Query Grok AI via browser automation and copy responses as text.

## What It Does

This skill enables automated interaction with Grok (grok.com) through Chrome browser automation. It handles:
- Typing queries via JavaScript (contenteditable inputs)
- Submitting queries and waiting for responses
- Copying response text to clipboard (no screenshots)
- Managing multiple queries and new chats
- Using DeepSearch feature

## Quick Usage Example

```bash
# 1. Open Chrome with Grok
open -a "Google Chrome" "https://grok.com"
sleep 3

# 2. Attach browser relay
/Users/eason/clawd/scripts/attach-browser-relay.sh

# 3. Get tab ID
browser action=tabs profile=chrome

# 4. Type query using JavaScript (Grok uses contenteditable)
browser action=act profile=chrome targetId=<ID> request={
  "kind": "evaluate",
  "fn": "(() => { const e = document.querySelector('[contenteditable=\"true\"]'); e.focus(); e.innerText = 'What is AI?'; return 'ok'; })()"
}

# 5. Submit
browser action=act profile=chrome targetId=<ID> request={"kind":"press","key":"Enter"}

# 6. Wait 10-20 seconds, then snapshot
browser action=snapshot profile=chrome targetId=<ID>

# 7. Find Copy button ref and click it
browser action=act profile=chrome targetId=<ID> request={"kind":"click","ref":"<copy_ref>"}

# 8. Read response from clipboard
pbpaste
```

## Key Features

- ✅ Text-based responses (copies to clipboard, no screenshots)
- ✅ Handles contenteditable input via JavaScript evaluate
- ✅ Supports DeepSearch mode
- ✅ Response detection (copy button, time indicator)
- ✅ New chat management for topic separation
- ✅ Chrome Browser Relay integration (profile=chrome)

## Requirements

- Chrome with Browser Relay extension installed
- Browser Relay attachment script
- OpenClaw browser automation tool