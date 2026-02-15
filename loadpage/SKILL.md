---
name: loadpage
description: Use when loading and retrieving content from web pages.
---

# LoadPage Skill

## Overview
Load and retrieve content from web pages using browser automation. Extract text, images, or structured data from URLs.

## When to Use
- Extracting content from a URL
- Retrieving web page data for analysis
- Scraping web content programmatically
- When you need persistent browser state

## When NOT to Use
- Simple HTTP requests (use fetch instead)
- When the page requires complex interactions
- When rate limiting is a concern

## Quick Reference
- Navigate to URL
- Extract content
- Take screenshot
- Fill forms

## Common Mistakes
- Not waiting for page load
- Ignoring JavaScript-rendered content
- Not handling redirects
