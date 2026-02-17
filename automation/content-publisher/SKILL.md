---
name: content-publisher
description: Automates drafting and publishing articles to Substack and Medium.
permissions:
  - browser
  - fs
---

# Content Publisher Agent

I help you build your personal brand by drafting and publishing content to Substack and Medium.

## Capabilities

- **Drafting**: I turn ideas into structured Markdown drafts.
- **publishing**: I navigate to platform editors and paste your content.
- **Cross-Posting**: I can help you sycn content between platforms.

## Commands

### `draft`
**Usage**: `draft [topic_or_context]`
**Description**: Generates a blog post.
**Instructions**:
1.  **Analyze Request**: Identify the topic, tone, and target audience.
2.  **Generate Content**:
    -   Write a catchy Title and Subtitle.
    -   Write the Body in Markdown (Use headings, lists, bold text).
    -   **Context**: Use `browser` to research the topic if needed.
3.  **Save**:
    -   Create a file in `memory/drafts/[YYYY-MM-DD]-[Topic-Slug].md`.
    -   Notify user: "Draft saved to [Path]. Please review."

### `publish`
**Usage**: `publish [file_path] [platform] [mode=draft|live]`
**Description**: Uploads a markdown file to the platform.
**Instructions**:
1.  **Read Draft**: Read the file at `file_path`. Extract Title, Subtitle, and Body.
2.  **Login Check**:
    -   Read `config/platforms.json` for URL.
    -   Check if logged in. If not, use credentials from `memory/credentials.md`.
3.  **Navigate to Editor**: Go to the "New Post" URL.
4.  **Input Content**:
    -   **Title**: specific instructions to find Title input and type.
    -   **Body**: specific instructions to find Body editor and paste/type the markdown content.
    -   **Formatting**: Note: Markdown might need conversion to rich text. Instruct agent to "Copy as Rich Text" or handle formatting manually if possible.
5.  **Finalize**:
    -   **Draft Mode** (Default): Click "Save Draft". Notify User to review in browser.
    -   **Live Mode**: Click "Publish". **CRITICAL**: Only do this if explicitly requested.

### `schedule`
**Usage**: `schedule [file_path] [platform] [datetime]`
**Description**: Schedules a post.
**Instructions**:
1.  Perform steps 1-4 of `publish`.
2.  **Schedule Flow**:
    -   Click "Settings" or "Schedule".
    -   Input the `datetime`.
    -   Confirm.

## Usage Guide

- **Write a Post**: `draft "The impact of Agentic AI on coding"`
- **Upload to Substack**: `publish memory/drafts/agentic-ai.md substack`
- **Upload to Medium**: `publish memory/drafts/agentic-ai.md medium`

## Configuration
- **Platforms**: `config/platforms.json`
- **Credentials**: `memory/credentials.md`
