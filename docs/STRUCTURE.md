# 1ai-skills Structure

Auto-generated from `SKILLS.json`. Last generated: `python3 scripts/generate-structure.py`

---

## Overview

**1306 skills** across **19 categories**.

---

## Category Index

- [agents](../agents/_index.md) — 14 skills
- [automation](../automation/_index.md) — 20 skills
- [content](../content/_index.md) — 56 skills
- [core](../core/_index.md) — 47 skills
- [cybersecurity](../cybersecurity/_index.md) — 788 skills
- [data](../data/_index.md) — 7 skills
- [development](../development/_index.md) — 90 skills
- [devops](../devops/_index.md) — 31 skills
- [financial](../financial/_index.md) — 18 skills
- [integrations](../integrations/_index.md) — 26 skills
- [marketing](../marketing/_index.md) — 42 skills
- [mcp](../mcp/_index.md) — 15 skills
- [meta](../meta/_index.md) — 13 skills
- [mindset](../mindset/_index.md) — 55 skills
- [operations](../operations/_index.md) — 19 skills
- [productivity](../productivity/_index.md) — 10 skills
- [research](../research/_index.md) — 23 skills
- [sales](../sales/_index.md) — 13 skills
- [trading](../trading/_index.md) — 19 skills

---

## Skills by Category

### Agents (agents/)

_Total: 14 skills_

Browse in [`agents/_index.md`](../agents/_index.md).

- [autonomous](../agents/autonomous/) — Five specialized autonomous agents (code, deploy, planning, research, review) working as a coordinated pipeline. From spec to shipped code with automated planning, research, review, and deployment gates. Use when working with autonomous agents.
  `agent` `ai-agent` `automation` `orchestration` `autonomous`

- [code-agent](../agents/autonomous/code-agent/) — Use when implement features from specs — reads requirements, writes code with tests, iterates until verification passes.
  `agent` `ai-agent` `automation` `code` `autonomous`

- [code-research](../agents/research/code-research/) — Produce structured understanding of unfamiliar codebases — architecture, data flows, dependencies, and conventions. Use when joining a new project, tracing feature implementations, or mapping system architecture.
  `ai-agent` `automation` `code` `orchestration` `research`

- [coding](../agents/coding/) — Five specialized coding agents (linter, perf, refactor, security, test) that enforce quality gates across the development lifecycle. From lint enforcement through performance profiling, refactoring, security auditing, and test coverage. Use when working with coding agents.
  `agent` `ai-agent` `automation` `coding` `linter`

- [deploy-agent](../agents/autonomous/deploy-agent/) — Use when ship code through controlled pipeline with verification gates and rollback plans.
  `agent` `ai-agent` `automation` `deploy` `autonomous`

- [linter-agent](../agents/coding/linter-agent/) — Use when detect and fix code style violations, enforce project conventions, ensure consistent formatting.
  `agent` `ai-agent` `automation` `linter` `coding`

- [market-research-agent](../agents/research/market-research-agent/) — Analyze markets, competitors, user segments, and trends to produce evidence-based business intelligence. Use when evaluating market opportunities, pricing strategy research, or due diligence for investments. Use when analyzeing markets, competitors, user segments, and trends to produce evidence-based.
  `agent` `ai-agent` `automation` `market` `orchestration`

- [perf-agent](../agents/coding/perf-agent/) — Use when measure before optimizing, target actual bottlenecks proven by profiling, verify with benchmarks.
  `agent` `ai-agent` `automation` `perf` `coding`

- [planning-agent](../agents/autonomous/planning-agent/) — Use when decompose complex tasks into executable steps with dependencies, risk assessment, and verification criteria.
  `agent` `ai-agent` `automation` `planning` `autonomous`

- [refactor-agent](../agents/coding/refactor-agent/) — Use when restructure code to improve readability, maintainability, extensibility without changing external behavior.
  `agent` `ai-agent` `automation` `refactor` `coding`

- [research-agent](../agents/autonomous/research-agent/) — Use when investigate topics deeply with cross-referenced sources and produce evidence-backed findings.
  `agent` `ai-agent` `automation` `research` `autonomous`

- [review-agent](../agents/autonomous/review-agent/) — Use when read code changes with adversarial intent to find bugs, security holes, logic errors, and performance traps.
  `agent` `ai-agent` `automation` `review` `autonomous`

- [security-agent](../agents/coding/security-agent/) — Use when bug bounty hunter and security auditor. Finds vulnerabilities before they find production.
  `agent` `ai-agent` `automation` `security` `coding`

- [test-agent](../agents/coding/test-agent/) — Use when write comprehensive test suites covering happy paths, error paths, edge cases, and integration points.
  `agent` `ai-agent` `automation` `test` `coding`

### Automation (automation/)

_Total: 20 skills_

Browse in [`automation/_index.md`](../automation/_index.md).

- [agent-reach-channels](../automation/scrapers/agent-reach-channels/) — Use when multi-platform e-commerce and messaging channel extraction (Shopee, TikTok Shop, WeChat)
  `ecommerce` `scraping` `agent-reach` `shopee` `tiktok`

- [bots](../automation/bots/) — Multi-platform bot automation hub — Telegram, Twitter/X, and WhatsApp bots for automated engagement, content distribution, and revenue generation.
  `automation` `bots` `telegram` `twitter` `whatsapp`

- [clawild-moltbook](../automation/clawild-moltbook/) — Autonomous crypto intelligence agent for Moltbook — blockchain analysis, social sentiment tracking, and real-time alpha detection. Use when working with clawild moltbook.
  `ai-agent` `automation` `clawild` `crypto` `moltbook`

- [content-publisher](../automation/content-publisher/) — Automates drafting and publishing articles to Substack and Medium with SEO optimization, editorial calendars, and cross-platform distribution.
  `automation` `content` `productivity` `publisher` `seo`

- [flowise-builder](../automation/flowise-builder/) — Flowise visual LLM workflow builder — drag-drop chatflows, API endpoints, document loaders, tools. Use when working with flowise builder.
  `api` `automation` `builder` `flowise` `productivity`

- [job-hunter](../automation/job-hunter/) — Autonomous job hunting agent with state tracking, tailored applications, ATS optimization, and multi-platform search across LinkedIn, Indeed, and Glassdoor. Use when working with job hunter.
  `ai-agent` `automation` `hunter` `job` `productivity`

- [joko-moltbook](../automation/joko-moltbook/) — Queue-driven Moltbook posting agent with deduplication, idempotent operations, exponential backoff retries, and real-time monitoring. Use when working with joko moltbook.
  `ai-agent` `automation` `joko` `moltbook` `monitoring`

- [lakefs-versioning](../automation/lakefs-versioning/) — LakeFS data versioning — Git-like branching for data lakes, atomic commits, time travel, CI/CD. Use when working with lakefs versioning.
  `automation` `lakefs` `productivity` `versioning` `workflow`

- [make-scenarios](../automation/make-scenarios/) — Make.com scenario automation — modules, routes, filters, error handlers, data stores, webhooks. Use when working with make scenarios.
  `automation` `make` `productivity` `scenarios` `webhook`

- [moltbook-interact](../automation/moltbook-interact/) — Automate Moltbook engagement — content posting, community management, sentiment-aware replies, and account growth at scale.
  `automation` `interact` `moltbook` `productivity` `workflow`

- [n8n-workflows](../automation/n8n-workflows/) — n8n workflow automation — nodes, triggers, expressions, credentials, webhooks, error handling. Use when working with n8n workflows.
  `automation` `n8n` `productivity` `webhook` `workflow`

- [pipedream-workflows](../automation/pipedream-workflows/) — Pipedream serverless workflows — triggers, code steps, pre-built actions, data stores, HTTP. Use when working with pipedream workflows.
  `automation` `pipedream` `productivity` `workflow` `workflows`

- [postai-automation](../automation/postai-automation/) — Automate TikTok and Instagram video creation from product images using POST AI — generates dozens of captioned, voiced-over variants for affiliate and e-commerce marketing.
  `automation` `postai` `productivity` `video` `voice`

- [postbridge-social-manager](../automation/postbridge-social-manager/) — Multi-platform social media posting, scheduling, analytics, and media management via PostBridge API for TikTok, Instagram, X, LinkedIn, and Facebook. Use when working with postbridge social manager.
  `api` `automation` `manager` `postbridge` `productivity`

- [scrapers](../automation/scrapers/) — Data extraction hub — content monitoring, price tracking, web scraping, and social listening for competitive intelligence, market research, and automated revenue generation.
  `automation` `scrapers` `content-monitor` `price-tracker` `smart-scraper`

- [telegram-userbot](../automation/telegram-userbot/) — Full MTProto control of Telegram account via Telethon. DM, Voice Note, Call, Video Call, Group/Channel management, member scraping, bot cloning, outreach automation, broadcast, CRM tracking, content reposting, scheduled messaging, webhook triggers. Use for all Telegram automation as a real user (not bot API).
  `api` `automation` `productivity` `telegram` `userbot`

- [voice-ai-agent](../automation/voice-ai-agent/) — AI voice agent for handling incoming calls, appointment scheduling, lead qualification, and 24/7 customer service without human intervention. Use when working with voice ai agent.
  `agent` `ai-agent` `automation` `productivity` `voice`

- [workflow-builder](../automation/workflow-builder/) — Build and automate business workflows with Notion task tracking, Slack notifications, Kanban boards, and cross-functional process orchestration.
  `automation` `builder` `notion` `productivity` `slack`

- [workflows](../automation/workflows/) — Use when workflow automation hub — cron scheduling, IFTTT triggers, n8n visual builder, webhook routing, and self-hosted Zapier alternatives for zero-vendor-lock-in automation.
  `automation` `workflows` `cron` `ifttt` `n8n`

- [zapier-patterns](../automation/zapier-patterns/) — Zapier automation patterns — triggers, actions, filters, formatters, paths, code steps. Use when working with zapier patterns.
  `api` `automation` `patterns` `productivity` `workflow`

### Content (content/)

_Total: 56 skills_

Browse in [`content/_index.md`](../content/_index.md).

- [accessibility-audit](../content/accessibility-audit/) — WCAG compliance audit — semantic HTML, ARIA, keyboard navigation, color contrast, and screen reader testing. Use when working with accessibility audit.
  `accessibility` `audit` `compliance` `content-creation` `digital-content`

- [ai-newsletter](../content/ai-newsletter/) — Build and monetize AI-powered email newsletters. Curate content, automate writing, and grow paid subscriptions. Generate $1K-20K/month.
  `content-creation` `digital-content` `email` `media` `newsletter`

- [ai-podcast](../content/ai-podcast/) — Create and automate AI-powered podcasts. Generate episodes from topics, URLs, or documents with multiple AI hosts. Build audience and monetize through sponsorships.
  `content-creation` `digital-content` `media` `podcast`

- [ant-design](../content/ant-design/) — Ant Design React component library — enterprise UI, forms, tables, charts, theming, ProComponents. Use when working with ant design.
  `ant` `content-creation` `design` `digital-content` `media`

- [anti-slop-frontend](../content/anti-slop-frontend/) — Anti-slop frontend framework for AI agents. Enforces better layout, typography, motion, and spacing to counter generic AI-generated boilerplate UIs. Use when building frontend, countering generic AI UIs, need distinctive visual design, image-to-code pipeline.
  `frontend` `design` `ui` `anti-slop` `taste`

- [auto-clipper](../content/video/auto-clipper/) — Use when automatically clip long videos into short, engaging highlights for TikTok, Reels, and YouTube Shorts using FFmpeg and AI scene detection.
  `auto` `clipper` `video`

- [b-roll-finder](../content/video/b-roll-finder/) — Find relevant B-roll and stock footage by analyzing script content with semantic search. Match video meaning to text instead of random selection. Use when sourcing stock footage, finding B-roll clips, or matching visuals to narration.
  `video` `semantic-search` `b-roll` `stock-footage` `ai`

- [canvas-design](../content/canvas-design/) — Design visual art and graphics using HTML5 Canvas, p5.js, or SVG. Create generative art, data visualizations, diagrams, and interactive graphics. Use when designing visual art and graphics using html5 canvas, p5.js, or.
  `design` `canvas` `graphics` `visualization` `generative-art`

- [chakra-ui](../content/chakra-ui/) — Chakra UI React component library — theming, responsive styles, color mode, component composition. Use when working with chakra ui.
  `chakra` `content-creation` `digital-content` `media`

- [clay-art-video-generator](../content/video/clay-art-video-generator/) — Use when clay art video generator skill.
  `clay` `art` `video` `generator`

- [comment-reply-manager](../content/comment-reply-manager/) — Monitor TikTok/Instagram comments, classify sentiment, auto-reply with FAQ answers, and DM high-intent commenters with LYNK affiliate links to convert engagement into sales. Use when monitoring tiktok/instagram comments, classify sentiment, auto-reply with faq answers, and.
  `comment` `content-creation` `digital-content` `manager` `media`

- [content-factory](../content/factory/) — All-in-one YouTube content generator: create full videos from prompts, generate vertical Shorts from text, or clip long videos into Shorts using free tools (ffmpeg, edge-tts, Pexels).
  `content` `content-creation` `digital-content` `factory` `media`

- [content-kingdom](../content/kingdom/) — Use when content Kingdom Orchestrator — the BRAIN that coordinates all 12 content phases. Sequences research → plan → script → create → review → schedule → post → engage → analyze → optimize → repurpose → scale.
  `content` `automation` `tiktok` `instagram` `postbridge`

- [content-planner-auto](../content/planner-auto/) — Auto-generate 30-day content calendars with pillar rotation, platform-optimized timing, multi-account rotation, seasonal Indonesian events, and PostBridge batch scheduling.
  `auto` `content` `content-creation` `digital-content` `media`

- [daisyui-components](../content/daisyui-components/) — daisyUI component library for Tailwind — themed components, colors, responsive, dark mode. Use when working with daisyui components.
  `components` `content-creation` `daisyui` `digital-content` `media`

- [design-tokens](../content/design-tokens/) — Design token systems — color, typography, spacing, and theme architecture for consistent design. Use when designing token systems — color, typography, spacing, and theme architecture.
  `content-creation` `design` `digital-content` `media` `tokens`

- [digital-real-estate](../content/digital-real-estate/) — Build and manage a portfolio of niche content sites generating affiliate and AdSense revenue with AI handling research, writing, SEO, and updates. Use when building and manage a portfolio of niche content sites generating.
  `content-creation` `digital` `digital-content` `estate` `media`

- [document-creator](../content/document-creator/) — Create, edit, and generate Office documents programmatically — Word, PowerPoint, Excel, and PDF. One interface for all document formats with shared methodology.
  `documents` `office` `docx` `pptx` `xlsx`

- [emil-design-skills](../content/emil-design-skills/) — Collection of 8 design engineering skills by Emil Kowalski (Vercel, Linear) — animation standards, UI craft, Apple design principles, library selection, and prototyping. Based on years of production experience. Use when the user asks about UI polish, animation decisions, or wants to audit/improve interface motion.
  `design` `animation` `ui` `motion` `css`

- [faceless-youtube](../content/video/faceless-youtube/) — Create and automate faceless YouTube channels using AI-generated scripts, TTS voiceovers, stock footage, and automated publishing workflows with zero on-camera presence.
  `content` `video` `faceless` `youtube` `automation`

- [frontend-design](../content/frontend-design/) — Design system patterns — component architecture, Tailwind mastery, visual hierarchy, and responsive layouts. Use when designing system patterns — component architecture, tailwind mastery, visual hierarchy,.
  `content-creation` `design` `digital-content` `frontend` `media`

- [frontend-ui-design](../content/frontend-ui-design/) — Design and build production-grade UI components using React, Vue, or vanilla HTML/CSS. Create responsive layouts, design systems, and accessible interfaces. Use when designing and build production-grade ui components using react, vue, or.
  `design` `frontend` `ui` `react` `css`

- [gemini-image-generator](../content/gemini-image-generator/) — Use when generating professional posed product images for e-commerce using Gemini AI with optimized prompts
  `content-creation` `digital-content` `gemini` `generator` `image`

- [geminigen-ai](../content/geminigen-ai/) — Unified multimedia API for image generation (nano-banana-pro, imagen-4), video generation (Grok, Veo, Sora), and text-to-speech. Replaces grok-video-generation, seedance, and gemini-image-generator. Use when working with geminigen ai.
  `api` `content-creation` `digital-content` `geminigen` `media`

- [humanizer](../content/humanizer/) — Transform AI-generated content into natural, human-sounding writing with proper tone and style. Use when working with humanizer.
  `content-creation` `digital-content` `humanizer` `media`

- [humanizer-zh](../content/humanizer-zh/) — Use when removing AI writing痕迹 from Chinese text to make it sound more natural and human-written.
  `content-creation` `digital-content` `humanizer` `media`

- [image-gen](../content/image-gen/) — AI image generation — Stable Diffusion, Midjourney, DALL-E, ComfyUI. Prompt engineering for images, inpainting, outpainting, ControlNet. Use when working with image gen.
  `content-creation` `digital-content` `gen` `image` `media`

- [larry-playbook](../content/larry-playbook/) — Autonomous AI agent that learns and improves viral content over time using Oliver Henry's proven formula. Use when working with larry playbook.
  `ai-agent` `content-creation` `digital-content` `larry` `media`

- [material-ui](../content/material-ui/) — Material UI (MUI) React components — theming, styled engine, data grid, date pickers, icons. Use when working with material ui.
  `content-creation` `digital-content` `material` `media`

- [minimalist-design](../content/minimalist-design/) — Dieter Rams' approach to timeless product design - less but better. Use when working with minimalist design.
  `content-creation` `design` `digital-content` `media` `minimalist`

- [monetization-strategist](../content/monetization-strategist/) — Turn content into revenue — newsletter businesses, YouTube automation, affiliate sites, digital product creation, funnel design, audience building. Use when building content-based revenue streams.
  `content-creation` `digital-content` `media` `monetization` `strategist`

- [multi-platform-distribution](../content/multi-platform-distribution/) — One piece of content becomes 10 — blog to Twitter thread, LinkedIn article, YouTube script, newsletter, TikTok script, podcast outline, Reddit post. Use when working with multi platform distribution.
  `content-creation` `digital-content` `distribution` `media` `multi`

- [novel-writing](../content/novel-writing/) — Complete novel and fiction writing skill covering story structure, character creation, world-building, dialogue, pacing, and chapter craft. Adopts Chinese novelist patterns (show-don't-tell, conflict, cliffhanger) plus Western frameworks. Includes kids books (picture book, middle grade) and Buku Bahasa Indonesia for Indonesian fiction. Use when writing novels, short stories, or children's fiction.
  `content` `writing` `fiction` `novel` `character`

- [pandacss-styling](../content/pandacss-styling/) — Panda CSS zero-runtime styling — token system, patterns, recipes, conditions, JSX styles. Use when working with pandacss styling.
  `content-creation` `digital-content` `media` `pandacss` `styling`

- [paperpod](../content/paperpod/) — Isolated agent runtime for code execution, live preview URLs, browser automation, 50+ tools (ffmpeg, sqlite, pandoc, imagemagick), LLM inference, and persistent memory — all via CLI or HTTP, no SDK or API keys required. Use when working with paperpod.
  `ai-agent` `api` `content-creation` `digital-content` `media`

- [postcss-plugins](../content/postcss-plugins/) — PostCSS plugin ecosystem — Autoprefixer, cssnano, nesting, custom plugins, preset configuration. Use when working with postcss plugins.
  `content-creation` `digital-content` `media` `plugins` `postcss`

- [radix-primitives](../content/radix-primitives/) — Radix UI headless primitives — accessible, unstyled React components for dialogs, dropdowns, tooltips. Use when working with radix primitives.
  `content-creation` `digital-content` `media` `primitives` `radix`

- [remotion](../content/video/remotion/) — Create, render, and manage programmatic videos using Remotion (React-based video framework). Covers compositions, frame-driven animation, transitions, effects, captions, audio, voiceover, FFmpeg post-production, and professional SaaS-grade motion design.
  `content-creation` `video-production` `remotion` `react` `animation`

- [responsive-design](../content/responsive-design/) — Mobile-first responsive design — breakpoints, fluid typography, container queries, and touch optimization. Use when working with responsive design.
  `content-creation` `design` `digital-content` `media` `responsive`

- [shadcn-ui](../content/shadcn-ui/) — shadcn/ui component library — copy-paste React components, Tailwind CSS, Radix primitives, theming. Use when working with shadcn ui.
  `content-creation` `digital-content` `media` `shadcn`

- [storybook-ui](../content/storybook-ui/) — Storybook for UI component development — stories, addons, controls, a11y testing, visual regression. Use when working with storybook ui.
  `content-creation` `digital-content` `media` `storybook` `testing`

- [styled-components](../content/styled-components/) — styled-components CSS-in-JS — tagged templates, theming, props, animations, SSR, performance. Use when working with styled components.
  `components` `content-creation` `digital-content` `media` `styled`

- [tailwind-advanced](../content/tailwind-advanced/) — Advanced Tailwind CSS — custom plugins, JIT, container queries, animations, dark mode, design systems. Use when working with tailwind advanced.
  `advanced` `content-creation` `digital-content` `media` `tailwind`

- [theme-factory](../content/theme-factory/) — Generate and apply professional color themes, typography systems, and design tokens for applications. Create consistent visual identities across platforms.
  `design` `themes` `colors` `typography` `design-tokens`

- [ui-critique](../content/ui-critique/) — Structured UI review — visual hierarchy, consistency, accessibility, and actionable improvement feedback. Use when working with ui critique.
  `content-creation` `critique` `digital-content` `media`

- [ui-ux-pro-max](../content/ui-ux-pro-max/) — Industry-specific design intelligence — 161 reasoning rules, 99 UX guidelines, 161 color palettes, 57 font pairings, 49 UI styles. Use when building professional UI, need industry-specific design, generating design systems, choosing colors or typography.
  `ui` `ux` `design` `design-system` `color-palette`

- [ultra-realistic-media](../content/ultra-realistic-media/) — ULTRA REALISTIC MEDIA GENERATION - TRAINING SKILL. Use when relevant to this domain.
  `content-creation` `digital-content` `media` `realistic` `ultra`

- [vanilla-extract](../content/vanilla-extract/) — Vanilla Extract zero-runtime CSS-in-JS — type-safe styles, Sprinkles, Recipes, themes. Use when working with vanilla extract.
  `content-creation` `digital-content` `extract` `media` `vanilla`

- [video-editor](../content/video/editor/) — Professional video post-production using FFmpeg — color grading, audio design, kinetic typography, transitions, motion effects, captions, brand overlays, and platform-optimized export for promotional and marketing videos. Use when editing videos, adding captions, color grading, or creating promo content.
  `content-creation` `video-production` `ffmpeg` `post-production` `color-grading`

- [video-gen](../content/video/gen/) — Generate videos with AI models — Runway, Kling, Sora, Pika, Seedance 2.0, Grok Imagine, Veo. Text-to-video, image-to-video, video extension, multi-modal references. Use when generating video from text prompts, animating images, or creating AI video content.
  `content-creation` `video-generation` `ai-video` `text-to-video` `image-to-video`

- [viral-content-creator](../content/viral-content-creator/) — Generate 50+ video variations from a single product image across TikTok, Instagram, Facebook, Twitter, and YouTube with hook-based A/B testing, viral score prediction, and autopilot scheduling.
  `content` `content-creation` `creator` `digital-content` `media`

- [viral-research-engine](../content/viral-research-engine/) — Research trending topics, generate viral hooks, find content gaps, analyze competitors, and get hashtag recommendations for Indonesian short-form video creators on TikTok, Reels, and Shorts.
  `content-creation` `digital-content` `engine` `media` `research`

- [voice-ai](../content/voice-ai/) — Voice AI — text-to-speech (ElevenLabs, OpenAI TTS), speech-to-text (Whisper), voice cloning, real-time voice agents. Use when working with voice ai.
  `ai-agent` `content-creation` `digital-content` `media` `text-to-speech`

- [voice-chatterbox-tts](../content/voice-chatterbox-tts/) — Free local TTS with voice cloning using Chatterbox. Zero API costs, word-level timing, whisper integration. Clone any voice with 10-60s reference audio. Use when generating narration, voiceovers, or custom AI voices.
  `tts` `voice-cloning` `local` `free` `whisper`

- [writing](../content/writing/) — Use when full-stack content production factory — ad copy, emails, long-form articles, product descriptions. Turn words into revenue with data-driven writing pipelines.
  `content-creation` `copywriting` `ad-copy` `email-marketing` `long-form`

- [writing-skills](../content/writing-skills/) — Use when creating new skills, editing existing skills, or verifying skills work before deployment
  `content-creation` `digital-content` `media` `skills` `writing`

### Core (core/)

_Total: 47 skills_

Browse in [`core/_index.md`](../core/_index.md).

- [adhd](../core/adhd/) — Parallel divergent ideation for agents — spawns N isolated reasoning branches under different cognitive frames, then scores, clusters, prunes traps, and deepens survivors. Use for open-ended design, architecture, naming, API surface decisions, fuzzy debugging, and brainstorming. Skip for syntax lookups or bugs with known root cause.
  `reasoning` `brainstorming` `decision-making` `cognitive-frames` `divergent-thinking`

- [agent-docs](../core/agent-docs/) — Use when writing documentation optimized for AI agent consumption - SKILL.md files, README files, API docs, or any documentation that will be read by LLMs in context windows.
  `agent` `ai-agent` `api` `docs` `infrastructure`

- [agent-harness-optimizer](../core/agent-harness-optimizer/) — Agent harness optimization patterns for token efficiency, memory persistence, session management, and cross-harness parity. Use when optimizing agent performance, reducing token costs,.
  `token-optimization` `memory-persistence` `session-management` `hooks` `cross-harness`

- [agent-security-scanner](../core/agent-security-scanner/) — Agentic security patterns for AI agent systems including attack vector defense, sandboxing, input sanitization, security scanning, CVE awareness, and least-privilege tool access. Use when.
  `security` `prompt-injection` `sandboxing` `agentshield` `least-privilege`

- [agent-self-improvement](../core/agent-self-improvement/) — Monitor performance of other skills, identify bottlenecks, suggest improvements, and auto-optimize the skill portfolio. Use when monitoring performance of other skills, identify bottlenecks, suggest improvements, and.
  `agent` `improvement` `infrastructure` `memory` `self`

- [ai-engineering-curriculum](../core/ai-engineering-curriculum/) — Structured AI engineering curriculum — 382 skills + 99 prompts across 20 phases covering ML, deep learning, LLMs, agents, and production systems. Use when learning AI, building AI skills,.
  `ai` `curriculum` `machine-learning` `deep-learning` `llm`

- [auto-git-commiter](../core/auto-git-commiter/) — Automatically commit and push OpenClaw changes to GitHub. Enable continuous improvement with automatic versioning, changelogs, and deployment-ready commits. Use when working with auto git commiter.
  `auto` `commiter` `git` `github` `infrastructure`

- [autogen-agents](../core/autogen-agents/) — AutoGen multi-agent conversations — AssistantAgent, UserProxyAgent, group chat, code execution. Use when working with autogen agents.
  `agents` `ai-agent` `autogen` `infrastructure` `memory`

- [autonomy-engine](../core/autonomy-engine/) — Core autonomy protocol for AI agent operations. Defines how agents operate 24/7 without human prompts — monitoring all systems, generating revenue, managing team, escalating decisions, and growing. Use this skill to understand an autonomous operating system. Use when working with autonomy engine.
  `autonomy` `engine` `infrastructure` `memory` `monitoring`

- [berkahkarya-orchestrator](../core/berkahkarya-orchestrator/) — Use when orchestrate multi-skill workflows by routing tasks to the right agents and coordinating cross-platform operations.
  `ai-agent` `berkahkarya` `infrastructure` `memory` `orchestrator`

- [book-to-skill](../core/book-to-skill/) — Convert technical books and documents (PDF, EPUB, DOCX, HTML, Markdown, RTF, MOBI) into structured agent skills with frameworks, mental models, chapter references, and decision rules. Includes full extraction pipeline. Use when the user wants to turn a book or document collection into a reusable agent skill for study and reference.
  `documentation` `skill-generation` `knowledge-management` `pdf` `epub`

- [cloudflare-router](../core/cloudflare-router/) — Manage Cloudflare DNS, CDN, and security rules via API. Use when configuring domains, SSL, WAF, or edge caching.
  `api` `cloudflare` `infrastructure` `memory` `router`

- [company-kb](../core/core/company-kb/) — company-kb — Company Knowledge Base Skill. Use when relevant to this domain.
  `company` `infrastructure` `memory` `self-improvement` `collaboration`

- [core](../core/core/) — Knowledge base hub — PARA-structured company memory combining company-kb and kb for persistent context, project documentation, and agent recall across sessions. Use when working with knowledge base, company knowledge, or persistent memory.
  `knowledge-base` `memory` `para` `infrastructure` `company`

- [crewai-agents](../core/crewai-agents/) — CrewAI multi-agent orchestration — agents, tasks, crews, tools, memory, delegation. Use when working with crewai agents.
  `agents` `ai-agent` `crewai` `infrastructure` `memory`

- [dify-workflow](../core/dify-workflow/) — Dify AI workflow platform — LLM apps, knowledge bases, agents, workflow orchestration, API deployment. Use when working with dify workflow.
  `ai-agent` `api` `dify` `infrastructure` `memory`

- [find-skills](../core/find-skills/) — Automatically discover, evaluate, and activate community skills when local skills don't cover user needs. Includes credibility scoring and safety checks for complete OpenClaw self-sufficiency.
  `find` `infrastructure` `memory` `self-improvement` `skills`

- [gateway-doctor](../core/gateway-doctor/) — Diagnose and fix MCP gateway routing issues, health checks, and server connectivity problems. Use when working with gateway doctor.
  `doctor` `gateway` `infrastructure` `memory` `self-improvement`

- [gemini-api-dev](../core/gemini-api-dev/) — Build applications using Google Gemini API. Handle chat completions, multimodal inputs, function calling, streaming, and grounding with Google Search. Use when building applications using google gemini api. handle chat completions, multimodal.
  `ai` `gemini` `google` `llm` `multimodal`

- [hive-mind](../core/hive-mind/) — Coordinate multi-agent consensus using TiDB-backed shared memory. Use when agents need to agree on decisions or share state.
  `ai-agent` `hive` `infrastructure` `memory` `mind`

- [joko-orchestrator](../core/joko-orchestrator/) — Use when deterministically coordinating autonomous planning and execution across available skills under strict guardrails.
  `infrastructure` `joko` `memory` `orchestrator` `self-improvement`

- [joko-proactive-agent](../core/joko-proactive-agent/) — Proactive agent that detects signals and suggests actions with Slack notifications. Use when working with joko proactive agent.
  `agent` `ai-agent` `infrastructure` `joko` `memory`

- [karpathy-coding-principles](../core/karpathy-coding-principles/) — Andrej Karpathy's 4 coding principles — think before coding, simplicity first, surgical changes, goal-driven execution. Use when coding, reviewing code quality, reducing overengineering,.
  `coding-principles` `code-quality` `best-practices` `karpathy` `simplicity`

- [kb](../core/core/kb/) — Use when querying and maintaining the knowledge base for project context, decisions, and architecture documentation on session start.
  `infrastructure` `memory` `self-improvement` `para` `persistence`

- [kb-memory](../core/kb-memory/) — Knowledge base and memory system for AI agents. Covers company KB, persistent memory, session recall, and brain architecture for context preservation.
  `knowledge-base` `memory` `context` `persistence` `recall`

- [langchain-patterns](../core/langchain-patterns/) — LangChain/LangGraph patterns — chains, agents, tools, memory, retrieval, graph workflows. Use when working with langchain patterns.
  `ai-agent` `infrastructure` `langchain` `memory` `patterns`

- [llamaindex-patterns](../core/llamaindex-patterns/) — LlamaIndex data framework — ingestion, indexing, query engines, chat engines, agents. Use when working with llamaindex patterns.
  `ai-agent` `infrastructure` `llamaindex` `memory` `patterns`

- [llm-deployment](../core/llm-deployment/) — LLM deployment and serving — vLLM, Ollama, TGI, llama.cpp. Model quantization, GPU optimization, API serving. Use when working with llm deployment.
  `api` `deployment` `infrastructure` `llm` `memory`

- [model-fine-tuning](../core/model-fine-tuning/) — Fine-tune LLMs and ML models — LoRA, QLoRA, PEFT, Hugging Face. Dataset prep, training, evaluation, deployment. Use when working with model fine tuning.
  `fine` `infrastructure` `machine-learning` `memory` `model`

- [model-router](../core/model-router/) — Route AI model requests to the optimal provider based on task, cost, latency, and capability requirements. Manage multi-provider LLM deployments. Use when working with model router.
  `ai` `llm` `routing` `multi-provider` `cost-optimization`

- [omniroute-integration](../core/omniroute-integration/) — Integrate with OmniRoute AI Router for multi-provider LLM routing, MCP server access, and A2A agent-to-agent orchestration. Use when integrateing with omniroute ai router for multi-provider llm routing, mcp.
  `ai-agent` `infrastructure` `integration` `memory` `omniroute`

- [prompt-engineering](../core/prompt-engineering/) — Advanced prompt engineering — chain-of-thought, few-shot, tree-of-thought, self-consistency, meta-prompting, system design, debugging, and optimization for production AI systems. Use when working with prompt engineering.
  `engineering` `infrastructure` `memory` `prompt` `self-improvement`

- [rag-builder](../core/rag-builder/) — RAG pipeline design — document chunking, embedding strategies, retrieval optimization, and answer generation. Use when working with rag builder.
  `builder` `infrastructure` `memory` `pipeline` `rag`

- [replicate-runner](../core/replicate-runner/) — Run AI models on Replicate cloud API. Deploy image generation, video creation, audio processing, and custom models without managing infrastructure. Use when working with replicate runner.
  `ai` `replicate` `models` `image-generation` `video`

- [revenue-engine](../core/revenue-engine/) — Manage revenue pipelines, track Stripe/analytics metrics, and automate financial reporting for SaaS businesses. Use when building revenue infrastructure.
  `engine` `infrastructure` `memory` `pipeline` `revenue`

- [runtime-self-improvement](../core/runtime-self-improvement/) — Automatically improve OpenClaw and 1ai-skills at runtime. Analyze performance, detect gaps, enhance skills, and self-optimize during operation. Use when working with runtime self improvement.
  `improvement` `infrastructure` `memory` `runtime` `self`

- [ruvector](../core/ruvector/) — Generate and manage vector embeddings for semantic search and RAG retrieval across knowledge bases.
  `infrastructure` `memory` `ruvector` `self-improvement`

- [self-improving](../core/self-improving/) — Self-reflection + Self-criticism + Auto-learning from corrections + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. Use when working with self improving.
  `ai-agent` `improving` `infrastructure` `memory` `self`

- [semantic-kernel](../core/semantic-kernel/) — Microsoft Semantic Kernel — AI orchestration, plugins, planners, memory, prompt templates. Use when working with semantic kernel.
  `infrastructure` `kernel` `memory` `self-improvement` `semantic`

- [skill-builder](../core/skill-builder/) — Automatically detect source types and build AI skills using Skill Seekers. Use when the user wants to create skills from documentation, repos, PDFs, videos, or other knowledge sources.
  `ai-infrastructure` `automation` `parsing` `scraping` `rag`

- [skill-performance-monitor](../core/skill-performance-monitor/) — Monitor and analyze skill effectiveness in real-time. Track usage, success rates, response quality, and user satisfaction for continuous optimization. Use when monitoring and analyze skill effectiveness in real-time. track usage, success.
  `infrastructure` `memory` `monitor` `performance` `self-improvement`

- [teamwork](../core/teamwork/) — Dynamically creates and manages AI agent teams for complex tasks. Invoke when user requests multi-agent collaboration, complex project execution, or when tasks require specialized roles and coordinated workflow. Use when working with teamwork.
  `ai-agent` `infrastructure` `memory` `self-improvement` `teamwork`

- [using-superpowers](../core/using-superpowers/) — Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
  `infrastructure` `memory` `self-improvement` `superpowers` `using`

- [vector-db-ops](../core/vector-db-ops/) — Vector database operations — Pinecone, Weaviate, Qdrant, ChromaDB. Indexing, querying, filtering, and managing vector embeddings for RAG and similarity search. Use when working with vector db ops.
  `infrastructure` `memory` `ops` `self-improvement` `vector`

- [vilona](../core/vilona/) — Use when foundational core infrastructure skill providing system foundation capabilities for the agent ecosystem.
  `infrastructure` `memory` `self-improvement` `vilona`

- [vilona-activate](../core/vilona-activate/) — Use when activate an AI general manager persona with full context awareness and multi-user adaptation.
  `activate` `infrastructure` `memory` `self-improvement`

- [zvec](../core/zvec/) — Zero-copy vector operations for efficient similarity search and embedding storage in agent memory systems. Use when working with zvec.
  `ai-agent` `infrastructure` `memory` `self-improvement` `zvec`

### Cybersecurity (cybersecurity/)

_Total: 788 skills_

Browse in [`cybersecurity/_index.md`](../cybersecurity/_index.md).

- [acquiring-disk-image-with-dd-and-dcfldd](../cybersecurity/acquiring-disk-image-with-dd-and-dcfldd/) — Create forensically sound bit-for-bit disk images using dd and dcfldd while preserving evidence integrity through hash verification. Use when createing forensically sound bit-for-bit disk images using dd and dcfldd.
  `forensics` `disk-imaging` `evidence-acquisition` `dd` `dcfldd`

- [ad-killer](../cybersecurity/ad-killer/) — Active Directory and Windows domain exploitation for enterprise penetration testing. Use when attacking Windows domains, exploiting AD misconfigurations, or performing lateral movement in enterprise environments.
  `ad` `active-directory` `cybersecurity` `exploitation` `killer`

- [ai-hacker](../cybersecurity/ai-hacker/) — AI and LLM security testing — prompt injection, model manipulation, data exfiltration via AI. Use when testing AI-powered applications, finding prompt injection vulnerabilities, or assessing LLM-integrated systems.
  `ai` `llm` `prompt-injection` `security` `testing`

- [analyzing-active-directory-acl-abuse](../cybersecurity/analyzing-active-directory-acl-abuse/) — Detect dangerous ACL misconfigurations in Active Directory using ldap3 to identify GenericAll, WriteDACL, and WriteOwner abuse paths. Use when detecting dangerous acl misconfigurations in active directory using ldap3 to.
  `active-directory` `acl-abuse` `ldap` `privilege-escalation`

- [analyzing-android-malware-with-apktool](../cybersecurity/analyzing-android-malware-with-apktool/) — Perform static analysis of Android APK malware samples using apktool for decompilation, jadx for Java source recovery, and androguard for permission analysis, manifest inspection, and suspicious API call detection. Use when performing static analysis of android apk malware samples using apktool.
  `Android` `APK` `apktool` `jadx` `androguard`

- [analyzing-api-gateway-access-logs](../cybersecurity/analyzing-api-gateway-access-logs/) — Parses API Gateway access logs (AWS API Gateway, Kong, Nginx) to detect BOLA/IDOR attacks, rate limit bypass, credential scanning, and injection attempts. Uses pandas for statistical analysis of request patterns and anomaly detection. Use when investigating API abuse or building API-specific threat detection rules.

  `analyzing` `api` `gateway` `access`

- [analyzing-apt-group-with-mitre-navigator](../cybersecurity/analyzing-apt-group-with-mitre-navigator/) — Analyze advanced persistent threat (APT) group techniques using MITRE ATT&CK Navigator to create layered heatmaps of adversary TTPs for detection gap analysis and threat-informed defense. Use when analyzeing advanced persistent threat (apt) group techniques using mitre att&ck.
  `mitre-attack` `navigator` `apt` `threat-actor` `ttp-analysis`

- [analyzing-azure-activity-logs-for-threats](../cybersecurity/analyzing-azure-activity-logs-for-threats/) — Queries Azure Monitor activity logs and sign-in logs via azure-monitor-query to detect suspicious administrative operations, impossible travel, privilege escalation, and resource modifications. Builds KQL queries for threat hunting in Azure environments. Use when investigating suspicious Azure tenant activity or building cloud SIEM detections.

  `azure` `cloud-security` `azure-monitor` `kql` `threat-hunting`

- [analyzing-bootkit-and-rootkit-samples](../cybersecurity/analyzing-bootkit-and-rootkit-samples/) — Analyzes bootkit and advanced rootkit malware that infects the Master Boot Record (MBR), Volume Boot Record (VBR), or UEFI firmware to gain persistence below the operating system. Covers boot sector analysis, UEFI module inspection, and anti-rootkit detection techniques. Activates for requests involving bootkit analysis, MBR malware investigation, UEFI persistence analysis, or pre-OS malware detection.

  `malware` `bootkit` `rootkit` `UEFI` `MBR-analysis`

- [analyzing-browser-forensics-with-hindsight](../cybersecurity/analyzing-browser-forensics-with-hindsight/) — Analyze Chromium-based browser artifacts using Hindsight to extract browsing history, downloads, cookies, cached content, autofill data, saved passwords, and browser extensions from Chrome, Edge, Brave, and Opera for forensic investigation. Use when analyzeing chromium-based browser artifacts using hindsight to extract browsing history,.
  `browser-forensics` `hindsight` `chrome-forensics` `chromium` `edge`

- [analyzing-campaign-attribution-evidence](../cybersecurity/analyzing-campaign-attribution-evidence/) — Campaign attribution analysis involves systematically evaluating evidence to determine which threat actor or group is responsible for a cyber operation. This skill covers collecting and weighting attr
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [analyzing-certificate-transparency-for-phishing](../cybersecurity/analyzing-certificate-transparency-for-phishing/) — Monitor Certificate Transparency logs using crt.sh and Certstream to detect phishing domains, lookalike certificates, and unauthorized certificate issuance targeting your organization. Use when monitoring certificate transparency logs using crt.sh and certstream to detect.
  `certificate-transparency` `ct-logs` `phishing` `crt-sh` `certstream`

- [analyzing-cloud-storage-access-patterns](../cybersecurity/analyzing-cloud-storage-access-patterns/) — Detect abnormal access patterns in AWS S3, GCS, and Azure Blob Storage by analyzing CloudTrail Data Events, GCS audit logs, and Azure Storage Analytics. Identifies after-hours bulk downloads, access from new IP addresses, unusual API calls (GetObject spikes), and potential data exfiltration using statistical baselines and time-series anomaly detection. Use when detecting abnormal access patterns in aws s3, gcs, and azure.
  `analyzing` `cloud` `storage` `access`

- [analyzing-cobalt-strike-beacon-configuration](../cybersecurity/analyzing-cobalt-strike-beacon-configuration/) — Extract and analyze Cobalt Strike beacon configuration from PE files and memory dumps to identify C2 infrastructure, malleable profiles, and operator tradecraft. Use when working with analyzing cobalt strike beacon configuration.
  `cobalt-strike` `beacon` `c2` `malware-analysis` `config-extraction`

- [analyzing-cobaltstrike-malleable-c2-profiles](../cybersecurity/_deprecated/analyzing-cobaltstrike-malleable-c2-profiles/) — Parse and analyze Cobalt Strike Malleable C2 profiles using dissect.cobaltstrike and pyMalleableC2 to extract C2 indicators, detect evasion techniques, and generate network detection signatures.
  `cobalt-strike` `malleable-c2` `c2-detection` `beacon-analysis` `network-signatures`

- [analyzing-command-and-control-communication](../cybersecurity/analyzing-command-and-control-communication/) — Analyzes malware command-and-control (C2) communication protocols to understand beacon patterns, command structures, data encoding, and infrastructure. Covers HTTP, HTTPS, DNS, and custom protocol C2 analysis for detection development and threat intelligence. Activates for requests involving C2 analysis, beacon detection, C2 protocol reverse engineering, or command-and-control infrastructure mapping.

  `malware` `C2` `command-and-control` `beacon` `protocol-analysis`

- [analyzing-cyber-kill-chain](../cybersecurity/analyzing-cyber-kill-chain/) — Analyzes intrusion activity against the Lockheed Martin Cyber Kill Chain framework to identify which phases an adversary has completed, where defenses succeeded or failed, and what controls would have interrupted the attack at earlier phases. Use when conducting post-incident analysis, building prevention-focused security controls, or mapping detection gaps to kill chain phases.
  `kill-chain` `Lockheed-Martin` `MITRE-ATT&CK` `intrusion-analysis` `defense-in-depth`

- [analyzing-disk-image-with-autopsy](../cybersecurity/analyzing-disk-image-with-autopsy/) — Perform comprehensive forensic analysis of disk images using Autopsy to recover files, examine artifacts, and build investigation timelines. Use when performing comprehensive forensic analysis of disk images using autopsy to.
  `forensics` `autopsy` `disk-analysis` `sleuth-kit` `file-recovery`

- [analyzing-dns-logs-for-exfiltration](../cybersecurity/analyzing-dns-logs-for-exfiltration/) — Analyzes DNS query logs to detect data exfiltration via DNS tunneling, DGA domain communication, and covert C2 channels using entropy analysis, query volume anomalies, and subdomain length detection in SIEM platforms. Use when SOC teams need to identify DNS-based threats that bypass traditional network security controls.

  `soc` `dns` `exfiltration` `dns-tunneling` `dga`

- [analyzing-docker-container-forensics](../cybersecurity/analyzing-docker-container-forensics/) — Investigate compromised Docker containers by analyzing images, layers, volumes, logs, and runtime artifacts to identify malicious activity and evidence. Use when working with analyzing docker container forensics.
  `forensics` `docker` `container-forensics` `container-security` `image-analysis`

- [analyzing-email-headers-for-phishing-investigation](../cybersecurity/analyzing-email-headers-for-phishing-investigation/) — Parse and analyze email headers to trace the origin of phishing emails, verify sender authenticity, and identify spoofing through SPF, DKIM, and DMARC validation. Use when working with analyzing email headers for phishing investigation.
  `forensics` `email-analysis` `phishing` `spf` `dkim`

- [analyzing-ethereum-smart-contract-vulnerabilities](../cybersecurity/analyzing-ethereum-smart-contract-vulnerabilities/) — Perform static and symbolic analysis of Solidity smart contracts using Slither and Mythril to detect reentrancy, integer overflow, access control, and other vulnerability classes before deployment to Ethereum mainnet. Use when performing static and symbolic analysis of solidity smart contracts using.
  `ethereum` `solidity` `smart-contract` `slither` `mythril`

- [analyzing-golang-malware-with-ghidra](../cybersecurity/analyzing-golang-malware-with-ghidra/) — Reverse engineer Go-compiled malware using Ghidra with specialized scripts for function recovery, string extraction, and type reconstruction in stripped Go binaries. Use when reverseing engineer go-compiled malware using ghidra with specialized scripts for.
  `golang` `ghidra` `reverse-engineering` `malware-analysis` `binary-analysis`

- [analyzing-heap-spray-exploitation](../cybersecurity/analyzing-heap-spray-exploitation/) — Detect and analyze heap spray attacks in memory dumps using Volatility3 plugins to identify NOP sled patterns, shellcode landing zones, and suspicious large allocations in process virtual address space. Use when detecting and analyze heap spray attacks in memory dumps using.
  `malware-analysis` `memory-forensics` `heap-spray` `volatility3` `exploit-analysis`

- [analyzing-indicators-of-compromise](../cybersecurity/analyzing-indicators-of-compromise/) — Analyzes indicators of compromise (IOCs) including IP addresses, domains, file hashes, URLs, and email artifacts to determine maliciousness confidence, campaign attribution, and blocking priority. Use when triaging IOCs from phishing emails, security alerts, or external threat feeds; enriching raw IOCs with multi-source intelligence; or making block/monitor/whitelist decisions. Activates for requests involving VirusTotal, AbuseIPDB, MalwareBazaar, MISP, or IOC enrichment pipelines.

  `IOC` `VirusTotal` `AbuseIPDB` `MalwareBazaar` `MISP`

- [analyzing-ios-app-security-with-objection](../cybersecurity/analyzing-ios-app-security-with-objection/) — Performs runtime mobile security exploration of iOS applications using Objection, a Frida-powered toolkit that enables security testers to interact with app internals without jailbreaking. Use when assessing iOS app security posture, bypassing client-side protections, dumping keychain items, inspecting filesystem storage, and evaluating runtime behavior. Activates for requests involving iOS security testing, Objection runtime analysis, Frida-based iOS assessment, or mobile runtime explo.
  `mobile-security` `ios` `objection` `frida` `owasp-mobile`

- [analyzing-kubernetes-audit-logs](../cybersecurity/analyzing-kubernetes-audit-logs/) — Parses Kubernetes API server audit logs (JSON lines) to detect exec-into-pod, secret access, RBAC modifications, privileged pod creation, and anonymous API access. Builds threat detection rules from audit event patterns. Use when investigating Kubernetes cluster compromise or building k8s-specific SIEM detection rules.

  `analyzing` `kubernetes` `audit` `logs`

- [analyzing-linux-audit-logs-for-intrusion](../cybersecurity/analyzing-linux-audit-logs-for-intrusion/) — Uses the Linux Audit framework (auditd) with ausearch and aureport utilities to detect intrusion attempts, unauthorized access, privilege escalation, and suspicious system activity. Covers audit rule configuration, log querying, timeline reconstruction, and integration with SIEM platforms. Activates for requests involving auditd analysis, Linux audit log investigation, ausearch queries, aureport summaries, or host-based intrusion detection on Linux.

  `auditd` `ausearch` `aureport` `linux-security` `intrusion-detection`

- [analyzing-linux-elf-malware](../cybersecurity/analyzing-linux-elf-malware/) — Analyzes malicious Linux ELF (Executable and Linkable Format) binaries including botnets, cryptominers, ransomware, and rootkits targeting Linux servers, containers, and cloud infrastructure. Covers static analysis, dynamic tracing, and reverse engineering of x86_64 and ARM ELF samples. Activates for requests involving Linux malware analysis, ELF binary investigation, Linux server compromise assessment, or container malware analysis.

  `malware` `Linux` `ELF` `reverse-engineering` `server-malware`

- [analyzing-linux-kernel-rootkits](../cybersecurity/analyzing-linux-kernel-rootkits/) — Detect kernel-level rootkits in Linux memory dumps using Volatility3 linux plugins (check_syscall, lsmod, hidden_modules), rkhunter system scanning, and /proc vs /sys discrepancy analysis to identify hooked syscalls, hidden kernel modules, and tampered system structures. Use when detecting kernel-level rootkits in linux memory dumps using volatility3 linux.
  `rootkit` `linux` `kernel` `volatility3` `memory-forensics`

- [analyzing-linux-system-artifacts](../cybersecurity/analyzing-linux-system-artifacts/) — Examine Linux system artifacts including auth logs, cron jobs, shell history, and system configuration to uncover evidence of compromise or unauthorized activity. Use when working with analyzing linux system artifacts.
  `forensics` `linux-forensics` `system-artifacts` `log-analysis` `persistence-detection`

- [analyzing-lnk-file-and-jump-list-artifacts](../cybersecurity/analyzing-lnk-file-and-jump-list-artifacts/) — Analyze Windows LNK shortcut files and Jump List artifacts to establish evidence of file access, program execution, and user activity using LECmd, JLECmd, and manual binary parsing of the Shell Link Binary format. Use when analyzeing windows lnk shortcut files and jump list artifacts to.
  `lnk-files` `jump-lists` `lecmd` `jlecmd` `windows-forensics`

- [analyzing-macro-malware-in-office-documents](../cybersecurity/analyzing-macro-malware-in-office-documents/) — Analyzes malicious VBA macros embedded in Microsoft Office documents (Word, Excel, PowerPoint) to identify download cradles, payload execution, persistence mechanisms, and anti-analysis techniques. Uses olevba, oledump, and VBA deobfuscation to extract the attack chain. Activates for requests involving Office macro analysis, VBA malware investigation, maldoc analysis, or document-based threat examination. . Use when working with analyzing macro malware in office documents.
  `malware` `macro` `Office` `VBA` `document-malware`

- [analyzing-malicious-pdf-with-peepdf](../cybersecurity/analyzing-malicious-pdf-with-peepdf/) — Perform static analysis of malicious PDF documents using peepdf, pdfid, and pdf-parser to extract embedded JavaScript, shellcode, and suspicious objects. Use when performing static analysis of malicious pdf documents using peepdf, pdfid,.
  `malware-analysis` `pdf` `peepdf` `pdfid` `pdf-parser`

- [analyzing-malicious-url-with-urlscan](../cybersecurity/analyzing-malicious-url-with-urlscan/) — URLScan.io is a free service for scanning and analyzing suspicious URLs. It captures screenshots, DOM content, HTTP transactions, JavaScript behavior, and network connections of web pages in an isolat. Use when working with analyzing malicious url with urlscan.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [analyzing-malware-behavior-with-cuckoo-sandbox](../cybersecurity/analyzing-malware-behavior-with-cuckoo-sandbox/) — Executes malware samples in Cuckoo Sandbox to observe runtime behavior including process creation, file system modifications, registry changes, network communications, and API calls. Generates comprehensive behavioral reports for malware classification and IOC extraction. Activates for requests involving dynamic malware analysis, sandbox detonation, behavioral analysis, or automated malware execution.

  `malware` `dynamic-analysis` `sandbox` `Cuckoo` `behavioral-analysis`

- [analyzing-malware-family-relationships-with-malpedia](../cybersecurity/analyzing-malware-family-relationships-with-malpedia/) — Use the Malpedia platform and API to research malware family relationships, track variant evolution, link families to threat actors, and integrate YARA rules for detection across malware lineages. Use when working with analyzing malware family relationships with malpedia.
  `malpedia` `malware-family` `yara` `threat-actor` `malware-tracking`

- [analyzing-malware-persistence-with-autoruns](../cybersecurity/analyzing-malware-persistence-with-autoruns/) — Use Sysinternals Autoruns to systematically identify and analyze malware persistence mechanisms across registry keys, scheduled tasks, services, drivers, and startup locations on Windows systems. Use when working with analyzing malware persistence with autoruns.
  `autoruns` `persistence` `malware-analysis` `sysinternals` `windows`

- [analyzing-malware-sandbox-evasion-techniques](../cybersecurity/analyzing-malware-sandbox-evasion-techniques/) — Detect sandbox evasion techniques in malware samples by analyzing timing checks, VM artifact queries, user interaction detection, and sleep inflation patterns from Cuckoo/AnyRun behavioral reports. Use when detecting sandbox evasion techniques in malware samples by analyzing timing.
  `sandbox-evasion` `malware-analysis` `cuckoo` `anyrun` `mitre-attack`

- [analyzing-memory-dumps-with-volatility](../cybersecurity/analyzing-memory-dumps-with-volatility/) — Analyzes RAM memory dumps from compromised systems using the Volatility framework to identify malicious processes, injected code, network connections, loaded modules, and extracted credentials. Supports Windows, Linux, and macOS memory forensics. Activates for requests involving memory forensics, RAM analysis, volatile data examination, process injection detection, or memory-resident malware investigation. . Use when working with analyzing memory dumps with volatility.
  `malware` `memory-forensics` `Volatility` `RAM-analysis` `incident-response`

- [analyzing-memory-forensics-with-lime-and-volatility](../cybersecurity/analyzing-memory-forensics-with-lime-and-volatility/) — Performs Linux memory acquisition using LiME (Linux Memory Extractor) kernel module and analysis with Volatility 3 framework. Extracts process lists, network connections, bash history, loaded kernel modules, and injected code from Linux memory images. Use when performing incident response on compromised Linux systems.

  `memory-forensics` `linux-forensics` `lime` `volatility` `incident-response`

- [analyzing-mft-for-deleted-file-recovery](../cybersecurity/analyzing-mft-for-deleted-file-recovery/) — Analyze the NTFS Master File Table ($MFT) to recover metadata and content of deleted files by examining MFT record entries, $LogFile, $UsnJrnl, and MFT slack space using MFTECmd, analyzeMFT, and X-Ways Forensics. Use when analyzeing the ntfs master file table ($mft) to recover metadata.
  `mft` `ntfs` `deleted-files` `file-recovery` `mftecmd`

- [analyzing-network-covert-channels-in-malware](../cybersecurity/analyzing-network-covert-channels-in-malware/) — Detect and analyze covert communication channels used by malware including DNS tunneling, ICMP exfiltration, steganographic HTTP, and protocol abuse for C2 and data exfiltration. Use when detecting and analyze covert communication channels used by malware including.
  `covert-channels` `dns-tunneling` `icmp-exfiltration` `malware-analysis` `network-forensics`

- [analyzing-network-flow-data-with-netflow](../cybersecurity/analyzing-network-flow-data-with-netflow/) — Parse NetFlow v9 and IPFIX records to detect volumetric anomalies, port scanning, data exfiltration, and C2 beaconing patterns. Uses the Python netflow library to decode flow records, builds traffic baselines, and applies statistical analysis to identify flows with abnormal byte counts, connection durations, and periodic timing patterns. Use when working with analyzing network flow data with netflow.
  `analyzing` `network` `flow` `data`

- [analyzing-network-packets-with-scapy](../cybersecurity/analyzing-network-packets-with-scapy/) — Craft, send, sniff, and dissect network packets using Scapy for protocol analysis, network reconnaissance, and traffic anomaly detection in authorized security testing. Use when working with analyzing network packets with scapy.
  `scapy` `packet-analysis` `network-forensics` `protocol-dissection` `pcap`

- [analyzing-network-traffic-for-incidents](../cybersecurity/analyzing-network-traffic-for-incidents/) — Use when analyzes network traffic captures and flow data to identify adversary activity during security incidents, including command-and-control communications, lateral movement, data exfiltration, and exploitation attempts. Uses Wireshark, Zeek, and NetFlow analysis techniques. Activates for requests involving network traffic analysis, packet capture investigation, PCAP analysis, network forensics, C2 traffic detection, or exfiltration detection.
'.
  `network-forensics` `PCAP-analysis` `Wireshark` `Zeek` `traffic-analysis`

- [analyzing-network-traffic-of-malware](../cybersecurity/analyzing-network-traffic-of-malware/) — Analyzes network traffic generated by malware during sandbox execution or live incident response to identify C2 protocols, data exfiltration channels, payload downloads, and lateral movement patterns using Wireshark, Zeek, and Suricata. Activates for requests involving malware network analysis, C2 traffic decoding, malware PCAP analysis, or network-based malware detection. . Use when working with analyzing network traffic of malware.
  `malware` `network-analysis` `PCAP` `Wireshark` `C2-detection`

- [analyzing-network-traffic-with-wireshark](../cybersecurity/analyzing-network-traffic-with-wireshark/) — Captures and analyzes network packet data using Wireshark and tshark to identify malicious traffic patterns, diagnose protocol issues, extract artifacts, and support incident response investigations on authorized network segments. . Use when working with analyzing network traffic with wireshark.
  `network-security` `wireshark` `packet-analysis` `traffic-analysis` `pcap`

- [analyzing-office365-audit-logs-for-compromise](../cybersecurity/analyzing-office365-audit-logs-for-compromise/) — Parse Office 365 Unified Audit Logs via Microsoft Graph API to detect email forwarding rule creation, inbox delegation, suspicious OAuth app grants, and other indicators of account compromise. Use when working with analyzing office365 audit logs for compromise.
  `Office365` `Microsoft-Graph` `audit-logs` `email-compromise` `inbox-rules`

- [analyzing-outlook-pst-for-email-forensics](../cybersecurity/analyzing-outlook-pst-for-email-forensics/) — Analyze Microsoft Outlook PST and OST files for email forensic evidence including message content, headers, attachments, deleted items, and metadata using libpff, pst-utils, and forensic email analysis tools for legal investigations and incident response. Use when analyzeing microsoft outlook pst and ost files for email forensic.
  `email-forensics` `pst` `ost` `outlook` `mapi`

- [analyzing-packed-malware-with-upx-unpacker](../cybersecurity/analyzing-packed-malware-with-upx-unpacker/) — Identifies and unpacks UPX-packed and other packed malware samples to expose the original executable code for static analysis. Covers both standard UPX unpacking and handling modified UPX headers that prevent automated decompression. Activates for requests involving malware unpacking, UPX decompression, packer removal, or preparing packed samples for analysis.

  `malware` `unpacking` `UPX` `packing` `static-analysis`

- [analyzing-pdf-malware-with-pdfid](../cybersecurity/analyzing-pdf-malware-with-pdfid/) — Analyzes malicious PDF files using PDFiD, pdf-parser, and peepdf to identify embedded JavaScript, shellcode, exploits, and suspicious objects without opening the document. Determines the attack vector and extracts embedded payloads for further analysis. Activates for requests involving PDF malware analysis, malicious document analysis, PDF exploit investigation, or suspicious attachment triage. . Use when working with analyzing pdf malware with pdfid.
  `malware` `PDF-analysis` `document-malware` `PDFiD` `static-analysis`

- [analyzing-persistence-mechanisms-in-linux](../cybersecurity/analyzing-persistence-mechanisms-in-linux/) — Detect and analyze Linux persistence mechanisms including crontab entries, systemd service units, LD_PRELOAD hijacking, bashrc modifications, and authorized_keys backdoors using auditd and file integrity monitoring. Use when detecting and analyze linux persistence mechanisms including crontab entries, systemd.
  `linux-persistence` `crontab` `systemd` `ld-preload` `auditd`

- [analyzing-powershell-empire-artifacts](../cybersecurity/analyzing-powershell-empire-artifacts/) — Detect PowerShell Empire framework artifacts in Windows event logs by identifying Base64 encoded launcher patterns, default user agents, staging URL structures, stager IOCs, and known Empire module signatures in Script Block Logging events. Use when detecting powershell empire framework artifacts in windows event logs by.
  `PowerShell-Empire` `threat-hunting` `Script-Block-Logging` `base64` `stager`

- [analyzing-powershell-script-block-logging](../cybersecurity/analyzing-powershell-script-block-logging/) — Parse Windows PowerShell Script Block Logs (Event ID 4104) from EVTX files to detect obfuscated commands, encoded payloads, and living-off-the-land techniques. Uses python-evtx to extract and reconstruct multi-block scripts, applies entropy analysis and pattern matching for Base64-encoded commands, Invoke-Expression abuse, download cradles, and AMSI bypass attempts. Use when working with analyzing powershell script block logging.
  `powershell` `script-block-logging` `event-id-4104` `obfuscation-detection` `windows-forensics`

- [analyzing-prefetch-files-for-execution-history](../cybersecurity/analyzing-prefetch-files-for-execution-history/) — Parse Windows Prefetch files to determine program execution history including run counts, timestamps, and referenced files for forensic investigation. Use when working with analyzing prefetch files for execution history.
  `forensics` `prefetch` `windows-artifacts` `execution-history` `timeline-analysis`

- [analyzing-ransomware-encryption-mechanisms](../cybersecurity/analyzing-ransomware-encryption-mechanisms/) — Analyzes encryption algorithms, key management, and file encryption routines used by ransomware families to assess decryption feasibility, identify implementation weaknesses, and support recovery efforts. Covers AES, RSA, ChaCha20, and hybrid encryption schemes. Activates for requests involving ransomware cryptanalysis, encryption analysis, key recovery assessment, or ransomware decryption feasibility.

  `malware` `ransomware` `encryption` `cryptanalysis` `reverse-engineering`

- [analyzing-ransomware-leak-site-intelligence](../cybersecurity/analyzing-ransomware-leak-site-intelligence/) — Monitor and analyze ransomware group data leak sites (DLS) to track victim postings, extract threat intelligence on group tactics, and assess sector-specific ransomware risk for proactive defense. Use when monitoring and analyze ransomware group data leak sites (dls) to.
  `ransomware` `leak-site` `data-leak` `extortion` `threat-intelligence`

- [analyzing-ransomware-network-indicators](../cybersecurity/analyzing-ransomware-network-indicators/) — Identify ransomware network indicators including C2 beaconing patterns, TOR exit node connections, data exfiltration flows, and encryption key exchange via Zeek conn.log and NetFlow analysis. Use when working with analyzing ransomware network indicators.
  `ransomware` `c2-beaconing` `zeek` `netflow` `tor`

- [analyzing-ransomware-payment-wallets](../cybersecurity/analyzing-ransomware-payment-wallets/) — Traces ransomware cryptocurrency payment flows using blockchain analysis tools such as Chainalysis Reactor, WalletExplorer, and blockchain.com APIs. Identifies wallet clusters, tracks fund movement through mixers and exchanges, and supports law enforcement attribution. Activates for requests involving ransomware payment tracing, bitcoin wallet analysis, cryptocurrency forensics, or blockchain intelligence gathering. . Use when working with analyzing ransomware payment wallets.
  `ransomware` `blockchain` `cryptocurrency` `forensics` `threat-intelligence`

- [analyzing-sbom-for-supply-chain-vulnerabilities](../cybersecurity/analyzing-sbom-for-supply-chain-vulnerabilities/) — Parses Software Bill of Materials (SBOM) in CycloneDX and SPDX JSON formats to identify supply chain vulnerabilities by correlating components against the NVD CVE database via the NVD 2.0 API. Builds dependency graphs, calculates risk scores, identifies transitive vulnerability paths, and generates compliance reports.
  `SBOM` `CycloneDX` `SPDX` `NVD` `CVE`

- [analyzing-security-logs-with-splunk](../cybersecurity/analyzing-security-logs-with-splunk/) — Leverages Splunk Enterprise Security and SPL (Search Processing Language) to investigate security incidents through log correlation, timeline reconstruction, and anomaly detection. Covers Windows event logs, firewall logs, proxy logs, and authentication data analysis. Activates for requests involving Splunk investigation, SPL queries, SIEM log analysis, security event correlation, or log-based incident investigation.

  `splunk` `SPL` `SIEM` `log-analysis` `security-monitoring`

- [analyzing-slack-space-and-file-system-artifacts](../cybersecurity/analyzing-slack-space-and-file-system-artifacts/) — Examine file system slack space, MFT entries, USN journal, and alternate data streams to recover hidden data and reconstruct file activity on NTFS volumes. Use when working with analyzing slack space and file system artifacts.
  `forensics` `slack-space` `ntfs` `mft` `usn-journal`

- [analyzing-supply-chain-malware-artifacts](../cybersecurity/analyzing-supply-chain-malware-artifacts/) — Investigate supply chain attack artifacts including trojanized software updates, compromised build pipelines, and sideloaded dependencies to identify intrusion vectors and scope of compromise. Use when working with analyzing supply chain malware artifacts.
  `supply-chain` `malware-analysis` `trojanized-software` `solarwinds` `3cx`

- [analyzing-threat-actor-ttps-with-mitre-attack](../cybersecurity/analyzing-threat-actor-ttps-with-mitre-attack/) — MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. This skill covers systematically mapping threat actor beh
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [analyzing-threat-actor-ttps-with-mitre-navigator](../cybersecurity/_deprecated/analyzing-threat-actor-ttps-with-mitre-navigator/) — Map advanced persistent threat (APT) group tactics, techniques, and procedures (TTPs) to the MITRE ATT&CK framework using the ATT&CK Navigator and attackcti Python library. The analyst queries STIX/TAXII data for group-technique associations, generates Navigator layer files for visualization, and compares defensive coverage against adversary profiles. Activates for requests involving APT TTP mapping, ATT&CK Navigator layers, threat actor profiling, or MITRE technique coverage analysis.
  `mitre-attack` `navigator` `threat-intelligence` `apt` `ttp-mapping`

- [analyzing-threat-intelligence-feeds](../cybersecurity/analyzing-threat-intelligence-feeds/) — Analyzes structured and unstructured threat intelligence feeds to extract actionable indicators, adversary tactics, and campaign context. Use when ingesting commercial or open-source CTI feeds, evaluating feed quality, normalizing data into STIX 2.1 format, or enriching existing IOCs with campaign attribution. Activates for requests involving ThreatConnect, Recorded Future, Mandiant Advantage, MISP, AlienVault OTX, or automated feed aggregation pipelines.

  `STIX` `TAXII` `MITRE-ATT&CK` `IOC` `ThreatConnect`

- [analyzing-threat-landscape-with-misp](../cybersecurity/analyzing-threat-landscape-with-misp/) — Analyze the threat landscape using MISP (Malware Information Sharing Platform) by querying event statistics, attribute distributions, threat actor galaxy clusters, and tag trends over time. Uses PyMISP to pull event data, compute IOC type breakdowns, identify top threat actors and malware families, and generate threat landscape reports with temporal trends.
  `analyzing` `threat` `landscape` `with`

- [analyzing-tls-certificate-transparency-logs](../cybersecurity/analyzing-tls-certificate-transparency-logs/) — Queries Certificate Transparency logs via crt.sh and pycrtsh to detect phishing domains, unauthorized certificate issuance, and shadow IT. Monitors newly issued certificates for typosquatting and brand impersonation using Levenshtein distance. Use for proactive phishing domain detection and certificate monitoring.

  `analyzing` `tls` `certificate` `transparency`

- [analyzing-typosquatting-domains-with-dnstwist](../cybersecurity/analyzing-typosquatting-domains-with-dnstwist/) — Detect typosquatting, homograph phishing, and brand impersonation domains using dnstwist to generate domain permutations and identify registered lookalike domains targeting your organization.
  `dnstwist` `typosquatting` `phishing` `domain-monitoring` `brand-protection`

- [analyzing-uefi-bootkit-persistence](../cybersecurity/analyzing-uefi-bootkit-persistence/) — Analyzes UEFI bootkit persistence mechanisms including firmware implants in SPI flash, EFI System Partition (ESP) modifications, Secure Boot bypass techniques, and UEFI variable manipulation. Covers detection of known bootkit families (BlackLotus, LoJax, MosaicRegressor, MoonBounce, CosmicStrand), ESP partition forensic inspection, chipsec-based firmware integrity verification, and Secure Boot configuration auditing.
  `UEFI` `bootkit` `firmware` `Secure-Boot` `chipsec`

- [analyzing-usb-device-connection-history](../cybersecurity/analyzing-usb-device-connection-history/) — Investigate USB device connection history from Windows registry, event logs, and setupapi logs to track removable media usage and potential data exfiltration. Use when working with analyzing usb device connection history.
  `forensics` `usb-forensics` `removable-media` `registry-analysis` `data-exfiltration`

- [analyzing-web-server-logs-for-intrusion](../cybersecurity/analyzing-web-server-logs-for-intrusion/) — Parse Apache and Nginx access logs to detect SQL injection attempts, local file inclusion, directory traversal, web scanner fingerprints, and brute-force patterns. Uses regex-based pattern matching against OWASP attack signatures, GeoIP enrichment for source attribution, and statistical anomaly detection for request frequency and response size outliers. Use when working with analyzing web server logs for intrusion.
  `analyzing` `web` `server` `logs`

- [analyzing-windows-amcache-artifacts](../cybersecurity/analyzing-windows-amcache-artifacts/) — Use when parses and analyzes the Windows Amcache.hve registry hive to extract evidence of program execution, application installation, and driver loading for digital forensics investigations. Uses Eric Zimmerman's AmcacheParser and Timeline Explorer for artifact extraction, SHA-1 hash correlation with threat intel, and timeline reconstruction. Activates for requests involving Amcache forensics, program execution evidence, Windows artifact analysis, or application compatibility cache investig...
  `amcache` `windows-forensics` `program-execution` `AmcacheParser` `eric-zimmerman`

- [analyzing-windows-event-logs-in-splunk](../cybersecurity/analyzing-windows-event-logs-in-splunk/) — Analyzes Windows Security, System, and Sysmon event logs in Splunk to detect authentication attacks, privilege escalation, persistence mechanisms, and lateral movement using SPL queries mapped to MITRE ATT&CK techniques. Use when SOC analysts need to investigate Windows-based threats, build detection queries, or perform forensic timeline analysis of Windows endpoints and domain controllers.

  `soc` `splunk` `windows-events` `sysmon` `event-logs`

- [analyzing-windows-lnk-files-for-artifacts](../cybersecurity/_deprecated/analyzing-windows-lnk-files-for-artifacts/) — Parse Windows LNK shortcut files to extract target paths, timestamps, volume information, and machine identifiers for forensic timeline reconstruction. Use when working with analyzing windows lnk files for artifacts.
  `forensics` `lnk-files` `windows-artifacts` `shortcut-analysis` `timeline-reconstruction`

- [analyzing-windows-prefetch-with-python](../cybersecurity/_deprecated/analyzing-windows-prefetch-with-python/) — Parse Windows Prefetch files using the windowsprefetch Python library to reconstruct application execution history, detect renamed or masquerading binaries, and identify suspicious program execution patterns. Use when working with analyzing windows prefetch with python.
  `digital-forensics` `windows` `prefetch` `execution-history` `incident-response`

- [analyzing-windows-registry-for-artifacts](../cybersecurity/analyzing-windows-registry-for-artifacts/) — Extract and analyze Windows Registry hives to uncover user activity, installed software, autostart entries, and evidence of system compromise. Use when working with analyzing windows registry for artifacts.
  `forensics` `windows-registry` `artifact-analysis` `regripper` `registry-explorer`

- [analyzing-windows-shellbag-artifacts](../cybersecurity/analyzing-windows-shellbag-artifacts/) — Analyze Windows Shellbag registry artifacts to reconstruct folder browsing activity, detect access to removable media and network shares, and establish user interaction with directories even after deletion using SBECmd and ShellBags Explorer. Use when analyzeing windows shellbag registry artifacts to reconstruct folder browsing activity,.
  `shellbags` `windows-registry` `sbecmd` `shellbags-explorer` `folder-access`

- [api-destroyer](../cybersecurity/api-destroyer/) — Aggressive API security testing for REST, GraphQL, gRPC, and WebSocket endpoints. Use when testing APIs for authorization flaws, injection, rate limiting bypass, or business logic abuse.
  `api` `aws` `cybersecurity` `destroyer` `graphql`

- [auditing-aws-s3-bucket-permissions](../cybersecurity/auditing-aws-s3-bucket-permissions/) — Systematically audit AWS S3 bucket permissions to identify publicly accessible buckets, overly permissive ACLs, misconfigured bucket policies, and missing encryption settings using AWS CLI, S3audit, and Prowler to enforce least-privilege data access controls. . Use when working with auditing aws s3 bucket permissions.
  `cloud-security` `aws` `s3` `bucket-permissions` `data-protection`

- [auditing-azure-active-directory-configuration](../cybersecurity/auditing-azure-active-directory-configuration/) — Auditing Microsoft Entra ID (Azure Active Directory) configuration to identify risky authentication policies, overly permissive role assignments, stale accounts, conditional access gaps, and guest user risks using AzureAD PowerShell, Microsoft Graph API, and ScoutSuite. . Use when working with auditing azure active directory configuration.
  `cloud-security` `azure` `entra-id` `active-directory` `iam-audit`

- [auditing-cloud-with-cis-benchmarks](../cybersecurity/auditing-cloud-with-cis-benchmarks/) — This skill details how to conduct cloud security audits using Center for Internet Security benchmarks for AWS, Azure, and GCP. It covers interpreting CIS Foundations Benchmark controls, running automated assessments with tools like Prowler and ScoutSuite, remediating failed controls, and maintaining continuous compliance monitoring against CIS v5 for AWS, v4 for Azure, and v4 for GCP.

  `cis-benchmarks` `cloud-audit` `compliance-assessment` `prowler` `security-hardening`

- [auditing-gcp-iam-permissions](../cybersecurity/auditing-gcp-iam-permissions/) — Auditing Google Cloud Platform IAM permissions to identify overly permissive bindings, primitive role usage, service account key proliferation, and cross-project access risks using gcloud CLI, Policy Analyzer, and IAM Recommender. . Use when working with auditing gcp iam permissions.
  `cloud-security` `gcp` `iam` `permissions-audit` `service-accounts`

- [auditing-kubernetes-cluster-rbac](../cybersecurity/auditing-kubernetes-cluster-rbac/) — Auditing Kubernetes cluster RBAC configurations to identify overly permissive roles, wildcard permissions, dangerous ClusterRoleBindings, service account abuse, and privilege escalation paths using kubectl, rbac-tool, KubiScan, and Kubeaudit. . Use when working with auditing kubernetes cluster rbac.
  `cloud-security` `kubernetes` `rbac` `access-control` `eks`

- [auditing-terraform-infrastructure-for-security](../cybersecurity/auditing-terraform-infrastructure-for-security/) — Auditing Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and OPA/Rego policies to detect overly permissive IAM policies, public resource exposure, missing encryption, and insecure defaults before cloud deployment. . Use when working with auditing terraform infrastructure for security.
  `cloud-security` `terraform` `infrastructure-as-code` `checkov` `tfsec`

- [auditing-tls-certificate-transparency-logs](../cybersecurity/auditing-tls-certificate-transparency-logs/) — Monitors Certificate Transparency (CT) logs to detect unauthorized certificate issuance, discover subdomains via CT data, and alert on suspicious certificate activity for owned domains. Uses the crt.sh API and direct CT log querying based on RFC 6962 to build continuous monitoring pipelines that catch rogue certificates, track CA behavior, and map the external attack surface. Use when working with auditing tls certificate transparency logs.
  `certificate-transparency` `CT-logs` `crt-sh` `subdomain-discovery` `TLS-monitoring`

- [auth-killer](../cybersecurity/auth-killer/) — Authentication and authorization bypass specialist — OAuth, SAML, JWT, SSO, MFA bypass. Use when testing login flows, breaking authentication mechanisms, or finding auth bypass vulnerabilities.
  `auth` `cybersecurity` `killer` `security` `testing`

- [automating-ioc-enrichment](../cybersecurity/automating-ioc-enrichment/) — Automates the enrichment of raw indicators of compromise with multi-source threat intelligence context using SOAR platforms, Python pipelines, or TIP playbooks to reduce analyst triage time and standardize enrichment outputs. Use when building automated enrichment workflows integrated with SIEM alerts, email submission pipelines, or bulk IOC processing from threat feeds.
  `SOAR` `enrichment` `IOC` `Cortex-XSOAR` `Splunk-SOAR`

- [bbot-recon](../cybersecurity/bbot-recon/) — Automated reconnaissance using BBOT (Black Lantern Security's recursive internet scanner). Use when performing bug bounty recon, attack surface management, subdomain enumeration, web.
  `bbot` `recon` `bug-bounty` `subdomain-enum` `osint`

- [binary-breaker](../cybersecurity/binary-breaker/) — Binary exploitation and reverse engineering for finding zero-days in compiled software. Use when analyzing binaries, finding memory corruption bugs, reverse engineering firmware, or hunting bugs in C/C++ applications.
  `binary` `breaker` `cybersecurity` `security` `exploit`

- [bounty-target-finder](../cybersecurity/bounty-target-finder/) — Find and prioritize high-paying bug bounty programs. Use when discovering new targets, comparing bounty payouts, filtering programs by scope, or building a target pipeline for continuous hunting.
  `bounty` `cybersecurity` `finder` `money` `pipeline`

- [bug-chain-builder](../cybersecurity/bug-chain-builder/) — Chain multiple low-severity bugs into critical impact for maximum bounty payouts. Use when combining vulnerabilities, escalating impact, or when a single bug isn't enough for a high-severity report.
  `bug` `builder` `chain` `cybersecurity` `security`

- [bug-hunting](../cybersecurity/bug-hunting/) — Automated bug bounty hunting workflow — recon, hunt, validate, report. Use when testing web applications for vulnerabilities, running security assessments, or preparing bug bounty submissions.
  `bug` `cybersecurity` `hunting` `security` `testing`

- [building-adversary-infrastructure-tracking-system](../cybersecurity/building-adversary-infrastructure-tracking-system/) — Build an automated system to track adversary infrastructure using passive DNS, certificate transparency, WHOIS data, and IP enrichment to map and monitor threat actor command-and-control networks.
  `infrastructure-tracking` `passive-dns` `c2` `whois` `threat-actor`

- [building-attack-pattern-library-from-cti-reports](../cybersecurity/building-attack-pattern-library-from-cti-reports/) — Extract and catalog attack patterns from cyber threat intelligence reports into a structured STIX-based library mapped to MITRE ATT&CK for detection engineering and threat-informed defense. Use when working with building attack pattern library from cti reports.
  `attack-pattern` `cti-reports` `mitre-attack` `stix` `detection-engineering`

- [building-automated-malware-submission-pipeline](../cybersecurity/building-automated-malware-submission-pipeline/) — Builds an automated malware submission and analysis pipeline that collects suspicious files from endpoints and email gateways, submits them to sandbox environments and multi-engine scanners, and generates verdicts with IOCs for SIEM integration. Use when SOC teams need to scale malware analysis beyond manual sandbox submissions for high-volume alert triage.

  `soc` `malware-analysis` `sandbox` `automation` `virustotal`

- [building-c2-infrastructure-with-sliver-framework](../cybersecurity/building-c2-infrastructure-with-sliver-framework/) — Build and configure a resilient command-and-control infrastructure using BishopFox's Sliver C2 framework with redirectors, HTTPS listeners, and multi-operator support for authorized red team engagements. Use when building and configure a resilient command-and-control infrastructure using bishopfox's sliver.
  `red-team` `c2-framework` `sliver` `command-and-control` `adversary-simulation`

- [building-cloud-siem-with-sentinel](../cybersecurity/building-cloud-siem-with-sentinel/) — This skill covers deploying Microsoft Sentinel as a cloud-native SIEM and SOAR platform for centralized security operations. It details configuring data connectors for multi-cloud log ingestion, writing KQL detection queries, building automated response playbooks with Logic Apps, and leveraging the Sentinel data lake for petabyte-scale threat hunting across AWS, Azure, and GCP security telemetry.

  `microsoft-sentinel` `cloud-siem` `kql-queries` `soar-automation` `threat-detection`

- [building-detection-rule-with-splunk-spl](../cybersecurity/building-detection-rule-with-splunk-spl/) — Build effective detection rules using Splunk Search Processing Language (SPL) correlation searches to identify security threats in SOC environments. Use when building effective detection rules using splunk search processing language (spl).
  `splunk` `spl` `detection-engineering` `correlation-search` `siem`

- [building-detection-rules-with-sigma](../cybersecurity/building-detection-rules-with-sigma/) — Builds vendor-agnostic detection rules using the Sigma rule format for threat detection across SIEM platforms including Splunk, Elastic, and Microsoft Sentinel. Use when creating portable detection logic from threat intelligence, mapping rules to MITRE ATT&CK techniques, or converting community Sigma rules into platform-specific queries using sigmac or pySigma backends.

  `soc` `sigma` `detection-rules` `siem` `mitre-attack`

- [building-devsecops-pipeline-with-gitlab-ci](../cybersecurity/building-devsecops-pipeline-with-gitlab-ci/) — Design and implement a comprehensive DevSecOps pipeline in GitLab CI/CD integrating SAST, DAST, container scanning, dependency scanning, and secret detection. Use when designing and implement a comprehensive devsecops pipeline in gitlab ci/cd.
  `gitlab-ci` `devsecops` `sast` `dast` `container-scanning`

- [building-identity-federation-with-saml-azure-ad](../cybersecurity/building-identity-federation-with-saml-azure-ad/) — Establish SAML 2.0 identity federation between on-premises Active Directory and Azure AD (Microsoft Entra ID) for seamless cross-domain authentication and SSO to cloud applications. Use when working with building identity federation with saml azure ad.
  `saml` `azure-ad` `entra-id` `federation` `identity`

- [building-identity-governance-lifecycle-process](../cybersecurity/building-identity-governance-lifecycle-process/) — Builds comprehensive identity governance and lifecycle management processes including joiner-mover-leaver automation, role mining, access request workflows, periodic recertification, and orphaned account remediation using IGA platforms. Activates for requests involving identity lifecycle management, JML processes, role-based access provisioning, or identity governance program design. . Use when working with building identity governance lifecycle process.
  `identity-governance` `lifecycle-management` `JML` `access-provisioning` `RBAC`

- [building-incident-response-dashboard](../cybersecurity/building-incident-response-dashboard/) — Builds real-time incident response dashboards in Splunk, Elastic, or Grafana to provide SOC analysts and leadership with situational awareness during active incidents, tracking affected systems, containment status, IOC spread, and response timeline. Use when IR teams need unified visibility during incident coordination and post-incident reporting.

  `soc` `dashboard` `incident-response` `splunk` `visualization`

- [building-incident-response-playbook](../cybersecurity/building-incident-response-playbook/) — Designs and documents structured incident response playbooks that define step-by-step procedures for specific incident types aligned with NIST SP 800-61r3 and SANS PICERL frameworks. Covers playbook structure, decision trees, escalation criteria, RACI matrices, and integration with SOAR platforms. Activates for requests involving IR playbook creation, incident response procedure documentation, response runbook development, or SOAR playbook design.

  `IR-playbook` `runbook` `NIST-800-61` `SOAR-integration` `response-procedures`

- [building-incident-timeline-with-timesketch](../cybersecurity/building-incident-timeline-with-timesketch/) — Build collaborative forensic incident timelines using Timesketch to ingest, normalize, and analyze multi-source event data for attack chain reconstruction and investigation documentation. Use when building collaborative forensic incident timelines using timesketch to ingest, normalize,.
  `timesketch` `timeline-analysis` `forensic-timeline` `plaso` `dfir`

- [building-ioc-defanging-and-sharing-pipeline](../cybersecurity/building-ioc-defanging-and-sharing-pipeline/) — Build an automated pipeline to defang indicators of compromise (URLs, IPs, domains, emails) for safe sharing and distribute them in STIX format through TAXII feeds and threat intelligence platforms.
  `ioc` `defanging` `threat-sharing` `stix` `pipeline`

- [building-ioc-enrichment-pipeline-with-opencti](../cybersecurity/building-ioc-enrichment-pipeline-with-opencti/) — OpenCTI is an open-source platform for managing cyber threat intelligence knowledge, built on STIX 2.1 as its native data model. This skill covers building an automated IOC enrichment pipeline using O
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [building-malware-incident-communication-template](../cybersecurity/building-malware-incident-communication-template/) — Build structured communication templates for malware incidents including stakeholder notifications, executive briefings, technical advisories, and regulatory disclosures with severity-based escalation procedures. Use when building structured communication templates for malware incidents including stakeholder notifications,.
  `incident-communication` `malware-response` `stakeholder-notification` `crisis-communication` `executive-briefing`

- [building-patch-tuesday-response-process](../cybersecurity/building-patch-tuesday-response-process/) — Establish a structured operational process to triage, test, and deploy Microsoft Patch Tuesday security updates within risk-based remediation SLAs. Use when working with building patch tuesday response process.
  `patch-management` `patch-tuesday` `microsoft` `wsus` `sccm`

- [building-phishing-reporting-button-workflow](../cybersecurity/building-phishing-reporting-button-workflow/) — Implement a phishing report button in email clients with automated triage workflow that analyzes user-reported suspicious emails and provides feedback to reporters.
  `phishing-reporting` `email-security` `incident-response` `security-awareness` `outlook`

- [building-ransomware-playbook-with-cisa-framework](../cybersecurity/building-ransomware-playbook-with-cisa-framework/) — Builds a structured ransomware incident response playbook aligned with the CISA StopRansomware Guide and NIST Cybersecurity Framework. Covers preparation, detection, containment, eradication, recovery, and post-incident phases with actionable checklists. Activates for requests involving ransomware response planning, CISA compliance, incident response playbook creation, or ransomware preparedness assessment.

  `ransomware` `incident-response` `CISA` `playbook` `compliance`

- [building-red-team-c2-infrastructure-with-havoc](../cybersecurity/building-red-team-c2-infrastructure-with-havoc/) — Deploy and configure the Havoc C2 framework with teamserver, HTTPS listeners, redirectors, and Demon agents for authorized red team operations. Use when deploying and configure the havoc c2 framework with teamserver, https.
  `havoc-c2` `command-and-control` `red-team-infrastructure` `post-exploitation` `adversary-emulation`

- [building-role-mining-for-rbac-optimization](../cybersecurity/building-role-mining-for-rbac-optimization/) — Apply bottom-up and top-down role mining techniques to discover optimal RBAC roles from existing user-permission assignments, reducing role explosion and enforcing least privilege. Use when working with building role mining for rbac optimization.
  `rbac` `role-mining` `identity-governance` `access-control` `least-privilege`

- [building-soc-escalation-matrix](../cybersecurity/building-soc-escalation-matrix/) — Build a structured SOC escalation matrix defining severity tiers, response SLAs, escalation paths, and notification procedures for security incidents. Use when building a structured soc escalation matrix defining severity tiers, response.
  `soc` `escalation` `incident-management` `severity` `sla`

- [building-soc-metrics-and-kpi-tracking](../cybersecurity/building-soc-metrics-and-kpi-tracking/) — Builds SOC performance metrics and KPI tracking dashboards measuring Mean Time to Detect (MTTD), Mean Time to Respond (MTTR), alert quality ratios, analyst productivity, and detection coverage using SIEM data. Use when SOC leadership needs operational visibility, continuous improvement tracking, or executive-level reporting on security operations effectiveness.

  `soc` `metrics` `kpi` `mttd` `mttr`

- [building-soc-playbook-for-ransomware](../cybersecurity/building-soc-playbook-for-ransomware/) — Builds a structured SOC incident response playbook for ransomware attacks covering detection, containment, eradication, and recovery phases with specific SIEM queries, isolation procedures, and decision trees. Use when SOC teams need formalized response procedures for ransomware incidents aligned to NIST SP 800-61 and MITRE ATT&CK ransomware techniques.

  `soc` `ransomware` `incident-response` `playbook` `nist`

- [building-threat-actor-profile-from-osint](../cybersecurity/building-threat-actor-profile-from-osint/) — Build comprehensive threat actor profiles using open-source intelligence (OSINT) techniques to document adversary motivations, capabilities, infrastructure, and TTPs for proactive defense. Use when building comprehensive threat actor profiles using open-source intelligence (osint) techniques.
  `osint` `threat-actor` `profiling` `maltego` `spiderfoot`

- [building-threat-feed-aggregation-with-misp](../cybersecurity/building-threat-feed-aggregation-with-misp/) — Deploy MISP (Malware Information Sharing Platform) to aggregate, correlate, and distribute threat intelligence feeds from multiple sources for centralized IOC management and automated SIEM integration.
  `misp` `threat-feed` `aggregation` `indicator` `sharing`

- [building-threat-hunt-hypothesis-framework](../cybersecurity/building-threat-hunt-hypothesis-framework/) — Build a systematic threat hunt hypothesis framework that transforms threat intelligence, attack patterns, and environmental data into testable hunting hypotheses. Use when building a systematic threat hunt hypothesis framework that transforms threat.
  `threat-hunting` `methodology` `hypothesis` `threat-intelligence` `hunting-framework`

- [building-threat-intelligence-enrichment-in-splunk](../cybersecurity/building-threat-intelligence-enrichment-in-splunk/) — Build automated threat intelligence enrichment pipelines in Splunk Enterprise Security using lookup tables, modular inputs, and the Threat Intelligence Framework.
  `splunk` `threat-intelligence` `enrichment` `ioc` `lookup`

- [building-threat-intelligence-feed-integration](../cybersecurity/building-threat-intelligence-feed-integration/) — Builds automated threat intelligence feed integration pipelines connecting STIX/TAXII feeds, open-source threat intel, and commercial TI platforms into SIEM and security tools for real-time IOC matching and alerting. Use when SOC teams need to operationalize threat intelligence by automating feed ingestion, normalization, scoring, and distribution to detection systems.

  `soc` `threat-intelligence` `stix` `taxii` `misp`

- [building-threat-intelligence-platform](../cybersecurity/building-threat-intelligence-platform/) — Building a Threat Intelligence Platform (TIP) involves deploying and integrating multiple CTI tools into a unified system for collecting, analyzing, enriching, and disseminating threat intelligence. T. Use when working with building threat intelligence platform.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [building-vulnerability-aging-and-sla-tracking](../cybersecurity/building-vulnerability-aging-and-sla-tracking/) — Implement a vulnerability aging dashboard and SLA tracking system to measure remediation performance against severity-based timelines and drive accountability. Use when implementing a vulnerability aging dashboard and sla tracking system to.
  `vulnerability-management` `sla-tracking` `remediation-metrics` `aging-report` `kpi`

- [building-vulnerability-dashboard-with-defectdojo](../cybersecurity/building-vulnerability-dashboard-with-defectdojo/) — Deploy DefectDojo as a centralized vulnerability management dashboard with scanner integrations, deduplication, metrics tracking, and Jira ticketing workflows. Use when deploying defectdojo as a centralized vulnerability management dashboard with scanner.
  `defectdojo` `vulnerability-management` `dashboard` `deduplication` `scanner-integration`

- [building-vulnerability-exception-tracking-system](../cybersecurity/building-vulnerability-exception-tracking-system/) — Build a vulnerability exception and risk acceptance tracking system with approval workflows, compensating controls documentation, and expiration management. Use when building a vulnerability exception and risk acceptance tracking system with.
  `vulnerability-exception` `risk-acceptance` `compensating-controls` `exception-tracking` `vulnerability-management`

- [building-vulnerability-scanning-workflow](../cybersecurity/building-vulnerability-scanning-workflow/) — Builds a structured vulnerability scanning workflow using tools like Nessus, Qualys, and OpenVAS to discover, prioritize, and track remediation of security vulnerabilities across infrastructure. Use when SOC teams need to establish recurring vulnerability assessment processes, integrate scan results with SIEM alerting, and build remediation tracking dashboards.

  `soc` `vulnerability-scanning` `nessus` `qualys` `openvas`

- [bypassing-authentication-with-forced-browsing](../cybersecurity/bypassing-authentication-with-forced-browsing/) — Discovering and accessing unprotected pages, APIs, and administrative interfaces by enumerating URLs and bypassing authentication controls during authorized security assessments. Use when working with bypassing authentication with forced browsing.
  `penetration-testing` `authentication-bypass` `forced-browsing` `ffuf` `directory-enumeration`

- [cloud-hunter](../cybersecurity/cloud-hunter/) — Cloud infrastructure misconfiguration hunting for AWS, GCP, and Azure. Use when testing cloud assets, finding exposed S3 buckets, hunting IAM misconfigs, or testing serverless applications.
  `aws` `azure` `cloud` `cybersecurity` `gcp`

- [collecting-indicators-of-compromise](../cybersecurity/collecting-indicators-of-compromise/) — Systematically collects, categorizes, and distributes indicators of compromise (IOCs) during and after security incidents to enable detection, blocking, and threat intelligence sharing. Covers network, host, email, and behavioral indicators using STIX/TAXII formats and threat intelligence platforms. Activates for requests involving IOC collection, indicator extraction, threat indicator sharing, compromise indicators, STIX export, or IOC enrichment.

  `IOC-collection` `threat-indicators` `STIX-TAXII` `MISP` `threat-intelligence-sharing`

- [collecting-threat-intelligence-with-misp](../cybersecurity/collecting-threat-intelligence-with-misp/) — MISP (Malware Information Sharing Platform) is an open-source threat intelligence platform for gathering, sharing, storing, and correlating Indicators of Compromise (IOCs) of targeted attacks, threat. Use when working with collecting threat intelligence with misp.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [collecting-volatile-evidence-from-compromised-host](../cybersecurity/collecting-volatile-evidence-from-compromised-host/) — Collect volatile forensic evidence from a compromised system following order of volatility, preserving memory, network connections, processes, and system state before they are lost. Use when working with collecting volatile evidence from compromised host.
  `incident-response` `dfir` `forensics` `volatile-evidence` `memory-forensics`

- [conducting-api-security-testing](../cybersecurity/conducting-api-security-testing/) — Conducts security testing of REST, GraphQL, and gRPC APIs to identify vulnerabilities in authentication, authorization, rate limiting, input validation, and business logic. The tester uses the OWASP API Security Top 10 as the testing framework, combining Burp Suite interception with Postman collections and custom scripts to test endpoint security at every privilege level. Use when working with conducting api security testing.
  `API-security` `OWASP-API-Top10` `REST` `GraphQL` `authorization-testing`

- [conducting-cloud-incident-response](../cybersecurity/conducting-cloud-incident-response/) — Responds to security incidents in cloud environments (AWS, Azure, GCP) by performing identity-based containment, cloud-native log analysis, resource isolation, and forensic evidence acquisition adapted for ephemeral cloud infrastructure. Activates for requests involving cloud incident response, AWS security incident, Azure compromise, GCP breach, cloud forensics, or cloud identity compromise. . Use when working with conducting cloud incident response.
  `cloud-IR` `AWS-forensics` `Azure-incident-response` `GCP-security` `identity-containment`

- [conducting-cloud-penetration-testing](../cybersecurity/conducting-cloud-penetration-testing/) — This skill outlines methodologies for performing authorized penetration testing against AWS, Azure, and GCP cloud environments. It covers understanding the shared responsibility model for testing scope, leveraging cloud-specific attack tools like Pacu and ScoutSuite, exploiting IAM misconfigurations, testing for SSRF to cloud metadata services, and reporting findings aligned to MITRE ATT&CK Cloud matrix.

  `cloud-pentesting` `offensive-security` `aws-exploitation` `shared-responsibility` `mitre-attack-cloud`

- [conducting-domain-persistence-with-dcsync](../cybersecurity/conducting-domain-persistence-with-dcsync/) — Perform DCSync attacks to replicate Active Directory credentials and establish domain persistence by extracting KRBTGT, Domain Admin, and service account hashes for Golden Ticket creation. Use when performing dcsync attacks to replicate active directory credentials and establish.
  `red-team` `active-directory` `dcsync` `persistence` `credential-dumping`

- [conducting-external-reconnaissance-with-osint](../cybersecurity/conducting-external-reconnaissance-with-osint/) — Conducts external reconnaissance using Open Source Intelligence (OSINT) techniques to map an organization's external attack surface without directly interacting with target systems. The tester gathers information from public sources including DNS records, certificate transparency logs, search engines, social media, code repositories, and data breach databases to build a comprehensive target profile. Use when working with conducting external reconnaissance with osint.
  `OSINT` `reconnaissance` `attack-surface` `footprinting` `passive-recon`

- [conducting-full-scope-red-team-engagement](../cybersecurity/conducting-full-scope-red-team-engagement/) — Plan and execute a comprehensive red team engagement covering reconnaissance through post-exploitation using MITRE ATT&CK-aligned TTPs to evaluate an organization's detection and response capabilities. Use when working with conducting full scope red team engagement.
  `red-team` `adversary-emulation` `mitre-attack` `penetration-testing` `offensive-security`

- [conducting-internal-network-penetration-test](../cybersecurity/conducting-internal-network-penetration-test/) — Execute an internal network penetration test simulating an insider threat or post-breach attacker to identify lateral movement paths, privilege escalation vectors, and sensitive data exposure within the corporate network. Use when working with conducting internal network penetration test.
  `internal-pentest` `lateral-movement` `privilege-escalation` `Responder` `Impacket`

- [conducting-internal-reconnaissance-with-bloodhound-ce](../cybersecurity/conducting-internal-reconnaissance-with-bloodhound-ce/) — Conduct internal Active Directory reconnaissance using BloodHound Community Edition to map attack paths, identify privilege escalation chains, and discover misconfigurations in domain environments. Use when conducting internal active directory reconnaissance using bloodhound community edition to.
  `red-team` `reconnaissance` `bloodhound` `active-directory` `attack-paths`

- [conducting-malware-incident-response](../cybersecurity/conducting-malware-incident-response/) — Responds to malware infections across enterprise endpoints by identifying the malware family, determining infection vectors, assessing spread, and executing eradication procedures. Covers the full lifecycle from detection through containment, analysis, removal, and recovery. Activates for requests involving malware response, malware eradication, trojan removal, worm containment, malware triage, or infected endpoint remediation.

  `malware-response` `malware-analysis` `eradication` `endpoint-remediation` `MITRE-ATT&CK`

- [conducting-man-in-the-middle-attack-simulation](../cybersecurity/conducting-man-in-the-middle-attack-simulation/) — Simulates man-in-the-middle attacks using Ettercap, mitmproxy, and Bettercap in authorized environments to intercept, analyze, and modify network traffic for testing encryption enforcement, certificate validation, and detection capabilities. . Use when working with conducting man in the middle attack simulation.
  `network-security` `mitm` `bettercap` `ettercap` `mitmproxy`

- [conducting-memory-forensics-with-volatility](../cybersecurity/_deprecated/conducting-memory-forensics-with-volatility/) — Performs memory forensics analysis using Volatility 3 to extract evidence of malware execution, process injection, network connections, and credential theft from RAM dumps captured during incident response. Covers memory acquisition, process analysis, DLL inspection, and malware detection. Activates for requests involving memory forensics, RAM analysis, Volatility framework, memory dump investigation, volatile evidence analysis, or live memory acquisition.

  `memory-forensics` `volatility` `RAM-analysis` `process-injection` `DFIR`

- [conducting-mobile-app-penetration-test](../cybersecurity/conducting-mobile-app-penetration-test/) — Use when conducts penetration testing of iOS and Android mobile applications following the OWASP Mobile Application Security Testing Guide (MASTG) to identify vulnerabilities in data storage, network communication, authentication, cryptography, and platform-specific security controls. The tester performs static analysis of application binaries, dynamic analysis at runtime, and API security testing to evaluate the complete mobile attack surface.
  `mobile-pentest` `OWASP-MASTG` `Android-security` `iOS-security` `mobile-application-security`

- [conducting-network-penetration-test](../cybersecurity/conducting-network-penetration-test/) — Conducts comprehensive network penetration tests against authorized target environments by performing host discovery, port scanning, service enumeration, vulnerability identification, and controlled exploitation to assess the security posture of network infrastructure. The tester follows PTES methodology from reconnaissance through post-exploitation and reporting. Use when working with conducting network penetration test.
  `network-pentest` `Nmap` `Metasploit` `vulnerability-exploitation` `infrastructure-security`

- [conducting-pass-the-ticket-attack](../cybersecurity/conducting-pass-the-ticket-attack/) — Pass-the-Ticket (PtT) is a lateral movement technique that uses stolen Kerberos tickets (TGT or TGS) to authenticate to services without knowing the user's password. By extracting Kerberos tickets fro. Use when working with conducting pass the ticket attack.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [conducting-phishing-incident-response](../cybersecurity/conducting-phishing-incident-response/) — Responds to phishing incidents by analyzing reported emails, extracting indicators, assessing credential compromise, quarantining malicious messages across the organization, and remediating affected accounts. Covers email header analysis, URL/attachment sandboxing, and mailbox-wide purge operations. Activates for requests involving phishing response, email incident, credential phishing, spear phishing investigation, or phishing remediation.

  `phishing-response` `email-security` `credential-compromise` `email-header-analysis` `mailbox-remediation`

- [conducting-post-incident-lessons-learned](../cybersecurity/conducting-post-incident-lessons-learned/) — Facilitate structured post-incident reviews to identify root causes, document what worked and failed, and produce actionable recommendations to improve future incident response. Use when working with conducting post incident lessons learned.
  `incident-response` `lessons-learned` `post-incident` `after-action-review` `process-improvement`

- [conducting-social-engineering-penetration-test](../cybersecurity/conducting-social-engineering-penetration-test/) — Design and execute a social engineering penetration test including phishing, vishing, smishing, and physical pretexting campaigns to measure human security resilience and identify training gaps. Use when designing and execute a social engineering penetration test including phishing,.
  `social-engineering` `phishing` `vishing` `pretexting` `GoPhish`

- [conducting-social-engineering-pretext-call](../cybersecurity/conducting-social-engineering-pretext-call/) — Plan and execute authorized vishing (voice phishing) pretext calls to assess employee susceptibility to social engineering and evaluate security awareness controls. Use when working with conducting social engineering pretext call.
  `social-engineering` `vishing` `pretext-call` `security-awareness` `red-team`

- [conducting-spearphishing-simulation-campaign](../cybersecurity/conducting-spearphishing-simulation-campaign/) — Spearphishing simulation is a targeted social engineering attack vector used by red teams to gain initial access. Unlike broad phishing campaigns, spearphishing uses OSINT-derived intelligence to craf. Use when working with conducting spearphishing simulation campaign.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [conducting-wireless-network-penetration-test](../cybersecurity/conducting-wireless-network-penetration-test/) — Conducts authorized wireless network penetration tests to assess the security of WiFi infrastructure by testing for weak encryption protocols, captive portal bypasses, evil twin attacks, WPA2/WPA3 handshake capture, rogue access point detection, and client-side attacks. The tester evaluates wireless authentication, network segmentation, and the effectiveness of wireless intrusion detection systems. Use when working with conducting wireless network penetration test.
  `wireless-pentest` `WiFi-security` `WPA2` `WPA3` `evil-twin`

- [configuring-active-directory-tiered-model](../cybersecurity/configuring-active-directory-tiered-model/) — Implement Microsoft's Enhanced Security Admin Environment (ESAE) tiered administration model for Active Directory. Covers Tier 0/1/2 separation, privileged access workstations (PAWs), administrative f
  `iam` `identity` `access-control` `active-directory` `tiered-model`

- [configuring-aws-verified-access-for-ztna](../cybersecurity/configuring-aws-verified-access-for-ztna/) — Configure AWS Verified Access to provide VPN-less zero trust network access to internal applications using identity and device posture verification with Cedar policy language. Use when configureing aws verified access to provide vpn-less zero trust network.
  `zero-trust` `aws` `verified-access` `ztna` `cedar-policy`

- [configuring-certificate-authority-with-openssl](../cybersecurity/configuring-certificate-authority-with-openssl/) — A Certificate Authority (CA) is the trust anchor in a PKI hierarchy, responsible for issuing, signing, and revoking digital certificates. This skill covers building a two-tier CA hierarchy (Root CA +
  `cryptography` `pki` `certificate-authority` `openssl` `x509`

- [configuring-host-based-intrusion-detection](../cybersecurity/configuring-host-based-intrusion-detection/) — Configures host-based intrusion detection systems (HIDS) to monitor endpoint file integrity, system calls, and configuration changes for security violations. Use when deploying OSSEC, Wazuh, or AIDE for endpoint monitoring, building file integrity monitoring (FIM) policies, or meeting compliance requirements for change detection. Activates for requests involving HIDS configuration, file integrity monitoring, OSSEC/Wazuh deployment, or host-based detection.

  `endpoint` `HIDS` `Wazuh` `OSSEC` `file-integrity-monitoring`

- [configuring-hsm-for-key-storage](../cybersecurity/configuring-hsm-for-key-storage/) — Hardware Security Modules (HSMs) are tamper-resistant physical devices that safeguard cryptographic keys and perform cryptographic operations in a hardened environment. Keys stored in an HSM never lea. Use when working with configuring hsm for key storage.
  `cryptography` `hsm` `key-management` `pkcs11` `hardware-security`

- [configuring-identity-aware-proxy-with-google-iap](../cybersecurity/configuring-identity-aware-proxy-with-google-iap/) — Configuring Google Cloud Identity-Aware Proxy (IAP) to enforce per-request identity verification for Compute Engine, App Engine, Cloud Run, and GKE services using access levels, context-aware policies, and programmatic access with service accounts. . Use when working with configuring identity aware proxy with google iap.
  `google-iap` `identity-aware-proxy` `gcp` `zero-trust` `access-context-manager`

- [configuring-ldap-security-hardening](../cybersecurity/configuring-ldap-security-hardening/) — Harden LDAP directory services against common attacks including credential harvesting, LDAP injection, anonymous binding, and channel binding bypass. Covers LDAPS enforcement, channel binding, LDAP si
  `iam` `identity` `access-control` `ldap` `directory-services`

- [configuring-microsegmentation-for-zero-trust](../cybersecurity/configuring-microsegmentation-for-zero-trust/) — Configure microsegmentation policies to enforce least-privilege workload-to-workload access using tools like VMware NSX, Illumio, and Calico, preventing lateral movement in zero trust architectures. Use when configureing microsegmentation policies to enforce least-privilege workload-to-workload access using tools.
  `zero-trust` `microsegmentation` `network-access` `lateral-movement` `network-security`

- [configuring-multi-factor-authentication-with-duo](../cybersecurity/configuring-multi-factor-authentication-with-duo/) — Deploy Cisco Duo multi-factor authentication across enterprise applications, VPN, RDP, and SSH access points. This skill covers Duo integration methods, adaptive authentication policies, device trust
  `iam` `identity` `access-control` `authentication` `mfa`

- [configuring-network-segmentation-with-vlans](../cybersecurity/configuring-network-segmentation-with-vlans/) — Designs and implements VLAN-based network segmentation on managed switches to isolate network zones, enforce access control between segments, and reduce the attack surface by limiting lateral movement paths in enterprise network environments. . Use when working with configuring network segmentation with vlans.
  `network-security` `vlan` `network-segmentation` `switch-security` `802.1q`

- [configuring-oauth2-authorization-flow](../cybersecurity/configuring-oauth2-authorization-flow/) — Configure secure OAuth 2.0 authorization flows including Authorization Code with PKCE, Client Credentials, and Device Authorization Grant. This skill covers flow selection, PKCE implementation, token
  `iam` `identity` `access-control` `authentication` `authorization`

- [configuring-pfsense-firewall-rules](../cybersecurity/configuring-pfsense-firewall-rules/) — Configures pfSense firewall rules, NAT policies, VPN tunnels, and traffic shaping to enforce network segmentation, control traffic flow, and protect internal network zones in enterprise and small-to-medium business environments. . Use when working with configuring pfsense firewall rules.
  `network-security` `pfsense` `firewall` `nat` `network-segmentation`

- [configuring-snort-ids-for-intrusion-detection](../cybersecurity/configuring-snort-ids-for-intrusion-detection/) — Installs, configures, and tunes Snort 3 intrusion detection system to monitor network traffic for malicious activity using custom and community rulesets, preprocessors, and alert output plugins on authorized network segments. . Use when working with configuring snort ids for intrusion detection.
  `network-security` `snort` `ids` `intrusion-detection` `rule-writing`

- [configuring-suricata-for-network-monitoring](../cybersecurity/configuring-suricata-for-network-monitoring/) — Deploys and configures Suricata IDS/IPS with Emerging Threats rulesets, EVE JSON logging, and custom rules for real-time network traffic inspection, threat detection, and integration with SIEM platforms for centralized security monitoring. . Use when working with configuring suricata for network monitoring.
  `network-security` `suricata` `ids` `ips` `network-monitoring`

- [configuring-tls-1-3-for-secure-communications](../cybersecurity/configuring-tls-1-3-for-secure-communications/) — TLS 1.3 (RFC 8446) is the latest version of the Transport Layer Security protocol, providing significant improvements over TLS 1.2 in both security and performance. It reduces handshake latency to 1-R. Use when working with configuring tls 1 3 for secure communications.
  `cryptography` `tls` `ssl` `transport-security` `network-security`

- [configuring-windows-defender-advanced-settings](../cybersecurity/configuring-windows-defender-advanced-settings/) — Configures Microsoft Defender for Endpoint (MDE) advanced protection settings including attack surface reduction rules, controlled folder access, network protection, and exploit protection. Use when hardening Windows endpoints beyond default Defender settings, deploying enterprise-grade endpoint protection, or meeting compliance requirements for advanced malware defense. Activates for requests involving Windows Defender configuration, ASR rules, MDE tuning, or Microsoft endpoint securit.
  `endpoint` `windows-security` `Microsoft-Defender` `ASR` `exploit-protection`

- [configuring-windows-event-logging-for-detection](../cybersecurity/configuring-windows-event-logging-for-detection/) — Configures Windows Event Logging with advanced audit policies to generate high-fidelity security events for threat detection and forensic investigation. Use when enabling audit policies for logon events, process creation, privilege use, and object access to feed SIEM detection rules. Activates for requests involving Windows audit policy, event log configuration, security logging, or detection-oriented logging.

  `endpoint` `windows-security` `event-logging` `audit-policy` `detection-engineering`

- [configuring-zscaler-private-access-for-ztna](../cybersecurity/configuring-zscaler-private-access-for-ztna/) — Configuring Zscaler Private Access (ZPA) to replace traditional VPN with zero trust network access by deploying App Connectors, defining application segments, configuring access policies based on user identity and device posture, and integrating with IdPs. . Use when working with configuring zscaler private access for ztna.
  `zscaler` `zpa` `ztna` `zero-trust` `app-connector`

- [containing-active-breach](../cybersecurity/containing-active-breach/) — Use when executes containment strategies to stop active adversary operations and prevent lateral movement during a confirmed security breach. Implements short-term and long-term containment using network segmentation, endpoint isolation, credential revocation, and access control modifications. Activates for requests involving breach containment, lateral movement prevention, network isolation, active threat containment, or live incident response.
'.
  `breach-containment` `lateral-movement` `network-isolation` `credential-revocation` `live-response`

- [continuous-hunter](../cybersecurity/continuous-hunter/) — Automated continuous bug hunting pipeline that runs 24/7 across multiple targets. Use when setting up persistent hunting, automating the find-report cycle, or scaling bug bounty income through automation.
  `continuous` `cybersecurity` `hunter` `pipeline` `security`

- [correlating-security-events-in-qradar](../cybersecurity/correlating-security-events-in-qradar/) — Correlates security events in IBM QRadar SIEM using AQL (Ariel Query Language), custom rules, building blocks, and offense management to detect multi-stage attacks across network, endpoint, and application log sources. Use when SOC analysts need to investigate QRadar offenses, build correlation rules, or tune detection logic for reducing false positives.

  `soc` `qradar` `siem` `aql` `correlation`

- [correlating-threat-campaigns](../cybersecurity/correlating-threat-campaigns/) — Correlates disparate security incidents, IOCs, and adversary behaviors across time and organizations to identify unified threat campaigns, attribute them to common threat actors, and extract shared indicators for improved detection. Use when multiple incidents exhibit overlapping indicators, when sector-wide attack campaigns require cross-organizational analysis, or when building campaign-level intelligence products.
  `campaign-analysis` `correlation` `MISP` `ATT&CK` `threat-actor`

- [crypto-breaker](../cybersecurity/crypto-breaker/) — Cryptographic attack techniques for breaking implementations, side-channel attacks, and exploiting crypto weaknesses. Use when assessing crypto implementations, finding side-channel leaks, or breaking custom cryptography.
  `breaker` `crypto` `cybersecurity` `security` `threat-defense`

- [decepticon-red-team](../cybersecurity/decepticon-red-team/) — Autonomous red team agent executing full attack chains with domain specialists. Use when running autonomous red team operations, simulating end-to-end attack chains, or planning engagements.
  `red-team` `autonomous` `attack-chain` `mitre-attack` `engagement-planning`

- [defi-incident-analysis](../cybersecurity/defi-incident-analysis/) — Analyze DeFi security incidents including flash loan attacks, oracle manipulation, reentrancy exploits, bridge hacks, and governance attacks to reconstruct attack chains and identify root causes. Use when investigating DeFi protocol exploits, analyzing smart contract attacks, or writing incident post-mortems.
  `blockchain` `defi` `incident` `analysis` `flash-loan`

- [deobfuscating-javascript-malware](../cybersecurity/deobfuscating-javascript-malware/) — Deobfuscates malicious JavaScript code used in web-based attacks, phishing pages, and dropper scripts by reversing encoding layers, eval chains, string manipulation, and control flow obfuscation to reveal the original malicious logic. Activates for requests involving JavaScript malware analysis, script deobfuscation, web skimmer analysis, or obfuscated dropper investigation. . Use when working with deobfuscating javascript malware.
  `malware` `JavaScript` `deobfuscation` `web-malware` `script-analysis`

- [deobfuscating-powershell-obfuscated-malware](../cybersecurity/deobfuscating-powershell-obfuscated-malware/) — Systematically deobfuscate multi-layer PowerShell malware using AST analysis, dynamic tracing, and tools like PSDecode and PowerDecode to reveal hidden payloads and C2 infrastructure. Use when working with deobfuscating powershell obfuscated malware.
  `powershell` `deobfuscation` `malware-analysis` `scripting` `obfuscation`

- [deploying-active-directory-honeytokens](../cybersecurity/deploying-active-directory-honeytokens/) — Deploys deception-based honeytokens in Active Directory including fake privileged accounts with AdminCount=1, fake SPNs for Kerberoasting detection (honeyroasting), decoy GPOs with cpassword traps, and fake BloodHound paths. Monitors Windows Security Event IDs 4769, 4625, 4662, 5136 for honeytoken interaction. Use when implementing AD deception defenses for detecting lateral movement, credential theft, and reconnaissance.

  `active-directory` `honeytokens` `kerberoasting` `deception` `detection`

- [deploying-cloudflare-access-for-zero-trust](../cybersecurity/deploying-cloudflare-access-for-zero-trust/) — Deploying Cloudflare Access with Cloudflare Tunnel to provide zero trust access to self-hosted and private applications, configuring identity-aware access policies, device posture checks, and WARP client enrollment for VPN replacement. . Use when working with deploying cloudflare access for zero trust.
  `cloudflare` `cloudflare-access` `zero-trust` `cloudflare-tunnel` `warp`

- [deploying-decoy-files-for-ransomware-detection](../cybersecurity/deploying-decoy-files-for-ransomware-detection/) — Use when deploys canary files (honeytokens) across file systems to detect ransomware encryption activity in real time. Uses strategically placed decoy documents monitored via file integrity monitoring or OS-level watchdogs to trigger alerts when ransomware modifies or encrypts them. Activates for requests involving ransomware canary deployment, honeyfile setup, deception-based ransomware detection, or file integrity monitoring for encryption.
'.
  `ransomware` `detection` `canary-files` `honeytokens` `deception`

- [deploying-edr-agent-with-crowdstrike](../cybersecurity/deploying-edr-agent-with-crowdstrike/) — Deploys and configures CrowdStrike Falcon EDR agents across enterprise endpoints to enable real-time threat detection, behavioral analysis, and automated response. Use when onboarding endpoints to EDR coverage, configuring detection policies, or integrating Falcon telemetry with SIEM platforms. Activates for requests involving CrowdStrike deployment, Falcon sensor installation, EDR policy configuration, or endpoint detection and response.

  `endpoint` `edr` `CrowdStrike` `Falcon` `threat-detection`

- [deploying-osquery-for-endpoint-monitoring](../cybersecurity/deploying-osquery-for-endpoint-monitoring/) — Deploys and configures osquery for real-time endpoint monitoring using SQL-based queries to inspect running processes, open ports, installed software, and system configuration. Use when building visibility into endpoint state, threat hunting across fleet, or implementing compliance monitoring. Activates for requests involving osquery deployment, endpoint visibility, fleet management, or SQL-based endpoint querying.

  `endpoint` `osquery` `endpoint-monitoring` `threat-hunting` `fleet-management`

- [deploying-palo-alto-prisma-access-zero-trust](../cybersecurity/deploying-palo-alto-prisma-access-zero-trust/) — Deploying Palo Alto Networks Prisma Access for SASE-based zero trust network access using GlobalProtect agents, ZTNA Connectors, security policy enforcement, and integration with Strata Cloud Manager for unified security management. . Use when working with deploying palo alto prisma access zero trust.
  `prisma-access` `palo-alto` `ztna` `sase` `globalprotect`

- [deploying-ransomware-canary-files](../cybersecurity/deploying-ransomware-canary-files/) — Deploys and monitors ransomware canary files across critical directories using Python's watchdog library for real-time filesystem event detection. Places strategically named decoy files that mimic high-value targets (financial records, credentials, database exports) in locations ransomware typically enumerates first. Use when working with deploying ransomware canary files.
  `ransomware` `canary-files` `watchdog` `detection` `early-warning`

- [deploying-software-defined-perimeter](../cybersecurity/deploying-software-defined-perimeter/) — Deploy a Software-Defined Perimeter using the CSA v2.0 specification with Single Packet Authorization, mutual TLS, and SDP controller/gateway configuration to enforce zero trust network access. Use when deploying a software-defined perimeter using the csa v2.0 specification with.
  `zero-trust` `sdp` `software-defined-perimeter` `network-access` `ztna`

- [deploying-tailscale-for-zero-trust-vpn](../cybersecurity/deploying-tailscale-for-zero-trust-vpn/) — Deploy and configure Tailscale as a WireGuard-based zero trust mesh VPN with identity-aware access controls, ACLs, and exit nodes for secure peer-to-peer connectivity. Use when deploying and configure tailscale as a wireguard-based zero trust mesh.
  `zero-trust` `tailscale` `wireguard` `mesh-vpn` `ztna`

- [detecting-ai-model-prompt-injection-attacks](../cybersecurity/detecting-ai-model-prompt-injection-attacks/) — Use when detects prompt injection attacks targeting LLM-based applications using a multi-layered defense combining regex pattern matching for known attack signatures, heuristic scoring for structural anomalies, and transformer-based classification with DeBERTa models. The detector analyzes user inputs before they reach the LLM, flagging direct injections (system prompt overrides, role-play escapes, instruction hijacking) and indirect injections (encoded payloads, multi-language obfuscation, d...
  `prompt-injection` `LLM-security` `OWASP-LLM-Top10` `NLP-classification` `input-validation`

- [detecting-anomalies-in-industrial-control-systems](../cybersecurity/detecting-anomalies-in-industrial-control-systems/) — This skill covers deploying anomaly detection systems for industrial control environments using machine learning models trained on OT network baselines, physics-based process models, and behavioral analysis of industrial protocol communications. It addresses building normal behavior profiles for SCADA polling patterns, detecting deviations in Modbus/DNP3/OPC UA traffic, identifying rogue devices, and correlating network anomalies with physical process data from historians.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [detecting-anomalous-authentication-patterns](../cybersecurity/detecting-anomalous-authentication-patterns/) — Detects anomalous authentication patterns using UEBA analytics, statistical baselines, and machine learning models to identify impossible travel, credential stuffing, brute force, password spraying, and compromised account behaviors across authentication logs. Activates for requests involving authentication anomaly detection, login behavior analysis, UEBA implementation, or suspicious sign-in investigation. . Use when working with detecting anomalous authentication patterns.
  `UEBA` `authentication-anomaly` `impossible-travel` `brute-force` `credential-stuffing`

- [detecting-api-enumeration-attacks](../cybersecurity/detecting-api-enumeration-attacks/) — Detect and prevent API enumeration attacks including BOLA and IDOR exploitation by monitoring sequential identifier access patterns and authorization failures. Use when detecting and prevent api enumeration attacks including bola and idor.
  `api-security` `enumeration` `bola` `idor` `broken-object-level-authorization`

- [detecting-arp-poisoning-in-network-traffic](../cybersecurity/detecting-arp-poisoning-in-network-traffic/) — Detect and prevent ARP spoofing attacks using ARPWatch, Dynamic ARP Inspection, Wireshark analysis, and custom monitoring scripts to protect against man-in-the-middle interception. Use when detecting and prevent arp spoofing attacks using arpwatch, dynamic arp.
  `arp-poisoning` `arp-spoofing` `mitm` `dynamic-arp-inspection` `arpwatch`

- [detecting-attacks-on-historian-servers](../cybersecurity/detecting-attacks-on-historian-servers/) — Detect cyber attacks targeting OT historian servers (OSIsoft PI, Ignition, Wonderware) that sit at the IT/OT boundary and serve as pivot points for lateral movement between enterprise and control networks, including data manipulation, unauthorized queries, and exploitation of historian-specific vulnerabilities. . Use when working with detecting attacks on historian servers.
  `ot-security` `ics` `historian` `osisoft-pi` `ignition`

- [detecting-attacks-on-scada-systems](../cybersecurity/detecting-attacks-on-scada-systems/) — This skill covers detecting cyber attacks targeting Supervisory Control and Data Acquisition (SCADA) systems including man-in-the-middle attacks on industrial protocols, unauthorized command injection into PLCs, HMI compromise, historian data manipulation, and denial-of-service against control system communications. It leverages OT-specific intrusion detection systems, industrial protocol anomaly detection, and process data analytics to identify attacks that traditional IT security tool.
  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [detecting-aws-cloudtrail-anomalies](../cybersecurity/detecting-aws-cloudtrail-anomalies/) — Detect unusual API call patterns in AWS CloudTrail logs using boto3, statistical baselining, and behavioral analysis to identify credential compromise, privilege escalation, and unauthorized resource access. Use when detecting unusual api call patterns in aws cloudtrail logs using.
  `cloud-security` `aws` `cloudtrail` `anomaly-detection` `threat-detection`

- [detecting-aws-credential-exposure-with-trufflehog](../cybersecurity/detecting-aws-credential-exposure-with-trufflehog/) — Detecting exposed AWS credentials in source code repositories, CI/CD pipelines, and configuration files using TruffleHog, git-secrets, and AWS-native detection mechanisms to prevent credential theft and unauthorized account access. . Use when working with detecting aws credential exposure with trufflehog.
  `cloud-security` `aws` `credential-exposure` `trufflehog` `secrets-detection`

- [detecting-aws-guardduty-findings-automation](../cybersecurity/detecting-aws-guardduty-findings-automation/) — Automate AWS GuardDuty threat detection findings processing using EventBridge and Lambda to enable real-time incident response, automatic quarantine of compromised resources, and security notification workflows.
  `aws` `guardduty` `eventbridge` `lambda` `threat-detection`

- [detecting-aws-iam-privilege-escalation](../cybersecurity/detecting-aws-iam-privilege-escalation/) — Detect AWS IAM privilege escalation paths using boto3 and Cloudsplaining policy analysis to identify overly permissive policies, dangerous permission combinations, and least-privilege violations. Use when detecting aws iam privilege escalation paths using boto3 and cloudsplaining.
  `aws` `iam` `privilege-escalation` `cloudsplaining` `boto3`

- [detecting-azure-lateral-movement](../cybersecurity/detecting-azure-lateral-movement/) — Detect lateral movement in Azure AD/Entra ID environments using Microsoft Graph API audit logs, Azure Sentinel KQL hunting queries, and sign-in anomaly correlation to identify privilege escalation, token theft, and cross-tenant pivoting. Use when detecting lateral movement in azure ad/entra id environments using microsoft.
  `azure` `entra-id` `lateral-movement` `sentinel` `kql`

- [detecting-azure-service-principal-abuse](../cybersecurity/detecting-azure-service-principal-abuse/) — Detect and investigate Azure service principal abuse including privilege escalation, credential compromise, admin consent bypass, and unauthorized enumeration in Microsoft Entra ID environments. Use when detecting and investigate azure service principal abuse including privilege escalation,.
  `azure` `entra-id` `service-principal` `privilege-escalation` `credential-abuse`

- [detecting-azure-storage-account-misconfigurations](../cybersecurity/detecting-azure-storage-account-misconfigurations/) — Audit Azure Blob and ADLS storage accounts for public access exposure, weak or long-lived SAS tokens, missing encryption at rest, disabled HTTPS-only traffic, and outdated TLS versions using the azure-mgmt-storage Python SDK. Use when auditing azure blob and adls storage accounts for public access.
  `Azure` `storage-accounts` `blob-storage` `ADLS` `SAS-tokens`

- [detecting-beaconing-patterns-with-zeek](../cybersecurity/detecting-beaconing-patterns-with-zeek/) — Performs statistical analysis of Zeek conn.log connection intervals to detect C2 beaconing patterns. Uses the ZAT library to load Zeek logs into Pandas DataFrames, calculates inter-arrival time standard deviation, and flags periodic connections with low jitter. Use when hunting for command-and-control callbacks in network data.

  `detecting` `beaconing` `patterns` `with`

- [detecting-bluetooth-low-energy-attacks](../cybersecurity/detecting-bluetooth-low-energy-attacks/) — Detects and analyzes Bluetooth Low Energy (BLE) security attacks including sniffing, replay attacks, GATT enumeration abuse, and Man-in-the-Middle interception. Uses Ubertooth One and nRF52840 sniffers for packet capture, the bleak Python library for GATT service enumeration, and crackle for BLE encryption cracking. Use when assessing IoT device BLE security, monitoring for BLE-based attacks on wireless infrastructure, or performing authorized BLE penetration testing.
  `ble` `bluetooth` `ubertooth` `nrf-sniffer` `gatt`

- [detecting-broken-object-property-level-authorization](../cybersecurity/detecting-broken-object-property-level-authorization/) — Detect and test for OWASP API3:2023 Broken Object Property Level Authorization vulnerabilities including excessive data exposure and mass assignment attacks. Use when detecting and test for owasp api3:2023 broken object property level.
  `api-security` `bopla` `owasp-api3` `mass-assignment` `excessive-data-exposure`

- [detecting-business-email-compromise](../cybersecurity/detecting-business-email-compromise/) — Business Email Compromise (BEC) is a sophisticated fraud scheme where attackers impersonate executives, vendors, or trusted partners to trick employees into transferring funds, sharing sensitive data,. Use when working with detecting business email compromise.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [detecting-cloud-threats-with-guardduty](../cybersecurity/detecting-cloud-threats-with-guardduty/) — This skill teaches security teams how to deploy and operationalize Amazon GuardDuty for continuous threat detection across AWS accounts and workloads. It covers enabling protection plans for S3, EKS, EC2 runtime monitoring, and Lambda, interpreting finding severity levels, and building automated response workflows using EventBridge and Lambda.

  `amazon-guardduty` `threat-detection` `aws-security` `runtime-monitoring` `cloud-soc`

- [detecting-command-and-control-over-dns](../cybersecurity/detecting-command-and-control-over-dns/) — Detects command-and-control (C2) communications tunneled through DNS protocol including DNS tunneling tools (Iodine, dnscat2, dns2tcp, Cobalt Strike DNS beacon), domain generation algorithms (DGA), encoded payload delivery via TXT/CNAME records, and DNS beaconing patterns. Covers Shannon entropy analysis of query subdomains, statistical anomaly detection, ML-based DGA classification, passive DNS correlation, and Zeek/Suricata signature development.
  `dns` `c2` `tunneling` `dga` `network-forensics`

- [detecting-compromised-cloud-credentials](../cybersecurity/detecting-compromised-cloud-credentials/) — Detecting compromised cloud credentials across AWS, Azure, and GCP by analyzing anomalous API activity, impossible travel patterns, unauthorized resource provisioning, and credential abuse indicators using GuardDuty, Defender for Identity, and SCC Event Threat Detection. . Use when working with detecting compromised cloud credentials.
  `cloud-security` `credential-compromise` `threat-detection` `guardduty` `incident-response`

- [detecting-container-drift-at-runtime](../cybersecurity/detecting-container-drift-at-runtime/) — Detect unauthorized modifications to running containers by monitoring for binary execution drift, file system changes, and configuration deviations from the original container image. Use when detecting unauthorized modifications to running containers by monitoring for binary.
  `container-drift` `runtime-security` `immutable-containers` `falco` `kubernetes`

- [detecting-container-escape-attempts](../cybersecurity/detecting-container-escape-attempts/) — Container escape is a critical attack technique where an adversary breaks out of container isolation to access the host system or other containers. Detection involves monitoring for escape indicators. Use when working with detecting container escape attempts.
  `containers` `kubernetes` `docker` `security` `runtime-security`

- [detecting-container-escape-with-falco-rules](../cybersecurity/detecting-container-escape-with-falco-rules/) — Detect container escape attempts in real-time using Falco runtime security rules that monitor syscalls, file access, and privilege escalation. Use when detecting container escape attempts in real-time using falco runtime security.
  `falco` `container-escape` `runtime-security` `syscall-monitoring` `kubernetes`

- [detecting-credential-dumping-techniques](../cybersecurity/detecting-credential-dumping-techniques/) — Detect LSASS credential dumping, SAM database extraction, and NTDS.dit theft using Sysmon Event ID 10, Windows Security logs, and SIEM correlation rules. Use when detecting lsass credential dumping, sam database extraction, and ntds.dit theft.
  `credential-dumping` `lsass` `mimikatz` `sysmon` `active-directory`

- [detecting-cryptomining-in-cloud](../cybersecurity/detecting-cryptomining-in-cloud/) — This skill teaches security teams how to detect and respond to unauthorized cryptocurrency mining operations in cloud environments. It covers identifying cryptomining indicators through compute usage anomalies, network traffic patterns to mining pools, GuardDuty CryptoCurrency findings, and runtime process monitoring on EC2, ECS, EKS, and Azure Automation workloads.

  `cryptomining-detection` `cloud-abuse` `resource-hijacking` `guardduty-crypto` `cost-anomaly`

- [detecting-dcsync-attack-in-active-directory](../cybersecurity/detecting-dcsync-attack-in-active-directory/) — Detect DCSync attacks where adversaries abuse Active Directory replication privileges to extract password hashes by monitoring for non-domain-controller accounts requesting directory replication via DsGetNCChanges. Use when detecting dcsync attacks where adversaries abuse active directory replication privileges.
  `threat-hunting` `active-directory` `dcsync` `credential-theft` `mitre-t1003-006`

- [detecting-deepfake-audio-in-vishing-attacks](../cybersecurity/detecting-deepfake-audio-in-vishing-attacks/) — Detects AI-generated deepfake audio used in voice phishing (vishing) attacks by extracting spectral features (MFCC, spectral centroid, spectral contrast, zero-crossing rate) and classifying samples with machine learning models. Supports batch analysis of audio files, generates confidence scores, and produces forensic reports.
  `deepfake-detection` `vishing` `audio-forensics` `MFCC` `spectral-analysis`

- [detecting-dll-sideloading-attacks](../cybersecurity/detecting-dll-sideloading-attacks/) — Detect DLL side-loading attacks where adversaries place malicious DLLs alongside legitimate applications to hijack execution flow for defense evasion. Use when detecting dll side-loading attacks where adversaries place malicious dlls alongside.
  `threat-hunting` `mitre-attack` `dll-sideloading` `defense-evasion` `t1574`

- [detecting-dnp3-protocol-anomalies](../cybersecurity/detecting-dnp3-protocol-anomalies/) — Detect anomalies in DNP3 (Distributed Network Protocol 3) communications used in SCADA systems by monitoring for unauthorized control commands, firmware update attempts, protocol violations, and deviations from baseline traffic patterns using deep packet inspection and machine learning approaches. . Use when working with detecting dnp3 protocol anomalies.
  `ot-security` `ics` `dnp3` `scada` `anomaly-detection`

- [detecting-dns-exfiltration-with-dns-query-analysis](../cybersecurity/detecting-dns-exfiltration-with-dns-query-analysis/) — Detect data exfiltration through DNS tunneling by analyzing query entropy, subdomain length, query volume, TXT record abuse, and response payload sizes using passive DNS monitoring. Use when detecting data exfiltration through dns tunneling by analyzing query entropy,.
  `dns-exfiltration` `dns-tunneling` `data-exfiltration` `threat-detection` `entropy-analysis`

- [detecting-email-account-compromise](../cybersecurity/detecting-email-account-compromise/) — Detect compromised O365 and Google Workspace email accounts by analyzing inbox rule creation, suspicious sign-in locations, mail forwarding rules, and unusual API access patterns via Microsoft Graph and audit logs. Use when detecting compromised o365 and google workspace email accounts by analyzing.
  `email-compromise` `office365` `microsoft-graph` `bec` `inbox-rules`

- [detecting-email-forwarding-rules-attack](../cybersecurity/detecting-email-forwarding-rules-attack/) — Detect malicious email forwarding rules created by adversaries to maintain persistent access to email communications for intelligence collection and BEC attacks. Use when detecting malicious email forwarding rules created by adversaries to maintain.
  `threat-hunting` `mitre-attack` `email-forwarding` `persistence` `bec`

- [detecting-evasion-techniques-in-endpoint-logs](../cybersecurity/detecting-evasion-techniques-in-endpoint-logs/) — Detects defense evasion techniques used by adversaries in endpoint logs including log tampering, timestomping, process injection, and security tool disabling. Use when investigating suspicious endpoint behavior, building detection rules for evasion tactics, or conducting threat hunting for stealthy adversary activity. Activates for requests involving evasion detection, defense evasion analysis, log tampering detection, or MITRE ATT&CK TA0005.

  `endpoint` `edr` `threat-hunting` `defense-evasion` `MITRE-ATT&CK`

- [detecting-exfiltration-over-dns-with-zeek](../cybersecurity/_deprecated/detecting-exfiltration-over-dns-with-zeek/) — Detect DNS-based data exfiltration by analyzing Zeek dns.log for high-entropy subdomains and anomalous query patterns. Use when detecting dns-based data exfiltration by analyzing zeek dns.log for high-entropy.
  `dns-exfiltration` `zeek` `entropy-analysis` `threat-hunting`

- [detecting-fileless-attacks-on-endpoints](../cybersecurity/_deprecated/detecting-fileless-attacks-on-endpoints/) — Detects fileless malware and in-memory attacks that execute entirely in RAM without writing persistent files to disk, evading traditional antivirus. Use when building detections for PowerShell-based attacks, reflective DLL injection, WMI persistence, and registry-resident malware. Activates for requests involving fileless malware detection, in-memory attacks, PowerShell exploitation, or living-off-the-land techniques.

  `endpoint` `fileless-malware` `memory-attacks` `PowerShell` `detection-engineering`

- [detecting-fileless-malware-techniques](../cybersecurity/detecting-fileless-malware-techniques/) — Detects and analyzes fileless malware that operates entirely in memory using PowerShell, WMI, .NET reflection, registry-resident payloads, and living-off-the-land binaries (LOLBins) without writing traditional executable files to disk. Activates for requests involving fileless threat detection, in-memory malware investigation, LOLBin abuse analysis, or WMI persistence examination. . Use when working with detecting fileless malware techniques.
  `malware` `fileless` `LOLBins` `memory-analysis` `detection`

- [detecting-golden-ticket-attacks-in-kerberos-logs](../cybersecurity/detecting-golden-ticket-attacks-in-kerberos-logs/) — Detect Golden Ticket attacks in Active Directory by analyzing Kerberos TGT anomalies including mismatched encryption types, impossible ticket lifetimes, non-existent accounts, and forged PAC signatures in domain controller event logs. Use when detecting golden ticket attacks in active directory by analyzing kerberos.
  `threat-hunting` `golden-ticket` `kerberos` `active-directory` `mitre-t1558-001`

- [detecting-golden-ticket-forgery](../cybersecurity/_deprecated/detecting-golden-ticket-forgery/) — Detect Kerberos Golden Ticket forgery by analyzing Windows Event ID 4769 for RC4 encryption downgrades (0x17), abnormal ticket lifetimes, and krbtgt account anomalies in Splunk and Elastic SIEM. Use when detecting kerberos golden ticket forgery by analyzing windows event id.
  `golden-ticket` `kerberos` `active-directory` `mimikatz` `splunk`

- [detecting-insider-data-exfiltration-via-dlp](../cybersecurity/detecting-insider-data-exfiltration-via-dlp/) — Detects insider data exfiltration by analyzing DLP policy violations, file access patterns, upload volume anomalies, and off-hours activity in endpoint and cloud logs. Uses pandas for behavioral analytics and statistical baselines. Use when investigating insider threats or building user behavior analytics for data loss prevention.

  `detecting` `insider` `data` `exfiltration`

- [detecting-insider-threat-behaviors](../cybersecurity/detecting-insider-threat-behaviors/) — Detect insider threat behavioral indicators including unusual data access, off-hours activity, mass file downloads, privilege abuse, and resignation-correlated data theft. Use when detecting insider threat behavioral indicators including unusual data access, off-hours.
  `threat-hunting` `mitre-attack` `insider-threat` `data-theft` `ueba`

- [detecting-insider-threat-with-ueba](../cybersecurity/detecting-insider-threat-with-ueba/) — Implement User and Entity Behavior Analytics using Elasticsearch/OpenSearch to build behavioral baselines, calculate anomaly scores, perform peer group analysis, and detect insider threat indicators such as data exfiltration, privilege abuse, and unauthorized access patterns. Use when implementing user and entity behavior analytics using elasticsearch/opensearch to build.
  `ueba` `insider-threat` `anomaly-detection` `elasticsearch` `behavior-analytics`

- [detecting-kerberoasting-attacks](../cybersecurity/detecting-kerberoasting-attacks/) — Detect Kerberoasting attacks by monitoring for anomalous Kerberos TGS requests targeting service accounts with SPNs for offline password cracking. Use when detecting kerberoasting attacks by monitoring for anomalous kerberos tgs requests.
  `threat-hunting` `mitre-attack` `kerberoasting` `credential-access` `kerberos`

- [detecting-lateral-movement-in-network](../cybersecurity/detecting-lateral-movement-in-network/) — Identifies lateral movement techniques in enterprise networks by analyzing authentication logs, network flows, SMB traffic, and RDP sessions using Zeek, Velociraptor, and SIEM correlation rules to detect attackers moving between systems. . Use when working with detecting lateral movement in network.
  `network-security` `lateral-movement` `threat-detection` `siem` `pass-the-hash`

- [detecting-lateral-movement-with-splunk](../cybersecurity/detecting-lateral-movement-with-splunk/) — Detect adversary lateral movement across networks using Splunk SPL queries against Windows authentication logs, SMB traffic, and remote service abuse. Use when detecting adversary lateral movement across networks using splunk spl queries.
  `threat-hunting` `mitre-attack` `lateral-movement` `splunk` `siem`

- [detecting-lateral-movement-with-zeek](../cybersecurity/detecting-lateral-movement-with-zeek/) — Detect lateral movement in network traffic using Zeek (formerly Bro) log analysis. Parses conn.log, smb_mapping.log, smb_files.log, dce_rpc.log, kerberos.log, and ntlm.log to identify SMB file transfers, NTLM account spray activity, remote service execution, and anomalous internal connections. . Use when working with detecting lateral movement with zeek.
  `zeek` `lateral-movement` `smb` `dce-rpc` `ntlm-spray`

- [detecting-living-off-the-land-attacks](../cybersecurity/detecting-living-off-the-land-attacks/) — Detect abuse of legitimate Windows binaries (LOLBins) used for living off the land attacks. Monitors process creation, command-line arguments, and parent-child relationships to identify suspicious LOLBin execution patterns. . Use when working with detecting living off the land attacks.
  `lolbins` `lotl` `fileless-attacks` `process-monitoring`

- [detecting-living-off-the-land-with-lolbas](../cybersecurity/_deprecated/detecting-living-off-the-land-with-lolbas/) — Detect Living Off the Land Binaries (LOLBins/LOLBAS) abuse including certutil, regsvr32, mshta, and rundll32 via process telemetry, Sigma rules, and parent-child process analysis. Use when detecting living off the land binaries (lolbins/lolbas) abuse including certutil,.
  `lolbas` `lolbins` `sigma-rules` `process-monitoring` `sysmon`

- [detecting-malicious-scheduled-tasks-with-sysmon](../cybersecurity/detecting-malicious-scheduled-tasks-with-sysmon/) — Use when detect malicious scheduled task creation and modification using Sysmon Event IDs 1 (Process Create for schtasks.exe), 11 (File Create for task XML), and Windows Security Event 4698/4702. The analyst correlates task creation with suspicious parent processes, public directory paths, and encoded command arguments to identify persistence and lateral movement via scheduled tasks. Activates for requests involving scheduled task detection, Sysmon persistence hunting, or T1053.
  `sysmon` `scheduled-tasks` `persistence` `detection` `threat-hunting`

- [detecting-mimikatz-execution-patterns](../cybersecurity/detecting-mimikatz-execution-patterns/) — Detect Mimikatz execution through command-line patterns, LSASS access signatures, binary indicators, and in-memory detection of known modules. Use when detecting mimikatz execution through command-line patterns, lsass access signatures, binary.
  `threat-hunting` `mitre-attack` `mimikatz` `credential-dumping` `edr`

- [detecting-misconfigured-azure-storage](../cybersecurity/detecting-misconfigured-azure-storage/) — Detecting misconfigured Azure Storage accounts including publicly accessible blob containers, missing encryption settings, overly permissive SAS tokens, disabled logging, and network access violations using Azure CLI, PowerShell, and Microsoft Defender for Storage. . Use when working with detecting misconfigured azure storage.
  `cloud-security` `azure` `storage-security` `blob-storage` `sas-tokens`

- [detecting-mobile-malware-behavior](../cybersecurity/detecting-mobile-malware-behavior/) — Detects and analyzes malicious behavior in mobile applications through behavioral analysis, permission abuse detection, network traffic monitoring, and dynamic instrumentation. Use when analyzing suspicious mobile applications for data exfiltration, command-and-control communication, credential stealing, SMS interception, or other malware indicators. Activates for requests involving mobile malware analysis, app behavior monitoring, trojan detection, or suspicious app investigation.

  `mobile-security` `android` `ios` `malware-analysis` `owasp-mobile`

- [detecting-modbus-command-injection-attacks](../cybersecurity/detecting-modbus-command-injection-attacks/) — Detect command injection attacks against Modbus TCP/RTU protocol in ICS environments by monitoring for unauthorized write operations, anomalous function codes, malformed frames, and deviations from established communication baselines using ICS-aware IDS and protocol deep packet inspection. . Use when working with detecting modbus command injection attacks.
  `ot-security` `ics` `modbus` `command-injection` `protocol-analysis`

- [detecting-modbus-protocol-anomalies](../cybersecurity/detecting-modbus-protocol-anomalies/) — This skill covers detecting anomalies in Modbus/TCP and Modbus RTU communications in industrial control systems. It addresses function code monitoring, register range validation, timing analysis, unauthorized client detection, and deep packet inspection for malformed Modbus frames. The skill leverages Zeek with Modbus protocol analyzers, Suricata IDS with OT rules, and custom Python-based detection using Markov chain models for normal Modbus transaction sequences.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [detecting-network-anomalies-with-zeek](../cybersecurity/detecting-network-anomalies-with-zeek/) — Deploys and configures Zeek (formerly Bro) network security monitor to passively analyze network traffic, generate structured logs, detect anomalous behavior, and create custom detection scripts for threat hunting and incident response.

  `network-security` `zeek` `network-monitoring` `anomaly-detection` `threat-hunting`

- [detecting-network-scanning-with-ids-signatures](../cybersecurity/detecting-network-scanning-with-ids-signatures/) — Detect network reconnaissance and port scanning using Suricata and Snort IDS signatures, threshold-based detection rules, and traffic anomaly analysis to identify Nmap, Masscan, and custom scanning activity. Use when detecting network reconnaissance and port scanning using suricata and snort.
  `ids` `nmap-detection` `port-scanning` `snort` `suricata`

- [detecting-ntlm-relay-with-event-correlation](../cybersecurity/detecting-ntlm-relay-with-event-correlation/) — Detect NTLM relay attacks through Windows Security Event correlation by analyzing Event 4624 LogonType 3 for IP-to-hostname mismatches, identifying Responder/LLMNR poisoning artifacts, auditing SMB and LDAP signing enforcement across the domain, and detecting NTLM downgrade attacks from NTLMv2 to NTLMv1 using event log analysis. . Use when working with detecting ntlm relay with event correlation.
  `threat-hunting` `NTLM-relay` `event-correlation` `T1557.001` `Event-4624`

- [detecting-oauth-token-theft](../cybersecurity/detecting-oauth-token-theft/) — Detects and responds to OAuth token theft and replay attacks in cloud environments, focusing on Microsoft Entra ID (Azure AD) token protection, conditional access policies, and sign-in anomaly detection. Covers access token theft, refresh token replay, Primary Refresh Token (PRT) abuse, and pass-the-cookie attacks. Activates for requests involving OAuth token theft detection, token replay prevention, Azure AD conditional access token protection, or cloud identity attack investigation.
  `oauth` `token-theft` `azure-ad` `entra-id` `conditional-access`

- [detecting-pass-the-hash-attacks](../cybersecurity/detecting-pass-the-hash-attacks/) — Detect Pass-the-Hash attacks by analyzing NTLM authentication patterns, identifying Type 3 logons with NTLM where Kerberos is expected, and correlating with credential dumping. Use when detecting pass-the-hash attacks by analyzing ntlm authentication patterns, identifying type.
  `threat-hunting` `mitre-attack` `pass-the-hash` `credential-access` `t1550`

- [detecting-pass-the-ticket-attacks](../cybersecurity/detecting-pass-the-ticket-attacks/) — Detect Kerberos Pass-the-Ticket (PtT) attacks by analyzing Windows Event IDs 4768, 4769, and 4771 for anomalous ticket usage patterns in Splunk and Elastic SIEM. Use when detecting kerberos pass-the-ticket (ptt) attacks by analyzing windows event ids.
  `kerberos` `pass-the-ticket` `active-directory` `splunk` `elastic`

- [detecting-port-scanning-with-fail2ban](../cybersecurity/detecting-port-scanning-with-fail2ban/) — Configures Fail2ban with custom filters and actions to detect port scanning activity, SSH brute force attempts, and network reconnaissance, automatically banning offending IP addresses and alerting security teams to suspicious network probing. . Use when working with detecting port scanning with fail2ban.
  `network-security` `fail2ban` `port-scanning` `intrusion-prevention` `automated-defense`

- [detecting-privilege-escalation-attempts](../cybersecurity/detecting-privilege-escalation-attempts/) — Detect privilege escalation attempts including token manipulation, UAC bypass, unquoted service paths, kernel exploits, and sudo/doas abuse across Windows and Linux. Use when detecting privilege escalation attempts including token manipulation, uac bypass, unquoted.
  `threat-hunting` `mitre-attack` `privilege-escalation` `token-manipulation` `uac-bypass`

- [detecting-privilege-escalation-in-kubernetes-pods](../cybersecurity/detecting-privilege-escalation-in-kubernetes-pods/) — Detect and prevent privilege escalation in Kubernetes pods by monitoring security contexts, capabilities, and syscall patterns with Falco and OPA policies. Use when detecting and prevent privilege escalation in kubernetes pods by monitoring.
  `kubernetes` `privilege-escalation` `security-context` `capabilities` `detection`

- [detecting-process-hollowing-technique](../cybersecurity/detecting-process-hollowing-technique/) — Detect process hollowing (T1055.012) by analyzing memory-mapped sections, hollowed process indicators, and parent-child process anomalies in EDR telemetry. Use when detecting process hollowing (t1055.012) by analyzing memory-mapped sections, hollowed process.
  `threat-hunting` `mitre-attack` `process-hollowing` `process-injection` `edr`

- [detecting-process-injection-techniques](../cybersecurity/detecting-process-injection-techniques/) — Detects and analyzes process injection techniques used by malware including classic DLL injection, process hollowing, APC injection, thread hijacking, and reflective loading. Uses memory forensics, API monitoring, and behavioral analysis to identify injection artifacts. Activates for requests involving process injection detection, code injection analysis, hollowed process investigation, or in-memory threat detection. . Use when working with detecting process injection techniques.
  `malware` `process-injection` `detection` `memory-forensics` `defense-evasion`

- [detecting-qr-code-phishing-with-email-security](../cybersecurity/detecting-qr-code-phishing-with-email-security/) — Detect and prevent QR code phishing (quishing) attacks that bypass traditional email security by embedding malicious URLs in QR code images within emails. Use when detecting and prevent qr code phishing (quishing) attacks that bypass.
  `quishing` `qr-code` `phishing` `email-security` `image-analysis`

- [detecting-ransomware-encryption-behavior](../cybersecurity/detecting-ransomware-encryption-behavior/) — Use when detects ransomware encryption activity in real time using entropy analysis, file system I/O monitoring, and behavioral heuristics. Identifies mass file modification patterns, abnormal entropy spikes in written data, and suspicious process behavior characteristic of ransomware encryption routines. Activates for requests involving ransomware behavioral detection, entropy-based file monitoring, I/O anomaly detection, or real-time encryption activity alerting.
'.
  `ransomware` `detection` `entropy` `behavioral-analysis` `file-monitoring`

- [detecting-ransomware-precursors-in-network](../cybersecurity/detecting-ransomware-precursors-in-network/) — Use when detects early-stage ransomware indicators in network traffic before encryption begins, including initial access broker activity, command-and-control beaconing, credential harvesting, reconnaissance scanning, and staging behavior. Uses network detection tools (Zeek, Suricata, Arkime), SIEM correlation rules, and threat intelligence feeds to identify ransomware precursor patterns such as Cobalt Strike beacons, Mimikatz network signatures, and RDP brute-force attempts.
  `ransomware` `detection` `network-security` `incident-response` `defense`

- [detecting-rdp-brute-force-attacks](../cybersecurity/detecting-rdp-brute-force-attacks/) — Detect RDP brute force attacks by analyzing Windows Security Event Logs for failed authentication patterns (Event ID 4625), successful logons after failures (Event ID 4624), NLA failures, and source IP frequency analysis. Use when detecting rdp brute force attacks by analyzing windows security event.
  `threat-detection` `rdp` `brute-force` `windows-event-logs` `blue-team`

- [detecting-rootkit-activity](../cybersecurity/detecting-rootkit-activity/) — Detects rootkit presence on compromised systems by identifying hidden processes, hooked system calls, modified kernel structures, hidden files, and covert network connections using memory forensics, cross-view detection, and integrity checking techniques. Activates for requests involving rootkit detection, hidden process discovery, kernel integrity checking, or system call hook analysis. . Use when working with detecting rootkit activity.
  `malware` `rootkit` `detection` `kernel-analysis` `memory-forensics`

- [detecting-s3-data-exfiltration-attempts](../cybersecurity/detecting-s3-data-exfiltration-attempts/) — Detecting data exfiltration attempts from AWS S3 buckets by analyzing CloudTrail S3 data events, VPC Flow Logs, GuardDuty findings, Amazon Macie alerts, and S3 access patterns to identify unauthorized bulk downloads and cross-account data transfers. . Use when working with detecting s3 data exfiltration attempts.
  `cloud-security` `aws` `s3` `data-exfiltration` `guardduty`

- [detecting-serverless-function-injection](../cybersecurity/detecting-serverless-function-injection/) — Use when detects and prevents code injection attacks targeting serverless functions (AWS Lambda, Azure Functions, Google Cloud Functions) through event source poisoning, malicious layer injection, runtime command execution, and IAM privilege escalation via function modification. The analyst combines static analysis of function code, CloudTrail event correlation, runtime behavior monitoring, and IAM policy auditing to identify injection vectors across the expanded serverless attack surface inc...
  `serverless-security` `Lambda-injection` `event-source-poisoning` `OWASP-serverless` `IAM-escalation`

- [detecting-service-account-abuse](../cybersecurity/detecting-service-account-abuse/) — Detect abuse of service accounts through anomalous interactive logons, privilege escalation, lateral movement, and unauthorized access patterns. Use when detecting abuse of service accounts through anomalous interactive logons, privilege.
  `threat-hunting` `mitre-attack` `service-accounts` `privilege-escalation` `t1078`

- [detecting-shadow-api-endpoints](../cybersecurity/detecting-shadow-api-endpoints/) — Discover and inventory shadow API endpoints that operate outside documented specifications using traffic analysis, code scanning, and API discovery platforms. Use when working with detecting shadow api endpoints.
  `api-security` `shadow-apis` `api-discovery` `undocumented-apis` `zombie-apis`

- [detecting-shadow-it-cloud-usage](../cybersecurity/detecting-shadow-it-cloud-usage/) — Detect unauthorized SaaS and cloud service usage (shadow IT) by analyzing proxy logs, DNS query logs, and netflow data using Python pandas for traffic pattern analysis and domain classification. Use when detecting unauthorized saas and cloud service usage (shadow it) by.
  `shadow-IT` `SaaS-discovery` `proxy-logs` `DNS-analysis` `netflow`

- [detecting-spearphishing-with-email-gateway](../cybersecurity/detecting-spearphishing-with-email-gateway/) — Spearphishing targets specific individuals using personalized, researched content that bypasses generic spam filters. Email security gateways (SEGs) like Microsoft Defender for Office 365, Proofpoint,. Use when working with detecting spearphishing with email gateway.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [detecting-sql-injection-via-waf-logs](../cybersecurity/detecting-sql-injection-via-waf-logs/) — Analyze WAF (ModSecurity/AWS WAF/Cloudflare) logs to detect SQL injection attack campaigns. Parses ModSecurity audit logs and JSON WAF event logs to identify SQLi patterns (UNION SELECT, OR 1=1, SLEEP(), BENCHMARK()), tracks attack sources, correlates multi-stage injection attempts, and generates incident reports with OWASP classification.
  `detecting` `sql` `injection` `via`

- [detecting-stuxnet-style-attacks](../cybersecurity/detecting-stuxnet-style-attacks/) — This skill covers detecting sophisticated cyber-physical attacks that follow the Stuxnet attack pattern of modifying PLC logic while spoofing sensor readings to hide the manipulation from operators. It addresses PLC logic integrity monitoring, physics-based process anomaly detection, engineering workstation compromise indicators, USB-borne attack vectors, and multi-stage attack chain detection spanning IT-to-OT lateral movement through to process manipulation.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [detecting-supply-chain-attacks-in-ci-cd](../cybersecurity/detecting-supply-chain-attacks-in-ci-cd/) — Scans GitHub Actions workflows and CI/CD pipeline configurations for supply chain attack vectors including unpinned actions, script injection via expressions, dependency confusion, and secrets exposure. Uses PyGithub and YAML parsing for automated audit. Use when hardening CI/CD pipelines or investigating compromised build systems.

  `detecting` `supply` `chain` `attacks`

- [detecting-suspicious-oauth-application-consent](../cybersecurity/detecting-suspicious-oauth-application-consent/) — Detect risky OAuth application consent grants in Azure AD / Microsoft Entra ID using Microsoft Graph API, audit logs, and permission analysis to identify illicit consent grant attacks. Use when detecting risky oauth application consent grants in azure ad /.
  `OAuth` `Azure-AD` `Entra-ID` `Microsoft-Graph` `illicit-consent`

- [detecting-suspicious-powershell-execution](../cybersecurity/detecting-suspicious-powershell-execution/) — Detect suspicious PowerShell execution patterns including encoded commands, download cradles, AMSI bypass attempts, and constrained language mode evasion. Use when detecting suspicious powershell execution patterns including encoded commands, download cradles,.
  `threat-hunting` `mitre-attack` `powershell` `execution` `t1059`

- [detecting-t1003-credential-dumping-with-edr](../cybersecurity/detecting-t1003-credential-dumping-with-edr/) — Detect OS credential dumping techniques targeting LSASS memory, SAM database, NTDS.dit, and cached credentials using EDR telemetry, Sysmon process access monitoring, and Windows security event correlation. Use when detecting os credential dumping techniques targeting lsass memory, sam database,.
  `threat-hunting` `credential-dumping` `lsass` `mitre-t1003` `edr`

- [detecting-t1055-process-injection-with-sysmon](../cybersecurity/detecting-t1055-process-injection-with-sysmon/) — Detect process injection techniques (T1055) including classic DLL injection, process hollowing, and APC injection by analyzing Sysmon events for cross-process memory operations, remote thread creation, and anomalous DLL loading patterns. Use when detecting process injection techniques (t1055) including classic dll injection, process.
  `threat-hunting` `process-injection` `sysmon` `mitre-t1055` `defense-evasion`

- [detecting-t1548-abuse-elevation-control-mechanism](../cybersecurity/detecting-t1548-abuse-elevation-control-mechanism/) — Detect abuse of elevation control mechanisms including UAC bypass, sudo exploitation, and setuid/setgid manipulation by monitoring registry modifications, process elevation flags, and unusual parent-child process relationships. Use when detecting abuse of elevation control mechanisms including uac bypass, sudo.
  `threat-hunting` `uac-bypass` `privilege-escalation` `mitre-t1548` `elevation-control`

- [detecting-typosquatting-packages-in-npm-pypi](../cybersecurity/detecting-typosquatting-packages-in-npm-pypi/) — Detects typosquatting attacks in npm and PyPI package registries by analyzing package name similarity using Levenshtein distance and other string metrics, examining publish date heuristics to identify recently created packages mimicking established ones, and flagging download count anomalies where suspicious packages have disproportionately low usage compared to their legitimate targets. Use when working with detecting typosquatting packages in npm pypi.
  `typosquatting` `npm` `pypi` `supply-chain` `package-security`

- [detecting-wmi-persistence](../cybersecurity/detecting-wmi-persistence/) — Detect WMI event subscription persistence by analyzing Sysmon Event IDs 19, 20, and 21 for malicious EventFilter, EventConsumer, and FilterToConsumerBinding creation. Use when detecting wmi event subscription persistence by analyzing sysmon event ids.
  `threat-hunting` `wmi` `persistence` `sysmon` `t1546.003`

- [eradicating-malware-from-infected-systems](../cybersecurity/eradicating-malware-from-infected-systems/) — Systematically remove malware, backdoors, and attacker persistence mechanisms from infected systems while ensuring complete eradication and preventing re-infection. Use when working with eradicating malware from infected systems.
  `incident-response` `eradication` `malware-removal` `persistence` `dfir`

- [evaluating-threat-intelligence-platforms](../cybersecurity/evaluating-threat-intelligence-platforms/) — Evaluates and selects Threat Intelligence Platform (TIP) products based on organizational requirements including feed integration capability, STIX/TAXII support, workflow automation, analyst interface, and total cost of ownership. Use when conducting a TIP procurement, migrating between TIP solutions, or assessing whether the current TIP meets program maturity requirements. Activates for requests involving ThreatConnect, MISP, OpenCTI, Anomali, EclecticIQ, or TIP procurement decisions.
  `TIP` `ThreatConnect` `MISP` `OpenCTI` `Anomali`

- [executing-active-directory-attack-simulation](../cybersecurity/executing-active-directory-attack-simulation/) — Executes authorized attack simulations against Active Directory environments to identify misconfigurations, weak credentials, dangerous privilege paths, and exploitable trust relationships that could lead to domain compromise. The tester uses BloodHound for attack path analysis, Mimikatz for credential extraction, and Impacket for protocol-level attacks including Kerberoasting, AS-REP Roasting, and delegation abuse. Use when working with executing active directory attack simulation.
  `Active-Directory` `BloodHound` `Mimikatz` `Kerberoasting` `domain-compromise`

- [executing-phishing-simulation-campaign](../cybersecurity/executing-phishing-simulation-campaign/) — Executes authorized phishing simulation campaigns to assess an organization's susceptibility to email-based social engineering attacks. The tester designs realistic phishing scenarios, builds credential harvesting infrastructure, sends targeted phishing emails, and tracks open rates, click-through rates, and credential submission rates to measure human security awareness. Use when working with executing phishing simulation campaign.
  `phishing-simulation` `social-engineering` `GoPhish` `email-security` `security-awareness`

- [executing-red-team-engagement-planning](../cybersecurity/executing-red-team-engagement-planning/) — Red team engagement planning is the foundational phase that defines scope, objectives, rules of engagement (ROE), threat model selection, and operational timelines before any offensive testing begins. Use when working with executing red team engagement planning.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [executing-red-team-exercise](../cybersecurity/executing-red-team-exercise/) — Use when executes comprehensive red team exercises that simulate real-world adversary operations against an organization's people, processes, and technology. The red team operates with stealth as a primary objective, employing the full attack lifecycle from initial reconnaissance through objective completion while testing the organization's detection and response capabilities. This differs from penetration testing by focusing on adversary emulation rather than vulnerability identification.
  `red-team` `adversary-emulation` `MITRE-ATT&CK` `Cobalt-Strike` `detection-assessment`

- [exploiting-active-directory-certificate-services-esc1](../cybersecurity/exploiting-active-directory-certificate-services-esc1/) — Exploit misconfigured Active Directory Certificate Services (AD CS) ESC1 vulnerability to request certificates as high-privileged users and escalate domain privileges during authorized red team assessments. Use when exploiting misconfigured active directory certificate services (ad cs) esc1 vulnerability.
  `red-team` `active-directory` `ad-cs` `esc1` `certificate-abuse`

- [exploiting-active-directory-with-bloodhound](../cybersecurity/exploiting-active-directory-with-bloodhound/) — BloodHound is a graph-based Active Directory reconnaissance tool that uses graph theory to reveal hidden and unintended relationships within AD environments. Red teams use BloodHound to identify attac. Use when working with exploiting active directory with bloodhound.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [exploiting-api-injection-vulnerabilities](../cybersecurity/exploiting-api-injection-vulnerabilities/) — Use when tests APIs for injection vulnerabilities including SQL injection, NoSQL injection, OS command injection, LDAP injection, and Server-Side Request Forgery (SSRF) through API parameters, headers, and request bodies. The tester crafts malicious payloads targeting different backend technologies and injection contexts to extract data, execute commands, or access internal services. Maps to OWASP API8:2023 Security Misconfiguration and API7:2023 SSRF.
  `api-security` `owasp` `injection` `sqli` `nosql`

- [exploiting-bgp-hijacking-vulnerabilities](../cybersecurity/exploiting-bgp-hijacking-vulnerabilities/) — Analyzes and simulates BGP hijacking scenarios in authorized lab environments to assess route origin validation, RPKI deployment, and BGP monitoring defenses against prefix hijacking and route leak attacks on internet routing infrastructure. . Use when working with exploiting bgp hijacking vulnerabilities.
  `network-security` `bgp` `routing-security` `rpki` `route-hijacking`

- [exploiting-broken-function-level-authorization](../cybersecurity/exploiting-broken-function-level-authorization/) — Use when tests APIs for Broken Function Level Authorization (BFLA) vulnerabilities where regular users can invoke administrative functions or access privileged API endpoints by directly calling them. The tester identifies admin and privileged endpoints, then attempts to access them with regular user credentials by manipulating HTTP methods, URL paths, and request parameters. Maps to OWASP API5:2023 Broken Function Level Authorization.
  `api-security` `owasp` `authorization` `bfla` `privilege-escalation`

- [exploiting-broken-link-hijacking](../cybersecurity/exploiting-broken-link-hijacking/) — Discover and exploit broken link hijacking vulnerabilities by identifying references to expired domains, decommissioned cloud resources, and dead external services that can be claimed by an attacker. Use when working with exploiting broken link hijacking.
  `broken-link-hijacking` `blh` `subdomain-takeover` `dead-link` `expired-domain`

- [exploiting-constrained-delegation-abuse](../cybersecurity/exploiting-constrained-delegation-abuse/) — Exploit Kerberos Constrained Delegation misconfigurations in Active Directory to impersonate privileged users via S4U2self and S4U2proxy extensions for lateral movement and privilege escalation. Use when exploiting kerberos constrained delegation misconfigurations in active directory to impersonate.
  `red-team` `active-directory` `kerberos` `constrained-delegation` `s4u2proxy`

- [exploiting-deeplink-vulnerabilities](../cybersecurity/exploiting-deeplink-vulnerabilities/) — Tests and exploits deep link (URL scheme and App Link) vulnerabilities in Android and iOS mobile applications to identify unauthorized access, data injection, intent hijacking, and redirect manipulation. Use when assessing mobile app attack surface through custom URI schemes, Android App Links, iOS Universal Links, or intent-based navigation. Activates for requests involving deep link security testing, URL scheme exploitation, mobile intent abuse, or link hijacking.

  `mobile-security` `android` `ios` `deep-links` `owasp-mobile`

- [exploiting-excessive-data-exposure-in-api](../cybersecurity/exploiting-excessive-data-exposure-in-api/) — Tests APIs for excessive data exposure where endpoints return more data than the client application needs, relying on the frontend to filter sensitive fields. The tester intercepts API responses and analyzes them for leaked PII, internal identifiers, debug information, or sensitive business data that the UI does not display but the API transmits. This maps to OWASP API3:2023 Broken Object Property Level Authorization. Use when working with exploiting excessive data exposure in api.
  `api-security` `owasp` `data-exposure` `rest-security` `pii-leakage`

- [exploiting-http-request-smuggling](../cybersecurity/exploiting-http-request-smuggling/) — Detecting and exploiting HTTP request smuggling vulnerabilities caused by Content-Length and Transfer-Encoding parsing discrepancies between front-end and back-end servers. Use when working with exploiting http request smuggling.
  `penetration-testing` `request-smuggling` `http-desync` `web-security` `burpsuite`

- [exploiting-idor-vulnerabilities](../cybersecurity/exploiting-idor-vulnerabilities/) — Identifying and exploiting Insecure Direct Object Reference vulnerabilities to access unauthorized resources by manipulating object identifiers in API requests and URLs. Use when working with exploiting idor vulnerabilities.
  `penetration-testing` `idor` `access-control` `owasp` `burpsuite`

- [exploiting-insecure-data-storage-in-mobile](../cybersecurity/exploiting-insecure-data-storage-in-mobile/) — Identifies and exploits insecure local data storage vulnerabilities in Android and iOS mobile applications including unencrypted databases, world-readable files, insecure SharedPreferences, plaintext credential storage, and improper keychain/keystore usage. Use when performing mobile penetration testing focused on OWASP M9 (Insecure Data Storage) or assessing compliance with MASVS-STORAGE requirements.
  `mobile-security` `android` `ios` `data-storage` `owasp-mobile`

- [exploiting-insecure-deserialization](../cybersecurity/exploiting-insecure-deserialization/) — Identifying and exploiting insecure deserialization vulnerabilities in Java, PHP, Python, and .NET applications to achieve remote code execution during authorized penetration tests. Use when working with exploiting insecure deserialization.
  `penetration-testing` `deserialization` `rce` `owasp` `web-security`

- [exploiting-ipv6-vulnerabilities](../cybersecurity/exploiting-ipv6-vulnerabilities/) — Identifies and exploits IPv6-specific vulnerabilities including SLAAC spoofing, Router Advertisement flooding, and IPv6 tunneling during authorized assessments to test dual-stack security controls and IPv6-aware network defenses. . Use when working with exploiting ipv6 vulnerabilities.
  `network-security` `ipv6` `slaac` `router-advertisement` `dual-stack-security`

- [exploiting-jwt-algorithm-confusion-attack](../cybersecurity/exploiting-jwt-algorithm-confusion-attack/) — Exploits JWT algorithm confusion vulnerabilities where the server's token verification library accepts the algorithm specified in the JWT header rather than enforcing a fixed algorithm. The tester manipulates the alg header to switch from RS256 to HS256 (using the RSA public key as the HMAC secret), sets alg to none to bypass signature verification, or exploits kid/jku/x5u header injection to supply attacker-controlled keys. Use when working with exploiting jwt algorithm confusion attack.
  `api-security` `jwt` `algorithm-confusion` `token-forgery` `cryptographic-attack`

- [exploiting-kerberoasting-with-impacket](../cybersecurity/exploiting-kerberoasting-with-impacket/) — Perform Kerberoasting attacks using Impacket's GetUserSPNs to extract and crack Kerberos TGS tickets for Active Directory service accounts. Use when performing kerberoasting attacks using impacket's getuserspns to extract and crack.
  `kerberoasting` `impacket` `active-directory` `credential-access` `kerberos`

- [exploiting-mass-assignment-in-rest-apis](../cybersecurity/exploiting-mass-assignment-in-rest-apis/) — Discover and exploit mass assignment vulnerabilities in REST APIs to escalate privileges, modify restricted fields, and bypass authorization controls by injecting unexpected parameters in API requests. Use when working with exploiting mass assignment in rest apis.
  `mass-assignment` `api-security` `privilege-escalation` `rest-api` `autobinding`

- [exploiting-ms17-010-eternalblue-vulnerability](../cybersecurity/exploiting-ms17-010-eternalblue-vulnerability/) — MS17-010 (EternalBlue) is a critical vulnerability in Microsoft's SMBv1 implementation that allows remote code execution. Originally discovered by the NSA and leaked by the Shadow Brokers in 2017, it. Use when working with exploiting ms17 010 eternalblue vulnerability.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [exploiting-nopac-cve-2021-42278-42287](../cybersecurity/exploiting-nopac-cve-2021-42278-42287/) — Exploit the noPac vulnerability chain (CVE-2021-42278 sAMAccountName spoofing and CVE-2021-42287 KDC PAC confusion) to escalate from standard domain user to Domain Admin in Active Directory environments. Use when exploiting the nopac vulnerability chain (cve-2021-42278 samaccountname spoofing and cve-2021-42287.
  `red-team` `active-directory` `nopac` `cve-2021-42278` `cve-2021-42287`

- [exploiting-nosql-injection-vulnerabilities](../cybersecurity/exploiting-nosql-injection-vulnerabilities/) — Detect and exploit NoSQL injection vulnerabilities in MongoDB, CouchDB, and other NoSQL databases to demonstrate authentication bypass, data extraction, and unauthorized access risks. Use when detecting and exploit nosql injection vulnerabilities in mongodb, couchdb, and.
  `nosql-injection` `mongodb` `authentication-bypass` `injection-attack` `web-security`

- [exploiting-oauth-misconfiguration](../cybersecurity/exploiting-oauth-misconfiguration/) — Identifying and exploiting OAuth 2.0 and OpenID Connect misconfigurations including redirect URI manipulation, token leakage, and authorization code theft during security assessments. Use when working with exploiting oauth misconfiguration.
  `penetration-testing` `oauth` `oidc` `authentication` `web-security`

- [exploiting-prototype-pollution-in-javascript](../cybersecurity/exploiting-prototype-pollution-in-javascript/) — Detect and exploit JavaScript prototype pollution vulnerabilities on both client-side and server-side applications to achieve XSS, RCE, and authentication bypass through property injection. Use when detecting and exploit javascript prototype pollution vulnerabilities on both client-side.
  `prototype-pollution` `javascript` `node-js` `xss` `rce`

- [exploiting-race-condition-vulnerabilities](../cybersecurity/exploiting-race-condition-vulnerabilities/) — Detect and exploit race condition vulnerabilities in web applications using Turbo Intruder's single-packet attack technique to bypass rate limits, duplicate transactions, and exploit time-of-check-to-time-of-use flaws. Use when detecting and exploit race condition vulnerabilities in web applications using.
  `race-condition` `turbo-intruder` `toctou` `concurrency` `single-packet-attack`

- [exploiting-server-side-request-forgery](../cybersecurity/exploiting-server-side-request-forgery/) — Identifying and exploiting SSRF vulnerabilities to access internal services, cloud metadata, and restricted network resources during authorized penetration tests. Use when working with exploiting server side request forgery.
  `penetration-testing` `ssrf` `owasp` `cloud-security` `web-security`

- [exploiting-smb-vulnerabilities-with-metasploit](../cybersecurity/exploiting-smb-vulnerabilities-with-metasploit/) — Identifies and exploits SMB protocol vulnerabilities using Metasploit Framework during authorized penetration tests to demonstrate risks from unpatched Windows systems, misconfigured shares, and weak authentication in enterprise networks. . Use when working with exploiting smb vulnerabilities with metasploit.
  `network-security` `smb` `metasploit` `exploitation` `eternalblue`

- [exploiting-sql-injection-vulnerabilities](../cybersecurity/exploiting-sql-injection-vulnerabilities/) — Identifies and exploits SQL injection vulnerabilities in web applications during authorized penetration tests using manual techniques and automated tools like sqlmap. The tester detects injection points through error-based, union-based, blind boolean, and time-based blind techniques across all major database engines (MySQL, PostgreSQL, MSSQL, Oracle) to demonstrate data extraction, authentication bypass, and potential remote code execution.
  `SQL-injection` `sqlmap` `database-security` `OWASP-A03` `injection-testing`

- [exploiting-sql-injection-with-sqlmap](../cybersecurity/exploiting-sql-injection-with-sqlmap/) — Detecting and exploiting SQL injection vulnerabilities using sqlmap to extract database contents during authorized penetration tests. Use when working with exploiting sql injection with sqlmap.
  `penetration-testing` `sql-injection` `sqlmap` `owasp` `database-security`

- [exploiting-template-injection-vulnerabilities](../cybersecurity/exploiting-template-injection-vulnerabilities/) — Detecting and exploiting Server-Side Template Injection (SSTI) vulnerabilities across Jinja2, Twig, Freemarker, and other template engines to achieve remote code execution. Use when working with exploiting template injection vulnerabilities.
  `penetration-testing` `ssti` `template-injection` `rce` `web-security`

- [exploiting-type-juggling-vulnerabilities](../cybersecurity/exploiting-type-juggling-vulnerabilities/) — Exploit PHP type juggling vulnerabilities caused by loose comparison operators to bypass authentication, circumvent hash verification, and manipulate application logic through type coercion attacks. Use when exploiting php type juggling vulnerabilities caused by loose comparison operators.
  `type-juggling` `php-security` `loose-comparison` `authentication-bypass` `magic-hash`

- [exploiting-vulnerabilities-with-metasploit-framework](../cybersecurity/exploiting-vulnerabilities-with-metasploit-framework/) — The Metasploit Framework is the world's most widely used penetration testing platform, maintained by Rapid7. It contains over 2,300 exploits, 1,200 auxiliary modules, and 400 post-exploitation modules. Use when working with exploiting vulnerabilities with metasploit framework.
  `vulnerability-management` `cve` `metasploit` `exploitation` `penetration-testing`

- [exploiting-websocket-vulnerabilities](../cybersecurity/exploiting-websocket-vulnerabilities/) — Testing WebSocket implementations for authentication bypass, cross-site hijacking, injection attacks, and insecure message handling during authorized security assessments. Use when working with exploiting websocket vulnerabilities.
  `penetration-testing` `websocket` `web-security` `owasp` `real-time`

- [exploiting-zerologon-vulnerability-cve-2020-1472](../cybersecurity/exploiting-zerologon-vulnerability-cve-2020-1472/) — Exploit the Zerologon vulnerability (CVE-2020-1472) in the Netlogon Remote Protocol to achieve domain controller compromise by resetting the machine account password to empty. Use when exploiting the zerologon vulnerability (cve-2020-1472) in the netlogon remote protocol.
  `zerologon` `cve-2020-1472` `netlogon` `domain-controller` `privilege-escalation`

- [extracting-browser-history-artifacts](../cybersecurity/extracting-browser-history-artifacts/) — Extract and analyze browser history, cookies, cache, downloads, and bookmarks from Chrome, Firefox, and Edge for forensic evidence of user web activity. Use when working with extracting browser history artifacts.
  `forensics` `browser-forensics` `chrome` `firefox` `edge`

- [extracting-config-from-agent-tesla-rat](../cybersecurity/extracting-config-from-agent-tesla-rat/) — Extract embedded configuration from Agent Tesla RAT samples including SMTP/FTP/Telegram exfiltration credentials, keylogger settings, and C2 endpoints using .NET decompilation and memory analysis. Use when working with extracting config from agent tesla rat.
  `agent-tesla` `rat` `config-extraction` `dotnet` `malware-analysis`

- [extracting-credentials-from-memory-dump](../cybersecurity/extracting-credentials-from-memory-dump/) — Extract cached credentials, password hashes, Kerberos tickets, and authentication tokens from memory dumps using Volatility and Mimikatz for forensic investigation. Use when working with extracting credentials from memory dump.
  `forensics` `credential-extraction` `memory-forensics` `volatility` `mimikatz`

- [extracting-iocs-from-malware-samples](../cybersecurity/extracting-iocs-from-malware-samples/) — Extracts indicators of compromise (IOCs) from malware samples including file hashes, network indicators (IPs, domains, URLs), host artifacts (file paths, registry keys, mutexes), and behavioral patterns for threat intelligence sharing and detection rule creation. Activates for requests involving IOC extraction, threat indicator harvesting, malware indicator collection, or building detection content from samples. . Use when working with extracting iocs from malware samples.
  `malware` `IOC-extraction` `threat-intelligence` `indicators` `detection`

- [extracting-memory-artifacts-with-rekall](../cybersecurity/extracting-memory-artifacts-with-rekall/) — Uses Rekall memory forensics framework to analyze memory dumps for process hollowing, injected code via VAD anomalies, hidden processes, and rootkit detection. Applies plugins like pslist, psscan, vadinfo, malfind, and dlllist to extract forensic artifacts from Windows memory images. Use during incident response memory analysis. . Use when working with extracting memory artifacts with rekall.
  `extracting` `memory` `artifacts` `with`

- [extracting-windows-event-logs-artifacts](../cybersecurity/extracting-windows-event-logs-artifacts/) — Extract, parse, and analyze Windows Event Logs (EVTX) using Chainsaw, Hayabusa, and EvtxECmd to detect lateral movement, persistence, and privilege escalation. Use when working with extracting windows event logs artifacts.
  `forensics` `windows-event-logs` `evtx` `chainsaw` `hayabusa`

- [fuzz-master](../cybersecurity/fuzz-master/) — Advanced fuzzing techniques for finding zero-days and hidden vulnerabilities. Use when automated scanners miss bugs, testing custom protocols, finding memory corruption, or hunting for novel attack vectors.
  `cybersecurity` `fuzz` `master` `security` `testing`

- [generating-threat-intelligence-reports](../cybersecurity/generating-threat-intelligence-reports/) — Generates structured cyber threat intelligence reports at strategic, operational, and tactical levels tailored to specific audiences including executives, security operations teams, and technical analysts. Use when producing finished intelligence products from raw collection data, creating sector threat briefings, or delivering post-incident intelligence assessments.
  `CTI` `threat-intelligence` `intelligence-products` `TLP` `PIR`

- [hackingtool](../cybersecurity/hackingtool/) — All-in-one terminal hacking toolkit — 185+ security tools across 20 categories with unified menu, search, and batch install. Use when setting up a pentest environment, launching security tools, or managing a hacking toolkit.
  `cybersecurity` `hackingtool` `penetration-testing` `security` `threat-defense`

- [hardening-docker-containers-for-production](../cybersecurity/hardening-docker-containers-for-production/) — Hardening Docker containers for production involves applying security best practices aligned with CIS Docker Benchmark v1.8.0 to minimize attack surface, prevent privilege escalation, and enforce leas. Use when working with hardening docker containers for production.
  `containers` `docker` `security` `hardening` `CIS-benchmark`

- [hardening-docker-daemon-configuration](../cybersecurity/hardening-docker-daemon-configuration/) — Harden the Docker daemon by configuring daemon.json with user namespace remapping, TLS authentication, rootless mode, and CIS benchmark controls. Use when working with hardening docker daemon configuration.
  `docker` `daemon-hardening` `container-security` `cis-benchmark` `rootless`

- [hardening-linux-endpoint-with-cis-benchmark](../cybersecurity/hardening-linux-endpoint-with-cis-benchmark/) — Hardens Linux endpoints using CIS Benchmark recommendations for Ubuntu, RHEL, and CentOS to reduce attack surface, enforce security baselines, and meet compliance requirements. Use when deploying new Linux servers, remediating audit findings, or establishing security baselines for Linux infrastructure. Activates for requests involving Linux hardening, CIS benchmarks for Linux, server security baselines, or Linux configuration compliance.

  `endpoint` `hardening` `linux-security` `CIS-benchmark` `Ubuntu`

- [hardening-windows-endpoint-with-cis-benchmark](../cybersecurity/hardening-windows-endpoint-with-cis-benchmark/) — Hardens Windows endpoints using CIS (Center for Internet Security) Benchmark recommendations to reduce attack surface, enforce security baselines, and meet compliance requirements. Use when deploying new Windows workstations or servers, remediating audit findings, or establishing organization-wide security baselines. Activates for requests involving Windows hardening, CIS benchmarks, GPO security baselines, or endpoint configuration compliance.

  `endpoint` `hardening` `windows-security` `CIS-benchmark` `GPO`

- [hexstrike-ai-pentest](../cybersecurity/hexstrike-ai-pentest/) — MCP-based cybersecurity automation with 150+ tools and 12 AI agents. Use when running automated pentests, solving CTF challenges, conducting bug bounty reconnaissance, or orchestrating.
  `pentest` `mcp` `automation` `bug-bounty` `ctf`

- [hunting-advanced-persistent-threats](../cybersecurity/hunting-advanced-persistent-threats/) — Proactively hunts for Advanced Persistent Threat (APT) activity within enterprise environments using hypothesis-driven searches across endpoint telemetry, network logs, and memory artifacts. Use when conducting scheduled threat hunting cycles, investigating anomalous behavior flagged by UEBA, or validating that known APT TTPs are not present in the environment. Activates for requests involving MITRE ATT&CK, Velociraptor, osquery, Zeek, or threat hunting playbooks.

  `MITRE-ATT&CK` `threat-hunting` `APT` `Velociraptor` `osquery`

- [hunting-credential-stuffing-attacks](../cybersecurity/hunting-credential-stuffing-attacks/) — Detects credential stuffing attacks by analyzing authentication logs for login velocity anomalies, ASN diversity, password spray patterns, and geographic distribution of failed logins. Uses statistical analysis on Splunk or raw log data. Use when investigating account takeover campaigns or building detection rules for auth abuse.

  `hunting` `credential` `stuffing` `attacks`

- [hunting-for-anomalous-powershell-execution](../cybersecurity/hunting-for-anomalous-powershell-execution/) — Use when hunt for malicious PowerShell activity by analyzing Script Block Logging (Event 4104), Module Logging (Event 4103), and process creation events. The analyst parses Windows Event Log EVTX files to detect obfuscated commands, AMSI bypass attempts, encoded payloads, credential dumping keywords, and suspicious download cradles. Activates for requests involving PowerShell threat hunting, script block analysis, encoded command detection, or AMSI bypass identification.
'.
  `powershell` `script-block-logging` `event-4104` `amsi` `threat-hunting`

- [hunting-for-beaconing-with-frequency-analysis](../cybersecurity/hunting-for-beaconing-with-frequency-analysis/) — Identify command-and-control beaconing patterns in network traffic by applying statistical frequency analysis, jitter calculation, and coefficient of variation scoring to detect periodic callbacks from compromised endpoints. Use when working with hunting for beaconing with frequency analysis.
  `threat-hunting` `beaconing` `c2-detection` `frequency-analysis` `network-traffic`

- [hunting-for-cobalt-strike-beacons](../cybersecurity/_deprecated/hunting-for-cobalt-strike-beacons/) — Detect Cobalt Strike beacon network activity using default TLS certificate signatures (serial 8BB00EE), JA3/JA3S/JARM fingerprints, HTTP C2 profile pattern matching, beacon jitter analysis, and named pipe detection via Zeek, Suricata, and Python PCAP analysis. Use when detecting cobalt strike beacon network activity using default tls certificate.
  `cobalt-strike` `beacon` `threat-hunting` `c2` `zeek`

- [hunting-for-command-and-control-beaconing](../cybersecurity/hunting-for-command-and-control-beaconing/) — Detect C2 beaconing patterns in network traffic using frequency analysis, jitter detection, and domain reputation to identify compromised endpoints communicating with adversary infrastructure. Use when detecting c2 beaconing patterns in network traffic using frequency analysis,.
  `threat-hunting` `mitre-attack` `c2` `beaconing` `network-analysis`

- [hunting-for-data-exfiltration-indicators](../cybersecurity/hunting-for-data-exfiltration-indicators/) — Hunt for data exfiltration through network traffic analysis, detecting unusual data flows, DNS tunneling, cloud storage uploads, and encrypted channel abuse. Use when hunting for data exfiltration through network traffic analysis, detecting unusual.
  `threat-hunting` `mitre-attack` `data-exfiltration` `dlp` `network-analysis`

- [hunting-for-data-staging-before-exfiltration](../cybersecurity/hunting-for-data-staging-before-exfiltration/) — Detect data staging activity before exfiltration by monitoring for archive creation with 7-Zip/RAR, unusual temp folder access, large file consolidation, and staging directory patterns via EDR and process telemetry. Use when detecting data staging activity before exfiltration by monitoring for archive.
  `data-staging` `exfiltration` `t1074` `archive-detection` `edr`

- [hunting-for-dcom-lateral-movement](../cybersecurity/hunting-for-dcom-lateral-movement/) — Hunt for DCOM-based lateral movement by detecting abuse of MMC20.Application, ShellBrowserWindow, and ShellWindows COM objects through Sysmon Event ID 1 (process creation) and Event ID 3 (network connection) correlation, WMI event analysis, RPC endpoint mapper traffic on port 135, and DCOM-specific parent-child process relationships. . Use when working with hunting for dcom lateral movement.
  `threat-hunting` `DCOM` `lateral-movement` `T1021.003` `Sysmon`

- [hunting-for-dcsync-attacks](../cybersecurity/hunting-for-dcsync-attacks/) — Detect DCSync attacks by analyzing Windows Event ID 4662 for unauthorized DS-Replication-Get-Changes requests from non-domain-controller accounts. Use when detecting dcsync attacks by analyzing windows event id 4662 for.
  `threat-hunting` `dcsync` `active-directory` `credential-access` `t1003.006`

- [hunting-for-defense-evasion-via-timestomping](../cybersecurity/hunting-for-defense-evasion-via-timestomping/) — Detect NTFS timestamp manipulation (MITRE T1070.006) by comparing $STANDARD_INFORMATION vs $FILE_NAME timestamps in the MFT. Uses analyzeMFT and Python to identify files with anomalous temporal patterns indicating anti-forensic timestomping activity. . Use when working with hunting for defense evasion via timestomping.
  `timestomping` `ntfs-forensics` `mft-analysis` `defense-evasion`

- [hunting-for-dns-based-persistence](../cybersecurity/hunting-for-dns-based-persistence/) — Hunt for DNS-based persistence mechanisms including DNS hijacking, dangling CNAME records, wildcard DNS abuse, and unauthorized zone modifications using passive DNS databases, SecurityTrails API, and DNS audit log analysis. Use when hunting for dns-based persistence mechanisms including dns hijacking, dangling cname.
  `dns` `persistence` `threat-hunting` `passive-dns` `dns-hijacking`

- [hunting-for-dns-tunneling-with-zeek](../cybersecurity/hunting-for-dns-tunneling-with-zeek/) — Detect DNS tunneling and data exfiltration by analyzing Zeek dns.log for high-entropy subdomain queries, excessive query volume, long query lengths, and unusual DNS record types indicating covert channel communication. Use when detecting dns tunneling and data exfiltration by analyzing zeek dns.log.
  `threat-hunting` `dns-tunneling` `zeek` `data-exfiltration` `covert-channel`

- [hunting-for-domain-fronting-c2-traffic](../cybersecurity/hunting-for-domain-fronting-c2-traffic/) — Detect domain fronting C2 traffic by analyzing SNI vs HTTP Host header mismatches in proxy logs and TLS certificate discrepancies using pyOpenSSL for certificate inspection. Use when detecting domain fronting c2 traffic by analyzing sni vs http.
  `domain-fronting` `c2-detection` `tls-inspection` `proxy-logs` `pyopenssl`

- [hunting-for-lateral-movement-via-wmi](../cybersecurity/hunting-for-lateral-movement-via-wmi/) — Detect WMI-based lateral movement by analyzing Windows Event ID 4688 process creation and Sysmon Event ID 1 for WmiPrvSE.exe child process patterns, remote process execution, and WMI event subscription persistence. Use when detecting wmi-based lateral movement by analyzing windows event id 4688.
  `threat-hunting` `lateral-movement` `wmi` `sysmon` `mitre-attack`

- [hunting-for-living-off-the-cloud-techniques](../cybersecurity/hunting-for-living-off-the-cloud-techniques/) — Hunt for adversary abuse of legitimate cloud services for C2, data staging, and exfiltration including abuse of Azure, AWS, GCP services, and SaaS platforms. Use when hunting for adversary abuse of legitimate cloud services for c2,.
  `threat-hunting` `mitre-attack` `cloud-abuse` `c2` `lotc`

- [hunting-for-living-off-the-land-binaries](../cybersecurity/_deprecated/hunting-for-living-off-the-land-binaries/) — Proactively hunt for adversary abuse of legitimate system binaries (LOLBins) to execute malicious payloads while evading detection. Use when working with hunting for living off the land binaries.
  `threat-hunting` `mitre-attack` `lolbins` `edr` `siem`

- [hunting-for-lolbins-execution-in-endpoint-logs](../cybersecurity/hunting-for-lolbins-execution-in-endpoint-logs/) — Hunt for adversary abuse of Living Off the Land Binaries (LOLBins) by analyzing endpoint process creation logs for suspicious execution patterns of legitimate Windows system binaries used for malicious purposes. Use when hunting for adversary abuse of living off the land binaries.
  `threat-hunting` `lolbins` `living-off-the-land` `endpoint-detection` `process-monitoring`

- [hunting-for-ntlm-relay-attacks](../cybersecurity/_deprecated/hunting-for-ntlm-relay-attacks/) — Detect NTLM relay attacks by analyzing Windows Event 4624 logon type 3 with NTLMSSP authentication, identifying IP-to-hostname mismatches, Responder traffic signatures, SMB signing status, and suspicious authentication patterns across the domain. Use when detecting ntlm relay attacks by analyzing windows event 4624 logon.
  `NTLM-relay` `Windows-events` `Event-4624` `NTLMSSP` `Responder`

- [hunting-for-persistence-mechanisms-in-windows](../cybersecurity/hunting-for-persistence-mechanisms-in-windows/) — Systematically hunt for adversary persistence mechanisms across Windows endpoints including registry, services, startup folders, and WMI subscriptions. Use when working with hunting for persistence mechanisms in windows.
  `threat-hunting` `mitre-attack` `persistence` `windows` `registry`

- [hunting-for-persistence-via-wmi-subscriptions](../cybersecurity/hunting-for-persistence-via-wmi-subscriptions/) — Hunt for adversary persistence through Windows Management Instrumentation event subscriptions by monitoring WMI consumer, filter, and binding creation events that execute malicious code triggered by system events. Use when hunting for adversary persistence through windows management instrumentation event subscriptions.
  `threat-hunting` `wmi-persistence` `mitre-t1546-003` `event-subscription` `windows`

- [hunting-for-process-injection-techniques](../cybersecurity/_deprecated/hunting-for-process-injection-techniques/) — Detect process injection techniques (T1055) including CreateRemoteThread, process hollowing, and DLL injection via Sysmon Event IDs 8 and 10 and EDR process telemetry. Use when detecting process injection techniques (t1055) including createremotethread, process hollowing, and.
  `process-injection` `t1055` `sysmon` `createremotethread` `dll-injection`

- [hunting-for-registry-persistence-mechanisms](../cybersecurity/hunting-for-registry-persistence-mechanisms/) — Hunt for registry-based persistence mechanisms including Run keys, Winlogon modifications, IFEO injection, and COM hijacking in Windows environments. Use when hunting for registry-based persistence mechanisms including run keys, winlogon modifications,.
  `threat-hunting` `mitre-attack` `registry` `persistence` `windows`

- [hunting-for-registry-run-key-persistence](../cybersecurity/_deprecated/hunting-for-registry-run-key-persistence/) — Detect MITRE ATT&CK T1547.001 registry Run key persistence by analyzing Sysmon Event ID 13 logs and registry queries to identify malicious auto-start entries. Use when detecting mitre att&ck t1547.001 registry run key persistence by analyzing.
  `persistence` `registry-run-keys` `t1547-001` `sysmon` `threat-hunting`

- [hunting-for-scheduled-task-persistence](../cybersecurity/hunting-for-scheduled-task-persistence/) — Hunt for adversary persistence via Windows Scheduled Tasks by analyzing task creation events, suspicious task actions, and unusual scheduling patterns. Use when hunting for adversary persistence via windows scheduled tasks by analyzing.
  `threat-hunting` `mitre-attack` `scheduled-tasks` `persistence` `t1053`

- [hunting-for-shadow-copy-deletion](../cybersecurity/hunting-for-shadow-copy-deletion/) — Hunt for Volume Shadow Copy deletion activity that indicates ransomware preparation or anti-forensics by monitoring vssadmin, wmic, and PowerShell shadow copy commands. Use when hunting for volume shadow copy deletion activity that indicates ransomware.
  `threat-hunting` `mitre-attack` `shadow-copy` `ransomware` `anti-forensics`

- [hunting-for-spearphishing-indicators](../cybersecurity/hunting-for-spearphishing-indicators/) — Hunt for spearphishing campaign indicators across email logs, endpoint telemetry, and network data to detect targeted email attacks. Use when hunting for spearphishing campaign indicators across email logs, endpoint telemetry,.
  `threat-hunting` `mitre-attack` `spearphishing` `initial-access` `email-security`

- [hunting-for-startup-folder-persistence](../cybersecurity/hunting-for-startup-folder-persistence/) — Detect T1547.001 startup folder persistence by monitoring Windows startup directories for suspicious file creation, analyzing autoruns entries, and using Python watchdog for real-time filesystem monitoring. Use when detecting t1547.001 startup folder persistence by monitoring windows startup directories.
  `threat-hunting` `T1547.001` `startup-folder` `persistence` `autoruns`

- [hunting-for-supply-chain-compromise](../cybersecurity/hunting-for-supply-chain-compromise/) — Hunt for supply chain compromise indicators including trojanized software updates, compromised dependencies, unauthorized code modifications, and tampered build artifacts. Use when hunting for supply chain compromise indicators including trojanized software updates,.
  `threat-hunting` `mitre-attack` `supply-chain` `initial-access` `t1195`

- [hunting-for-suspicious-scheduled-tasks](../cybersecurity/hunting-for-suspicious-scheduled-tasks/) — Hunt for adversary persistence and execution via Windows scheduled tasks by analyzing task creation events, suspicious task properties, and unusual execution patterns that indicate T1053.005 abuse. Use when hunting for adversary persistence and execution via windows scheduled tasks.
  `threat-hunting` `scheduled-tasks` `persistence` `mitre-t1053-005` `windows`

- [hunting-for-t1098-account-manipulation](../cybersecurity/hunting-for-t1098-account-manipulation/) — Hunt for MITRE ATT&CK T1098 account manipulation including shadow admin creation, SID history injection, group membership changes, and credential modifications using Windows Security Event Logs. Use when hunting for mitre att&ck t1098 account manipulation including shadow admin.
  `threat-hunting` `mitre-attack` `t1098` `account-manipulation` `active-directory`

- [hunting-for-unusual-network-connections](../cybersecurity/hunting-for-unusual-network-connections/) — Hunt for unusual network connections by analyzing outbound traffic patterns, rare destinations, non-standard ports, and anomalous connection frequencies from endpoints. Use when hunting for unusual network connections by analyzing outbound traffic patterns,.
  `threat-hunting` `mitre-attack` `network-analysis` `c2` `anomaly-detection`

- [hunting-for-unusual-service-installations](../cybersecurity/hunting-for-unusual-service-installations/) — Detect suspicious Windows service installations (MITRE ATT&CK T1543.003) by parsing System event logs for Event ID 7045, analyzing service binary paths, and identifying indicators of persistence mechanisms. Use when detecting suspicious windows service installations (mitre att&ck t1543.003) by parsing.
  `threat-hunting` `T1543.003` `service-installation` `persistence` `Event-7045`

- [hunting-for-webshell-activity](../cybersecurity/hunting-for-webshell-activity/) — Hunt for web shell deployments on internet-facing servers by analyzing file creation in web directories, suspicious process spawning from web servers, and anomalous HTTP patterns. Use when hunting for web shell deployments on internet-facing servers by analyzing.
  `threat-hunting` `mitre-attack` `webshell` `persistence` `web-server`

- [implementing-aes-encryption-for-data-at-rest](../cybersecurity/implementing-aes-encryption-for-data-at-rest/) — AES (Advanced Encryption Standard) is a symmetric block cipher standardized by NIST (FIPS 197) used to protect classified and sensitive data. This skill covers implementing AES-256 encryption in GCM m
  `cryptography` `encryption` `aes` `data-at-rest` `symmetric-encryption`

- [implementing-alert-fatigue-reduction](../cybersecurity/implementing-alert-fatigue-reduction/) — Implements strategies to reduce SOC alert fatigue by tuning detection rules, consolidating duplicate alerts, implementing risk-based alerting, and measuring alert quality metrics to maintain analyst effectiveness and prevent critical alert dismissal. Use when SOC teams face overwhelming alert volumes, high false positive rates, or declining analyst performance.

  `soc` `alert-fatigue` `tuning` `risk-based-alerting` `false-positive`

- [implementing-anti-phishing-training-program](../cybersecurity/implementing-anti-phishing-training-program/) — Security awareness training is the human layer of phishing defense. An effective anti-phishing training program combines regular simulations, interactive learning modules, metric tracking, and positiv. Use when working with implementing anti phishing training program.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [implementing-anti-ransomware-group-policy](../cybersecurity/implementing-anti-ransomware-group-policy/) — Configures Windows Group Policy Objects (GPO) to prevent ransomware execution and limit its spread. Implements AppLocker rules, Software Restriction Policies, Controlled Folder Access, attack surface reduction rules, and network protection settings. Activates for requests involving Windows GPO hardening against ransomware, AppLocker configuration, Controlled Folder Access setup, or endpoint protection via Group Policy. . Use when working with implementing anti ransomware group policy.
  `ransomware` `group-policy` `windows` `AppLocker` `hardening`

- [implementing-api-abuse-detection-with-rate-limiting](../cybersecurity/implementing-api-abuse-detection-with-rate-limiting/) — Implement API abuse detection using token bucket, sliding window, and adaptive rate limiting algorithms to prevent DDoS, brute force, and credential stuffing attacks. Use when implementing api abuse detection using token bucket, sliding window, and.
  `api-security` `rate-limiting` `token-bucket` `sliding-window` `ddos-protection`

- [implementing-api-gateway-security-controls](../cybersecurity/implementing-api-gateway-security-controls/) — Implements security controls at the API gateway layer including authentication enforcement, rate limiting, request validation, IP allowlisting, TLS termination, and threat protection. The engineer configures API gateways (Kong, AWS API Gateway, Azure APIM, Apigee) to act as a centralized security enforcement point that validates, throttles, and monitors all API traffic before it reaches backend services. Use when working with implementing api gateway security controls.
  `api-security` `api-gateway` `kong` `aws-api-gateway` `rate-limiting`

- [implementing-api-key-security-controls](../cybersecurity/implementing-api-key-security-controls/) — Implements secure API key generation, storage, rotation, and revocation controls to protect API authentication credentials from leakage, brute force, and abuse. The engineer designs API key formats with sufficient entropy, implements secure hashing for storage, enforces per-key scoping and rate limiting, monitors for leaked keys in public repositories, and builds key rotation workflows. Use when working with implementing api key security controls.
  `api-security` `api-keys` `credential-management` `key-rotation` `secret-management`

- [implementing-api-rate-limiting-and-throttling](../cybersecurity/implementing-api-rate-limiting-and-throttling/) — Use when implements API rate limiting and throttling controls using token bucket, sliding window, and fixed window algorithms to protect against brute force attacks, credential stuffing, resource exhaustion, and API abuse. The engineer configures per-user, per-IP, and per-endpoint rate limits using Redis-backed counters, API gateway plugins, or application middleware, and implements proper HTTP 429 responses with Retry-After headers.
  `api-security` `rate-limiting` `throttling` `redis` `token-bucket`

- [implementing-api-schema-validation-security](../cybersecurity/implementing-api-schema-validation-security/) — Implement API schema validation using OpenAPI specifications and JSON Schema to enforce input/output contracts and prevent injection, data exposure, and mass assignment attacks. Use when implementing api schema validation using openapi specifications and json schema.
  `api-security` `schema-validation` `openapi` `json-schema` `input-validation`

- [implementing-api-security-posture-management](../cybersecurity/implementing-api-security-posture-management/) — Implement API Security Posture Management to continuously discover, classify, and score APIs based on risk while enforcing security policies across the API lifecycle. Use when implementing api security posture management to continuously discover, classify, and.
  `api-security` `aspm` `api-posture-management` `api-discovery` `risk-scoring`

- [implementing-api-security-testing-with-42crunch](../cybersecurity/implementing-api-security-testing-with-42crunch/) — Implement comprehensive API security testing using the 42Crunch platform to perform static audit and dynamic conformance scanning of OpenAPI specifications. Use when implementing comprehensive api security testing using the 42crunch platform to.
  `api-security` `42crunch` `openapi` `api-audit` `api-scan`

- [implementing-api-threat-protection-with-apigee](../cybersecurity/implementing-api-threat-protection-with-apigee/) — Implement API threat protection using Google Apigee policies including JSON/XML threat protection, OAuth 2.0, SpikeArrest, and Advanced API Security for OWASP Top 10 defense. Use when implementing api threat protection using google apigee policies including json/xml.
  `apigee` `api-gateway` `threat-protection` `json-threat-protection` `xml-threat-protection`

- [implementing-application-whitelisting-with-applocker](../cybersecurity/implementing-application-whitelisting-with-applocker/) — Implements application whitelisting using Windows AppLocker to restrict unauthorized software execution on endpoints, reducing attack surface from malware, unauthorized tools, and shadow IT. Use when enforcing application control policies, meeting compliance requirements for software restriction, or preventing execution of unsigned or untrusted binaries. Activates for requests involving AppLocker, application whitelisting, software restriction, or executable control.

  `endpoint` `AppLocker` `application-whitelisting` `windows-security` `software-restriction`

- [implementing-aqua-security-for-container-scanning](../cybersecurity/implementing-aqua-security-for-container-scanning/) — Deploy Aqua Security's Trivy scanner to detect vulnerabilities, misconfigurations, secrets, and license issues in container images across CI/CD pipelines and registries. Use when deploying aqua security's trivy scanner to detect vulnerabilities, misconfigurations, secrets,.
  `aqua-security` `trivy` `container-scanning` `vulnerability-scanning` `sbom`

- [implementing-attack-path-analysis-with-xm-cyber](../cybersecurity/implementing-attack-path-analysis-with-xm-cyber/) — Deploy XM Cyber's continuous exposure management platform to map attack paths, identify choke points, and prioritize the 2% of exposures that threaten critical assets. Use when deploying xm cyber's continuous exposure management platform to map attack.
  `xm-cyber` `attack-path-analysis` `exposure-management` `ctem` `choke-points`

- [implementing-attack-surface-management](../cybersecurity/implementing-attack-surface-management/) — Implements external attack surface management (EASM) using Shodan, Censys, and ProjectDiscovery tools (subfinder, httpx, nuclei) for asset discovery, subdomain enumeration, service fingerprinting, and exposure scoring. Includes a weighted risk scoring algorithm based on OWASP attack surface analysis methodology and the Relative Attack Surface Quotient (RSQ). Use when building continuous ASM programs or performing external reconnaissance for security assessments.

  `attack-surface` `reconnaissance` `shodan` `censys` `subfinder`

- [implementing-aws-config-rules-for-compliance](../cybersecurity/implementing-aws-config-rules-for-compliance/) — Implementing AWS Config rules for continuous compliance monitoring of AWS resources, deploying managed and custom rules aligned to CIS and PCI DSS frameworks, configuring automatic remediation with SSM Automation, and aggregating compliance data across accounts. . Use when working with implementing aws config rules for compliance.
  `cloud-security` `aws` `config-rules` `compliance` `automation`

- [implementing-aws-iam-permission-boundaries](../cybersecurity/implementing-aws-iam-permission-boundaries/) — Configure IAM permission boundaries in AWS to delegate role creation to developers while enforcing maximum privilege limits set by the security team. Use when configureing iam permission boundaries in aws to delegate role creation.
  `aws` `iam` `permission-boundaries` `least-privilege` `delegation`

- [implementing-aws-macie-for-data-classification](../cybersecurity/implementing-aws-macie-for-data-classification/) — Implement Amazon Macie to automatically discover, classify, and protect sensitive data in S3 buckets using machine learning and pattern matching for PII, financial data, and credentials detection. Use when implementing amazon macie to automatically discover, classify, and protect sensitive.
  `aws` `macie` `data-classification` `s3` `pii`

- [implementing-aws-nitro-enclave-security](../cybersecurity/implementing-aws-nitro-enclave-security/) — Use when implements AWS Nitro Enclave-based confidential computing environments with cryptographic attestation, KMS policy integration using PCR-based condition keys, and secure vsock communication channels. The practitioner builds enclave images, configures attestation-aware KMS policies, validates attestation documents against the AWS Nitro PKI root of trust, and establishes isolated computation pipelines for processing sensitive data such as PII, cryptographic keys, and healthcare records.
  `AWS-Nitro-Enclaves` `confidential-computing` `attestation` `KMS` `enclave-isolation`

- [implementing-aws-security-hub](../cybersecurity/implementing-aws-security-hub/) — This skill covers deploying AWS Security Hub as a centralized cloud security posture management platform that aggregates findings from GuardDuty, Inspector, Macie, and third-party tools. It details enabling security standards like CIS AWS Foundations Benchmark, configuring automated remediation, and building executive dashboards for compliance tracking across multi-account AWS organizations.

  `aws-security-hub` `cspm` `compliance-automation` `security-standards` `finding-aggregation`

- [implementing-aws-security-hub-compliance](../cybersecurity/implementing-aws-security-hub-compliance/) — Implementing AWS Security Hub to aggregate security findings across AWS accounts, enable compliance standards like CIS AWS Foundations and PCI DSS, configure automated remediation with EventBridge and Lambda, and create custom security insights for organizational risk management.

  `cloud-security` `aws` `security-hub` `compliance` `cspm`

- [implementing-azure-ad-privileged-identity-management](../cybersecurity/implementing-azure-ad-privileged-identity-management/) — Configure Microsoft Entra Privileged Identity Management to enforce just-in-time role activation, approval workflows, and access reviews for Azure AD privileged roles. Use when configureing microsoft entra privileged identity management to enforce just-in-time role.
  `azure-ad` `pim` `entra-id` `just-in-time` `privileged-roles`

- [implementing-azure-defender-for-cloud](../cybersecurity/implementing-azure-defender-for-cloud/) — Implementing Microsoft Defender for Cloud to enable cloud security posture management, workload protection across VMs, containers, databases, and storage, configure security recommendations, and set up adaptive security controls with automated remediation.

  `cloud-security` `azure` `defender-for-cloud` `cspm` `cwpp`

- [implementing-beyondcorp-zero-trust-access-model](../cybersecurity/implementing-beyondcorp-zero-trust-access-model/) — Implementing Google's BeyondCorp zero trust access model to eliminate implicit trust from the network perimeter, enforce identity-aware access controls using IAP, Access Context Manager, and Chrome Enterprise Premium for VPN-less secure application access. . Use when working with implementing beyondcorp zero trust access model.
  `beyondcorp` `zero-trust` `google-cloud` `iap` `identity-aware-proxy`

- [implementing-bgp-security-with-rpki](../cybersecurity/implementing-bgp-security-with-rpki/) — Implement BGP route origin validation using RPKI with Route Origin Authorizations, RPKI-to-Router protocol, and ROV policies on Cisco and Juniper routers to prevent route hijacking. Use when implementing bgp route origin validation using rpki with route origin.
  `bgp` `rpki` `route-origin-validation` `rov` `roa`

- [implementing-browser-isolation-for-zero-trust](../cybersecurity/implementing-browser-isolation-for-zero-trust/) — Use when deploys remote browser isolation (RBI) as a core component of a Zero Trust architecture. Implements isolation policies with URL categorization and risk-based routing, content disarming and reconstruction (CDR) for file sanitization, data loss prevention controls within isolated sessions, and integration with Secure Web Gateway and ZTNA platforms. Based on Cloudflare Browser Isolation, Menlo Security, and Zscaler RBI approaches.
  `browser-isolation` `zero-trust` `RBI` `CDR` `URL-categorization`

- [implementing-canary-tokens-for-network-intrusion](../cybersecurity/implementing-canary-tokens-for-network-intrusion/) — Deploys DNS, HTTP, and AWS API key canary tokens across network infrastructure to detect unauthorized access and lateral movement. Integrates with webhook alerting (Slack, Teams, email, generic HTTP) for real-time intrusion notifications. Provides automated token generation, placement strategies, and monitoring for enterprise network environments. Use when building deception-based network intrusion detection with Canarytokens.org and Thinkst Canary platforms.

  `canary-tokens` `intrusion-detection` `deception` `network-security` `honeytokens`

- [implementing-cisa-zero-trust-maturity-model](../cybersecurity/implementing-cisa-zero-trust-maturity-model/) — Implement the CISA Zero Trust Maturity Model v2.0 across the five pillars of identity, devices, networks, applications, and data to achieve progressive organizational zero trust maturity. Use when implementing the cisa zero trust maturity model v2.0 across the.
  `zero-trust` `cisa` `maturity-model` `federal-compliance` `governance`

- [implementing-cloud-dlp-for-data-protection](../cybersecurity/implementing-cloud-dlp-for-data-protection/) — Implementing Cloud Data Loss Prevention (DLP) using Amazon Macie, Azure Information Protection, and Google Cloud DLP API to discover, classify, and protect sensitive data across cloud storage, databases, and data pipelines. . Use when working with implementing cloud dlp for data protection.
  `cloud-security` `dlp` `data-protection` `macie` `data-classification`

- [implementing-cloud-security-posture-management](../cybersecurity/implementing-cloud-security-posture-management/) — Implementing Cloud Security Posture Management (CSPM) to continuously monitor multi-cloud environments for misconfigurations, compliance violations, and security risks using Prowler, ScoutSuite, AWS Security Hub, Azure Defender, and GCP Security Command Center. . Use when working with implementing cloud security posture management.
  `cloud-security` `cspm` `multi-cloud` `compliance` `prowler`

- [implementing-cloud-trail-log-analysis](../cybersecurity/implementing-cloud-trail-log-analysis/) — Implementing AWS CloudTrail log analysis for security monitoring, threat detection, and forensic investigation using Athena, CloudWatch Logs Insights, and SIEM integration to identify unauthorized access, privilege escalation, and suspicious API activity. . Use when working with implementing cloud trail log analysis.
  `cloud-security` `aws` `cloudtrail` `log-analysis` `threat-detection`

- [implementing-cloud-vulnerability-posture-management](../cybersecurity/implementing-cloud-vulnerability-posture-management/) — Implement Cloud Security Posture Management using AWS Security Hub, Azure Defender for Cloud, and open-source tools like Prowler and ScoutSuite for multi-cloud vulnerability detection. Use when implementing cloud security posture management using aws security hub, azure.
  `cspm` `cloud-security` `aws-security-hub` `azure-defender` `prowler`

- [implementing-cloud-waf-rules](../cybersecurity/implementing-cloud-waf-rules/) — This skill covers deploying and tuning Web Application Firewall rules on AWS WAF, Azure WAF, and Cloudflare to protect cloud-hosted applications against OWASP Top 10 attacks. It details configuring managed rule sets, creating custom rules for business logic protection, implementing rate limiting, deploying bot management, and reducing false positives through rule tuning and logging analysis.

  `cloud-waf` `aws-waf` `azure-waf` `cloudflare-waf` `owasp-protection`

- [implementing-cloud-workload-protection](../cybersecurity/implementing-cloud-workload-protection/) — Implements cloud workload protection using boto3 and google-cloud APIs for runtime security monitoring, process anomaly detection, and file integrity checking on EC2/GCE instances. Scans for cryptomining, reverse shells, and unauthorized binaries. Use when building runtime security controls for cloud compute workloads.

  `implementing` `cloud` `workload` `protection`

- [implementing-code-signing-for-artifacts](../cybersecurity/implementing-code-signing-for-artifacts/) — This skill covers implementing code signing for build artifacts to ensure integrity and authenticity throughout the software supply chain. It addresses signing binaries, packages, and containers using GPG, Sigstore, and platform-specific signing tools, establishing trust chains, and verifying signatures in deployment pipelines.

  `devsecops` `cicd` `code-signing` `supply-chain` `sigstore`

- [implementing-conditional-access-policies-azure-ad](../cybersecurity/implementing-conditional-access-policies-azure-ad/) — Configure Microsoft Entra ID (Azure AD) Conditional Access policies for zero trust access control. Covers signal-based policy design, device compliance requirements, risk-based authentication, named l
  `iam` `identity` `access-control` `azure-ad` `entra-id`

- [implementing-conduit-security-for-ot-remote-access](../cybersecurity/implementing-conduit-security-for-ot-remote-access/) — Implement secure conduit architecture for OT remote access following IEC 62443 zones and conduits model, deploying jump servers, MFA-enabled gateways, session recording, and approval-based workflows to control vendor and engineer access to industrial control systems without exposing OT networks directly. . Use when working with implementing conduit security for ot remote access.
  `ot-security` `ics` `remote-access` `iec62443` `jump-server`

- [implementing-container-image-minimal-base-with-distroless](../cybersecurity/implementing-container-image-minimal-base-with-distroless/) — Reduce container attack surface by building application images on Google distroless base images that contain only the application runtime with no shell, package manager, or unnecessary OS utilities. Use when working with implementing container image minimal base with distroless.
  `distroless` `container-images` `minimal-base` `attack-surface` `docker`

- [implementing-container-network-policies-with-calico](../cybersecurity/implementing-container-network-policies-with-calico/) — Enforce Kubernetes network segmentation using Calico CNI network policies and global network policies to control pod-to-pod traffic, restrict egress, and implement zero-trust microsegmentation. Use when working with implementing container network policies with calico.
  `container-security` `kubernetes` `calico` `network-policy` `microsegmentation`

- [implementing-continuous-security-validation-with-bas](../cybersecurity/implementing-continuous-security-validation-with-bas/) — Deploy Breach and Attack Simulation tools to continuously validate security control effectiveness by safely emulating real-world attack techniques across the kill chain. Use when deploying breach and attack simulation tools to continuously validate security.
  `breach-attack-simulation` `bas` `security-validation` `safebreach` `attackiq`

- [implementing-data-loss-prevention-with-microsoft-purview](../cybersecurity/implementing-data-loss-prevention-with-microsoft-purview/) — Use when implements data loss prevention policies using Microsoft Purview to protect sensitive information across Exchange Online, SharePoint, OneDrive, Teams, endpoint devices, and Power BI. The analyst configures sensitivity labels with encryption and content marking, creates DLP policies using built-in and custom sensitive information types with regex patterns, deploys endpoint DLP rules to control file operations on Windows and macOS devices, and monitors policy effectiveness through Acti...
  `DLP` `Microsoft-Purview` `sensitivity-labels` `endpoint-DLP` `data-classification`

- [implementing-ddos-mitigation-with-cloudflare](../cybersecurity/implementing-ddos-mitigation-with-cloudflare/) — Configure Cloudflare DDoS protection with managed rulesets, rate limiting, WAF rules, Bot Management, and origin protection to mitigate volumetric, protocol, and application-layer attacks. Use when configureing cloudflare ddos protection with managed rulesets, rate limiting, waf.
  `ddos` `cloudflare` `ddos-mitigation` `rate-limiting` `waf`

- [implementing-deception-based-detection-with-canarytoken](../cybersecurity/implementing-deception-based-detection-with-canarytoken/) — Deploy and monitor Canary Tokens via the Thinkst Canary API for deception-based breach detection using web bug tokens, DNS tokens, document tokens, and AWS key tokens. Use when deploying and monitor canary tokens via the thinkst canary api.
  `canarytoken` `deception` `honeytokens` `breach-detection` `Thinkst-Canary`

- [implementing-delinea-secret-server-for-pam](../cybersecurity/implementing-delinea-secret-server-for-pam/) — Implements Delinea Secret Server for privileged access management (PAM) including secret vault configuration, role-based access policies, automated password rotation, session recording, and integration with Active Directory and cloud platforms. Activates for requests involving PAM deployment, privileged credential vaulting, secret server administration, or password rotation automation.

  `PAM` `Delinea` `Secret-Server` `privileged-access` `password-vault`

- [implementing-device-posture-assessment-in-zero-trust](../cybersecurity/implementing-device-posture-assessment-in-zero-trust/) — Implementing device posture assessment as a zero trust access control by integrating endpoint health signals from CrowdStrike ZTA, Microsoft Intune, and Jamf into conditional access policies that enforce compliance before granting resource access. . Use when working with implementing device posture assessment in zero trust.
  `device-posture` `zero-trust` `endpoint-compliance` `crowdstrike-zta` `intune`

- [implementing-devsecops-security-scanning](../cybersecurity/implementing-devsecops-security-scanning/) — Integrates Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), and Software Composition Analysis (SCA) into CI/CD pipelines using open-source tools. Covers Semgrep for SAST, Trivy for SCA and container scanning, OWASP ZAP for DAST, and Gitleaks for secrets detection. Activates for requests involving DevSecOps pipeline setup, automated security scanning in CI/CD, SAST/DAST/SCA integration, or shift-left security implementation.

  `devsecops` `SAST` `DAST` `SCA` `semgrep`

- [implementing-diamond-model-analysis](../cybersecurity/implementing-diamond-model-analysis/) — The Diamond Model of Intrusion Analysis provides a structured framework for analyzing cyber intrusions by examining four core features - Adversary, Capability, Infrastructure, and Victim. This skill covers implementing the Diamond Model programmatically to classify and correlate intrusion events, build activity threads, and generate pivot-ready intelligence.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [implementing-digital-signatures-with-ed25519](../cybersecurity/implementing-digital-signatures-with-ed25519/) — Ed25519 is a high-performance digital signature algorithm using the Edwards curve Curve25519. It provides 128-bit security with 64-byte signatures and 32-byte keys, offering significant advantages ove. Use when working with implementing digital signatures with ed25519.
  `cryptography` `digital-signatures` `ed25519` `authentication` `integrity`

- [implementing-disk-encryption-with-bitlocker](../cybersecurity/implementing-disk-encryption-with-bitlocker/) — Implements full disk encryption using Microsoft BitLocker on Windows endpoints to protect data at rest from unauthorized access in case of device loss or theft. Use when deploying encryption for compliance requirements, securing mobile workstations, or implementing data protection controls across the enterprise. Activates for requests involving BitLocker encryption, disk encryption, TPM configuration, or data-at-rest protection.

  `endpoint` `encryption` `BitLocker` `TPM` `data-protection`

- [implementing-dmarc-dkim-spf-email-security](../cybersecurity/implementing-dmarc-dkim-spf-email-security/) — SPF, DKIM, and DMARC form the three pillars of email authentication. Together they prevent domain spoofing, validate message integrity, and define policies for handling unauthenticated mail. Proper im. Use when working with implementing dmarc dkim spf email security.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [implementing-dragos-platform-for-ot-monitoring](../cybersecurity/implementing-dragos-platform-for-ot-monitoring/) — Deploy and configure the Dragos Platform for OT network monitoring, leveraging its 600+ industrial protocol parsers, intelligence-driven threat detection analytics, and asset visibility capabilities to protect ICS environments against threat groups like VOLTZITE, GRAPHITE, and BAUXITE. . Use when working with implementing dragos platform for ot monitoring.
  `ot-security` `ics` `dragos` `threat-detection` `ot-monitoring`

- [implementing-ebpf-security-monitoring](../cybersecurity/implementing-ebpf-security-monitoring/) — Implements eBPF-based security monitoring using Cilium Tetragon for real-time process execution tracking, network connection observability, file access auditing, and runtime enforcement. Covers TracingPolicy CRD authoring with kprobe/tracepoint hooks, in-kernel filtering via matchArgs/matchBinaries selectors, JSON event export, and integration with SIEM pipelines. Use when building kernel-level runtime security observability for Linux hosts or Kubernetes clusters.

  `implementing` `ebpf` `security` `monitoring` `tetragon`

- [implementing-email-sandboxing-with-proofpoint](../cybersecurity/implementing-email-sandboxing-with-proofpoint/) — Email sandboxing detonates suspicious attachments and URLs in isolated environments to detect zero-day malware and evasive phishing payloads. Proofpoint Targeted Attack Protection (TAP) is an industry. Use when working with implementing email sandboxing with proofpoint.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [implementing-end-to-end-encryption-for-messaging](../cybersecurity/implementing-end-to-end-encryption-for-messaging/) — End-to-end encryption (E2EE) ensures that only the communicating parties can read messages, with no intermediary (including the server) able to decrypt them. This skill implements a simplified version. Use when working with implementing end to end encryption for messaging.
  `cryptography` `encryption` `e2e` `messaging` `signal-protocol`

- [implementing-endpoint-detection-with-wazuh](../cybersecurity/implementing-endpoint-detection-with-wazuh/) — Deploy and configure Wazuh SIEM/XDR for endpoint detection including agent management, custom decoder and rule XML creation, alert querying via the Wazuh REST API, and automated response actions.
  `siem` `xdr` `wazuh` `endpoint-detection` `custom-rules`

- [implementing-endpoint-dlp-controls](../cybersecurity/implementing-endpoint-dlp-controls/) — Implements endpoint Data Loss Prevention (DLP) controls to detect and prevent sensitive data exfiltration through email, USB, cloud storage, and printing. Use when deploying DLP agents, creating content inspection policies, or preventing unauthorized data movement from endpoints. Activates for requests involving DLP, data exfiltration prevention, content inspection, or sensitive data protection on endpoints.

  `endpoint` `DLP` `data-loss-prevention` `data-protection` `content-inspection`

- [implementing-envelope-encryption-with-aws-kms](../cybersecurity/implementing-envelope-encryption-with-aws-kms/) — Envelope encryption is a strategy where data is encrypted with a data encryption key (DEK), and the DEK itself is encrypted with a master key (KEK) managed by AWS KMS. This approach allows encrypting. Use when working with implementing envelope encryption with aws kms.
  `cryptography` `encryption` `aws` `kms` `envelope-encryption`

- [implementing-epss-score-for-vulnerability-prioritization](../cybersecurity/implementing-epss-score-for-vulnerability-prioritization/) — Integrate FIRST's Exploit Prediction Scoring System (EPSS) API to prioritize vulnerability remediation based on real-world exploitation probability within 30 days. Use when integrateing first's exploit prediction scoring system (epss) api to prioritize.
  `epss` `vulnerability-prioritization` `first` `exploit-prediction` `cvss`

- [implementing-file-integrity-monitoring-with-aide](../cybersecurity/implementing-file-integrity-monitoring-with-aide/) — Configure AIDE (Advanced Intrusion Detection Environment) for file integrity monitoring including baseline creation, scheduled integrity checks, change detection, and alerting. Use when configureing aide (advanced intrusion detection environment) for file integrity monitoring.
  `aide` `file-integrity` `hids` `baseline` `intrusion-detection`

- [implementing-fuzz-testing-in-cicd-with-aflplusplus](../cybersecurity/implementing-fuzz-testing-in-cicd-with-aflplusplus/) — Integrate AFL++ coverage-guided fuzz testing into CI/CD pipelines to discover memory corruption, input handling, and logic vulnerabilities in C/C++ and compiled applications. Use when integrateing afl++ coverage-guided fuzz testing into ci/cd pipelines to discover.
  `aflplusplus` `fuzz-testing` `cicd` `coverage-guided-fuzzing` `security-testing`

- [implementing-gcp-binary-authorization](../cybersecurity/implementing-gcp-binary-authorization/) — Implement GCP Binary Authorization to enforce deploy-time security controls that ensure only trusted, attested container images are deployed to Google Kubernetes Engine and Cloud Run. Use when implementing gcp binary authorization to enforce deploy-time security controls that.
  `gcp` `binary-authorization` `container-security` `supply-chain` `gke`

- [implementing-gcp-organization-policy-constraints](../cybersecurity/implementing-gcp-organization-policy-constraints/) — Implement GCP Organization Policy constraints to enforce security guardrails across the entire resource hierarchy, restricting risky configurations and ensuring compliance at organization, folder, and project levels. Use when implementing gcp organization policy constraints to enforce security guardrails across.
  `gcp` `organization-policy` `constraints` `governance` `compliance`

- [implementing-gcp-vpc-firewall-rules](../cybersecurity/implementing-gcp-vpc-firewall-rules/) — Implementing and auditing GCP VPC firewall rules to enforce network segmentation, restrict ingress and egress traffic, apply hierarchical firewall policies across the organization, and monitor firewall rule effectiveness using VPC Flow Logs. . Use when working with implementing gcp vpc firewall rules.
  `cloud-security` `gcp` `vpc` `firewall-rules` `network-security`

- [implementing-gdpr-data-protection-controls](../cybersecurity/implementing-gdpr-data-protection-controls/) — The General Data Protection Regulation (EU) 2016/679 (GDPR) is the EU's comprehensive data protection law governing the collection, processing, storage, and transfer of personal data. This skill cover
  `compliance` `governance` `gdpr` `privacy` `data-protection`

- [implementing-gdpr-data-subject-access-request](../cybersecurity/implementing-gdpr-data-subject-access-request/) — Automates GDPR Data Subject Access Request (DSAR) workflows including identity verification, PII discovery across databases and files using regex and NER, data mapping, response templating per Article 15 requirements, deadline tracking, and audit logging. Covers ICO/EDPB guidance compliance, exemption handling, and scalable batch processing. Use when building or auditing DSAR response capabilities under GDPR/UK GDPR.

  `gdpr` `dsar` `privacy` `pii-discovery` `data-subject-rights`

- [implementing-github-advanced-security-for-code-scanning](../cybersecurity/implementing-github-advanced-security-for-code-scanning/) — Configure GitHub Advanced Security with CodeQL to perform automated static analysis and vulnerability detection across repositories at enterprise scale.
  `github-advanced-security` `codeql` `sast` `code-scanning` `supply-chain-security`

- [implementing-google-workspace-admin-security](../cybersecurity/implementing-google-workspace-admin-security/) — Implements comprehensive Google Workspace security hardening including admin console configuration, phishing-resistant MFA enforcement, DLP policies, email authentication (SPF/DKIM/DMARC), OAuth app control, and external sharing restrictions. Activates for requests involving Google Workspace hardening, G Suite security configuration, or cloud office security administration. . Use when working with implementing google workspace admin security.
  `Google-Workspace` `admin-security` `MFA` `DMARC` `DLP`

- [implementing-google-workspace-phishing-protection](../cybersecurity/implementing-google-workspace-phishing-protection/) — Configure Google Workspace advanced phishing and malware protection settings including pre-delivery scanning, attachment protection, spoofing detection, and Enhanced Safe Browsing. Use when configureing google workspace advanced phishing and malware protection settings including.
  `google-workspace` `gmail` `phishing` `email-security` `safe-browsing`

- [implementing-google-workspace-sso-configuration](../cybersecurity/implementing-google-workspace-sso-configuration/) — Configure SAML 2.0 single sign-on for Google Workspace with a third-party identity provider, enabling centralized authentication and enforcing organization-wide access policies. Use when configureing saml 2.0 single sign-on for google workspace with a.
  `google-workspace` `sso` `saml` `identity-provider` `authentication`

- [implementing-hardware-security-key-authentication](../cybersecurity/implementing-hardware-security-key-authentication/) — Implements FIDO2/WebAuthn hardware security key authentication including registration ceremonies, authentication flows, YubiKey enrollment, and passkey migration strategies. Builds a complete relying party server using the python-fido2 library that supports cross-platform authenticators, resident key (discoverable credential) workflows, and user verification policies. Use when working with implementing hardware security key authentication.
  `FIDO2` `WebAuthn` `hardware-security-key` `YubiKey` `passkeys`

- [implementing-hashicorp-vault-dynamic-secrets](../cybersecurity/implementing-hashicorp-vault-dynamic-secrets/) — Implements HashiCorp Vault dynamic secrets engines for database credentials, AWS IAM keys, and PKI certificates with automatic generation, lease management, and credential rotation to eliminate static secrets in application configurations. Activates for requests involving Vault secrets engine configuration, dynamic database credentials, ephemeral cloud credentials, or automated secret rotation.

  `HashiCorp-Vault` `dynamic-secrets` `secrets-management` `database-credentials` `AWS-secrets`

- [implementing-honeypot-for-ransomware-detection](../cybersecurity/implementing-honeypot-for-ransomware-detection/) — Deploys canary files, honeypot shares, and decoy systems to detect ransomware activity at the earliest possible stage. Configures canary tokens embedded in strategic file locations that trigger alerts when ransomware attempts encryption, uses honeypot network shares that mimic high-value targets, and deploys Thinkst Canary appliances for comprehensive deception-based detection. Use when working with implementing honeypot for ransomware detection.
  `ransomware` `detection` `honeypot` `canary` `defense`

- [implementing-honeytokens-for-breach-detection](../cybersecurity/implementing-honeytokens-for-breach-detection/) — Deploys canary tokens and honeytokens (fake AWS credentials, DNS canaries, document beacons, database records) that trigger alerts when accessed by attackers. Uses the Canarytokens API and custom webhook integrations for breach detection. Use when building deception-based early warning systems for intrusion detection.

  `implementing` `honeytokens` `for` `breach`

- [implementing-ics-firewall-with-tofino](../cybersecurity/implementing-ics-firewall-with-tofino/) — Deploy and configure Tofino industrial firewalls from Belden/Hirschmann to protect SCADA systems and PLCs using deep packet inspection for OT protocols including Modbus, EtherNet/IP, OPC, and S7comm, enforcing granular access control between ICS security zones. . Use when working with implementing ics firewall with tofino.
  `ot-security` `ics` `firewall` `tofino` `belden`

- [implementing-identity-governance-with-sailpoint](../cybersecurity/implementing-identity-governance-with-sailpoint/) — Deploy SailPoint IdentityNow or IdentityIQ for identity governance and administration. Covers identity lifecycle management, access request workflows, certification campaigns, role mining, SOD policy
  `iam` `identity` `access-control` `governance` `sailpoint`

- [implementing-identity-verification-for-zero-trust](../cybersecurity/implementing-identity-verification-for-zero-trust/) — Implement continuous identity verification for zero trust using phishing-resistant MFA (FIDO2/WebAuthn), risk-based conditional access, and identity governance aligned with the CISA Zero Trust Maturity Model. Use when implementing continuous identity verification for zero trust using phishing-resistant mfa.
  `zero-trust` `identity` `authentication` `mfa` `identity-verification`

- [implementing-iec-62443-security-zones](../cybersecurity/implementing-iec-62443-security-zones/) — This skill covers designing and implementing security zones and conduits for industrial automation and control systems (IACS) per IEC 62443-3-2. It addresses zone partitioning based on risk assessment, assigning Security Level targets (SL-T), designing conduit security controls, implementing microsegmentation with industrial firewalls, and validating zone architecture through traffic analysis and penetration testing against the Purdue Reference Model.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [implementing-image-provenance-verification-with-cosign](../cybersecurity/implementing-image-provenance-verification-with-cosign/) — Sign and verify container image provenance using Sigstore Cosign with keyless OIDC-based signing, attestations, and Kubernetes admission enforcement. Use when working with implementing image provenance verification with cosign.
  `cosign` `sigstore` `image-signing` `supply-chain` `provenance`

- [implementing-immutable-backup-with-restic](../cybersecurity/implementing-immutable-backup-with-restic/) — Implements immutable backup strategy using restic with S3-compatible storage and object lock for ransomware-resistant data protection. Automates backup creation, integrity verification via restic check --read-data, snapshot retention policy enforcement, and restore testing. Integrates with AWS S3 Object Lock, MinIO, and Backblaze B2 for WORM (Write Once Read Many) storage that prevents backup deletion or encryption by ransomware actors.

  `restic` `backup` `immutable` `ransomware` `s3`

- [implementing-infrastructure-as-code-security-scanning](../cybersecurity/implementing-infrastructure-as-code-security-scanning/) — This skill covers implementing automated security scanning for Infrastructure as Code (IaC) templates using tools like Checkov, tfsec, and KICS. It addresses detecting misconfigurations in Terraform, CloudFormation, Kubernetes manifests, and Helm charts before deployment, establishing policy-based governance, and integrating IaC scanning into CI/CD pipelines to prevent insecure cloud resource provisioning.

  `devsecops` `cicd` `iac-security` `checkov` `tfsec`

- [implementing-iso-27001-information-security-management](../cybersecurity/implementing-iso-27001-information-security-management/) — ISO/IEC 27001:2022 is the international standard for establishing, implementing, maintaining, and continually improving an Information Security Management System (ISMS). This skill covers the complete
  `compliance` `governance` `iso27001` `isms` `risk-management`

- [implementing-just-in-time-access-provisioning](../cybersecurity/implementing-just-in-time-access-provisioning/) — Implement Just-In-Time (JIT) access provisioning to eliminate standing privileges by granting temporary, time-bound access only when needed. This skill covers JIT architecture design, approval workflo
  `iam` `identity` `access-control` `jit` `provisioning`

- [implementing-jwt-signing-and-verification](../cybersecurity/implementing-jwt-signing-and-verification/) — JSON Web Tokens (JWT) defined in RFC 7519 are compact, URL-safe tokens used for authentication and authorization in web applications. This skill covers implementing secure JWT signing with HMAC-SHA256
  `cryptography` `jwt` `authentication` `token-security` `digital-signatures`

- [implementing-kubernetes-network-policy-with-calico](../cybersecurity/implementing-kubernetes-network-policy-with-calico/) — Implement Kubernetes network segmentation using Calico NetworkPolicy and GlobalNetworkPolicy for zero-trust pod-to-pod communication. Use when implementing kubernetes network segmentation using calico networkpolicy and globalnetworkpolicy for.
  `calico` `kubernetes` `network-policy` `network-segmentation` `zero-trust`

- [implementing-kubernetes-pod-security-standards](../cybersecurity/implementing-kubernetes-pod-security-standards/) — Pod Security Standards (PSS) define three levels of security policies -- Privileged, Baseline, and Restricted -- enforced by the Pod Security Admission (PSA) controller built into Kubernetes 1.25+. PS. Use when working with implementing kubernetes pod security standards.
  `containers` `kubernetes` `security` `pod-security` `PSA`

- [implementing-llm-guardrails-for-security](../cybersecurity/implementing-llm-guardrails-for-security/) — Implements input and output validation guardrails for LLM-powered applications to prevent prompt injection, data leakage, toxic content generation, and hallucinated outputs. Builds a security validation pipeline using NVIDIA NeMo Guardrails Colang definitions, custom Python validators for PII detection and content policy enforcement, and the Guardrails AI framework for structured output validation. Use when working with implementing llm guardrails for security.
  `LLM-guardrails` `NeMo-Guardrails` `input-validation` `output-filtering` `AI-safety`

- [implementing-log-forwarding-with-fluentd](../cybersecurity/implementing-log-forwarding-with-fluentd/) — Configure Fluentd and Fluent Bit for centralized log aggregation, routing, filtering, and enrichment across distributed infrastructure. Use when configureing fluentd and fluent bit for centralized log aggregation, routing,.
  `fluentd` `fluent-bit` `log-aggregation` `log-forwarding` `siem`

- [implementing-log-integrity-with-blockchain](../cybersecurity/implementing-log-integrity-with-blockchain/) — Build an append-only log integrity chain using SHA-256 hash chaining for tamper detection. Each log entry is hashed with the previous entry's hash to create a blockchain-like structure where modifying any entry invalidates all subsequent hashes. Implements log ingestion, chain verification, tamper detection with pinpoint identification, and periodic checkpoint anchoring to external timestamping services. Use when building an append-only log integrity chain using sha-256 hash chaining.
  `implementing` `log` `integrity` `with`

- [implementing-memory-protection-with-dep-aslr](../cybersecurity/implementing-memory-protection-with-dep-aslr/) — Implements memory protection mechanisms including DEP (Data Execution Prevention), ASLR (Address Space Layout Randomization), CFG (Control Flow Guard), and other exploit mitigations to prevent memory corruption attacks. Use when hardening endpoints against buffer overflow exploits, ROP chains, and code injection. Activates for requests involving memory protection, exploit mitigation, DEP, ASLR, or CFG configuration.

  `endpoint` `memory-protection` `DEP` `ASLR` `exploit-mitigation`

- [implementing-microsegmentation-with-guardicore](../cybersecurity/implementing-microsegmentation-with-guardicore/) — Implementing microsegmentation using Akamai Guardicore Segmentation to map application dependencies, create granular network policies, visualize east-west traffic flows, and enforce least-privilege communication between workloads across data centers and cloud. . Use when working with implementing microsegmentation with guardicore.
  `microsegmentation` `guardicore` `akamai` `zero-trust` `east-west-traffic`

- [implementing-mimecast-targeted-attack-protection](../cybersecurity/implementing-mimecast-targeted-attack-protection/) — Deploy Mimecast Targeted Threat Protection including URL Protect, Attachment Protect, Impersonation Protect, and Internal Email Protect to defend against advanced phishing and spearphishing attacks. Use when deploying mimecast targeted threat protection including url protect, attachment protect,.
  `mimecast` `email-security` `targeted-threat-protection` `url-protect` `impersonation`

- [implementing-mitre-attack-coverage-mapping](../cybersecurity/implementing-mitre-attack-coverage-mapping/) — Implement MITRE ATT&CK coverage mapping to identify detection gaps, prioritize rule development, and measure SOC detection maturity against adversary techniques. Use when implementing mitre att&ck coverage mapping to identify detection gaps, prioritize.
  `mitre-attack` `detection-coverage` `gap-analysis` `attack-navigator` `soc`

- [implementing-mobile-application-management](../cybersecurity/implementing-mobile-application-management/) — Implements Mobile Application Management (MAM) policies to protect enterprise data on managed and unmanaged mobile devices through app-level controls including data loss prevention, selective wipe, app configuration, and containerization. Use when securing corporate apps on BYOD devices, implementing Intune App Protection Policies, or enforcing data separation between personal and work apps.
  `mobile-security` `android` `ios` `mam` `enterprise-security`

- [implementing-mtls-for-zero-trust-services](../cybersecurity/implementing-mtls-for-zero-trust-services/) — Configures mutual TLS (mTLS) authentication between microservices using Python cryptography library for certificate generation and ssl module for TLS verification. Validates certificate chains, checks expiration, and audits mTLS deployment status. Use when implementing zero-trust service-to-service authentication.

  `implementing` `mtls` `for` `zero`

- [implementing-nerc-cip-compliance-controls](../cybersecurity/implementing-nerc-cip-compliance-controls/) — This skill covers implementing North American Electric Reliability Corporation Critical Infrastructure Protection (NERC CIP) compliance controls for Bulk Electric System (BES) cyber systems. It addresses asset categorization (CIP-002), electronic security perimeters (CIP-005), system security management (CIP-007), configuration management (CIP-010), supply chain risk management (CIP-013), and the 2025 updates including mandatory MFA for remote access and expanded low-impact asset requir.
  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [implementing-network-access-control](../cybersecurity/implementing-network-access-control/) — Implements 802.1X port-based network access control using RADIUS authentication, PacketFence NAC, and switch configurations to enforce identity-based access policies, posture assessment, and automatic VLAN assignment for authorized devices. . Use when working with implementing network access control.
  `network-security` `nac` `802.1x` `radius` `packetfence`

- [implementing-network-access-control-with-cisco-ise](../cybersecurity/implementing-network-access-control-with-cisco-ise/) — Deploy Cisco Identity Services Engine for 802.1X wired and wireless authentication, MAC Authentication Bypass, posture assessment, and dynamic VLAN assignment for network access control. Use when deploying cisco identity services engine for 802.1x wired and wireless.
  `cisco-ise` `802.1x` `nac` `radius` `network-access-control`

- [implementing-network-deception-with-honeypots](../cybersecurity/implementing-network-deception-with-honeypots/) — Deploy and manage network honeypots using OpenCanary, T-Pot, or Cowrie to detect unauthorized access, lateral movement, and attacker reconnaissance. Use when deploying and manage network honeypots using opencanary, t-pot, or cowrie.
  `deception` `honeypot` `opencanary` `cowrie` `t-pot`

- [implementing-network-intrusion-prevention-with-suricata](../cybersecurity/implementing-network-intrusion-prevention-with-suricata/) — Deploy and configure Suricata as a network intrusion prevention system with custom rules, Emerging Threats rulesets, and inline traffic inspection for real-time threat blocking. Use when deploying and configure suricata as a network intrusion prevention system.
  `suricata` `ips` `ids` `intrusion-prevention` `network-security`

- [implementing-network-policies-for-kubernetes](../cybersecurity/implementing-network-policies-for-kubernetes/) — Kubernetes NetworkPolicies provide pod-level network segmentation by defining ingress and egress rules that control traffic flow between pods, namespaces, and external endpoints. Combined with CNI plu. Use when working with implementing network policies for kubernetes.
  `containers` `kubernetes` `security` `network-policies` `microsegmentation`

- [implementing-network-segmentation-for-ot](../cybersecurity/implementing-network-segmentation-for-ot/) — This skill covers implementing network segmentation in Operational Technology environments using VLANs, industrial firewalls, data diodes, and software-defined networking. It addresses the Purdue Model-based segmentation strategy, migration from flat networks to segmented architectures without disrupting operations, configuring OT-aware firewalls with industrial protocol deep packet inspection, and validating segmentation effectiveness through traffic analysis.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [implementing-network-segmentation-with-firewall-zones](../cybersecurity/implementing-network-segmentation-with-firewall-zones/) — Design and implement network segmentation using firewall security zones, VLANs, ACLs, and microsegmentation policies to restrict lateral movement and enforce least-privilege network access. Use when designing and implement network segmentation using firewall security zones, vlans,.
  `network-segmentation` `firewall-zones` `vlan` `microsegmentation` `lateral-movement`

- [implementing-network-traffic-analysis-with-arkime](../cybersecurity/implementing-network-traffic-analysis-with-arkime/) — Deploy and query Arkime (formerly Moloch) for full packet capture network traffic analysis. Uses the Arkime API v3 to search sessions, download PCAPs, analyze connection patterns, detect beaconing behavior, and identify suspicious network flows. Monitors DNS queries, HTTP traffic, and TLS certificate anomalies across captured traffic. Use when deploying and query arkime (formerly moloch) for full packet capture.
  `implementing` `network` `traffic` `analysis`

- [implementing-network-traffic-baselining](../cybersecurity/implementing-network-traffic-baselining/) — Build network traffic baselines from NetFlow/IPFIX data using Python pandas for statistical analysis, z-score anomaly detection, and hourly/daily traffic pattern profiling. Use when building network traffic baselines from netflow/ipfix data using python pandas.
  `netflow` `ipfix` `traffic-analysis` `baselining` `anomaly-detection`

- [implementing-next-generation-firewall-with-palo-alto](../cybersecurity/implementing-next-generation-firewall-with-palo-alto/) — Configure and deploy Palo Alto Networks next-generation firewalls with App-ID, User-ID, zone-based policies, SSL decryption, and threat prevention profiles for enterprise network security. Use when configureing and deploy palo alto networks next-generation firewalls with app-id,.
  `palo-alto` `ngfw` `firewall` `app-id` `user-id`

- [implementing-opa-gatekeeper-for-policy-enforcement](../cybersecurity/implementing-opa-gatekeeper-for-policy-enforcement/) — Enforce Kubernetes admission policies using OPA Gatekeeper with ConstraintTemplates, Rego rules, and the Gatekeeper policy library. Use when working with implementing opa gatekeeper for policy enforcement.
  `opa` `gatekeeper` `kubernetes` `admission-control` `policy-as-code`

- [implementing-ot-incident-response-playbook](../cybersecurity/implementing-ot-incident-response-playbook/) — Develop and implement OT-specific incident response playbooks aligned with SANS PICERL framework, IEC 62443, and NIST SP 800-82 that address unique ICS challenges including safety-critical systems, limited downtime tolerance, and coordination between IT SOC, OT engineering, and plant operations teams. . Use when working with implementing ot incident response playbook.
  `ot-security` `ics` `incident-response` `playbook` `sans`

- [implementing-ot-network-traffic-analysis-with-nozomi](../cybersecurity/implementing-ot-network-traffic-analysis-with-nozomi/) — Deploy Nozomi Networks Guardian sensors for passive OT network traffic analysis to achieve comprehensive asset visibility, real-time threat detection, and vulnerability assessment across industrial control systems without disrupting operations, leveraging behavioral anomaly detection and protocol-aware monitoring. . Use when working with implementing ot network traffic analysis with nozomi.
  `ot-security` `ics` `nozomi` `guardian` `network-monitoring`

- [implementing-pam-for-database-access](../cybersecurity/implementing-pam-for-database-access/) — Deploy privileged access management for database systems including Oracle, SQL Server, PostgreSQL, and MySQL. Covers session proxy configuration, credential vaulting, query auditing, dynamic credentia
  `iam` `identity` `access-control` `privileged-access` `pam`

- [implementing-passwordless-auth-with-microsoft-entra](../cybersecurity/implementing-passwordless-auth-with-microsoft-entra/) — Implements passwordless authentication using Microsoft Entra ID with FIDO2 security keys, Windows Hello for Business, Microsoft Authenticator passkeys, and certificate-based authentication to eliminate password-based attacks. Activates for requests involving passwordless deployment, FIDO2 passkey configuration, phishing-resistant MFA, or Microsoft Entra authentication method policies. . Use when working with implementing passwordless auth with microsoft entra.
  `passwordless` `FIDO2` `passkeys` `Microsoft-Entra` `Windows-Hello`

- [implementing-passwordless-authentication-with-fido2](../cybersecurity/implementing-passwordless-authentication-with-fido2/) — Deploy FIDO2/WebAuthn passwordless authentication using security keys and platform authenticators. Covers WebAuthn API integration, FIDO2 server configuration, passkey enrollment, biometric authentica
  `iam` `identity` `access-control` `authentication` `fido2`

- [implementing-patch-management-for-ot-systems](../cybersecurity/implementing-patch-management-for-ot-systems/) — This skill covers implementing a structured patch management program for OT/ICS environments where traditional IT patching approaches can cause process disruption or safety hazards. It addresses vendor compatibility testing, risk-based patch prioritization, staged deployment through test environments, maintenance window coordination, rollback procedures, and compensating controls when patches cannot be applied due to operational constraints or vendor restrictions.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [implementing-patch-management-workflow](../cybersecurity/implementing-patch-management-workflow/) — Patch management is the systematic process of identifying, testing, deploying, and verifying software updates to remediate vulnerabilities across an organization's IT infrastructure. An effective patc. Use when working with implementing patch management workflow.
  `vulnerability-management` `patch-management` `wsus` `sccm` `ansible`

- [implementing-pci-dss-compliance-controls](../cybersecurity/implementing-pci-dss-compliance-controls/) — PCI DSS 4.0.1 establishes 12 requirements across 6 control objectives for organizations that store, process, or transmit cardholder data. With PCI DSS 3.2.1 retiring April 2024 and 51 new requirements. Use when working with implementing pci dss compliance controls.
  `compliance` `governance` `pci-dss` `payment-security` `cardholder-data`

- [implementing-pod-security-admission-controller](../cybersecurity/implementing-pod-security-admission-controller/) — Implement Kubernetes Pod Security Admission to enforce baseline and restricted security profiles at namespace level using built-in admission controller. Use when implementing kubernetes pod security admission to enforce baseline and restricted.
  `kubernetes` `pod-security-admission` `psa` `pod-security-standards` `admission-controller`

- [implementing-policy-as-code-with-open-policy-agent](../cybersecurity/implementing-policy-as-code-with-open-policy-agent/) — This skill covers implementing Open Policy Agent (OPA) and Gatekeeper for policy-as-code enforcement in Kubernetes and CI/CD pipelines. It addresses writing Rego policies, deploying OPA Gatekeeper as a Kubernetes admission controller, testing policies in development, and integrating policy evaluation into deployment pipelines.

  `devsecops` `cicd` `opa` `gatekeeper` `policy-as-code`

- [implementing-privileged-access-management-with-cyberark](../cybersecurity/implementing-privileged-access-management-with-cyberark/) — Deploy CyberArk Privileged Access Management to discover, vault, rotate, and monitor privileged credentials across enterprise infrastructure. This skill covers vault architecture, session isolation, c
  `iam` `identity` `access-control` `privileged-access` `pam`

- [implementing-privileged-access-workstation](../cybersecurity/implementing-privileged-access-workstation/) — Design and implement Privileged Access Workstations (PAWs) with device hardening, just-in-time access, and integration with CyberArk or BeyondTrust for secure administrative operations. Use when designing and implement privileged access workstations (paws) with device hardening,.
  `privileged-access` `PAW` `zero-trust` `device-hardening` `CyberArk`

- [implementing-privileged-session-monitoring](../cybersecurity/implementing-privileged-session-monitoring/) — Implements privileged session monitoring and recording using Privileged Access Management (PAM) solutions, focusing on CyberArk Privileged Session Manager (PSM) and open-source alternatives. Covers session recording configuration, keystroke logging, real-time monitoring, risk-based session analysis, and compliance audit trail generation.
  `PAM` `CyberArk` `PSM` `privileged-session` `session-recording`

- [implementing-proofpoint-email-security-gateway](../cybersecurity/implementing-proofpoint-email-security-gateway/) — Deploy and configure Proofpoint Email Protection as a secure email gateway to detect and block phishing, malware, BEC, and spam before messages reach user inboxes. Use when deploying and configure proofpoint email protection as a secure email.
  `email-security` `proofpoint` `secure-email-gateway` `phishing` `anti-spam`

- [implementing-purdue-model-network-segmentation](../cybersecurity/implementing-purdue-model-network-segmentation/) — Implement network segmentation based on the Purdue Enterprise Reference Architecture (PERA) model to separate industrial control system networks into hierarchical security zones from Level 0 physical process through Level 5 enterprise, enforcing strict traffic control between OT and IT domains. . Use when working with implementing purdue model network segmentation.
  `ot-security` `ics` `purdue-model` `network-segmentation` `iec62443`

- [implementing-ransomware-backup-strategy](../cybersecurity/implementing-ransomware-backup-strategy/) — Designs and implements a ransomware-resilient backup strategy following the 3-2-1-1-0 methodology (3 copies, 2 media types, 1 offsite, 1 immutable/air-gapped, 0 errors on restore verification). Configures backup schedules aligned to RPO/RTO requirements, implements backup credential isolation to prevent ransomware from compromising backup infrastructure, and establishes automated restore testing.
  `ransomware` `backup` `incident-response` `defense` `recovery`

- [implementing-ransomware-kill-switch-detection](../cybersecurity/implementing-ransomware-kill-switch-detection/) — Use when detects and exploits ransomware kill switch mechanisms including mutex-based execution guards, domain-based kill switches, and registry-based termination checks. Implements proactive mutex vaccination and kill switch domain monitoring to prevent ransomware from executing. Activates for requests involving ransomware kill switch analysis, mutex vaccination, WannaCry-style domain kill switches, or malware execution guard detection.
'.
  `ransomware` `kill-switch` `mutex` `detection` `WannaCry`

- [implementing-rapid7-insightvm-for-scanning](../cybersecurity/implementing-rapid7-insightvm-for-scanning/) — Deploy and configure Rapid7 InsightVM Security Console and Scan Engines for authenticated and unauthenticated vulnerability scanning across enterprise environments. Use when deploying and configure rapid7 insightvm security console and scan engines.
  `rapid7` `insightvm` `vulnerability-scanning` `nexpose` `scan-engine`

- [implementing-rbac-hardening-for-kubernetes](../cybersecurity/implementing-rbac-hardening-for-kubernetes/) — Harden Kubernetes Role-Based Access Control by implementing least-privilege policies, auditing role bindings, eliminating cluster-admin sprawl, and integrating external identity providers. Use when working with implementing rbac hardening for kubernetes.
  `kubernetes` `rbac` `access-control` `least-privilege` `security-hardening`

- [implementing-rsa-key-pair-management](../cybersecurity/implementing-rsa-key-pair-management/) — RSA (Rivest-Shamir-Adleman) is the most widely deployed asymmetric cryptographic algorithm, used for digital signatures, key exchange, and encryption. This skill covers generating, storing, rotating,
  `cryptography` `rsa` `key-management` `pki` `asymmetric-encryption`

- [implementing-runtime-application-self-protection](../cybersecurity/implementing-runtime-application-self-protection/) — Deploy Runtime Application Self-Protection (RASP) agents to detect and block attacks from within application runtime, covering OpenRASP integration, attack pattern detection, and security policy configuration for Java and Python web applications. Use when deploying runtime application self-protection (rasp) agents to detect and block.
  `rasp` `application-security` `openrasp` `runtime-protection` `sqli`

- [implementing-runtime-security-with-tetragon](../cybersecurity/implementing-runtime-security-with-tetragon/) — Implement eBPF-based runtime security observability and enforcement in Kubernetes clusters using Cilium Tetragon for kernel-level threat detection and policy enforcement. Use when implementing ebpf-based runtime security observability and enforcement in kubernetes clusters.
  `tetragon` `ebpf` `runtime-security` `kubernetes` `cilium`

- [implementing-saml-sso-with-okta](../cybersecurity/implementing-saml-sso-with-okta/) — Implement SAML 2.0 Single Sign-On (SSO) using Okta as the Identity Provider (IdP). This skill covers end-to-end configuration of SAML authentication flows, attribute mapping, certificate management, a
  `iam` `identity` `access-control` `authentication` `saml`

- [implementing-scim-provisioning-with-okta](../cybersecurity/implementing-scim-provisioning-with-okta/) — Implement automated user provisioning and deprovisioning using SCIM 2.0 protocol with Okta as the identity provider.
  `scim` `okta` `provisioning` `identity-management` `automation`

- [implementing-secret-scanning-with-gitleaks](../cybersecurity/implementing-secret-scanning-with-gitleaks/) — This skill covers implementing Gitleaks for detecting and preventing hardcoded secrets in git repositories. It addresses configuring pre-commit hooks, CI/CD pipeline integration, custom rule authoring for organization-specific secrets, baseline management for existing repositories, and remediation workflows for exposed credentials.

  `devsecops` `cicd` `secret-scanning` `gitleaks` `pre-commit`

- [implementing-secrets-management-with-vault](../cybersecurity/implementing-secrets-management-with-vault/) — This skill covers deploying HashiCorp Vault for centralized secrets management across cloud environments, including dynamic secret generation for databases and cloud providers, transit encryption, PKI certificate management, and Kubernetes integration. It addresses eliminating hardcoded credentials from application code and CI/CD pipelines by implementing short-lived, automatically rotated secrets.

  `hashicorp-vault` `secrets-management` `dynamic-secrets` `credential-rotation` `zero-trust`

- [implementing-secrets-scanning-in-ci-cd](../cybersecurity/implementing-secrets-scanning-in-ci-cd/) — Integrate gitleaks and trufflehog into CI/CD pipelines to detect leaked secrets before deployment. Use when integrateing gitleaks and trufflehog into ci/cd pipelines to detect leaked.
  `secrets-scanning` `gitleaks` `trufflehog` `ci-cd`

- [implementing-security-chaos-engineering](../cybersecurity/implementing-security-chaos-engineering/) — Implements security chaos engineering experiments that deliberately disable or degrade security controls to verify detection and response capabilities. Tests WAF bypass, firewall rule removal, log pipeline disruption, and EDR disablement scenarios using boto3 and subprocess. Use when validating SOC detection coverage and resilience.

  `implementing` `security` `chaos` `engineering`

- [implementing-security-information-sharing-with-stix2](../cybersecurity/implementing-security-information-sharing-with-stix2/) — Create, validate, and share STIX 2.1 threat intelligence objects using the stix2 Python library. Covers indicators, malware, campaigns, relationships, bundles, and TAXII 2.1 publishing.

  `stix` `taxii` `threat-sharing` `intelligence-exchange`

- [implementing-security-monitoring-with-datadog](../cybersecurity/implementing-security-monitoring-with-datadog/) — Implements security monitoring using Datadog Cloud SIEM, Cloud Security Management (CSM), and Workload Protection to detect threats, enforce compliance, and respond to security events across cloud and hybrid infrastructure. Covers Agent deployment, log source ingestion, detection rule creation, security dashboards, and automated notification workflows. Activates for requests involving Datadog security setup, Cloud SIEM configuration, CSM threat detection, or security monitoring dashboards.
  `siem` `monitoring` `datadog` `cloud-security` `log-analysis`

- [implementing-semgrep-for-custom-sast-rules](../cybersecurity/implementing-semgrep-for-custom-sast-rules/) — Write custom Semgrep SAST rules in YAML to detect application-specific vulnerabilities, enforce coding standards, and integrate into CI/CD pipelines. Use when writeing custom semgrep sast rules in yaml to detect application-specific.
  `semgrep` `sast` `static-analysis` `custom-rules` `devsecops`

- [implementing-siem-correlation-rules-for-apt](../cybersecurity/implementing-siem-correlation-rules-for-apt/) — Write multi-event correlation rules that detect APT lateral movement by chaining Windows authentication events, process execution telemetry, and network connection logs across hosts. Uses Splunk SPL and Sigma rule format to correlate Event IDs 4624, 4648, 4688, and Sysmon Events 1/3 within sliding time windows to surface attack sequences invisible to single-event detections. Use when writeing multi-event correlation rules that detect apt lateral movement by.
  `implementing` `siem` `correlation` `rules`

- [implementing-siem-use-case-tuning](../cybersecurity/implementing-siem-use-case-tuning/) — Tune SIEM detection rules to reduce false positives by analyzing alert volumes, creating whitelists, adjusting thresholds, and measuring detection efficacy metrics in Splunk and Elastic. Use when working with implementing siem use case tuning.
  `siem` `detection-engineering` `false-positive-reduction` `splunk` `elastic`

- [implementing-siem-use-cases-for-detection](../cybersecurity/implementing-siem-use-cases-for-detection/) — Implements SIEM detection use cases by designing correlation rules, threshold alerts, and behavioral analytics mapped to MITRE ATT&CK techniques across Splunk, Elastic, and Sentinel. Use when SOC teams need to expand detection coverage, formalize use case lifecycle management, or build a detection library aligned to organizational threat profile.

  `soc` `siem` `use-cases` `detection-engineering` `mitre-attack`

- [implementing-sigstore-for-software-signing](../cybersecurity/implementing-sigstore-for-software-signing/) — Use when implements Sigstore-based software signing and verification using Cosign keyless signing, Rekor transparency log verification, and Fulcio certificate authority integration to establish cryptographic provenance for container images, binaries, and software artifacts. The practitioner configures OIDC-based identity binding, verifies signing events against the Rekor transparency log, and integrates signing workflows into CI/CD pipelines.
  `sigstore` `cosign` `rekor` `fulcio` `software-signing`

- [implementing-soar-automation-with-phantom](../cybersecurity/implementing-soar-automation-with-phantom/) — Implements Security Orchestration, Automation, and Response (SOAR) workflows using Splunk SOAR (formerly Phantom) to automate alert triage, IOC enrichment, containment actions, and incident response playbooks. Use when SOC teams need to reduce manual analyst work, standardize response procedures, or integrate multiple security tools into automated workflows.

  `soc` `soar` `phantom` `splunk-soar` `automation`

- [implementing-soar-playbook-for-phishing](../cybersecurity/implementing-soar-playbook-for-phishing/) — Automate phishing incident response using Splunk SOAR REST API to create containers, add artifacts, and trigger playbooks
  `soar` `splunk-phantom` `phishing` `incident-response`

- [implementing-soar-playbook-with-palo-alto-xsoar](../cybersecurity/implementing-soar-playbook-with-palo-alto-xsoar/) — Implement automated incident response playbooks in Cortex XSOAR to orchestrate security workflows across SOC tools and reduce manual response time.
  `xsoar` `soar` `palo-alto` `playbook` `automation`

- [implementing-stix-taxii-feed-integration](../cybersecurity/implementing-stix-taxii-feed-integration/) — STIX (Structured Threat Information eXpression) and TAXII (Trusted Automated eXchange of Intelligence Information) are OASIS open standards for representing and transporting cyber threat intelligence.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [implementing-supply-chain-security-with-in-toto](../cybersecurity/implementing-supply-chain-security-with-in-toto/) — Implement software supply chain integrity verification for container builds using the in-toto framework to create cryptographically signed attestations across CI/CD pipeline steps. Use when implementing software supply chain integrity verification for container builds using.
  `in-toto` `supply-chain-security` `attestation` `slsa` `sigstore`

- [implementing-syslog-centralization-with-rsyslog](../cybersecurity/implementing-syslog-centralization-with-rsyslog/) — Configure rsyslog for centralized log collection with TLS encryption, custom templates, and log rotation. Generates server and client configuration files with GnuTLS stream drivers, x509 certificate authentication, per-host log segregation, and reliable queue settings for high-availability syslog infrastructure.
  `implementing` `syslog` `centralization` `with`

- [implementing-taxii-server-with-opentaxii](../cybersecurity/implementing-taxii-server-with-opentaxii/) — Deploy and configure an OpenTAXII server to share and consume STIX-formatted cyber threat intelligence using the TAXII 2.1 protocol for automated indicator exchange between organizations.
  `taxii` `stix` `opentaxii` `threat-sharing` `cti`

- [implementing-threat-intelligence-lifecycle-management](../cybersecurity/implementing-threat-intelligence-lifecycle-management/) — Implement a structured threat intelligence lifecycle encompassing planning, collection, processing, analysis, dissemination, and feedback stages to produce actionable intelligence for organizational decision-making. Use when implementing a structured threat intelligence lifecycle encompassing planning, collection, processing,.
  `threat-intelligence` `lifecycle` `intelligence-cycle` `collection` `analysis`

- [implementing-threat-modeling-with-mitre-attack](../cybersecurity/implementing-threat-modeling-with-mitre-attack/) — Implements threat modeling using the MITRE ATT&CK framework to map adversary TTPs against organizational assets, assess detection coverage gaps, and prioritize defensive investments. Use when SOC teams need to align detection engineering with threat landscape, conduct threat assessments for new environments, or justify security tool procurement.

  `soc` `mitre-attack` `threat-modeling` `ttp` `detection-coverage`

- [implementing-ticketing-system-for-incidents](../cybersecurity/implementing-ticketing-system-for-incidents/) — Implements an integrated incident ticketing system connecting SIEM alerts to ServiceNow, Jira, or TheHive for structured incident tracking, SLA management, escalation workflows, and compliance documentation. Use when SOC teams need formalized incident lifecycle management with automated ticket creation, assignment routing, and resolution tracking.

  `soc` `ticketing` `servicenow` `jira` `thehive`

- [implementing-usb-device-control-policy](../cybersecurity/implementing-usb-device-control-policy/) — Implements USB device control policies to restrict unauthorized removable media access on endpoints, preventing data exfiltration and malware introduction via USB devices. Use when deploying device control via Group Policy, Intune, or EDR platforms to enforce USB restrictions. Activates for requests involving USB control, removable media policy, device control, or data loss prevention via USB.

  `endpoint` `USB-control` `device-control` `data-loss-prevention` `removable-media`

- [implementing-velociraptor-for-ir-collection](../cybersecurity/implementing-velociraptor-for-ir-collection/) — Deploy and configure Velociraptor for scalable endpoint forensic artifact collection during incident response using VQL queries, hunts, and pre-built artifact packs across Windows, Linux, and macOS environments. Use when deploying and configure velociraptor for scalable endpoint forensic artifact collection.
  `velociraptor` `dfir` `endpoint-collection` `vql` `forensic-artifacts`

- [implementing-vulnerability-management-with-greenbone](../cybersecurity/implementing-vulnerability-management-with-greenbone/) — Deploy and operate Greenbone/OpenVAS vulnerability management using the python-gvm library to create scan targets, execute vulnerability scans, and parse scan reports via GMP protocol. Use when deploying and operate greenbone/openvas vulnerability management using the python-gvm library.
  `openvas` `greenbone` `vulnerability-scanning` `gmp` `python-gvm`

- [implementing-vulnerability-remediation-sla](../cybersecurity/implementing-vulnerability-remediation-sla/) — Vulnerability remediation SLAs define mandatory timeframes for patching or mitigating identified vulnerabilities based on severity, asset criticality, and exploit availability. Effective SLA programs. Use when working with implementing vulnerability remediation sla.
  `vulnerability-management` `cve` `sla` `remediation` `patch-management`

- [implementing-vulnerability-sla-breach-alerting](../cybersecurity/implementing-vulnerability-sla-breach-alerting/) — Build automated alerting for vulnerability remediation SLA breaches with severity-based timelines, escalation workflows, and compliance reporting dashboards.
  `vulnerability-sla` `remediation-tracking` `alerting` `compliance` `sla-breach`

- [implementing-web-application-logging-with-modsecurity](../cybersecurity/implementing-web-application-logging-with-modsecurity/) — Use when configure ModSecurity WAF with OWASP Core Rule Set (CRS) for web application logging, tune rules to reduce false positives, analyze audit logs for attack detection, and implement custom SecRules for application-specific threats. The analyst configures SecRuleEngine, SecAuditEngine, and CRS paranoia levels to balance security coverage with operational stability. Activates for requests involving WAF configuration, ModSecurity rule tuning, web application audit logging, or CRS deployment.
  `modsecurity` `waf` `crs` `owasp` `web-security`

- [implementing-zero-knowledge-proof-for-authentication](../cybersecurity/implementing-zero-knowledge-proof-for-authentication/) — Zero-Knowledge Proofs (ZKPs) allow a prover to demonstrate knowledge of a secret (such as a password or private key) without revealing the secret itself. This skill implements the Schnorr identificati. Use when working with implementing zero knowledge proof for authentication.
  `cryptography` `zero-knowledge-proof` `authentication` `privacy` `zkp`

- [implementing-zero-standing-privilege-with-cyberark](../cybersecurity/implementing-zero-standing-privilege-with-cyberark/) — Deploy CyberArk Secure Cloud Access to eliminate standing privileges in hybrid and multi-cloud environments using just-in-time access with time, entitlement, and approval controls. Use when deploying cyberark secure cloud access to eliminate standing privileges in.
  `cyberark` `zero-standing-privilege` `jit-access` `pam` `cloud-security`

- [implementing-zero-trust-dns-with-nextdns](../cybersecurity/implementing-zero-trust-dns-with-nextdns/) — Implement NextDNS as a zero trust DNS filtering layer with encrypted resolution, threat intelligence blocking, privacy protection, and organizational policy enforcement across all endpoints. Use when implementing nextdns as a zero trust dns filtering layer with.
  `zero-trust` `dns` `nextdns` `dns-over-https` `dns-over-tls`

- [implementing-zero-trust-for-saas-applications](../cybersecurity/implementing-zero-trust-for-saas-applications/) — Implementing zero trust access controls for SaaS applications using CASB, SSPM, conditional access policies, OAuth app governance, and session controls to enforce identity verification, device compliance, and data protection for cloud-hosted services. . Use when working with implementing zero trust for saas applications.
  `zero-trust` `saas-security` `casb` `sspm` `conditional-access`

- [implementing-zero-trust-in-cloud](../cybersecurity/implementing-zero-trust-in-cloud/) — This skill guides organizations through implementing zero trust architecture in cloud environments following NIST SP 800-207 and Google BeyondCorp principles. It covers identity-centric access controls, micro-segmentation, continuous verification, device trust assessment, and deploying Identity-Aware Proxy to eliminate implicit network trust in AWS, Azure, and GCP environments.

  `zero-trust` `beyondcorp` `identity-aware-proxy` `micro-segmentation` `continuous-verification`

- [implementing-zero-trust-network-access](../cybersecurity/implementing-zero-trust-network-access/) — Implementing Zero Trust Network Access (ZTNA) in cloud environments by configuring identity-aware proxies, micro-segmentation, continuous verification with conditional access policies, and replacing traditional VPN-based access with BeyondCorp-style architectures across AWS, Azure, and GCP. . Use when working with implementing zero trust network access.
  `cloud-security` `zero-trust` `ztna` `beyondcorp` `identity-aware-proxy`

- [implementing-zero-trust-network-access-with-zscaler](../cybersecurity/_deprecated/implementing-zero-trust-network-access-with-zscaler/) — Implement Zero Trust Network Access using Zscaler Private Access (ZPA) to replace traditional VPN with identity-based, context-aware access to private applications through the Zscaler Zero Trust Exchange. Use when implementing zero trust network access using zscaler private access (zpa).
  `zero-trust` `ztna` `zscaler` `network-access` `vpn-replacement`

- [implementing-zero-trust-with-beyondcorp](../cybersecurity/_deprecated/implementing-zero-trust-with-beyondcorp/) — Deploy Google BeyondCorp Enterprise zero trust access controls using Identity-Aware Proxy (IAP), context-aware access policies, device trust validation, and Access Context Manager to enforce identity and posture-based access to GCP resources and internal applications. Use when deploying google beyondcorp enterprise zero trust access controls using identity-aware.
  `zero-trust` `beyondcorp` `google-cloud` `iap` `context-aware-access`

- [implementing-zero-trust-with-hashicorp-boundary](../cybersecurity/implementing-zero-trust-with-hashicorp-boundary/) — Implement HashiCorp Boundary for identity-aware zero trust infrastructure access management with dynamic credential brokering, session recording, and Vault integration. Use when implementing hashicorp boundary for identity-aware zero trust infrastructure access management.
  `zero-trust` `hashicorp` `boundary` `privileged-access` `vault`

- [integrating-dast-with-owasp-zap-in-pipeline](../cybersecurity/integrating-dast-with-owasp-zap-in-pipeline/) — This skill covers integrating OWASP ZAP (Zed Attack Proxy) for Dynamic Application Security Testing in CI/CD pipelines. It addresses configuring baseline, full, and API scans against running applications, interpreting ZAP findings, tuning scan policies, and establishing DAST quality gates in GitHub Actions and GitLab CI.

  `devsecops` `cicd` `dast` `owasp-zap` `dynamic-testing`

- [integrating-sast-into-github-actions-pipeline](../cybersecurity/integrating-sast-into-github-actions-pipeline/) — This skill covers integrating Static Application Security Testing (SAST) tools—CodeQL and Semgrep—into GitHub Actions CI/CD pipelines. It addresses configuring automated code scanning on pull requests and pushes, tuning rules to reduce false positives, uploading SARIF results to GitHub Advanced Security, and establishing quality gates that block merges when high-severity vulnerabilities are detected.

  `devsecops` `cicd` `sast` `codeql` `semgrep`

- [intercepting-mobile-traffic-with-burpsuite](../cybersecurity/intercepting-mobile-traffic-with-burpsuite/) — Intercepts and analyzes HTTP/HTTPS traffic from mobile applications using Burp Suite proxy to identify insecure API communications, authentication flaws, data leakage, and server-side vulnerabilities. Use when performing mobile application penetration testing, assessing API security, or evaluating client-server communication patterns. Activates for requests involving mobile traffic interception, Burp Suite mobile proxy, API security testing, or mobile HTTPS analysis.

  `mobile-security` `android` `ios` `burp-suite` `traffic-interception`

- [investigating-insider-threat-indicators](../cybersecurity/investigating-insider-threat-indicators/) — Investigates insider threat indicators including data exfiltration attempts, unauthorized access patterns, policy violations, and pre-departure behaviors using SIEM analytics, DLP alerts, and HR data correlation. Use when SOC teams receive insider threat referrals from HR, detect anomalous data movement by employees, or need to build investigation timelines for potential insider threats.

  `soc` `insider-threat` `data-exfiltration` `dlp` `ueba`

- [investigating-phishing-email-incident](../cybersecurity/investigating-phishing-email-incident/) — Investigates phishing email incidents from initial user report through header analysis, URL/attachment detonation, impacted user identification, and containment actions using SOC tools like Splunk, Microsoft Defender, and sandbox analysis platforms. Use when a reported phishing email requires full incident investigation to determine scope and impact.

  `soc` `phishing` `incident-response` `email-security` `splunk`

- [investigating-ransomware-attack-artifacts](../cybersecurity/investigating-ransomware-attack-artifacts/) — Identify, collect, and analyze ransomware attack artifacts to determine the variant, initial access vector, encryption scope, and recovery options. Use when working with investigating ransomware attack artifacts.
  `forensics` `ransomware` `malware-analysis` `incident-response` `encryption-recovery`

- [iot-hunter](../cybersecurity/iot-hunter/) — IoT and embedded device security testing — firmware analysis, hardware interfaces, protocol exploitation. Use when testing IoT devices, extracting firmware, analyzing embedded systems, or finding hardware vulnerabilities. Use when working with iot hunter.
  `cybersecurity` `hunter` `iot` `security` `testing`

- [kernel-killer](../cybersecurity/kernel-killer/) — Linux and Windows kernel exploitation for privilege escalation. Use when finding kernel vulnerabilities, exploiting kernel drivers, or escalating privileges from user to root/system.
  `cybersecurity` `kernel` `killer` `security` `threat-defense`

- [managing-cloud-identity-with-okta](../cybersecurity/managing-cloud-identity-with-okta/) — This skill covers implementing Okta as a centralized identity provider for cloud environments, configuring SSO integration with AWS, Azure, and GCP, deploying phishing- resistant MFA with Okta FastPass, managing lifecycle automation for user provisioning and deprovisioning, and enforcing adaptive access policies based on device posture and risk signals.

  `okta` `cloud-identity` `single-sign-on` `phishing-resistant-mfa` `identity-lifecycle`

- [managing-intelligence-lifecycle](../cybersecurity/managing-intelligence-lifecycle/) — Manages the end-to-end cyber threat intelligence lifecycle from planning and direction through collection, processing, analysis, dissemination, and feedback to ensure intelligence products meet stakeholder requirements and continuously improve. Use when establishing or maturing a CTI program, defining intelligence requirements with business stakeholders, or building feedback loops between intelligence consumers and producers.
  `CTI` `intelligence-lifecycle` `PIR` `NIST-SP-800-150` `threat-intelligence-program`

- [mapping-mitre-attack-techniques](../cybersecurity/mapping-mitre-attack-techniques/) — Maps observed adversary behaviors, security alerts, and detection rules to MITRE ATT&CK techniques and sub-techniques to quantify detection coverage and guide control prioritization. Use when building an ATT&CK-based coverage heatmap, tagging SIEM alerts with technique IDs, aligning security controls to adversary playbooks, or reporting threat exposure to executives. Activates for requests involving ATT&CK Navigator, Sigma rules, MITRE D3FEND, or coverage gap analysis.

  `MITRE-ATT&CK` `ATT&CK-Navigator` `Sigma` `D3FEND` `TTP`

- [mobile-hacking](../cybersecurity/mobile-hacking/) — Android and mobile application security testing — emulators, rooting, traffic interception, dynamic instrumentation. Use when testing mobile apps for vulnerabilities, reversing APKs, or bypassing security controls on Android.
  `cybersecurity` `hacking` `mobile` `security` `testing`

- [monitoring-darkweb-sources](../cybersecurity/monitoring-darkweb-sources/) — Monitors dark web forums, marketplaces, paste sites, and ransomware leak sites for mentions of organizational assets, leaked credentials, threatened attacks, and threat actor communications to provide early warning intelligence. Use when establishing dark web monitoring coverage, investigating specific data breach claims, or enriching incident investigations with dark web context. Use when working with monitoring darkweb sources.
  `dark-web` `OSINT` `credential-monitoring` `ransomware-leaks` `Recorded-Future`

- [monitoring-scada-modbus-traffic-anomalies](../cybersecurity/monitoring-scada-modbus-traffic-anomalies/) — Use when monitors Modbus TCP traffic on SCADA and ICS networks to detect anomalous function code usage, unauthorized register writes, and suspicious communication patterns. The analyst uses deep packet inspection with pymodbus, Scapy, and Zeek to baseline normal PLC/RTU communication behavior, then applies statistical and rule-based anomaly detection to identify reconnaissance, parameter manipulation, and denial-of-service attacks targeting Modbus devices on port 502.
  `Modbus-TCP` `SCADA` `ICS-security` `deep-packet-inspection` `anomaly-detection`

- [onchain-transaction-forensics](../cybersecurity/onchain-transaction-forensics/) — Trace and analyze blockchain transactions to investigate illicit fund flows, identify wallet clusters, and map transaction graphs across multiple blockchains. Use when investigating stolen funds, following money trails on-chain, analyzing suspicious addresses, or tracing cross-chain transactions.
  `blockchain` `forensics` `onchain` `transactions` `wallet`

- [pentest-agent-orchestrator](../cybersecurity/pentest-agent-orchestrator/) — Orchestrate 35 specialized Claude Code subagents for offensive security. Use when planning a pentest, routing tasks to specialist agents, or conducting multi-phase security assessments.
  `pentest` `multi-agent` `orchestration` `red-team` `claude-code`

- [pentestagent-tui](../cybersecurity/pentestagent-tui/) — AI-powered pentesting terminal UI with 4 modes (Assist, Agent, Crew, Interact) and RAG knowledge system. Use when running interactive pentests, multi-agent security assessments, or.
  `pentest` `tui` `multi-agent` `rag` `knowledge-graph`

- [performing-access-recertification-with-saviynt](../cybersecurity/performing-access-recertification-with-saviynt/) — Configure and execute access recertification campaigns in Saviynt Enterprise Identity Cloud to validate user entitlements, revoke excessive access, and maintain compliance with SOX, SOC2, and HIPAA. Use when configureing and execute access recertification campaigns in saviynt enterprise identity.
  `saviynt` `access-recertification` `identity-governance` `compliance` `certification-campaign`

- [performing-access-review-and-certification](../cybersecurity/performing-access-review-and-certification/) — Conduct systematic access reviews and certifications to ensure users have appropriate access rights aligned with their roles. This skill covers review campaign design, reviewer selection, risk-based p
  `iam` `identity` `access-control` `access-review` `certification`

- [performing-active-directory-bloodhound-analysis](../cybersecurity/performing-active-directory-bloodhound-analysis/) — Use BloodHound and SharpHound to enumerate Active Directory relationships and identify attack paths from compromised users to Domain Admin. Use when working with performing active directory bloodhound analysis.
  `bloodhound` `active-directory` `sharphound` `attack-path` `ad-enumeration`

- [performing-active-directory-compromise-investigation](../cybersecurity/performing-active-directory-compromise-investigation/) — Investigate Active Directory compromise by analyzing authentication logs, replication metadata, Group Policy changes, and Kerberos ticket anomalies to identify attacker persistence and lateral movement paths. Use when working with performing active directory compromise investigation.
  `active-directory` `compromise-investigation` `identity-forensics` `kerberos` `lateral-movement`

- [performing-active-directory-forest-trust-attack](../cybersecurity/performing-active-directory-forest-trust-attack/) — Enumerate and audit Active Directory forest trust relationships using impacket for SID filtering analysis, trust key extraction, cross-forest SID history abuse detection, and inter-realm Kerberos ticket assessment. Use when working with performing active directory forest trust attack.
  `active-directory` `forest-trust` `impacket` `SID-filtering` `kerberos`

- [performing-active-directory-penetration-test](../cybersecurity/performing-active-directory-penetration-test/) — Conduct a focused Active Directory penetration test to enumerate domain objects, discover attack paths with BloodHound, exploit Kerberos weaknesses, escalate privileges via ADCS/DCSync, and demonstrate domain compromise. Use when conducting a focused active directory penetration test to enumerate domain.
  `active-directory` `BloodHound` `Kerberoasting` `Impacket` `DCSync`

- [performing-active-directory-vulnerability-assessment](../cybersecurity/performing-active-directory-vulnerability-assessment/) — Assess Active Directory security posture using PingCastle, BloodHound, and Purple Knight to identify misconfigurations, privilege escalation paths, and attack vectors. Use when working with performing active directory vulnerability assessment.
  `active-directory` `pingcastle` `bloodhound` `purple-knight` `ad-security`

- [performing-adversary-in-the-middle-phishing-detection](../cybersecurity/performing-adversary-in-the-middle-phishing-detection/) — Detect and respond to Adversary-in-the-Middle (AiTM) phishing attacks that use reverse proxy kits like EvilProxy, Evilginx, and Tycoon 2FA to bypass MFA and steal session tokens. Use when detecting and respond to adversary-in-the-middle (aitm) phishing attacks that use.
  `aitm` `evilproxy` `evilginx` `phishing` `mfa-bypass`

- [performing-agentless-vulnerability-scanning](../cybersecurity/performing-agentless-vulnerability-scanning/) — Configure and execute agentless vulnerability scanning using network protocols, cloud snapshot analysis, and API-based discovery to assess systems without installing endpoint agents. Use when configureing and execute agentless vulnerability scanning using network protocols, cloud.
  `agentless-scanning` `vulnerability-assessment` `cloud-security` `ssh` `wmi`

- [performing-ai-driven-osint-correlation](../cybersecurity/performing-ai-driven-osint-correlation/) — Use AI and LLM-based reasoning to correlate findings across multiple OSINT sources—username enumeration, email lookups, social media profiles, domain records, breach databases, and dark-web mentions—into unified intelligence profiles with confidence scoring and link analysis. Use when working with performing ai driven osint correlation.
  `osint` `ai-correlation` `threat-intelligence` `reconnaissance` `link-analysis`

- [performing-alert-triage-with-elastic-siem](../cybersecurity/performing-alert-triage-with-elastic-siem/) — Perform systematic alert triage in Elastic Security SIEM to rapidly classify, prioritize, and investigate security alerts for SOC operations. Use when performing systematic alert triage in elastic security siem to rapidly.
  `elastic` `siem` `alert-triage` `soc` `elastic-security`

- [performing-android-app-static-analysis-with-mobsf](../cybersecurity/performing-android-app-static-analysis-with-mobsf/) — Performs automated static analysis of Android applications using Mobile Security Framework (MobSF) to identify hardcoded secrets, insecure permissions, vulnerable components, weak cryptography, and code-level security flaws without executing the application. Use when assessing Android APK/AAB files for security vulnerabilities before deployment, during penetration testing, or as part of CI/CD security gates.
  `mobile-security` `android` `mobsf` `static-analysis` `owasp-mobile`

- [performing-api-fuzzing-with-restler](../cybersecurity/performing-api-fuzzing-with-restler/) — Use when uses Microsoft RESTler to perform stateful REST API fuzzing by automatically generating and executing test sequences that exercise API endpoints, discover producer-consumer dependencies between requests, and find security and reliability bugs. The tester compiles an OpenAPI specification into a RESTler fuzzing grammar, configures authentication, runs test/fuzz-lean/fuzz modes, and analyzes results for 500 errors, authentication bypasses, resource leaks, and payload injection vulnerab...
  `api-security` `fuzzing` `restler` `automated-testing` `openapi`

- [performing-api-inventory-and-discovery](../cybersecurity/performing-api-inventory-and-discovery/) — Performs API inventory and discovery to identify all API endpoints in an organization's environment including documented, undocumented, shadow, zombie, and deprecated APIs. The tester uses passive traffic analysis, active scanning, DNS enumeration, JavaScript analysis, and cloud resource inventory to build a comprehensive API catalog. Maps to OWASP API9:2023 Improper Inventory Management. Use when working with performing api inventory and discovery.
  `api-security` `owasp` `api-discovery` `shadow-api` `inventory`

- [performing-api-rate-limiting-bypass](../cybersecurity/performing-api-rate-limiting-bypass/) — Use when tests API rate limiting implementations for bypass vulnerabilities by manipulating request headers, IP addresses, HTTP methods, API versions, and encoding schemes to circumvent request throttling controls. The tester identifies rate limit headers, determines enforcement mechanisms, and attempts bypasses including X-Forwarded-For spoofing, parameter pollution, case variation, and endpoint path manipulation. Maps to OWASP API4:2023 Unrestricted Resource Consumption.
  `api-security` `owasp` `rate-limiting` `throttling` `brute-force`

- [performing-api-security-testing-with-postman](../cybersecurity/performing-api-security-testing-with-postman/) — Uses Postman to perform structured API security testing by building collections that test for OWASP API Security Top 10 vulnerabilities including authentication bypass, authorization flaws, injection, and data exposure. The tester creates environments with multiple user roles, writes test scripts for automated security validation, and integrates Postman with OWASP ZAP and Newman for CI/CD security testing.
  `api-security` `postman` `owasp` `automated-testing` `security-validation`

- [performing-arp-spoofing-attack-simulation](../cybersecurity/performing-arp-spoofing-attack-simulation/) — Simulates ARP spoofing attacks in authorized lab or pentest environments using arpspoof, Ettercap, and Scapy to demonstrate man-in-the-middle risks, test network detection capabilities, and validate ARP inspection countermeasures. . Use when working with performing arp spoofing attack simulation.
  `network-security` `arp-spoofing` `mitm` `ettercap` `layer2-attack`

- [performing-asset-criticality-scoring-for-vulns](../cybersecurity/performing-asset-criticality-scoring-for-vulns/) — Develop and apply a multi-factor asset criticality scoring model to weight vulnerability prioritization based on business impact, data sensitivity, and operational importance. Use when developing and apply a multi-factor asset criticality scoring model to.
  `asset-criticality` `vulnerability-prioritization` `risk-management` `cmdb` `business-impact`

- [performing-authenticated-scan-with-openvas](../cybersecurity/performing-authenticated-scan-with-openvas/) — Configure and execute authenticated vulnerability scans using OpenVAS/Greenbone Vulnerability Management with SSH and SMB credentials for comprehensive host-level assessment. Use when configureing and execute authenticated vulnerability scans using openvas/greenbone vulnerability management.
  `openvas` `gvm` `authenticated-scan` `vulnerability-scanning` `greenbone`

- [performing-authenticated-vulnerability-scan](../cybersecurity/performing-authenticated-vulnerability-scan/) — Authenticated (credentialed) vulnerability scanning uses valid system credentials to log into target hosts and perform deep inspection of installed software, patches, configurations, and security sett. Use when working with performing authenticated vulnerability scan.
  `vulnerability-management` `cve` `authenticated-scanning` `credentials` `nessus`

- [performing-automated-malware-analysis-with-cape](../cybersecurity/performing-automated-malware-analysis-with-cape/) — Deploy and operate CAPEv2 sandbox for automated malware analysis with behavioral monitoring, payload extraction, configuration parsing, and anti-evasion capabilities.
  `cape` `sandbox` `automated-analysis` `malware-analysis` `behavioral-analysis`

- [performing-aws-account-enumeration-with-scout-suite](../cybersecurity/performing-aws-account-enumeration-with-scout-suite/) — Perform comprehensive security posture assessment of AWS accounts using ScoutSuite to enumerate resources, identify misconfigurations, and generate actionable security reports.
  `aws` `scoutsuite` `cloud-security` `enumeration` `misconfiguration`

- [performing-aws-privilege-escalation-assessment](../cybersecurity/performing-aws-privilege-escalation-assessment/) — Performing authorized privilege escalation assessments in AWS environments to identify IAM misconfigurations that allow users or roles to elevate their permissions using Pacu, CloudFox, Principal Mapper, and manual IAM policy analysis techniques. . Use when working with performing aws privilege escalation assessment.
  `cloud-security` `aws` `privilege-escalation` `iam` `pacu`

- [performing-bandwidth-throttling-attack-simulation](../cybersecurity/performing-bandwidth-throttling-attack-simulation/) — Simulates bandwidth throttling and network degradation attacks using tc, iperf3, and Scapy in authorized environments to test quality-of-service controls, application resilience, and network monitoring detection of traffic manipulation attacks. . Use when working with performing bandwidth throttling attack simulation.
  `network-security` `bandwidth-throttling` `qos` `traffic-shaping` `network-resilience`

- [performing-binary-exploitation-analysis](../cybersecurity/performing-binary-exploitation-analysis/) — Analyze binary exploitation techniques including buffer overflows and ROP chains using pwntools Python library. Covers checksec analysis, gadget discovery with ROPgadget, and exploit development for CTF and authorized security assessments.

  `binary-exploitation` `pwntools` `rop-chains` `buffer-overflow`

- [performing-blind-ssrf-exploitation](../cybersecurity/performing-blind-ssrf-exploitation/) — Detect and exploit blind Server-Side Request Forgery vulnerabilities using out-of-band techniques, DNS interactions, and timing analysis to access internal services and cloud metadata endpoints. Use when detecting and exploit blind server-side request forgery vulnerabilities using out-of-band.
  `blind-ssrf` `ssrf` `out-of-band` `burp-collaborator` `cloud-metadata`

- [performing-bluetooth-security-assessment](../cybersecurity/performing-bluetooth-security-assessment/) — Assess Bluetooth Low Energy device security by scanning, enumerating GATT services, and detecting vulnerabilities. Use when working with performing bluetooth security assessment.
  `bluetooth` `ble` `gatt` `wireless-security`

- [performing-brand-monitoring-for-impersonation](../cybersecurity/performing-brand-monitoring-for-impersonation/) — Monitor for brand impersonation attacks across domains, social media, mobile apps, and dark web channels to detect phishing campaigns, fake sites, and unauthorized brand usage targeting your organization. Use when monitoring for brand impersonation attacks across domains, social media, mobile.
  `brand-monitoring` `impersonation` `phishing` `domain-monitoring` `social-media`

- [performing-clickjacking-attack-test](../cybersecurity/performing-clickjacking-attack-test/) — Testing web applications for clickjacking vulnerabilities by assessing frame embedding controls and crafting proof-of-concept overlay attacks during authorized security assessments. Use when working with performing clickjacking attack test.
  `penetration-testing` `clickjacking` `ui-redressing` `web-security` `owasp`

- [performing-cloud-asset-inventory-with-cartography](../cybersecurity/performing-cloud-asset-inventory-with-cartography/) — Perform comprehensive cloud asset inventory and relationship mapping using Cartography to build a Neo4j security graph of infrastructure assets, IAM permissions, and attack paths across AWS, GCP, and Azure. Use when performing comprehensive cloud asset inventory and relationship mapping using cartography.
  `cartography` `neo4j` `cloud-security` `asset-inventory` `attack-path`

- [performing-cloud-forensics-investigation](../cybersecurity/performing-cloud-forensics-investigation/) — Conduct forensic investigations in cloud environments by collecting and analyzing logs, snapshots, and metadata from AWS, Azure, and GCP services. Use when conducting forensic investigations in cloud environments by collecting and analyzing.
  `forensics` `cloud-forensics` `aws` `azure` `gcp`

- [performing-cloud-forensics-with-aws-cloudtrail](../cybersecurity/performing-cloud-forensics-with-aws-cloudtrail/) — Perform forensic investigation of AWS environments using CloudTrail logs to reconstruct attacker activity, identify compromised credentials, and analyze API call patterns. Use when performing forensic investigation of aws environments using cloudtrail logs to.
  `cloud-security` `aws` `cloudtrail` `forensics` `incident-response`

- [performing-cloud-incident-containment-procedures](../cybersecurity/performing-cloud-incident-containment-procedures/) — Execute cloud-native incident containment across AWS, Azure, and GCP by isolating compromised resources, revoking credentials, preserving forensic evidence, and applying security group restrictions to prevent lateral movement. Use when working with performing cloud incident containment procedures.
  `cloud-security` `incident-containment` `aws` `azure` `gcp`

- [performing-cloud-log-forensics-with-athena](../cybersecurity/performing-cloud-log-forensics-with-athena/) — Uses AWS Athena to query CloudTrail, VPC Flow Logs, S3 access logs, and ALB logs for forensic investigation. Covers CREATE TABLE DDL with partition projection, forensic SQL queries for detecting unauthorized access, data exfiltration, lateral movement, and privilege escalation. Use when investigating AWS security incidents or building cloud-native forensic workflows at scale.

  `cloud` `forensics` `athena` `aws` `cloudtrail`

- [performing-cloud-native-forensics-with-falco](../cybersecurity/performing-cloud-native-forensics-with-falco/) — Uses Falco YAML rules for runtime threat detection in containers and Kubernetes, monitoring syscalls for shell spawns, file tampering, network anomalies, and privilege escalation. Manages Falco rules via the Falco gRPC API and parses Falco alert output. Use when building container runtime security or investigating k8s cluster compromises.

  `performing` `cloud` `native` `forensics`

- [performing-cloud-native-threat-hunting-with-aws-detective](../cybersecurity/performing-cloud-native-threat-hunting-with-aws-detective/) — Hunt for threats in AWS environments using Detective behavior graphs, entity investigation timelines, GuardDuty finding correlation, and automated entity profiling across IAM users, EC2 instances, and IP addresses.
  `aws-detective` `threat-hunting` `cloud-security` `guardduty` `behavior-graph`

- [performing-cloud-penetration-testing-with-pacu](../cybersecurity/performing-cloud-penetration-testing-with-pacu/) — Performing authorized AWS penetration testing using Pacu, the open-source AWS exploitation framework, to enumerate IAM configurations, discover privilege escalation paths, test credential harvesting, and validate security controls through systematic attack simulation. . Use when working with performing cloud penetration testing with pacu.
  `cloud-security` `aws` `pacu` `penetration-testing` `offensive-security`

- [performing-cloud-storage-forensic-acquisition](../cybersecurity/performing-cloud-storage-forensic-acquisition/) — Perform forensic acquisition and analysis of cloud storage services including Google Drive, OneDrive, Dropbox, and Box by collecting both API-based remote data and local sync client artifacts from endpoint devices. Use when performing forensic acquisition and analysis of cloud storage services including.
  `cloud-forensics` `google-drive` `onedrive` `dropbox` `box`

- [performing-container-escape-detection](../cybersecurity/performing-container-escape-detection/) — Detects container escape attempts by analyzing namespace configurations, privileged container checks, dangerous capability assignments, and host path mounts using the kubernetes Python client. Identifies CVE-2022-0492 style escapes via cgroup abuse. Use when auditing container security posture or investigating escape attempts.

  `performing` `container` `escape` `detection`

- [performing-container-image-hardening](../cybersecurity/performing-container-image-hardening/) — This skill covers hardening container images by minimizing attack surface, removing unnecessary packages, implementing multi-stage builds, configuring non-root users, and applying CIS Docker Benchmark recommendations to produce secure production-ready images.

  `devsecops` `cicd` `container-hardening` `docker` `cis-benchmark`

- [performing-container-security-scanning-with-trivy](../cybersecurity/performing-container-security-scanning-with-trivy/) — Scan container images, filesystems, and Kubernetes manifests for vulnerabilities, misconfigurations, exposed secrets, and license compliance issues using Aqua Security Trivy with SBOM generation and CI/CD integration. Use when scaning container images, filesystems, and kubernetes manifests for vulnerabilities, misconfigurations,.
  `trivy` `container-security` `vulnerability-scanning` `sbom` `docker`

- [performing-content-security-policy-bypass](../cybersecurity/performing-content-security-policy-bypass/) — Analyze and bypass Content Security Policy implementations to achieve cross-site scripting by exploiting misconfigurations, JSONP endpoints, unsafe directives, and policy injection techniques. Use when analyzeing and bypass content security policy implementations to achieve cross-site.
  `csp-bypass` `content-security-policy` `xss` `script-injection` `nonce-bypass`

- [performing-credential-access-with-lazagne](../cybersecurity/performing-credential-access-with-lazagne/) — Extract stored credentials from compromised endpoints using the LaZagne post-exploitation tool to recover passwords from browsers, databases, system vaults, and applications during authorized red team operations. Use when working with performing credential access with lazagne.
  `red-team` `credential-access` `lazagne` `post-exploitation` `password-recovery`

- [performing-cryptographic-audit-of-application](../cybersecurity/performing-cryptographic-audit-of-application/) — A cryptographic audit systematically reviews an application's use of cryptographic primitives, protocols, and key management to identify vulnerabilities such as weak algorithms, insecure modes, hardco. Use when working with performing cryptographic audit of application.
  `cryptography` `audit` `security-review` `compliance` `vulnerability-assessment`

- [performing-csrf-attack-simulation](../cybersecurity/performing-csrf-attack-simulation/) — Testing web applications for Cross-Site Request Forgery vulnerabilities by crafting forged requests that exploit authenticated user sessions during authorized security assessments. Use when working with performing csrf attack simulation.
  `penetration-testing` `csrf` `owasp` `web-security` `session-management`

- [performing-cve-prioritization-with-kev-catalog](../cybersecurity/performing-cve-prioritization-with-kev-catalog/) — Leverage the CISA Known Exploited Vulnerabilities catalog alongside EPSS and CVSS to prioritize CVE remediation based on real-world exploitation evidence. Use when working with performing cve prioritization with kev catalog.
  `cisa-kev` `cve` `vulnerability-prioritization` `epss` `bod-22-01`

- [performing-dark-web-monitoring-for-threats](../cybersecurity/performing-dark-web-monitoring-for-threats/) — Dark web monitoring involves systematically scanning Tor hidden services, underground forums, paste sites, and dark web marketplaces to identify threats targeting an organization, including leaked cre. Use when working with performing dark web monitoring for threats.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [performing-deception-technology-deployment](../cybersecurity/performing-deception-technology-deployment/) — Deploys deception technology including honeypots, honeytokens, and decoy systems to detect attackers who have bypassed perimeter defenses, providing high-fidelity alerts with near-zero false positive rates. Use when SOC teams need early warning of lateral movement, credential abuse, or internal reconnaissance by deploying convincing traps across the network.

  `soc` `deception` `honeypot` `honeytoken` `canary`

- [performing-directory-traversal-testing](../cybersecurity/performing-directory-traversal-testing/) — Testing web applications for path traversal vulnerabilities that allow reading or writing arbitrary files on the server by manipulating file path parameters. Use when working with performing directory traversal testing.
  `penetration-testing` `directory-traversal` `path-traversal` `lfi` `owasp`

- [performing-disk-forensics-investigation](../cybersecurity/performing-disk-forensics-investigation/) — Use when conducts disk forensics investigations using forensic imaging, file system analysis, artifact recovery, and timeline reconstruction to support incident response cases. Utilizes tools such as FTK Imager, Autopsy, and The Sleuth Kit for evidence acquisition, deleted file recovery, and artifact examination. Activates for requests involving disk forensics, hard drive analysis, forensic imaging, file recovery, evidence acquisition, or digital forensic investigation.
'.
  `disk-forensics` `forensic-imaging` `evidence-acquisition` `file-recovery` `chain-of-custody`

- [performing-dmarc-policy-enforcement-rollout](../cybersecurity/performing-dmarc-policy-enforcement-rollout/) — Execute a phased DMARC rollout from p=none monitoring through p=quarantine to p=reject enforcement, ensuring all legitimate email sources are authenticated before blocking unauthorized senders. Use when working with performing dmarc policy enforcement rollout.
  `dmarc` `spf` `dkim` `email-authentication` `anti-spoofing`

- [performing-dns-enumeration-and-zone-transfer](../cybersecurity/performing-dns-enumeration-and-zone-transfer/) — Enumerates DNS records, attempts zone transfers, brute-forces subdomains, and maps DNS infrastructure during authorized reconnaissance to identify attack surface, misconfigurations, and information disclosure in target domains. . Use when working with performing dns enumeration and zone transfer.
  `network-security` `dns` `enumeration` `zone-transfer` `reconnaissance`

- [performing-dns-tunneling-detection](../cybersecurity/performing-dns-tunneling-detection/) — Detects DNS tunneling by computing Shannon entropy of DNS query names, analyzing query length distributions, inspecting TXT record payloads, and identifying high subdomain cardinality. Uses scapy for packet capture analysis and statistical methods to distinguish legitimate DNS from covert channels. Use when hunting for data exfiltration.

  `performing` `dns` `tunneling` `detection`

- [performing-docker-bench-security-assessment](../cybersecurity/performing-docker-bench-security-assessment/) — Docker Bench for Security is an open-source script that checks dozens of common best practices around deploying Docker containers in production. Based on the CIS Docker Benchmark, it audits host confi. Use when working with performing docker bench security assessment.
  `containers` `docker` `security` `CIS-benchmark` `assessment`

- [performing-dynamic-analysis-of-android-app](../cybersecurity/performing-dynamic-analysis-of-android-app/) — Performs runtime dynamic analysis of Android applications using Frida, Objection, and Android Debug Bridge to observe application behavior during execution, intercept function calls, modify runtime values, and identify vulnerabilities that static analysis misses. Use when testing Android apps for runtime security flaws, hooking sensitive methods, bypassing client-side protections, or analyzing obfuscated applications.
  `mobile-security` `android` `frida` `dynamic-analysis` `owasp-mobile`

- [performing-dynamic-analysis-with-any-run](../cybersecurity/performing-dynamic-analysis-with-any-run/) — Performs interactive dynamic malware analysis using the ANY.RUN cloud sandbox to observe real-time execution behavior, interact with malware prompts, and capture process trees, network traffic, and system changes. Activates for requests involving interactive sandbox analysis, cloud-based malware detonation, real-time behavioral observation, or ANY.RUN usage. . Use when working with performing dynamic analysis with any run.
  `malware` `dynamic-analysis` `sandbox` `ANY.RUN` `interactive-analysis`

- [performing-endpoint-forensics-investigation](../cybersecurity/performing-endpoint-forensics-investigation/) — Performs digital forensics investigation on compromised endpoints including memory acquisition, disk imaging, artifact analysis, and timeline reconstruction. Use when investigating security incidents, collecting evidence for legal proceedings, or analyzing endpoint compromise scope. Activates for requests involving endpoint forensics, memory analysis, disk forensics, or incident investigation.

  `endpoint` `forensics` `memory-analysis` `disk-imaging` `incident-investigation`

- [performing-endpoint-vulnerability-remediation](../cybersecurity/performing-endpoint-vulnerability-remediation/) — Performs vulnerability remediation on endpoints by prioritizing CVEs based on risk scoring, deploying patches, applying configuration changes, and validating fixes. Use when remediating findings from vulnerability scans, responding to critical CVE advisories, or maintaining endpoint compliance with patch management SLAs. Activates for requests involving vulnerability remediation, CVE patching, endpoint vulnerability management, or security fix deployment.

  `endpoint` `vulnerability-management` `patching` `CVE` `remediation`

- [performing-entitlement-review-with-sailpoint-iiq](../cybersecurity/performing-entitlement-review-with-sailpoint-iiq/) — Performs entitlement review and access certification campaigns using SailPoint IdentityIQ including manager certifications, targeted entitlement reviews, role-based access validation, SOD violation remediation, and automated revocation workflows. Activates for requests involving access reviews, entitlement certifications, SailPoint IIQ governance, or periodic user access recertification.

  `SailPoint` `IdentityIQ` `access-review` `entitlement-certification` `IGA`

- [performing-external-network-penetration-test](../cybersecurity/performing-external-network-penetration-test/) — Conduct a comprehensive external network penetration test to identify vulnerabilities in internet-facing infrastructure using PTES methodology, reconnaissance, scanning, exploitation, and reporting. Use when conducting a comprehensive external network penetration test to identify vulnerabilities.
  `external-pentest` `network-security` `PTES` `OSSTMM` `Nmap`

- [performing-false-positive-reduction-in-siem](../cybersecurity/performing-false-positive-reduction-in-siem/) — Perform systematic SIEM false positive reduction through rule tuning, threshold adjustment, correlation refinement, and threat intelligence enrichment to combat alert fatigue. Use when performing systematic siem false positive reduction through rule tuning, threshold.
  `siem` `false-positive` `alert-tuning` `detection-engineering` `alert-fatigue`

- [performing-file-carving-with-foremost](../cybersecurity/performing-file-carving-with-foremost/) — Recover files from disk images and unallocated space using Foremost's header-footer signature carving to extract evidence regardless of file system state. Use when working with performing file carving with foremost.
  `forensics` `file-carving` `foremost` `data-recovery` `evidence-recovery`

- [performing-firmware-extraction-with-binwalk](../cybersecurity/performing-firmware-extraction-with-binwalk/) — Performs firmware image extraction and analysis using binwalk to identify embedded filesystems, compressed archives, bootloaders, kernel images, and cryptographic material. Covers entropy analysis for detecting encrypted or compressed regions, recursive extraction of nested archives, SquashFS/CramFS/JFFS2 filesystem mounting, and string analysis for credential and configuration discovery.
  `firmware` `binwalk` `extraction` `entropy` `IoT-security`

- [performing-firmware-malware-analysis](../cybersecurity/performing-firmware-malware-analysis/) — Analyzes firmware images for embedded malware, backdoors, and unauthorized modifications targeting routers, IoT devices, UEFI/BIOS, and embedded systems. Covers firmware extraction, filesystem analysis, binary reverse engineering, and bootkit detection. Activates for requests involving firmware security analysis, IoT malware investigation, UEFI rootkit detection, or embedded device compromise assessment.

  `malware` `firmware` `IoT` `UEFI` `embedded-security`

- [performing-fuzzing-with-aflplusplus](../cybersecurity/performing-fuzzing-with-aflplusplus/) — Use when perform coverage-guided fuzzing of compiled binaries using AFL++ (American Fuzzy Lop Plus Plus) to discover memory corruption, crashes, and security vulnerabilities. The tester instruments target binaries with afl-cc/afl-clang-fast, manages input corpora with afl-cmin and afl-tmin, runs parallel fuzzing campaigns with afl-fuzz, and triages crashes using CASR or GDB scripts. Activates for requests involving binary fuzzing, crash discovery, coverage-guided testing, or AFL++ fuzzing cam...
  `fuzzing` `aflplusplus` `coverage-guided` `crash-triage` `binary-analysis`

- [performing-gcp-penetration-testing-with-gcpbucketbrute](../cybersecurity/performing-gcp-penetration-testing-with-gcpbucketbrute/) — Perform GCP security testing using GCPBucketBrute for storage bucket enumeration, gcloud IAM privilege escalation path analysis, and service account permission auditing. Use when performing gcp security testing using gcpbucketbrute for storage bucket enumeration,.
  `gcp` `cloud-pentesting` `bucket-enumeration` `iam-audit` `privilege-escalation`

- [performing-gcp-security-assessment-with-forseti](../cybersecurity/performing-gcp-security-assessment-with-forseti/) — Performing comprehensive security assessments of Google Cloud Platform environments using Forseti Security, Security Command Center, and gcloud CLI to audit IAM policies, firewall rules, storage permissions, and compliance against CIS GCP Foundations Benchmark. . Use when working with performing gcp security assessment with forseti.
  `cloud-security` `gcp` `forseti` `security-command-center` `iam-audit`

- [performing-graphql-depth-limit-attack](../cybersecurity/performing-graphql-depth-limit-attack/) — Execute and test GraphQL depth limit attacks using deeply nested recursive queries to identify denial-of-service vulnerabilities in GraphQL APIs. Use when working with performing graphql depth limit attack.
  `graphql` `depth-limit` `denial-of-service` `nested-queries` `api-security`

- [performing-graphql-introspection-attack](../cybersecurity/performing-graphql-introspection-attack/) — Use when performs GraphQL introspection attacks to extract the full API schema including types, queries, mutations, subscriptions, and field definitions from GraphQL endpoints. The tester uses introspection queries to map the attack surface, identifies sensitive fields and mutations, tests for query depth and complexity limits, and exploits GraphQL-specific vulnerabilities including batching attacks, alias-based brute force, and nested query DoS.
  `api-security` `graphql` `introspection` `schema-extraction` `query-abuse`

- [performing-graphql-security-assessment](../cybersecurity/performing-graphql-security-assessment/) — Assessing GraphQL API endpoints for introspection leaks, injection attacks, authorization flaws, and denial-of-service vulnerabilities during authorized security tests. Use when working with performing graphql security assessment.
  `penetration-testing` `graphql` `api-security` `owasp` `web-security`

- [performing-hardware-security-module-integration](../cybersecurity/performing-hardware-security-module-integration/) — Integrate Hardware Security Modules (HSMs) using PKCS#11 interface for cryptographic key management, signing operations, and secure key storage with python-pkcs11, AWS CloudHSM, and YubiHSM2. Use when integrateing hardware security modules (hsms) using pkcs#11 interface for cryptographic.
  `HSM` `PKCS11` `CloudHSM` `YubiHSM2` `key-management`

- [performing-hash-cracking-with-hashcat](../cybersecurity/performing-hash-cracking-with-hashcat/) — Hash cracking is an essential skill for penetration testers and security auditors to evaluate password strength. Hashcat is the world's fastest password recovery tool, supporting over 300 hash types w. Use when working with performing hash cracking with hashcat.
  `cryptography` `hash-cracking` `password-security` `hashcat` `penetration-testing`

- [performing-http-parameter-pollution-attack](../cybersecurity/performing-http-parameter-pollution-attack/) — Execute HTTP Parameter Pollution attacks to bypass input validation, WAF rules, and security controls by injecting duplicate parameters that are processed differently by front-end and back-end systems. Use when working with performing http parameter pollution attack.
  `http-parameter-pollution` `hpp` `waf-bypass` `input-validation` `web-security`

- [performing-ics-asset-discovery-with-claroty](../cybersecurity/performing-ics-asset-discovery-with-claroty/) — Perform comprehensive ICS/OT asset discovery using Claroty xDome platform, leveraging passive monitoring, Claroty Edge active queries, and integration ecosystem to gain full visibility into industrial control system assets including PLCs, RTUs, HMIs, and network infrastructure across Purdue Model levels. . Use when working with performing ics asset discovery with claroty.
  `ot-security` `ics` `asset-discovery` `claroty` `xdome`

- [performing-indicator-lifecycle-management](../cybersecurity/performing-indicator-lifecycle-management/) — Indicator lifecycle management tracks IOCs from initial discovery through validation, enrichment, deployment, monitoring, and eventual retirement. This skill covers implementing systematic processes f
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [performing-initial-access-with-evilginx3](../cybersecurity/performing-initial-access-with-evilginx3/) — Perform authorized initial access using EvilGinx3 adversary-in-the-middle phishing framework to capture session tokens and bypass multi-factor authentication during red team engagements. Use when performing authorized initial access using evilginx3 adversary-in-the-middle phishing framework to.
  `red-team` `initial-access` `phishing` `evilginx` `mfa-bypass`

- [performing-insider-threat-investigation](../cybersecurity/performing-insider-threat-investigation/) — Use when investigates insider threat incidents involving employees, contractors, or trusted partners who misuse authorized access to steal data, sabotage systems, or violate security policies. Combines digital forensics, user behavior analytics, and HR/legal coordination to build an evidence-based case. Activates for requests involving insider threat investigation, employee data theft, privilege misuse, user behavior anomaly, or internal threat detection.
'.
  `insider-threat` `user-behavior-analytics` `data-exfiltration` `privilege-misuse` `DFIR`

- [performing-ioc-enrichment-automation](../cybersecurity/performing-ioc-enrichment-automation/) — Automates Indicator of Compromise (IOC) enrichment by orchestrating lookups across VirusTotal, AbuseIPDB, Shodan, MISP, and other intelligence sources to provide contextual scoring and disposition recommendations. Use when SOC analysts need rapid multi-source enrichment of IPs, domains, URLs, and file hashes during alert triage or incident investigation.

  `soc` `ioc` `enrichment` `automation` `virustotal`

- [performing-ios-app-security-assessment](../cybersecurity/performing-ios-app-security-assessment/) — Performs comprehensive iOS application security assessments using Frida for dynamic instrumentation, Objection for runtime exploration, SSL pinning bypass for traffic interception, keychain extraction for credential analysis, and IPA static analysis for binary-level review. Use when conducting authorized iOS penetration tests, evaluating mobile app security posture against OWASP MASTG, or assessing iOS app data protection and transport security controls.
  `mobile-security` `ios` `frida` `objection` `ssl-pinning`

- [performing-iot-security-assessment](../cybersecurity/performing-iot-security-assessment/) — Performs comprehensive security assessments of IoT devices and their ecosystems by testing hardware interfaces, firmware, network communications, cloud APIs, and companion mobile applications. The tester uses firmware extraction and analysis, hardware debugging via UART and JTAG, network protocol analysis, and runtime exploitation to identify vulnerabilities across all layers of the IoT stack. Use when working with performing iot security assessment.
  `IoT-security` `firmware-analysis` `embedded-systems` `hardware-hacking` `UART-JTAG`

- [performing-ip-reputation-analysis-with-shodan](../cybersecurity/performing-ip-reputation-analysis-with-shodan/) — Analyze IP address reputation using the Shodan API to identify open ports, running services, known vulnerabilities, and hosting context for threat intelligence enrichment and incident triage. Use when analyzeing ip address reputation using the shodan api to identify.
  `shodan` `ip-reputation` `enrichment` `threat-intelligence` `reconnaissance`

- [performing-jwt-none-algorithm-attack](../cybersecurity/performing-jwt-none-algorithm-attack/) — Execute and test the JWT none algorithm attack to bypass signature verification by manipulating the alg header field in JSON Web Tokens. Use when working with performing jwt none algorithm attack.
  `jwt` `none-algorithm` `authentication-bypass` `token-manipulation` `signature-bypass`

- [performing-kerberoasting-attack](../cybersecurity/performing-kerberoasting-attack/) — Kerberoasting is a post-exploitation technique that targets service accounts in Active Directory by requesting Kerberos TGS (Ticket Granting Service) tickets for accounts with Service Principal Names. Use when working with performing kerberoasting attack.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [performing-kubernetes-cis-benchmark-with-kube-bench](../cybersecurity/performing-kubernetes-cis-benchmark-with-kube-bench/) — Audit Kubernetes cluster security posture against CIS benchmarks using kube-bench with automated checks for control plane, worker nodes, and RBAC.
  `kube-bench` `cis-benchmark` `kubernetes` `compliance` `hardening`

- [performing-kubernetes-etcd-security-assessment](../cybersecurity/performing-kubernetes-etcd-security-assessment/) — Assess the security posture of Kubernetes etcd clusters by evaluating encryption at rest, TLS configuration, access controls, backup encryption, and network isolation. Use when working with performing kubernetes etcd security assessment.
  `kubernetes` `etcd` `encryption` `tls` `security-assessment`

- [performing-kubernetes-penetration-testing](../cybersecurity/performing-kubernetes-penetration-testing/) — Kubernetes penetration testing systematically evaluates cluster security by simulating attacker techniques against the API server, kubelet, etcd, pods, RBAC, network policies, and secrets. Using tools. Use when working with performing kubernetes penetration testing.
  `containers` `kubernetes` `security` `penetration-testing` `offensive-security`

- [performing-lateral-movement-detection](../cybersecurity/performing-lateral-movement-detection/) — Detects lateral movement techniques including Pass-the-Hash, PsExec, WMI execution, RDP pivoting, and SMB-based spreading using SIEM correlation of Windows event logs, network flow data, and endpoint telemetry mapped to MITRE ATT&CK Lateral Movement (TA0008) techniques. . Use when working with performing lateral movement detection.
  `soc` `lateral-movement` `mitre-attack` `pass-the-hash` `psexec`

- [performing-lateral-movement-with-wmiexec](../cybersecurity/performing-lateral-movement-with-wmiexec/) — Perform lateral movement across Windows networks using WMI-based remote execution techniques including Impacket wmiexec.py, CrackMapExec, and native WMI commands for stealthy post-exploitation during red team engagements. Use when performing lateral movement across windows networks using wmi-based remote execution.
  `red-team` `lateral-movement` `wmiexec` `wmi` `post-exploitation`

- [performing-linux-log-forensics-investigation](../cybersecurity/performing-linux-log-forensics-investigation/) — Perform forensic investigation of Linux system logs including syslog, auth.log, systemd journal, kern.log, and application logs to reconstruct user activity, detect unauthorized access, and establish event timelines on compromised Linux systems. Use when performing forensic investigation of linux system logs including syslog, auth.log,.
  `linux-forensics` `syslog` `auth-log` `systemd-journal` `journalctl`

- [performing-log-analysis-for-forensic-investigation](../cybersecurity/performing-log-analysis-for-forensic-investigation/) — Collect, parse, and correlate system, application, and security logs to reconstruct events and establish timelines during forensic investigations. Use when working with performing log analysis for forensic investigation.
  `forensics` `log-analysis` `siem` `event-correlation` `timeline-analysis`

- [performing-log-source-onboarding-in-siem](../cybersecurity/performing-log-source-onboarding-in-siem/) — Perform structured log source onboarding into SIEM platforms by configuring collectors, parsers, normalization, and validation for complete security visibility. Use when performing structured log source onboarding into siem platforms by configuring.
  `siem` `log-onboarding` `log-management` `data-ingestion` `parsing`

- [performing-malware-hash-enrichment-with-virustotal](../cybersecurity/performing-malware-hash-enrichment-with-virustotal/) — Enrich malware file hashes using the VirusTotal API to retrieve detection rates, behavioral analysis, YARA matches, and contextual threat intelligence for incident triage and IOC validation. Use when working with performing malware hash enrichment with virustotal.
  `virustotal` `malware-analysis` `hash-enrichment` `ioc` `threat-intelligence`

- [performing-malware-ioc-extraction](../cybersecurity/performing-malware-ioc-extraction/) — Malware IOC extraction is the process of analyzing malicious software to identify actionable indicators of compromise including file hashes, network indicators (C2 domains, IP addresses, URLs), regist. Use when working with performing malware ioc extraction.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [performing-malware-persistence-investigation](../cybersecurity/performing-malware-persistence-investigation/) — Systematically investigate all persistence mechanisms on Windows and Linux systems to identify how malware survives reboots and maintains access. Use when working with performing malware persistence investigation.
  `forensics` `malware-persistence` `autoruns` `registry` `scheduled-tasks`

- [performing-malware-triage-with-yara](../cybersecurity/performing-malware-triage-with-yara/) — Performs rapid malware triage and classification using YARA rules to match file patterns, strings, byte sequences, and structural characteristics against known malware families and suspicious indicators. Covers rule writing, scanning, and integration with analysis pipelines. Activates for requests involving YARA rule creation, malware classification, pattern matching, sample triage, or signature-based detection.

  `malware` `YARA` `triage` `classification` `pattern-matching`

- [performing-memory-forensics-with-volatility3](../cybersecurity/_deprecated/performing-memory-forensics-with-volatility3/) — Analyze volatile memory dumps using Volatility 3 to extract running processes, network connections, loaded modules, and evidence of malicious activity. Use when analyzeing volatile memory dumps using volatility 3 to extract running.
  `forensics` `memory-forensics` `volatility` `ram-analysis` `malware-detection`

- [performing-memory-forensics-with-volatility3-plugins](../cybersecurity/performing-memory-forensics-with-volatility3-plugins/) — Analyze memory dumps using Volatility3 plugins to detect injected code, rootkits, credential theft, and malware artifacts in Windows, Linux, and macOS memory images. Use when analyzeing memory dumps using volatility3 plugins to detect injected code,.
  `memory-forensics` `volatility3` `malware-analysis` `incident-response` `process-injection`

- [performing-mobile-app-certificate-pinning-bypass](../cybersecurity/performing-mobile-app-certificate-pinning-bypass/) — Bypasses SSL/TLS certificate pinning implementations in Android and iOS applications to enable traffic interception during authorized security assessments. Covers OkHttp, TrustManager, NSURLSession, and third-party pinning library bypass techniques using Frida, Objection, and custom scripts. Activates for requests involving certificate pinning bypass, SSL pinning defeat, mobile TLS interception, or proxy-resistant app testing.

  `mobile-security` `android` `ios` `certificate-pinning` `frida`

- [performing-mobile-device-forensics-with-cellebrite](../cybersecurity/performing-mobile-device-forensics-with-cellebrite/) — Acquire and analyze mobile device data using Cellebrite UFED and open-source tools to extract communications, location data, and application artifacts. Use when working with performing mobile device forensics with cellebrite.
  `forensics` `mobile-forensics` `cellebrite` `smartphone-analysis` `ios-forensics`

- [performing-network-forensics-with-wireshark](../cybersecurity/performing-network-forensics-with-wireshark/) — Capture and analyze network traffic using Wireshark and tshark to reconstruct network events, extract artifacts, and identify malicious communications. Use when working with performing network forensics with wireshark.
  `forensics` `network-forensics` `wireshark` `pcap` `packet-analysis`

- [performing-network-packet-capture-analysis](../cybersecurity/performing-network-packet-capture-analysis/) — Perform forensic analysis of network packet captures (PCAP/PCAPNG) using Wireshark, tshark, and tcpdump to reconstruct network communications, extract transferred files, identify malicious traffic, and establish evidence of data exfiltration or command-and-control activity. Use when performing forensic analysis of network packet captures (pcap/pcapng) using wireshark,.
  `pcap` `wireshark` `tshark` `tcpdump` `network-forensics`

- [performing-network-traffic-analysis-with-tshark](../cybersecurity/performing-network-traffic-analysis-with-tshark/) — Automate network traffic analysis using tshark and pyshark for protocol statistics, suspicious flow detection, DNS anomaly identification, and IOC extraction from PCAP files
  `tshark` `pyshark` `pcap` `packet-analysis` `network-forensics`

- [performing-network-traffic-analysis-with-zeek](../cybersecurity/performing-network-traffic-analysis-with-zeek/) — Deploy Zeek network security monitor to capture, parse, and analyze network traffic metadata for threat detection, anomaly identification, and forensic investigation. Use when deploying zeek network security monitor to capture, parse, and analyze.
  `zeek` `network-monitoring` `traffic-analysis` `ids` `nids`

- [performing-nist-csf-maturity-assessment](../cybersecurity/performing-nist-csf-maturity-assessment/) — Assess organizational cybersecurity maturity against NIST CSF framework. Evaluate identify, protect, detect, respond, and recover functions with actionable gap analysis. The NIST Cybersecurity Framework (CSF) 2.0, released in February 2024, provides a comprehensive taxonomy for managing cybersecurity risk through six core Functions - Govern, Identify, Protect, Detect, Respond, and Recover. This skill covers conducting a maturity assessment against the CSF using Implementation Tiers to me.
  `compliance` `governance` `nist` `csf` `maturity-assessment`

- [performing-oauth-scope-minimization-review](../cybersecurity/performing-oauth-scope-minimization-review/) — Performs OAuth 2.0 scope minimization review to identify over-permissioned third-party application integrations, excessive API scopes, unused token grants, and risky OAuth consent patterns across identity providers and SaaS platforms. Activates for requests involving OAuth scope audit, API permission review, third-party app risk assessment, or consent grant minimization. . Use when working with performing oauth scope minimization review.
  `OAuth` `scope-minimization` `API-security` `consent-review` `third-party-risk`

- [performing-oil-gas-cybersecurity-assessment](../cybersecurity/performing-oil-gas-cybersecurity-assessment/) — This skill covers conducting cybersecurity assessments specific to oil and gas facilities including upstream (exploration/production), midstream (pipeline/transport), and downstream (refining/distribution) operations. It addresses SCADA systems controlling pipeline operations, DCS for refinery process control, safety instrumented systems for hazardous processes, remote terminal units at unmanned wellhead sites, and compliance with API 1164, TSA Pipeline Security Directives, IEC 62443, an.
  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [performing-open-source-intelligence-gathering](../cybersecurity/performing-open-source-intelligence-gathering/) — Open Source Intelligence (OSINT) gathering is the first active phase of a red team engagement, where operators collect publicly available information about the target organization to identify attack s. Use when working with performing open source intelligence gathering.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [performing-osint-with-spiderfoot](../cybersecurity/performing-osint-with-spiderfoot/) — Automate OSINT collection using SpiderFoot REST API and CLI for target profiling, module-based reconnaissance, and structured result analysis across 200+ data sources
  `osint` `spiderfoot` `reconnaissance` `threat-intelligence` `attack-surface`

- [performing-ot-network-security-assessment](../cybersecurity/performing-ot-network-security-assessment/) — This skill covers conducting comprehensive security assessments of Operational Technology (OT) networks including SCADA systems, DCS architectures, and industrial control system communication paths. It addresses the Purdue Reference Model layers, identifies IT/OT convergence risks, evaluates firewall rules between zones, and maps industrial protocol traffic (Modbus, DNP3, OPC UA, EtherNet/IP) to detect misconfigurations, unauthorized connections, and attack surfaces in critical infrastr.
  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [performing-ot-vulnerability-assessment-with-claroty](../cybersecurity/performing-ot-vulnerability-assessment-with-claroty/) — This skill covers performing vulnerability assessments in OT environments using the Claroty xDome platform for comprehensive asset discovery, risk scoring, vulnerability correlation, and remediation prioritization. It addresses passive vulnerability identification through traffic analysis, active safe querying of OT devices, integration with CVE databases and ICS-CERT advisories, and risk-based prioritization that accounts for operational impact and compensating controls.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [performing-ot-vulnerability-scanning-safely](../cybersecurity/performing-ot-vulnerability-scanning-safely/) — Perform vulnerability scanning in OT/ICS environments safely using passive monitoring, native protocol queries, and carefully controlled active scanning with Tenable OT Security to identify vulnerabilities without disrupting industrial processes or crashing legacy controllers. . Use when working with performing ot vulnerability scanning safely.
  `ot-security` `ics` `vulnerability-scanning` `tenable` `nessus`

- [performing-packet-injection-attack](../cybersecurity/performing-packet-injection-attack/) — Crafts and injects custom network packets using Scapy, hping3, and Nemesis during authorized security assessments to test firewall rules, IDS detection, protocol handling, and network stack resilience against malformed and spoofed traffic. . Use when working with performing packet injection attack.
  `network-security` `packet-injection` `scapy` `hping3` `protocol-testing`

- [performing-paste-site-monitoring-for-credentials](../cybersecurity/performing-paste-site-monitoring-for-credentials/) — Monitor paste sites like Pastebin and GitHub Gists for leaked credentials, API keys, and sensitive data dumps using automated scraping and keyword matching to detect breaches early.
  `paste-monitoring` `credential-leak` `pastebin` `data-breach` `threat-intelligence`

- [performing-phishing-simulation-with-gophish](../cybersecurity/performing-phishing-simulation-with-gophish/) — GoPhish is an open-source phishing simulation framework used by security teams to conduct authorized phishing awareness campaigns. It provides campaign management, email template creation, landing pag. Use when working with performing phishing simulation with gophish.
  `phishing` `email-security` `social-engineering` `dmarc` `awareness`

- [performing-physical-intrusion-assessment](../cybersecurity/performing-physical-intrusion-assessment/) — Conduct authorized physical penetration testing using tailgating, badge cloning, lock bypassing, and rogue device deployment to evaluate facility security controls. Use when conducting authorized physical penetration testing using tailgating, badge cloning, lock.
  `physical-security` `red-team` `tailgating` `badge-cloning` `lock-picking`

- [performing-plc-firmware-security-analysis](../cybersecurity/performing-plc-firmware-security-analysis/) — This skill covers analyzing Programmable Logic Controller (PLC) firmware for security vulnerabilities including hardcoded credentials, insecure update mechanisms, backdoor functions, memory corruption flaws, and undocumented debug interfaces. It addresses firmware extraction from common PLC platforms (Siemens S7, Allen-Bradley, Schneider Modicon), static analysis of firmware images, dynamic analysis in emulated environments, and comparison against known-good baselines to detect tampering.
  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [performing-post-quantum-cryptography-migration](../cybersecurity/performing-post-quantum-cryptography-migration/) — Assesses organizational readiness for post-quantum cryptography migration per NIST FIPS 203/204/205 standards. Performs cryptographic inventory scanning to identify quantum-vulnerable algorithms (RSA, ECDH, ECDSA), evaluates hybrid TLS configurations with X25519MLKEM768, and validates CRYSTALS-Kyber (ML-KEM) and CRYSTALS-Dilithium (ML-DSA) readiness. Implements crypto-agility assessment using oqs-provider for OpenSSL. Use when working with performing post quantum cryptography migration.
  `post-quantum` `PQC` `CRYSTALS-Kyber` `ML-KEM` `ML-DSA`

- [performing-power-grid-cybersecurity-assessment](../cybersecurity/performing-power-grid-cybersecurity-assessment/) — This skill covers conducting cybersecurity assessments of electric power grid infrastructure including generation facilities, transmission substations, distribution systems, and energy management system (EMS) control centers. It addresses NERC CIP compliance verification, substation automation security, IEC 61850 protocol analysis, synchrophasor (PMU) network security, and the unique threat landscape targeting power grid operations as demonstrated by Industroyer/CrashOverride and related.
  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [performing-privacy-impact-assessment](../cybersecurity/performing-privacy-impact-assessment/) — Automates the Privacy Impact Assessment (PIA) workflow including data flow mapping, privacy risk scoring matrices, GDPR Article 35 DPIA and CCPA/CPRA alignment checks, data inventory cataloging, and remediation tracking. Implements the NIST Privacy Framework PRAM methodology and ICO DPIA guidance for systematic identification and mitigation of privacy risks across processing activities.
  `privacy` `impact-assessment` `GDPR` `CCPA` `NIST`

- [performing-privilege-escalation-assessment](../cybersecurity/performing-privilege-escalation-assessment/) — Performs privilege escalation assessments on compromised Linux and Windows systems to identify paths from low-privilege access to root or SYSTEM-level control. The tester enumerates misconfigurations, vulnerable services, kernel exploits, SUID binaries, unquoted service paths, and credential stores to demonstrate the full impact of an initial compromise. Use when working with performing privilege escalation assessment.
  `privilege-escalation` `post-exploitation` `Linux-privesc` `Windows-privesc` `local-exploitation`

- [performing-privilege-escalation-on-linux](../cybersecurity/performing-privilege-escalation-on-linux/) — Linux privilege escalation involves elevating from a low-privilege user account to root access on a compromised system. Red teams exploit misconfigurations, vulnerable services, kernel exploits, and w. Use when working with performing privilege escalation on linux.
  `red-team` `adversary-simulation` `mitre-attack` `exploitation` `post-exploitation`

- [performing-privileged-account-access-review](../cybersecurity/performing-privileged-account-access-review/) — Conduct systematic reviews of privileged accounts to validate access rights, identify excessive permissions, and enforce least privilege across PAM infrastructure. Use when conducting systematic reviews of privileged accounts to validate access rights,.
  `pam` `access-review` `privileged-accounts` `least-privilege` `compliance`

- [performing-privileged-account-discovery](../cybersecurity/performing-privileged-account-discovery/) — Discover and inventory all privileged accounts across enterprise infrastructure including domain admins, local admins, service accounts, database admins, cloud IAM roles, and application admin account. Use when working with performing privileged account discovery.
  `iam` `identity` `access-control` `privileged-access` `discovery`

- [performing-purple-team-atomic-testing](../cybersecurity/performing-purple-team-atomic-testing/) — Executes Atomic Red Team tests mapped to MITRE ATT&CK techniques, performs coverage gap analysis across the ATT&CK matrix, and runs detection validation loops to measure blue team visibility. Covers Invoke-AtomicRedTeam PowerShell execution, ATT&CK Navigator layer generation for heatmaps, Sigma rule correlation, and continuous atomic testing pipelines.
  `purple-team` `atomic-red-team` `mitre-attack` `detection-engineering` `adversary-emulation`

- [performing-purple-team-exercise](../cybersecurity/performing-purple-team-exercise/) — Performs purple team exercises by coordinating red team adversary emulation with blue team detection validation using MITRE ATT&CK-mapped attack scenarios, real-time detection testing, and collaborative gap remediation. Use when SOC teams need to validate detection capabilities, improve analyst skills, and close detection gaps through structured offensive-defensive collaboration.

  `soc` `purple-team` `red-team` `blue-team` `mitre-attack`

- [performing-ransomware-response](../cybersecurity/performing-ransomware-response/) — Use when executes a structured ransomware incident response from initial detection through containment, forensic analysis, decryption assessment, recovery, and post-incident hardening. Addresses ransom negotiation considerations, backup integrity verification, and regulatory notification requirements. Activates for requests involving ransomware response, ransomware recovery, crypto-ransomware, data encryption attack, ransom payment decision, or ransomware containment.
'.
  `ransomware` `encryption-recovery` `backup-restoration` `ransom-negotiation` `CISA-guidance`

- [performing-ransomware-tabletop-exercise](../cybersecurity/performing-ransomware-tabletop-exercise/) — Plans and facilitates tabletop exercises simulating ransomware incidents to test organizational readiness, decision-making, and communication procedures. Designs realistic scenarios based on current ransomware threat actors (LockBit, ALPHV/BlackCat, Cl0p), injects covering double extortion, backup destruction, and regulatory notification requirements. Evaluates participant responses against NIST CSF and CISA guidelines. Use when working with performing ransomware tabletop exercise.
  `ransomware` `incident-response` `tabletop-exercise` `defense` `preparedness`

- [performing-red-team-phishing-with-gophish](../cybersecurity/performing-red-team-phishing-with-gophish/) — Automate GoPhish phishing simulation campaigns using the Python gophish library. Creates email templates with tracking pixels, configures SMTP sending profiles, builds target groups from CSV, launches campaigns, and analyzes results including open rates, click rates, and credential submission statistics for security awareness assessment.
  `performing` `red` `team` `phishing`

- [performing-red-team-with-covenant](../cybersecurity/performing-red-team-with-covenant/) — Conduct red team operations using the Covenant C2 framework for authorized adversary simulation, including listener setup, grunt deployment, task execution, and lateral movement tracking. Use when conducting red team operations using the covenant c2 framework for.
  `red-team` `c2` `covenant` `adversary-simulation` `penetration-testing`

- [performing-s7comm-protocol-security-analysis](../cybersecurity/performing-s7comm-protocol-security-analysis/) — Perform security analysis of Siemens S7comm and S7CommPlus protocols used by SIMATIC S7 PLCs to identify vulnerabilities including replay attacks, integrity bypass, unauthorized CPU stop commands, and program download manipulation exploiting weaknesses in S7-300, S7-400, S7-1200, and S7-1500 controllers. . Use when working with performing s7comm protocol security analysis.
  `ot-security` `ics` `s7comm` `siemens` `plc-security`

- [performing-sca-dependency-scanning-with-snyk](../cybersecurity/performing-sca-dependency-scanning-with-snyk/) — This skill covers implementing Software Composition Analysis (SCA) using Snyk to detect vulnerable open-source dependencies in CI/CD pipelines. It addresses scanning package manifests and lockfiles, automated fix pull request generation, license compliance checking, continuous monitoring of deployed applications, and integration with GitHub, GitLab, and Jenkins pipelines.

  `devsecops` `cicd` `sca` `snyk` `dependency-scanning`

- [performing-scada-hmi-security-assessment](../cybersecurity/performing-scada-hmi-security-assessment/) — Perform security assessments of SCADA Human-Machine Interface (HMI) systems to identify vulnerabilities in web-based HMIs, thin-client configurations, authentication mechanisms, and communication channels between HMI and PLCs, aligned with IEC 62443 and NIST SP 800-82 guidelines. . Use when working with performing scada hmi security assessment.
  `ot-security` `ics` `scada` `hmi` `security-assessment`

- [performing-second-order-sql-injection](../cybersecurity/performing-second-order-sql-injection/) — Detect and exploit second-order SQL injection vulnerabilities where malicious input is stored in a database and later executed in an unsafe SQL query during a different application operation. Use when detecting and exploit second-order sql injection vulnerabilities where malicious input.
  `second-order-sqli` `stored-sql-injection` `sql-injection` `database-security` `web-security`

- [performing-security-headers-audit](../cybersecurity/performing-security-headers-audit/) — Auditing HTTP security headers including CSP, HSTS, X-Frame-Options, and cookie attributes to identify missing or misconfigured browser-level protections. Use when working with performing security headers audit.
  `penetration-testing` `security-headers` `csp` `hsts` `owasp`

- [performing-serverless-function-security-review](../cybersecurity/performing-serverless-function-security-review/) — Performing security reviews of serverless functions across AWS Lambda, Azure Functions, and GCP Cloud Functions to identify overly permissive execution roles, insecure environment variables, injection vulnerabilities, and missing runtime protections. . Use when working with performing serverless function security review.
  `cloud-security` `serverless` `lambda` `azure-functions` `cloud-functions`

- [performing-service-account-audit](../cybersecurity/performing-service-account-audit/) — Audit service accounts across enterprise infrastructure to identify orphaned, over-privileged, and non-compliant accounts. This skill covers discovery of service accounts in Active Directory, cloud pl
  `iam` `identity` `access-control` `service-accounts` `audit`

- [performing-service-account-credential-rotation](../cybersecurity/performing-service-account-credential-rotation/) — Automate credential rotation for service accounts across Active Directory, cloud platforms, and application databases to eliminate stale secrets and reduce compromise risk.
  `service-accounts` `credential-rotation` `secrets-management` `pam` `automation`

- [performing-soap-web-service-security-testing](../cybersecurity/performing-soap-web-service-security-testing/) — Perform security testing of SOAP web services by analyzing WSDL definitions and testing for XML injection, XXE, WS-Security bypass, and SOAPAction spoofing. Use when performing security testing of soap web services by analyzing wsdl.
  `soap` `web-services` `wsdl` `xml-injection` `xxe`

- [performing-soc-tabletop-exercise](../cybersecurity/performing-soc-tabletop-exercise/) — Performs tabletop exercises for SOC teams simulating security incidents through discussion-based scenarios to test incident response procedures, communication workflows, and decision-making under pressure without impacting production systems. Use when organizations need to validate IR playbooks, train analysts, or meet compliance requirements for incident response testing.

  `soc` `tabletop` `exercise` `incident-response` `training`

- [performing-soc2-type2-audit-preparation](../cybersecurity/performing-soc2-type2-audit-preparation/) — Automates SOC 2 Type II audit preparation including gap assessment against AICPA Trust Services Criteria (CC1-CC9), evidence collection from cloud providers and identity systems, control testing validation, remediation tracking, and continuous compliance monitoring. Covers all five TSC categories (Security, Availability, Processing Integrity, Confidentiality, Privacy) with automated evidence gathering from AWS, Azure, GCP, Okta, GitHub, and Jira.
  `performing` `soc2` `type2` `audit` `preparation`

- [performing-sqlite-database-forensics](../cybersecurity/performing-sqlite-database-forensics/) — Perform forensic analysis of SQLite databases to recover deleted records from freelists and WAL files, decode encoded timestamps, and extract evidence from browser history, messaging apps, and mobile device databases. Use when performing forensic analysis of sqlite databases to recover deleted records.
  `sqlite` `database-forensics` `freelist` `wal` `write-ahead-log`

- [performing-ssl-certificate-lifecycle-management](../cybersecurity/performing-ssl-certificate-lifecycle-management/) — SSL/TLS certificate lifecycle management encompasses the full process of requesting, issuing, deploying, monitoring, renewing, and revoking X.509 certificates. Poor certificate management is a leading. Use when working with performing ssl certificate lifecycle management.
  `cryptography` `ssl` `certificates` `pki` `tls`

- [performing-ssl-stripping-attack](../cybersecurity/performing-ssl-stripping-attack/) — Simulates SSL stripping attacks using sslstrip, Bettercap, and mitmproxy in authorized environments to test HSTS enforcement, certificate validation, and HTTPS upgrade mechanisms that protect users from downgrade attacks on encrypted connections. . Use when working with performing ssl stripping attack.
  `network-security` `ssl-stripping` `https` `hsts` `tls-security`

- [performing-ssl-tls-inspection-configuration](../cybersecurity/performing-ssl-tls-inspection-configuration/) — Configure SSL/TLS inspection on network security devices to decrypt, inspect, and re-encrypt HTTPS traffic for threat detection while managing certificates, exemptions, and privacy compliance. Use when configureing ssl/tls inspection on network security devices to decrypt, inspect,.
  `ssl-inspection` `tls-decryption` `https-inspection` `certificate-management` `proxy`

- [performing-ssl-tls-security-assessment](../cybersecurity/performing-ssl-tls-security-assessment/) — Assess SSL/TLS server configurations using the sslyze Python library to evaluate cipher suites, certificate chains, protocol versions, HSTS headers, and known vulnerabilities like Heartbleed and ROBOT. Use when working with performing ssl tls security assessment.
  `network-security` `ssl` `tls` `sslyze` `certificate`

- [performing-ssrf-vulnerability-exploitation](../cybersecurity/performing-ssrf-vulnerability-exploitation/) — Test for Server-Side Request Forgery vulnerabilities by probing cloud metadata endpoints, internal network services, and protocol handlers through user-controllable URL parameters. Tests AWS/GCP/Azure metadata APIs (169.254.169.254), internal port scanning via HTTP, URL scheme bypass techniques, and DNS rebinding detection. Use when testing for server-side request forgery vulnerabilities by probing cloud metadata.
  `performing` `ssrf` `vulnerability` `exploitation`

- [performing-static-malware-analysis-with-pe-studio](../cybersecurity/performing-static-malware-analysis-with-pe-studio/) — Use when performs static analysis of Windows PE (Portable Executable) malware samples using PEStudio to examine file headers, imports, strings, resources, and indicators without executing the binary. Identifies suspicious characteristics including packing, anti-analysis techniques, and malicious imports. Activates for requests involving static malware analysis, PE file inspection, Windows executable analysis, or pre-execution malware triage.
'.
  `malware` `static-analysis` `PE-analysis` `PEStudio` `reverse-engineering`

- [performing-steganography-detection](../cybersecurity/performing-steganography-detection/) — Detect and extract hidden data embedded in images, audio, and other media files using steganalysis tools to uncover covert communication channels. Use when detecting and extract hidden data embedded in images, audio, and.
  `forensics` `steganography` `steganalysis` `hidden-data` `covert-channels`

- [performing-subdomain-enumeration-with-subfinder](../cybersecurity/performing-subdomain-enumeration-with-subfinder/) — Enumerate subdomains of target domains using ProjectDiscovery's Subfinder passive reconnaissance tool to map the attack surface during security assessments. Use when working with performing subdomain enumeration with subfinder.
  `subdomain-enumeration` `reconnaissance` `bug-bounty` `attack-surface` `subfinder`

- [performing-supply-chain-attack-simulation](../cybersecurity/performing-supply-chain-attack-simulation/) — Simulate and detect software supply chain attacks including typosquatting detection via Levenshtein distance, dependency confusion testing against private registries, package hash verification with pip, and known vulnerability scanning with pip-audit. Use when working with performing supply chain attack simulation.
  `supply-chain` `typosquatting` `dependency-confusion` `package-verification` `pip-audit`

- [performing-thick-client-application-penetration-test](../cybersecurity/performing-thick-client-application-penetration-test/) — Conduct a thick client application penetration test to identify insecure local storage, hardcoded credentials, DLL hijacking, memory manipulation, and insecure API communication in desktop applications using dnSpy, Procmon, and Burp Suite. Use when conducting a thick client application penetration test to identify insecure.
  `thick-client` `desktop-application` `dnSpy` `Procmon` `DLL-hijacking`

- [performing-threat-emulation-with-atomic-red-team](../cybersecurity/performing-threat-emulation-with-atomic-red-team/) — Executes Atomic Red Team tests for MITRE ATT&CK technique validation using the atomic-operator Python framework. Loads test definitions from YAML atomics, runs attack simulations, and validates detection coverage. Use when testing SIEM detection rules, validating EDR coverage, or conducting purple team exercises.

  `performing` `threat` `emulation` `with`

- [performing-threat-hunting-with-elastic-siem](../cybersecurity/performing-threat-hunting-with-elastic-siem/) — Performs proactive threat hunting in Elastic Security SIEM using KQL/EQL queries, detection rules, and Timeline investigation to identify threats that evade automated detection. Use when SOC teams need to hunt for specific ATT&CK techniques, investigate anomalous behaviors, or validate detection coverage gaps using Elasticsearch and Kibana Security.

  `soc` `elastic` `siem` `threat-hunting` `kql`

- [performing-threat-hunting-with-yara-rules](../cybersecurity/performing-threat-hunting-with-yara-rules/) — Use YARA pattern-matching rules to hunt for malware, suspicious files, and indicators of compromise across filesystems and memory dumps. Covers rule authoring, yara-python scanning, and integration with threat intel feeds.

  `yara` `malware-detection` `threat-hunting` `pattern-matching`

- [performing-threat-intelligence-sharing-with-misp](../cybersecurity/performing-threat-intelligence-sharing-with-misp/) — Use PyMISP to create, enrich, and share threat intelligence events on a MISP platform, including IOC management, feed integration, STIX export, and community sharing workflows. Use when working with performing threat intelligence sharing with misp.
  `misp` `pymisp` `threat-intelligence` `ioc-sharing` `stix`

- [performing-threat-landscape-assessment-for-sector](../cybersecurity/performing-threat-landscape-assessment-for-sector/) — Conduct a sector-specific threat landscape assessment by analyzing threat actor targeting patterns, common attack vectors, and industry-specific vulnerabilities to inform organizational risk management. Use when conducting a sector-specific threat landscape assessment by analyzing threat actor.
  `threat-landscape` `sector-analysis` `risk-assessment` `threat-intelligence` `industry-targeting`

- [performing-threat-modeling-with-owasp-threat-dragon](../cybersecurity/performing-threat-modeling-with-owasp-threat-dragon/) — Use OWASP Threat Dragon to create data flow diagrams, identify threats using STRIDE and LINDDUN methodologies, and generate threat model reports for secure design review.
  `threat-modeling` `owasp` `threat-dragon` `stride` `linddun`

- [performing-timeline-reconstruction-with-plaso](../cybersecurity/performing-timeline-reconstruction-with-plaso/) — Build comprehensive forensic super-timelines using Plaso (log2timeline) to correlate events across file systems, logs, and artifacts into a unified chronological view. Use when building comprehensive forensic super-timelines using plaso (log2timeline) to correlate events.
  `forensics` `timeline-analysis` `plaso` `log2timeline` `super-timeline`

- [performing-user-behavior-analytics](../cybersecurity/performing-user-behavior-analytics/) — Performs User and Entity Behavior Analytics (UEBA) to detect anomalous user activities including impossible travel, unusual access patterns, privilege abuse, and insider threats using SIEM-based behavioral baselines and statistical analysis. Use when SOC teams need to identify compromised accounts or insider threats through deviation from established behavioral norms.

  `soc` `ueba` `user-behavior` `insider-threat` `anomaly-detection`

- [performing-vlan-hopping-attack](../cybersecurity/performing-vlan-hopping-attack/) — Simulates VLAN hopping attacks using switch spoofing and double tagging techniques in authorized environments to test VLAN segmentation effectiveness and validate switch port security configurations against Layer 2 bypass attacks. . Use when working with performing vlan hopping attack.
  `network-security` `vlan-hopping` `layer2-attack` `switch-security` `802.1q`

- [performing-vulnerability-scanning-with-nessus](../cybersecurity/performing-vulnerability-scanning-with-nessus/) — Performs authenticated and unauthenticated vulnerability scanning using Tenable Nessus to identify known vulnerabilities, misconfigurations, default credentials, and missing patches across network infrastructure, servers, and applications. The scanner correlates findings with CVE databases and CVSS scores to produce prioritized remediation guidance. Activates for requests involving vulnerability scanning, Nessus assessment, patch compliance checking, or automated vulnerability detection.
  `vulnerability-scanning` `Nessus` `CVE` `patch-management` `Tenable`

- [performing-web-application-firewall-bypass](../cybersecurity/performing-web-application-firewall-bypass/) — Bypass Web Application Firewall protections using encoding techniques, HTTP method manipulation, parameter pollution, and payload obfuscation to deliver SQL injection, XSS, and other attack payloads past WAF detection rules. Use when working with performing web application firewall bypass.
  `waf-bypass` `waf-evasion` `sql-injection` `xss` `payload-obfuscation`

- [performing-web-application-penetration-test](../cybersecurity/performing-web-application-penetration-test/) — Performs systematic security testing of web applications following the OWASP Web Security Testing Guide (WSTG) methodology to identify vulnerabilities in authentication, authorization, input validation, session management, and business logic. The tester uses Burp Suite as the primary interception proxy alongside manual testing techniques to find flaws that automated scanners miss.
  `web-application-pentest` `OWASP` `Burp-Suite` `WSTG` `application-security`

- [performing-web-application-scanning-with-nikto](../cybersecurity/performing-web-application-scanning-with-nikto/) — Nikto is an open-source web server and web application scanner that tests against over 7,000 potentially dangerous files/programs, checks for outdated versions of over 1,250 servers, and identifies ve. Use when working with performing web application scanning with nikto.
  `vulnerability-management` `cve` `nikto` `web-scanning` `owasp`

- [performing-web-application-vulnerability-triage](../cybersecurity/performing-web-application-vulnerability-triage/) — Triage web application vulnerability findings from DAST/SAST scanners using OWASP risk rating methodology to separate true positives from false positives and prioritize remediation. Use when working with performing web application vulnerability triage.
  `web-application` `vulnerability-triage` `owasp` `dast` `sast`

- [performing-web-cache-deception-attack](../cybersecurity/performing-web-cache-deception-attack/) — Execute web cache deception attacks by exploiting path normalization discrepancies between CDN caching layers and origin servers to cache and retrieve sensitive authenticated content. Use when working with performing web cache deception attack.
  `web-cache-deception` `cdn-attack` `cache-poisoning` `path-normalization` `cloudflare`

- [performing-web-cache-poisoning-attack](../cybersecurity/performing-web-cache-poisoning-attack/) — Exploiting web cache mechanisms to serve malicious content to other users by poisoning cached responses through unkeyed headers and parameters during authorized security tests. Use when working with performing web cache poisoning attack.
  `penetration-testing` `cache-poisoning` `web-security` `cdn` `burpsuite`

- [performing-wifi-password-cracking-with-aircrack](../cybersecurity/performing-wifi-password-cracking-with-aircrack/) — Captures WPA/WPA2 handshakes and performs offline password cracking using aircrack-ng, hashcat, and dictionary attacks during authorized wireless security assessments to evaluate passphrase strength and wireless network security posture. . Use when working with performing wifi password cracking with aircrack.
  `network-security` `wifi` `aircrack-ng` `wpa2` `wireless-security`

- [performing-windows-artifact-analysis-with-eric-zimmerman-tools](../cybersecurity/performing-windows-artifact-analysis-with-eric-zimmerman-tools/) — Perform comprehensive Windows forensic artifact analysis using Eric Zimmerman's open-source EZ Tools suite including KAPE, MFTECmd, PECmd, LECmd, JLECmd, and Timeline Explorer for parsing registry hives, prefetch files, event logs, and file system metadata. Use when performing comprehensive windows forensic artifact analysis using eric zimmerman's open-source.
  `eric-zimmerman` `ez-tools` `kape` `mftecmd` `pecmd`

- [performing-wireless-network-penetration-test](../cybersecurity/performing-wireless-network-penetration-test/) — Execute a wireless network penetration test to assess WiFi security by capturing handshakes, cracking WPA2/WPA3 keys, detecting rogue access points, and testing wireless segmentation using Aircrack-ng and related tools. Use when working with performing wireless network penetration test.
  `wireless-pentest` `WiFi` `Aircrack-ng` `WPA2` `WPA3`

- [performing-wireless-security-assessment-with-kismet](../cybersecurity/performing-wireless-security-assessment-with-kismet/) — Conduct wireless network security assessments using Kismet to detect rogue access points, hidden SSIDs, weak encryption, and unauthorized clients through passive RF monitoring. Use when conducting wireless network security assessments using kismet to detect rogue.
  `kismet` `wireless-security` `wifi-assessment` `rogue-ap` `802.11`

- [performing-yara-rule-development-for-detection](../cybersecurity/performing-yara-rule-development-for-detection/) — Develop precise YARA rules for malware detection by identifying unique byte patterns, strings, and behavioral indicators in executable files while minimizing false positives. Use when developing precise yara rules for malware detection by identifying unique.
  `yara` `malware-detection` `signature-development` `threat-hunting` `pattern-matching`

- [prioritizing-vulnerabilities-with-cvss-scoring](../cybersecurity/prioritizing-vulnerabilities-with-cvss-scoring/) — The Common Vulnerability Scoring System (CVSS) is the industry standard framework maintained by FIRST (Forum of Incident Response and Security Teams) for assessing vulnerability severity. CVSS v4.0 (r. Use when working with prioritizing vulnerabilities with cvss scoring.
  `vulnerability-management` `cve` `cvss` `risk` `prioritization`

- [processing-stix-taxii-feeds](../cybersecurity/processing-stix-taxii-feeds/) — Processes STIX 2.1 threat intelligence bundles delivered via TAXII 2.1 servers, normalizing objects into platform-native schemas and routing them to appropriate consuming systems. Use when onboarding new TAXII collection endpoints, automating bi-directional intelligence sharing with ISACs, or building pipeline validation for malformed STIX bundles. Activates for requests involving OASIS STIX, TAXII server configuration, MISP TAXII, or Cortex XSOAR feed integrations.

  `STIX-2.1` `TAXII-2.1` `OASIS` `MISP` `CTI`

- [profiling-threat-actor-groups](../cybersecurity/profiling-threat-actor-groups/) — Develops comprehensive threat actor profiles for APT groups, criminal organizations, and hacktivist collectives by aggregating TTP documentation, historical campaign data, tooling fingerprints, and attribution indicators from multiple intelligence sources. Use when briefing executives on sector-specific threats, updating threat model assumptions, or prioritizing defensive controls against specific adversaries.
  `MITRE-ATT&CK` `threat-actor` `APT` `CrowdStrike` `Mandiant`

- [program-player](../cybersecurity/program-player/) — Get invited to private bug bounty programs and build reputation on platforms. Use when building platform reputation, applying to private programs, or optimizing your hunter profile for maximum opportunities.
  `cybersecurity` `player` `program` `security` `threat-defense`

- [recon-automation](../cybersecurity/recon-automation/) — Automated reconnaissance and attack surface mapping. Use when mapping a target's infrastructure, discovering subdomains, or enumerating attack surface before security testing.
  `cybersecurity` `recon` `security` `testing` `threat-defense`

- [recovering-deleted-files-with-photorec](../cybersecurity/recovering-deleted-files-with-photorec/) — Recover deleted files from disk images and storage media using PhotoRec's file signature-based carving engine regardless of file system damage. Use when working with recovering deleted files with photorec.
  `forensics` `file-recovery` `photorec` `file-carving` `data-recovery`

- [recovering-from-ransomware-attack](../cybersecurity/recovering-from-ransomware-attack/) — Executes structured recovery from a ransomware incident following NIST and CISA frameworks, including environment isolation, forensic evidence preservation, clean infrastructure rebuild, prioritized system restoration from verified backups, credential reset, and validation against re-infection. Covers Active Directory recovery, database restoration, and application stack rebuild in dependency order.
  `ransomware` `recovery` `incident-response` `backup` `defense`

- [remediating-s3-bucket-misconfiguration](../cybersecurity/remediating-s3-bucket-misconfiguration/) — This skill provides step-by-step procedures for identifying and remediating Amazon S3 bucket misconfigurations that expose sensitive data to unauthorized access. It covers enabling S3 Block Public Access at account and bucket levels, auditing bucket policies and ACLs, enforcing encryption, configuring access logging, and deploying automated remediation using AWS Config and Lambda.

  `s3-security` `bucket-misconfiguration` `data-exposure` `public-access-block` `aws-config`

- [report-generator](../cybersecurity/report-generator/) — Generate professional security vulnerability reports for bug bounty platforms. Use when documenting security findings, preparing bug bounty submissions, or creating assessment reports.
  `cybersecurity` `generator` `report` `security` `threat-defense`

- [reverse-engineering-android-malware-with-jadx](../cybersecurity/reverse-engineering-android-malware-with-jadx/) — Use when reverse engineers malicious Android APK files using JADX decompiler to analyze Java/Kotlin source code, identify malicious functionality including data theft, C2 communication, privilege escalation, and overlay attacks. Examines manifest permissions, receivers, services, and native libraries. Activates for requests involving Android malware analysis, APK reverse engineering, mobile malware investigation, or Android threat analysis.
'.
  `malware` `Android` `reverse-engineering` `JADX` `mobile-malware`

- [reverse-engineering-dotnet-malware-with-dnspy](../cybersecurity/reverse-engineering-dotnet-malware-with-dnspy/) — Reverse engineers .NET malware using dnSpy decompiler and debugger to analyze C#/VB.NET source code, identify obfuscation techniques, extract configurations, and understand malicious functionality including stealers, RATs, and loaders. Activates for requests involving .NET malware analysis, C# malware decompilation, managed code reverse engineering, or .NET obfuscation analysis. . Use when working with reverse engineering dotnet malware with dnspy.
  `malware` `dotnet` `reverse-engineering` `dnSpy` `decompilation`

- [reverse-engineering-ios-app-with-frida](../cybersecurity/reverse-engineering-ios-app-with-frida/) — Reverse engineers iOS applications using Frida dynamic instrumentation to understand internal logic, extract encryption keys, bypass security controls, and discover hidden functionality without source code access. Use when performing authorized iOS penetration testing, analyzing proprietary protocols, understanding obfuscated logic, or extracting runtime secrets from iOS binaries.
  `mobile-security` `ios` `frida` `reverse-engineering` `owasp-mobile`

- [reverse-engineering-malware-with-ghidra](../cybersecurity/reverse-engineering-malware-with-ghidra/) — Reverse engineers malware binaries using NSA's Ghidra disassembler and decompiler to understand internal logic, cryptographic routines, C2 protocols, and evasion techniques at the assembly and pseudo-C level. Activates for requests involving malware reverse engineering, disassembly analysis, decompilation, binary analysis, or understanding malware internals. . Use when working with reverse engineering malware with ghidra.
  `malware` `reverse-engineering` `Ghidra` `disassembly` `decompilation`

- [reverse-engineering-ransomware-encryption-routine](../cybersecurity/reverse-engineering-ransomware-encryption-routine/) — Reverse engineer ransomware encryption routines to identify cryptographic algorithms, key generation flaws, and potential decryption opportunities using static and dynamic analysis. Use when reverseing engineer ransomware encryption routines to identify cryptographic algorithms, key.
  `ransomware` `encryption` `reverse-engineering` `cryptanalysis` `aes`

- [reverse-engineering-rust-malware](../cybersecurity/reverse-engineering-rust-malware/) — Reverse engineer Rust-compiled malware using IDA Pro and Ghidra with techniques for handling non-null-terminated strings, crate dependency extraction, and Rust-specific control flow analysis. Use when reverseing engineer rust-compiled malware using ida pro and ghidra with.
  `rust` `reverse-engineering` `malware-analysis` `ghidra` `ida-pro`

- [saas-orchestrator](../cybersecurity/saas-orchestrator/) — Wraps the existing 23 security skills into a sellable security-as-a-Service offering — automated pentest reports, compliance checking, client management
  `compliance` `cybersecurity` `orchestrator` `penetration-testing` `saas`

- [scanning-container-images-with-grype](../cybersecurity/scanning-container-images-with-grype/) — Scan container images for known vulnerabilities using Anchore Grype with SBOM-based matching and configurable severity thresholds. Use when scaning container images for known vulnerabilities using anchore grype with.
  `grype` `vulnerability-scanning` `container-security` `sbom` `anchore`

- [scanning-containers-with-trivy-in-cicd](../cybersecurity/scanning-containers-with-trivy-in-cicd/) — This skill covers integrating Aqua Security's Trivy scanner into CI/CD pipelines for comprehensive container image vulnerability detection. It addresses scanning Docker images for OS package and application dependency CVEs, detecting misconfigurations in Dockerfiles, scanning filesystem and git repositories, and establishing severity-based quality gates that block deployment of vulnerable images.

  `devsecops` `cicd` `trivy` `container-security` `vulnerability-scanning`

- [scanning-docker-images-with-trivy](../cybersecurity/scanning-docker-images-with-trivy/) — Trivy is a comprehensive open-source vulnerability scanner by Aqua Security that detects vulnerabilities in OS packages, language-specific dependencies, misconfigurations, secrets, and license violati. Use when working with scanning docker images with trivy.
  `containers` `docker` `security` `trivy` `vulnerability-scanning`

- [scanning-infrastructure-with-nessus](../cybersecurity/scanning-infrastructure-with-nessus/) — Tenable Nessus is the industry-leading vulnerability scanner used to identify security weaknesses across network infrastructure including servers, workstations, network devices, and operating systems. Use when working with scanning infrastructure with nessus.
  `vulnerability-management` `cve` `nessus` `tenable` `infrastructure-scanning`

- [scanning-kubernetes-manifests-with-kubesec](../cybersecurity/scanning-kubernetes-manifests-with-kubesec/) — Perform security risk analysis on Kubernetes resource manifests using Kubesec to identify misconfigurations, privilege escalation risks, and deviations from security best practices. Use when performing security risk analysis on kubernetes resource manifests using kubesec.
  `kubesec` `kubernetes` `manifest-scanning` `security-scanning` `devsecops`

- [scanning-network-with-nmap-advanced](../cybersecurity/scanning-network-with-nmap-advanced/) — Performs advanced network reconnaissance using Nmap's scripting engine, timing controls, evasion techniques, and output parsing to discover hosts, enumerate services, detect vulnerabilities, and fingerprint operating systems across authorized target networks. . Use when working with scanning network with nmap advanced.
  `network-security` `nmap` `port-scanning` `service-enumeration` `reconnaissance`

- [securing-api-gateway-with-aws-waf](../cybersecurity/securing-api-gateway-with-aws-waf/) — Securing API Gateway endpoints with AWS WAF by configuring managed rule groups for OWASP Top 10 protection, creating custom rate limiting rules, implementing bot control, setting up IP reputation filtering, and monitoring WAF metrics for security effectiveness. . Use when working with securing api gateway with aws waf.
  `cloud-security` `aws` `waf` `api-gateway` `rate-limiting`

- [securing-aws-iam-permissions](../cybersecurity/securing-aws-iam-permissions/) — This skill guides practitioners through hardening AWS Identity and Access Management configurations to enforce least privilege access across cloud accounts. It covers IAM policy scoping, permission boundaries, Access Analyzer integration, and credential rotation strategies to reduce the blast radius of compromised identities.

  `aws-iam` `least-privilege` `permission-boundaries` `access-analyzer` `cloud-identity`

- [securing-aws-lambda-execution-roles](../cybersecurity/securing-aws-lambda-execution-roles/) — Securing AWS Lambda execution roles by implementing least-privilege IAM policies, applying permission boundaries, restricting resource-based policies, using IAM Access Analyzer to validate permissions, and enforcing role scoping through SCPs. . Use when working with securing aws lambda execution roles.
  `cloud-security` `aws` `lambda` `iam` `least-privilege`

- [securing-azure-with-microsoft-defender](../cybersecurity/securing-azure-with-microsoft-defender/) — This skill instructs security practitioners on deploying Microsoft Defender for Cloud as a cloud-native application protection platform for Azure, multi-cloud, and hybrid environments. It covers enabling Defender plans for servers, containers, storage, and databases, configuring security recommendations, managing Secure Score, and integrating with the unified Defender portal for centralized threat management.

  `microsoft-defender` `azure-security` `cnapp` `secure-score` `cloud-workload-protection`

- [securing-container-registry-images](../cybersecurity/securing-container-registry-images/) — Securing container registry images by implementing vulnerability scanning with Trivy and Grype, enforcing image signing with Cosign and Sigstore, configuring registry access controls, and building CI/CD pipelines that prevent deploying unscanned or unsigned images. . Use when working with securing container registry images.
  `cloud-security` `containers` `registry` `image-scanning` `trivy`

- [securing-container-registry-with-harbor](../cybersecurity/securing-container-registry-with-harbor/) — Harbor is an open-source container registry that provides security features including vulnerability scanning (integrated Trivy), image signing (Notary/Cosign), RBAC, content trust policies, replicatio. Use when working with securing container registry with harbor.
  `containers` `kubernetes` `docker` `security` `registry`

- [securing-github-actions-workflows](../cybersecurity/securing-github-actions-workflows/) — This skill covers hardening GitHub Actions workflows against supply chain attacks, credential theft, and privilege escalation. It addresses pinning actions to SHA digests, minimizing GITHUB_TOKEN permissions, protecting secrets from exfiltration, preventing script injection in workflow expressions, and implementing required reviewers for workflow changes.

  `devsecops` `cicd` `github-actions` `supply-chain` `workflow-security`

- [securing-helm-chart-deployments](../cybersecurity/securing-helm-chart-deployments/) — Secure Helm chart deployments by validating chart integrity, scanning templates for misconfigurations, and enforcing security contexts in Kubernetes releases. Use when working with securing helm chart deployments.
  `helm` `kubernetes` `chart-security` `supply-chain` `configuration-security`

- [securing-historian-server-in-ot-environment](../cybersecurity/securing-historian-server-in-ot-environment/) — This skill covers hardening and securing process historian servers (OSIsoft PI, Honeywell PHD, GE Proficy, AVEVA Historian) in OT environments. It addresses network placement across Purdue levels, access control for historian interfaces, data replication through DMZ using data diodes or PI-to-PI connectors, SQL injection prevention in historian queries, and integrity protection of process data used for safety analysis, regulatory reporting, and process optimization.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [securing-kubernetes-on-cloud](../cybersecurity/securing-kubernetes-on-cloud/) — This skill covers hardening managed Kubernetes clusters on EKS, AKS, and GKE by implementing Pod Security Standards, network policies, workload identity, RBAC scoping, image admission controls, and runtime security monitoring. It addresses cloud-specific security features including IRSA for EKS, Workload Identity for GKE, and Managed Identities for AKS.

  `kubernetes-security` `eks` `aks` `gke` `pod-security-standards`

- [securing-remote-access-to-ot-environment](../cybersecurity/securing-remote-access-to-ot-environment/) — This skill covers implementing secure remote access to OT/ICS environments for operators, engineers, and vendors while preventing unauthorized access that could compromise industrial operations. It addresses jump server architecture, multi-factor authentication, session recording, privileged access management, vendor remote access controls, and compliance with IEC 62443 and NERC CIP-005 remote access requirements.

  `ot-security` `ics` `scada` `industrial-control` `iec62443`

- [securing-serverless-functions](../cybersecurity/securing-serverless-functions/) — This skill covers security hardening for serverless compute platforms including AWS Lambda, Azure Functions, and Google Cloud Functions. It addresses least privilege IAM roles, dependency vulnerability scanning, secrets management integration, input validation, function URL authentication, and runtime monitoring to protect against injection attacks, credential theft, and supply chain compromises.

  `serverless-security` `aws-lambda` `azure-functions` `function-hardening` `supply-chain`

- [security-agent-hardening](../cybersecurity/security-agent-hardening/) — Secure AI agents against prompt injection, jailbreaking, data exfiltration, and supply chain attacks. Implement guardrails, sandboxing, and monitoring for safe autonomous operation. Use when working with security agent hardening.
  `agent-security` `prompt-injection` `guardrails` `sandboxing` `llm-security`

- [smart-contract-exploiter](../cybersecurity/smart-contract-exploiter/) — Automated smart contract vulnerability scanning and exploit development for bug bounty. Use when auditing Solidity/Vyper contracts, building PoC exploits for DeFi protocols, hunting on.
  `smart-contract` `solidity` `vyper` `defi` `exploit`

- [social-engineer](../cybersecurity/social-engineer/) — Social engineering and phishing for authorized security assessments. Use when testing human attack vectors, conducting phishing simulations, or assessing organizational security awareness.
  `cybersecurity` `engineer` `security` `social` `social-media`

- [supply-chain-attacker](../cybersecurity/supply-chain-attacker/) — Software supply chain attack testing — dependency confusion, typosquatting, malicious packages, CI/CD pipeline exploitation. Use when assessing supply chain security, testing package managers, or finding supply chain vulnerabilities.
  `attacker` `chain` `cicd` `cybersecurity` `dependency`

- [testing-android-intents-for-vulnerabilities](../cybersecurity/testing-android-intents-for-vulnerabilities/) — Tests Android inter-process communication (IPC) through intents for vulnerabilities including intent injection, unauthorized component access, broadcast sniffing, pending intent hijacking, and content provider data leakage. Use when assessing Android app attack surface through exported components, testing intent-based data flows, or evaluating IPC security. Activates for requests involving Android intent security, IPC testing, exported component analysis, or Drozer assessment.

  `mobile-security` `android` `intents` `ipc-security` `owasp-mobile`

- [testing-api-authentication-weaknesses](../cybersecurity/testing-api-authentication-weaknesses/) — Tests API authentication mechanisms for weaknesses including broken token validation, missing authentication on endpoints, weak password policies, credential stuffing susceptibility, token leakage in URLs or logs, and session management flaws. The tester evaluates JWT implementation, API key handling, OAuth flows, and session token entropy to identify authentication bypasses. Maps to OWASP API2:2023 Broken Authentication. Use when working with testing api authentication weaknesses.
  `api-security` `owasp` `authentication` `jwt` `session-management`

- [testing-api-for-broken-object-level-authorization](../cybersecurity/testing-api-for-broken-object-level-authorization/) — Use when tests REST and GraphQL APIs for Broken Object Level Authorization (BOLA/IDOR) vulnerabilities where an authenticated user can access or modify resources belonging to other users by manipulating object identifiers in API requests. The tester intercepts API calls, identifies object ID parameters (numeric IDs, UUIDs, slugs), and systematically replaces them with IDs belonging to other users to determine if the server enforces per-object authorization.
  `api-security` `owasp` `bola` `idor` `authorization`

- [testing-api-for-mass-assignment-vulnerability](../cybersecurity/testing-api-for-mass-assignment-vulnerability/) — Use when tests APIs for mass assignment (auto-binding) vulnerabilities where clients can modify object properties they should not have access to by including additional parameters in API requests. The tester identifies writable endpoints, adds undocumented fields to request bodies (role, isAdmin, price, balance), and checks if the server binds these to the data model without filtering. Part of OWASP API3:2023 Broken Object Property Level Authorization.
  `api-security` `owasp` `mass-assignment` `auto-binding` `parameter-tampering`

- [testing-api-security-with-owasp-top-10](../cybersecurity/testing-api-security-with-owasp-top-10/) — Systematically assessing REST and GraphQL API endpoints against the OWASP API Security Top 10 risks using automated and manual testing techniques.
  `penetration-testing` `api-security` `owasp` `rest-api` `graphql`

- [testing-cors-misconfiguration](../cybersecurity/testing-cors-misconfiguration/) — Identifying and exploiting Cross-Origin Resource Sharing misconfigurations that allow unauthorized cross-domain data access and credential theft during security assessments. Use when working with testing cors misconfiguration.
  `penetration-testing` `cors` `web-security` `owasp` `same-origin-policy`

- [testing-for-broken-access-control](../cybersecurity/testing-for-broken-access-control/) — Systematically testing web applications for broken access control vulnerabilities including privilege escalation, missing function-level checks, and insecure direct object references. Use when working with testing for broken access control.
  `penetration-testing` `access-control` `authorization` `owasp` `privilege-escalation`

- [testing-for-business-logic-vulnerabilities](../cybersecurity/testing-for-business-logic-vulnerabilities/) — Identifying flaws in application business logic that allow price manipulation, workflow bypass, and privilege escalation beyond what technical vulnerability scanners can detect. Use when working with testing for business logic vulnerabilities.
  `penetration-testing` `business-logic` `owasp` `web-security` `burpsuite`

- [testing-for-email-header-injection](../cybersecurity/testing-for-email-header-injection/) — Test web application email functionality for SMTP header injection vulnerabilities that allow attackers to inject additional email headers, modify recipients, and abuse contact forms for spam relay. Use when testing web application email functionality for smtp header injection vulnerabilities.
  `email-injection` `smtp-injection` `crlf-injection` `header-injection` `spam-relay`

- [testing-for-host-header-injection](../cybersecurity/testing-for-host-header-injection/) — Test web applications for HTTP Host header injection vulnerabilities to identify password reset poisoning, web cache poisoning, SSRF, and virtual host routing manipulation risks. Use when testing web applications for http host header injection vulnerabilities to.
  `host-header-injection` `password-reset-poisoning` `cache-poisoning` `virtual-host` `web-security`

- [testing-for-json-web-token-vulnerabilities](../cybersecurity/testing-for-json-web-token-vulnerabilities/) — Test JWT implementations for critical vulnerabilities including algorithm confusion, none algorithm bypass, kid parameter injection, and weak secret exploitation to achieve authentication bypass and privilege escalation. Use when testing jwt implementations for critical vulnerabilities including algorithm confusion, none.
  `jwt` `json-web-token` `algorithm-confusion` `authentication-bypass` `token-forgery`

- [testing-for-open-redirect-vulnerabilities](../cybersecurity/testing-for-open-redirect-vulnerabilities/) — Identify and test open redirect vulnerabilities in web applications by analyzing URL redirection parameters, bypass techniques, and exploitation chains for phishing and token theft. Use when working with testing for open redirect vulnerabilities.
  `open-redirect` `url-redirect` `phishing` `owasp` `url-validation`

- [testing-for-sensitive-data-exposure](../cybersecurity/testing-for-sensitive-data-exposure/) — Identifying sensitive data exposure vulnerabilities including API key leakage, PII in responses, insecure storage, and unprotected data transmission during security assessments. Use when working with testing for sensitive data exposure.
  `penetration-testing` `data-exposure` `pii` `owasp` `web-security`

- [testing-for-xml-injection-vulnerabilities](../cybersecurity/testing-for-xml-injection-vulnerabilities/) — Test web applications for XML injection vulnerabilities including XXE, XPath injection, and XML entity attacks to identify data exposure and server-side request forgery risks. Use when testing web applications for xml injection vulnerabilities including xxe, xpath.
  `xml-injection` `xxe` `xpath-injection` `xml-parsing` `web-security`

- [testing-for-xss-vulnerabilities](../cybersecurity/testing-for-xss-vulnerabilities/) — Tests web applications for Cross-Site Scripting (XSS) vulnerabilities by injecting JavaScript payloads into reflected, stored, and DOM-based contexts to demonstrate client-side code execution, session hijacking, and user impersonation. The tester identifies all injection points and output contexts, crafts context-appropriate payloads, and bypasses sanitization and CSP protections. Use when working with testing for xss vulnerabilities.
  `XSS` `cross-site-scripting` `client-side-security` `OWASP-A03` `JavaScript-injection`

- [testing-for-xss-vulnerabilities-with-burpsuite](../cybersecurity/testing-for-xss-vulnerabilities-with-burpsuite/) — Identifying and validating cross-site scripting vulnerabilities using Burp Suite's scanner, intruder, and repeater tools during authorized security assessments. Use when working with testing for xss vulnerabilities with burpsuite.
  `penetration-testing` `xss` `burpsuite` `owasp` `web-security`

- [testing-for-xxe-injection-vulnerabilities](../cybersecurity/testing-for-xxe-injection-vulnerabilities/) — Discovering and exploiting XML External Entity injection vulnerabilities to read server files, perform SSRF, and exfiltrate data during authorized penetration tests. Use when working with testing for xxe injection vulnerabilities.
  `penetration-testing` `xxe` `xml-injection` `owasp` `web-security`

- [testing-jwt-token-security](../cybersecurity/testing-jwt-token-security/) — Assessing JSON Web Token implementations for cryptographic weaknesses, algorithm confusion attacks, and authorization bypass vulnerabilities during security engagements. Use when working with testing jwt token security.
  `penetration-testing` `jwt` `authentication` `web-security` `token-security`

- [testing-mobile-api-authentication](../cybersecurity/testing-mobile-api-authentication/) — Tests authentication and authorization mechanisms in mobile application APIs to identify broken authentication, insecure token management, session fixation, privilege escalation, and IDOR vulnerabilities. Use when performing API security assessments against mobile app backends, testing JWT implementations, evaluating OAuth flows, or assessing session management.
  `mobile-security` `android` `ios` `api-security` `authentication`

- [testing-oauth2-implementation-flaws](../cybersecurity/testing-oauth2-implementation-flaws/) — Tests OAuth 2.0 and OpenID Connect implementations for security flaws including authorization code interception, redirect URI manipulation, CSRF in OAuth flows, token leakage, scope escalation, and PKCE bypass. The tester evaluates the authorization server, client application, and token handling for common misconfigurations that enable account takeover or unauthorized access. Use when working with testing oauth2 implementation flaws.
  `api-security` `oauth2` `oidc` `authentication` `redirect-uri`

- [testing-ransomware-recovery-procedures](../cybersecurity/testing-ransomware-recovery-procedures/) — Test and validate ransomware recovery procedures including backup restore operations, RTO/RPO target verification, recovery sequencing, and clean restore validation to ensure organizational resilience against destructive ransomware attacks. Use when testing and validate ransomware recovery procedures including backup restore operations,.
  `incident-response` `ransomware` `disaster-recovery` `backup` `rto`

- [testing-websocket-api-security](../cybersecurity/testing-websocket-api-security/) — Use when tests WebSocket API implementations for security vulnerabilities including missing authentication on WebSocket upgrade, Cross-Site WebSocket Hijacking (CSWSH), injection attacks through WebSocket messages, insufficient input validation, denial-of-service via message flooding, and information leakage through WebSocket frames. The tester intercepts WebSocket handshakes and messages using Burp Suite, crafts malicious payloads, and tests for authorization bypass on WebSocket channels.
  `api-security` `websocket` `cswsh` `real-time` `injection`

- [token-nft-scam-investigation](../cybersecurity/token-nft-scam-investigation/) — Investigate token and NFT scams including rug pulls, honeypot tokens, pump-and-dump schemes, wash trading, and NFT floor manipulation to identify fraudulent patterns and trace perpetrator wallets. Use when analyzing suspicious token launches, investigating NFT fraud, or detecting market manipulation.
  `blockchain` `token` `nft` `scam` `investigation`

- [tracking-threat-actor-infrastructure](../cybersecurity/tracking-threat-actor-infrastructure/) — Threat actor infrastructure tracking involves monitoring and mapping adversary-controlled assets including command-and-control (C2) servers, phishing domains, exploit kit hosts, bulletproof hosting, a. Use when working with tracking threat actor infrastructure.
  `threat-intelligence` `cti` `ioc` `mitre-attack` `stix`

- [triaging-security-alerts-in-splunk](../cybersecurity/triaging-security-alerts-in-splunk/) — Triages security alerts in Splunk Enterprise Security by classifying severity, investigating notable events, correlating related telemetry, and making escalation or closure decisions using SPL queries and the Incident Review dashboard. Use when SOC analysts face queued alerts from correlation searches, need to prioritize investigation order, or must document triage decisions for handoff to Tier 2/3 analysts.

  `soc` `splunk` `alert-triage` `siem` `notable-events`

- [triaging-security-incident](../cybersecurity/triaging-security-incident/) — Performs initial triage of security incidents to determine severity, scope, and required response actions using the NIST SP 800-61r3 and SANS PICERL frameworks. Classifies incidents by type, assigns priority based on business impact, and routes to appropriate response teams. Activates for requests involving incident triage, security alert classification, severity assessment, incident prioritization, or initial incident analysis. . Use when working with triaging security incident.
  `incident-triage` `NIST-800-61` `SANS-PICERL` `severity-classification` `SOC-operations`

- [triaging-security-incident-with-ir-playbook](../cybersecurity/triaging-security-incident-with-ir-playbook/) — Classify and prioritize security incidents using structured IR playbooks to determine severity, assign response teams, and initiate appropriate response procedures. Use when working with triaging security incident with ir playbook.
  `incident-response` `triage` `playbook` `severity-classification` `soc`

- [triaging-vulnerabilities-with-ssvc-framework](../cybersecurity/triaging-vulnerabilities-with-ssvc-framework/) — Triage and prioritize vulnerabilities using CISA's Stakeholder-Specific Vulnerability Categorization (SSVC) decision tree framework to produce actionable remediation priorities. Use when working with triaging vulnerabilities with ssvc framework.
  `ssvc` `vulnerability-triage` `cisa` `vulnerability-prioritization` `decision-tree`

- [validating-backup-integrity-for-recovery](../cybersecurity/validating-backup-integrity-for-recovery/) — Validate backup integrity through cryptographic hash verification, automated restore testing, corruption detection, and recoverability checks to ensure backups are reliable for disaster recovery and ransomware response scenarios.
  `incident-response` `backup` `integrity` `hash-verification` `restore-testing`

- [vulnerability-scanner](../cybersecurity/vulnerability-scanner/) — AI-powered vulnerability scanning with intelligent payload generation. Use when scanning web applications for specific vulnerability types, generating exploit payloads, or running automated security tests.
  `cybersecurity` `scanner` `security` `threat-defense` `vulnerability`

- [wallet-address-intelligence](../cybersecurity/wallet-address-intelligence/) — Profile and cluster blockchain wallet addresses to identify entity associations, assess risk levels, and build address reputation intelligence across multiple chains. Use when analyzing wallet behavior, clustering related addresses, assessing counterparty risk, or building address intelligence reports.
  `blockchain` `wallet` `address` `intelligence` `clustering`

- [web3-auditor](../cybersecurity/web3-auditor/) — Smart contract and DeFi security auditing for maximum bounty payouts. Use when auditing Solidity/Vyper contracts, testing DeFi protocols, hunting web3 vulnerabilities, or preparing Immunefi submissions.
  `auditor` `cybersecurity` `security` `testing` `threat-defense`

- [writeup-cash](../cybersecurity/writeup-cash/) — Monetize bug bounty findings through writeups, tools, and consulting. Use when turning security research into income streams, writing paid writeups, or building a security brand.
  `cash` `cybersecurity` `money` `security` `threat-defense`

### Data (data/)

_Total: 7 skills_

Browse in [`data/_index.md`](../data/_index.md).

- [airflow-pipelines](../data/airflow-pipelines/) — Apache Airflow workflow orchestration — DAGs, operators, sensors, XComs, pools, scheduling. Use when working with airflow pipelines.
  `airflow` `analytics` `data-analysis` `pipelines` `visualization`

- [analysis](../data/analysis/) — Full-stack data analysis pipeline — clean, detect anomalies, generate reports, and create visualizations with production pandas. Turn raw data into paid deliverables.
  `analytics` `data-cleaning` `anomaly-detection` `reporting` `visualization`

- [dagster-pipelines](../data/dagster-pipelines/) — Dagster data orchestration — software-defined assets, ops, jobs, schedules, sensors, IO managers. Use when working with dagster pipelines.
  `analytics` `dagster` `data-analysis` `pipelines` `visualization`

- [dbt-transform](../data/dbt-transform/) — dbt data transformation — models, tests, macros, sources, snapshots, documentation, packages. Use when working with dbt transform.
  `analytics` `data-analysis` `dbt` `transform` `visualization`

- [prefect-flows](../data/prefect-flows/) — Prefect workflow orchestration — flows, tasks, deployments, work pools, schedules, retries. Use when working with prefect flows.
  `analytics` `data-analysis` `flows` `prefect` `visualization`

- [spark-processing](../data/spark-processing/) — Apache Spark distributed processing — DataFrames, SQL, streaming, MLlib, cluster management. Use when working with spark processing.
  `analytics` `data-analysis` `machine-learning` `processing` `spark`

- [temporal-workflows](../data/temporal-workflows/) — Temporal durable workflows — workflow/activity definitions, retries, signals, queries, versioning. Use when working with temporal workflows.
  `analytics` `data-analysis` `temporal` `visualization` `workflow`

### Development (development/)

_Total: 90 skills_

Browse in [`development/_index.md`](../development/_index.md).

- [agent-arena-skill](../development/agent-arena-skill/) — Skill: agent-arena-skill. See SKILL.md body for details. Use when this domain is relevant.
  `agent` `ai-agent` `arena` `coding` `skill`

- [agent-daily-planner](../development/agent-daily-planner/) — Generate daily plans with task priorities, track shipped work, and maintain cross-session accountability using deep work principles.
  `agent` `coding` `daily` `planner` `software-engineering`

- [agentic-quality-engineering](../development/agentic-quality-engineering/) — AI-powered quality engineering with flaky test detection, mutation testing, chaos engineering, risk-based test prioritization, and cross-project pattern learning. Use when building quality.
  `quality-engineering` `flaky-tests` `mutation-testing` `chaos-engineering` `risk-based-testing`

- [ai-saas-builder](../development/ai-saas-builder/) — Takes a problem statement and produces a deployable micro-SaaS product — landing page, auth, payments, database, API, and billing. Use when building micro-SaaS products solo.
  `api` `builder` `coding` `saas` `software-engineering`

- [ai-skill-integration-guide](../development/ai-skill-integration-guide/) — Meta-skill for integrating external GitHub skill repos into 1ai-skills. Covers discovery, deduplication, format conversion, category mapping, validation, and quality gates. Use when integrating external skill repos, bulk skill imports, skill format conversion.
  `meta` `integration` `skills` `github` `bulk-import`

- [android-jetpack](../development/android-jetpack/) — Android Jetpack Compose — declarative UI, state management, Material Design, and Play Store deployment. Use when working with android jetpack.
  `android` `coding` `jetpack` `software-engineering` `testing`

- [api-design](../development/api-design/) — REST API design — resource modeling, versioning, pagination, error handling, OpenAPI/Swagger documentation. Use when working with api design.
  `api` `coding` `design` `rest-api` `software-engineering`

- [api-gateway](../development/api-gateway/) — API gateway design — rate limiting, authentication, routing, caching, request transformation. Kong, Traefik, custom gateways. Use when working with api gateway.
  `api` `coding` `gateway` `software-engineering` `testing`

- [api-testing](../development/api-testing/) — REST and GraphQL API testing — contract testing, schema validation, and integration test automation. Use when working with api testing.
  `api` `coding` `graphql` `rest-api` `software-engineering`

- [app-store-optimization](../development/app-store-optimization/) — App Store and Play Store optimization — keywords, screenshots, reviews, and conversion rate optimization. Use when working with app store optimization.
  `app` `coding` `optimization` `software-engineering` `store`

- [appwrite-patterns](../development/appwrite-patterns/) — Appwrite backend-as-a-service — auth, database, storage, functions, realtime for web/mobile/desktop. Use when working with appwrite patterns.
  `appwrite` `coding` `patterns` `software-engineering` `testing`

- [automated-test-generator](../development/automated-test-generator/) — Generate test suites, analyze coverage, and scaffold E2E tests automatically. Use when creating tests for existing code, improving test coverage, scaffolding integration tests, or setting.
  `test-generation` `coverage-analysis` `e2e-testing` `test-automation` `quality-assurance`

- [brainstorming](../development/brainstorming/) — Effective brainstorming skill for features and projects. Clarify intent, explore options, and guide design decisions to align with user goals. Use when working with brainstorming.
  `brainstorming` `coding` `software-engineering` `testing`

- [browser-testing-devtools](../development/browser-testing-devtools/) — Test web applications using browser DevTools, Playwright, or Puppeteer. Automate E2E testing, visual regression, performance auditing, and accessibility checking.
  `testing` `browser` `devtools` `playwright` `e2e`

- [cassandra-patterns](../development/cassandra-patterns/) — Apache Cassandra patterns — data modeling, CQL, partition keys, clustering, replication, performance tuning. Use when working with cassandra patterns.
  `cassandra` `coding` `patterns` `software-engineering` `testing`

- [cherry-picked-agent-skills](../development/cherry-picked-agent-skills/) — 6 unique agent skills cherry-picked from Addy Osmani's agent-skills — interview extraction, idea refinement, adversarial review, source-driven development, context engineering, and deprecation workflows. Use when requirements gathering, idea refinement, adversarial review, documentation-driven dev, context optimization, code deprecation.
  `agent-skills` `methodology` `interview` `context-engineering` `deprecation`

- [cicd-deployment](../development/cicd-deployment/) — Build production CI/CD pipelines with GitHub Actions, Docker, zero-downtime blue/green deploys, rollback, and Telegram alerts. Use when building production ci/cd pipelines with github actions, docker, zero-downtime blue/green.
  `cicd` `coding` `deployment` `docker` `github`

- [cockroachdb-patterns](../development/cockroachdb-patterns/) — CockroachDB distributed SQL — PostgreSQL compatible, serializable isolation, geo-partitioning, multi-region. Use when working with cockroachdb patterns.
  `cockroachdb` `coding` `patterns` `software-engineering` `testing`

- [code-reviewer](../development/code-reviewer/) — Professional code review skill. Review local changes or PRs for correctness, maintainability, and best practices. Based on playbooks.com community skill. Use when working with code reviewer.
  `code` `coding` `reviewer` `software-engineering` `testing`

- [code-simplification](../development/code-simplification/) — Simplifies code for clarity. Use when code is overly complex, has unnecessary abstractions, or when refactoring for readability.
  `code` `coding` `simplification` `software-engineering` `testing`

- [content-validation-workflow](../development/content-validation-workflow/) — Validate AI-generated content quality through sample generation, human review gates, and controlled batch production workflows. Use when working with content validation workflow.
  `coding` `content` `software-engineering` `testing` `validation`

- [context-engineering](../development/context-engineering/) — Design and manage the context window for AI coding agents. Structure prompts, manage file loading, and optimize token usage for maximum agent effectiveness. Use when designing and manage the context window for ai coding agents.
  `engineering` `context` `prompts` `ai-agents` `token-optimization`

- [css-frameworks](../development/css-frameworks/) — CSS framework patterns — Tailwind CSS, Bootstrap, PostCSS, Sass, CSS Modules, CSS-in-JS. Use when working with css frameworks.
  `coding` `css` `frameworks` `software-engineering` `testing`

- [cypress-e2e](../development/cypress-e2e/) — Cypress E2E testing — component testing, API testing, fixtures, custom commands, CI integration. Use when working with cypress e2e.
  `api` `coding` `cypress` `e2e` `software-engineering`

- [daily-dev-agentic](../development/daily-dev-agentic/) — Skill: daily-dev-agentic. See SKILL.md body for details. Use when this domain is relevant.
  `agentic` `ai-agent` `coding` `daily` `dev`

- [database-migration](../development/database-migration/) — Safe database migrations — schema changes, data migrations, rollback strategies, and zero-downtime deploys. Use when working with database migration.
  `coding` `database` `migration` `software-engineering` `testing`

- [dependency-scanner](../development/dependency-scanner/) — Automated dependency auditing for npm, pip, cargo, go. Detect vulnerabilities, outdated packages, license conflicts, and supply chain risks. Generate SBOMs and compliance reports.
  `security` `dependencies` `vulnerabilities` `supply-chain` `sbom`

- [drizzle-orm](../development/drizzle-orm/) — Drizzle ORM — type-safe SQL, schema definitions, migrations, queries, relations for TypeScript/Node.js. Use when working with drizzle orm.
  `coding` `drizzle` `orm` `software-engineering` `testing`

- [dynamodb-patterns](../development/dynamodb-patterns/) — Amazon DynamoDB patterns — single table design, GSI/LSI, DynamoDB Streams, PartiQL, performance optimization. Use when working with dynamodb patterns.
  `coding` `dynamodb` `patterns` `software-engineering` `testing`

- [electron-apps](../development/electron-apps/) — Electron desktop app development — main/renderer process, IPC, native menus, auto-update, packaging. Use when working with electron apps.
  `apps` `coding` `electron` `software-engineering` `testing`

- [engineering-hard-rules](../development/engineering-hard-rules/) — Non-negotiable engineering protocol for AI agents. Enforces READ→THINK→DECIDE→PLAN→BUILD→VERIFY→DOCS→REVIEW loop. Use when any code change requires evidence-first execution, blast radius.
  `engineering-discipline` `code-quality` `evidence-first` `enforcement-protocol` `agent-safety`

- [esbuild-bundler](../development/esbuild-bundler/) — esbuild bundler configuration — blazing fast JS/TS bundling, plugins, watch mode, minification. Use when working with esbuild bundler.
  `bundler` `coding` `esbuild` `software-engineering` `testing`

- [event-driven](../development/event-driven/) — Event-driven architecture — event sourcing, CQRS, saga pattern, event buses, pub/sub patterns. Use when working with event driven.
  `coding` `driven` `event` `software-engineering` `testing`

- [executing-plans](../development/executing-plans/) — Use when you have a completed, Momus-approved plan artifact ready for execution with checkpoint discipline
  `coding` `executing` `plans` `software-engineering` `testing`

- [finishing-a-development-branch](../development/finishing-a-development-branch/) — Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
  `branch` `coding` `finishing` `software-engineering` `testing`

- [firebase-patterns](../development/firebase-patterns/) — Firebase patterns and integration — Firestore queries, auth flows, cloud functions, security rules, SDK setup, and real-time data. Use when working with firebase patterns, integrating firebase.
  `coding` `firebase` `firestore` `auth` `cloud-functions`

- [flutter-dev](../development/flutter-dev/) — Flutter cross-platform development — Dart, widgets, state management, platform channels, Firebase integration. Use when working with flutter dev.
  `coding` `dev` `flutter` `software-engineering` `testing`

- [free-dev-resources](../development/free-dev-resources/) — Recommend free-tier developer services and SaaS tools. Use when choosing free infrastructure, comparing free tiers, setting up side projects, or optimizing costs for startups and indie devs.
  `free-tier` `saas` `cost-optimization` `developer-tools` `cloud`

- [git-master](../development/git-master/) — Handles advanced Git workflows. Use when rebasing, squashing, bisecting, or managing complex branch histories.
  `coding` `git` `master` `software-engineering` `testing`

- [git-workflow-mastery](../development/git-workflow-mastery/) — Master Git workflows including branching strategies, interactive rebase, cherry-pick, bisect, worktrees, and advanced merge conflict resolution. Use when working with git workflow mastery.
  `git` `version-control` `branching` `rebase` `worktrees`

- [graphql-api](../development/graphql-api/) — GraphQL API development — schema design, resolvers, subscriptions, federation. Apollo, Relay, performance optimization. Use when working with graphql api.
  `api` `coding` `graphql` `software-engineering` `testing`

- [grpc](../development/grpc/) — gRPC development — Protocol Buffers, service definitions, streaming, interceptors, load balancing. Use when working with grpc.
  `coding` `grpc` `software-engineering` `testing`

- [incremental-implementation](../development/incremental-implementation/) — Delivers changes incrementally. Use when implementing any feature or change that touches more than one file.
  `coding` `implementation` `incremental` `software-engineering` `testing`

- [ionic-capacitor](../development/ionic-capacitor/) — Ionic + Capacitor hybrid mobile apps — Angular/React/Vue, native plugins, PWA, App Store deployment. Use when working with ionic capacitor.
  `capacitor` `coding` `ionic` `software-engineering` `testing`

- [ios-swiftui](../development/ios-swiftui/) — SwiftUI development — declarative UI, state management, navigation, and Apple ecosystem integration. Use when working with ios swiftui.
  `coding` `ios` `software-engineering` `swiftui` `testing`

- [job-queues](../development/job-queues/) — Background job processing — Bull/BullMQ, agenda, delayed jobs, retries, rate limiting, scheduled tasks. Use when working with job queues.
  `coding` `job` `queues` `software-engineering` `testing`

- [kafka-patterns](../development/kafka-patterns/) — Apache Kafka patterns — producers, consumers, topics, consumer groups, exactly-once semantics, event sourcing. Use when working with kafka patterns.
  `coding` `kafka` `patterns` `software-engineering` `testing`

- [linux-gui-control](../development/linux-gui-control/) — Automate Linux desktop GUI interactions using xdotool, wmctrl, and dogtail for window management, mouse/keyboard simulation, and accessibility inspection.
  `coding` `control` `gui` `linux` `software-engineering`

- [message-queue](../development/message-queue/) — Message queue patterns — RabbitMQ, Redis Streams, SQS. Task queues, pub/sub, dead letter queues, retry logic. Use when working with message queue.
  `coding` `message` `queue` `software-engineering` `testing`

- [monorepo-tooling](../development/monorepo-tooling/) — Monorepo management — Turborepo, Nx, pnpm workspaces, shared packages, CI optimization. Use when working with monorepo tooling.
  `coding` `monorepo` `software-engineering` `testing` `tooling`

- [neon-postgres](../development/neon-postgres/) — Neon serverless Postgres — branching, autoscaling, connection pooling, edge-compatible Postgres. Use when working with neon postgres.
  `coding` `neon` `postgres` `software-engineering` `testing`

- [nodejs-patterns](../development/nodejs-patterns/) — Node.js patterns — Express, Fastify, streams, worker threads, clustering, performance optimization. Use when working with nodejs patterns.
  `coding` `nodejs` `patterns` `software-engineering` `testing`

- [payment-integration](../development/payment-integration/) — Payment platform integration — Stripe, Paddle, Lemon Squeezy. Checkout flows, subscriptions, webhooks, billing management. Use when working with payment integration.
  `coding` `integration` `payment` `software-engineering` `testing`

- [planetscale-patterns](../development/planetscale-patterns/) — PlanetScale MySQL — branching, deploy requests, Vitess sharding, connection handling, schema management. Use when working with planetscale patterns.
  `coding` `patterns` `planetscale` `software-engineering` `testing`

- [playwright-e2e](../development/playwright-e2e/) — End-to-end test automation with Playwright — cross-browser testing, page objects, and CI integration. Use when working with playwright e2e.
  `coding` `e2e` `playwright` `software-engineering` `testing`

- [pocketbase-patterns](../development/pocketbase-patterns/) — PocketBase — single-file backend with SQLite, realtime subscriptions, auth, file storage, custom JS extensions. Use when working with pocketbase patterns.
  `coding` `patterns` `pocketbase` `software-engineering` `testing`

- [postgres-queries](../development/postgres-queries/) — PostgreSQL optimization — query tuning, schema design, indexing strategies, and performance analysis. Use when working with postgres queries.
  `coding` `postgres` `queries` `software-engineering` `testing`

- [prd-generator](../development/prd-generator/) — Generate detailed Product Requirement Documents (PRDs) from feature descriptions. Create structured specifications ready for implementation.
  `coding` `generator` `prd` `software-engineering` `testing`

- [prisma-orm](../development/prisma-orm/) — Prisma ORM — schema modeling, migrations, client queries, middleware, performance optimization. Use when working with prisma orm.
  `coding` `orm` `prisma` `software-engineering` `testing`

- [qa-review-fix-loop](../development/qa-review-fix-loop/) — Comprehensive QA→Review→Fix loop protocol for any codebase. Layer-based testing with evidence requirements. Use when performing full QA cycles, codebase audits, pre-release testing, or.
  `qa` `testing` `quality-assurance` `review-loop` `defect-tracking`

- [query-optimizer](../development/query-optimizer/) — Slow query analysis — EXPLAIN plans, index recommendations, N+1 detection, and caching strategies. Use when working with query optimizer.
  `coding` `optimizer` `query` `software-engineering` `testing`

- [rabbitmq-patterns](../development/rabbitmq-patterns/) — RabbitMQ patterns — exchanges, queues, routing, dead letter queues, priority queues, clustering. Use when working with rabbitmq patterns.
  `coding` `patterns` `rabbitmq` `software-engineering` `testing`

- [react-native-expo](../development/react-native-expo/) — React Native with Expo — managed workflow, native modules, navigation, and app store deployment. Use when working with react native expo.
  `coding` `expo` `native` `react` `software-engineering`

- [receiving-code-review](../development/receiving-code-review/) — Use when getting code feedback, before implementing suggestions.
  `code` `coding` `receiving` `review` `software-engineering`

- [requesting-code-review](../development/requesting-code-review/) — Use when completing tasks, implementing major features, or before merging to verify work meets requirements
  `code` `coding` `requesting` `review` `software-engineering`

- [security-headers](../development/security-headers/) — Web security headers — CSP, CORS, HSTS, X-Frame-Options. Configure, audit, and harden HTTP security headers. Use when working with security headers.
  `coding` `headers` `security` `software-engineering` `testing`

- [sequelize-patterns](../development/sequelize-patterns/) — Sequelize ORM patterns — models, associations, migrations, transactions, hooks, TypeScript support. Use when working with sequelize patterns.
  `coding` `patterns` `sequelize` `software-engineering` `testing`

- [spec-driven-development](../development/spec-driven-development/) — Write a PRD covering objectives, commands, structure, code style, testing, and boundaries before any code. Spec before code, always. Use when writeing a prd covering objectives, commands, structure, code style, testing,.
  `engineering` `spec` `prd` `planning` `requirements`

- [storybook-dev](../development/storybook-dev/) — Storybook component development — stories, addons, controls, accessibility testing, visual regression. Use when working with storybook dev.
  `coding` `dev` `software-engineering` `storybook` `testing`

- [subagent-driven-development](../development/subagent-driven-development/) — Use when executing implementation plans with independent tasks in the current session
  `coding` `driven` `software-engineering` `subagent` `testing`

- [supabase-patterns](../development/supabase-patterns/) — Supabase patterns — Row Level Security, edge functions, real-time subscriptions, auth integration, setup, and configuration. Use when working with supabase patterns.
  `coding` `patterns` `software-engineering` `supabase` `testing`

- [surrealdb-patterns](../development/surrealdb-patterns/) — SurrealDB multi-model database — document, graph, key-value. SurrealQL, realtime subscriptions, embedded mode. Use when working with surrealdb patterns.
  `coding` `patterns` `software-engineering` `surrealdb` `testing`

- [svelte-framework](../development/svelte-framework/) — Svelte and SvelteKit development — runes, stores, server-side rendering, form actions, streaming, edge deployment, and patterns. Use when working with svelte framework.
  `coding` `framework` `software-engineering` `svelte` `patterns`

- [swiftui-patterns](../development/swiftui-patterns/) — SwiftUI native iOS/macOS development — declarative UI, Combine, Core Data, widgets, App Clips. Use when working with swiftui patterns.
  `coding` `patterns` `software-engineering` `swiftui` `testing`

- [systematic-debugging](../development/systematic-debugging/) — Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
  `coding` `debugging` `software-engineering` `systematic` `testing`

- [task-scheduler](../development/task-scheduler/) — Task scheduling and cron patterns — node-cron, BullMQ, Celery, systemd timers. Recurring jobs, distributed scheduling. Use when working with task scheduler.
  `coding` `cron` `scheduler` `software-engineering` `task`

- [tauri-apps](../development/tauri-apps/) — Tauri desktop app development — Rust backend, web frontend, native APIs, small binary size, cross-platform. Use when working with tauri apps.
  `api` `apps` `coding` `software-engineering` `tauri`

- [test-coverage-analyzer](../development/test-coverage-analyzer/) — Identify untested code paths — coverage reports, gap analysis, and test prioritization. Use when working with test coverage analyzer.
  `analyzer` `coding` `coverage` `software-engineering` `test`

- [test-driven-development](../development/test-driven-development/) — Use when implementing any feature or bugfix, before writing implementation code
  `coding` `driven` `software-engineering` `test` `testing`

- [typeorm-patterns](../development/typeorm-patterns/) — TypeORM patterns — entities, repositories, migrations, relations, query builder, active record vs data mapper. Use when working with typeorm patterns.
  `coding` `patterns` `software-engineering` `testing` `typeorm`

- [using-git-worktrees](../development/using-git-worktrees/) — Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
  `coding` `git` `software-engineering` `testing` `using`

- [verification-before-completion](../development/verification-before-completion/) — Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
  `before` `coding` `completion` `software-engineering` `testing`

- [visual-regression](../development/visual-regression/) — Visual regression testing — screenshot comparison, baseline management, and UI change detection. Use when working with visual regression.
  `coding` `regression` `software-engineering` `testing` `visual`

- [vite-config](../development/vite-config/) — Vite build tool configuration — plugins, SSR, library mode, environment variables, dev server proxy. Use when working with vite config.
  `coding` `config` `software-engineering` `testing` `vite`

- [voice-ai-builder](../development/voice-ai-builder/) — Build voice-based AI agents for phone calls, meetings, customer support, and sales qualification using Vapi, Bland, and Retell. Use when building voice-based ai agents for phone calls, meetings, customer support,.
  `ai-agent` `api` `builder` `coding` `software-engineering`

- [vue-framework](../development/vue-framework/) — Vue.js 3 development patterns — Composition API, Pinia state management, Vue Router, Nuxt.js SSR/SSG, component architecture, performance optimization. Use when working with vue patterns or vue framework.
  `api` `coding` `patterns` `software-engineering` `framework`

- [wails-apps](../development/wails-apps/) — Wails desktop app development — Go backend, web frontend, native bindings, small binary, cross-platform. Use when working with wails apps.
  `apps` `coding` `software-engineering` `testing` `wails`

- [webpack-config](../development/webpack-config/) — Webpack 5 configuration — loaders, plugins, code splitting, tree shaking, module federation, dev server. Use when working with webpack config.
  `coding` `config` `software-engineering` `testing` `webpack`

- [websocket](../development/websocket/) — WebSocket development — real-time bidirectional communication, Socket.IO, native WebSocket API, scaling patterns. Use when working with websocket.
  `api` `coding` `software-engineering` `testing` `websocket`

- [writing-plans](../development/writing-plans/) — Use when you have a spec or requirements for a multi-step task, before touching code
  `coding` `plans` `software-engineering` `testing` `writing`

### Devops (devops/)

_Total: 31 skills_

Browse in [`devops/_index.md`](../devops/_index.md).

- [ansible-automation](../devops/ansible-automation/) — Ansible automation — playbooks, roles, inventory, variables, handlers, Galaxy, AWX. Use when working with ansible automation.
  `ansible` `automation` `ci-cd` `devops` `infrastructure`

- [argocd-gitops](../devops/argocd-gitops/) — ArgoCD GitOps — declarative continuous delivery, application sync, drift detection, multi-cluster. Use when working with argocd gitops.
  `argocd` `ci-cd` `devops` `gitops` `infrastructure`

- [aws-ops](../devops/aws-ops/) — AWS operations — EC2, S3, Lambda, RDS, ECS, IAM, CloudFormation. Infrastructure and cost optimization. Use when working with aws ops.
  `aws` `ci-cd` `devops` `infrastructure` `ops`

- [azure-ops](../devops/azure-ops/) — Azure operations — Virtual Machines, App Service, Azure Functions, AKS, Cosmos DB, Azure AD. Use when working with azure ops.
  `azure` `ci-cd` `devops` `infrastructure` `ops`

- [buildkite-pipelines](../devops/buildkite-pipelines/) — Buildkite CI pipelines — pipeline YAML, steps, agents, artifacts, test splitting, dynamic pipelines. Use when working with buildkite pipelines.
  `ai-agent` `buildkite` `ci-cd` `devops` `infrastructure`

- [ci-cd-pipeline](../devops/ci-cd-pipeline/) — CI/CD pipeline design with GitHub Actions, GitLab CI — build, test, deploy automation. Use when setting up CI/CD pipelines or automating deployments.
  `ci-cd` `devops` `github` `infrastructure` `pipeline`

- [cilium-networking](../devops/cilium-networking/) — Cilium eBPF networking — Kubernetes CNI, network policies, load balancing, observability with Hubble. Use when working with cilium networking.
  `ci-cd` `cilium` `devops` `infrastructure` `kubernetes`

- [circleci-config](../devops/circleci-config/) — CircleCI configuration — workflows, jobs, orbs, caching, contexts, dynamic config. Use when working with circleci config.
  `ci-cd` `circleci` `config` `devops` `infrastructure`

- [consul-service-mesh](../devops/consul-service-mesh/) — HashiCorp Consul — service discovery, health checking, KV store, service mesh, intentions. Use when working with consul service mesh.
  `ci-cd` `consul` `devops` `infrastructure` `mesh`

- [docker](../devops/docker/) — Use when full-stack DevOps pipeline — Docker Compose for local dev, Dockerfile optimization for production images, Kubernetes deployment for scale. Turn container ops into a service business.
  `devops` `docker` `compose` `kubernetes` `k8s`

- [dockerfile-optimize](../devops/dockerfile-optimize/) — Dockerfile optimization — multi-stage builds, layer caching, security hardening, minimal images. Use when optimizing Docker builds or hardening container security.
  `ci-cd` `devops` `docker` `dockerfile` `infrastructure`

- [drone-ci](../devops/drone-ci/) — Drone CI — container-native CI/CD, YAML pipelines, plugins, secrets, multi-machine builds. Use when working with drone ci.
  `ci-cd` `devops` `drone` `infrastructure` `machine-learning`

- [edge-computing](../devops/edge-computing/) — Edge computing — Cloudflare Workers, Vercel Edge, Deno Deploy. Edge rendering, caching, edge databases. Use when working with edge computing.
  `ci-cd` `computing` `devops` `edge` `infrastructure`

- [envoy-proxy](../devops/envoy-proxy/) — Envoy proxy — L4/L7 filtering, load balancing, circuit breaking, observability, extensibility. Use when working with envoy proxy.
  `ci-cd` `devops` `envoy` `infrastructure` `proxy`

- [fluxcd-gitops](../devops/fluxcd-gitops/) — Flux CD GitOps — source controllers, kustomize/helm controllers, image automation, notifications. Use when working with fluxcd gitops.
  `ci-cd` `devops` `fluxcd` `gitops` `infrastructure`

- [free-cloud-infrastructure](../devops/free-cloud-infrastructure/) — Recommend free-tier cloud infrastructure for compute, storage, serverless, databases, and CDN. Use when provisioning free cloud resources, comparing always-free vs trial tiers, or building.
  `free-tier` `cloud` `infrastructure` `cost-optimization` `serverless`

- [gcp-ops](../devops/gcp-ops/) — Google Cloud operations — Compute Engine, Cloud Run, BigQuery, Cloud Functions, GKE, IAM. Use when working with gcp ops.
  `ci-cd` `devops` `gcp` `infrastructure` `ops`

- [helm-charts](../devops/helm-charts/) — Helm chart development — templates, values, hooks, dependencies, chart testing, repository management. Use when working with helm charts.
  `charts` `ci-cd` `devops` `helm` `infrastructure`

- [istio-mesh](../devops/istio-mesh/) — Istio service mesh — traffic management, security, observability for Kubernetes microservices. Use when working with istio mesh.
  `ci-cd` `devops` `infrastructure` `istio` `kubernetes`

- [jenkins-pipelines](../devops/jenkins-pipelines/) — Jenkins pipeline as code — Declarative/Scripted pipelines, shared libraries, agents, stages, credentials. Use when working with jenkins pipelines.
  `ai-agent` `ci-cd` `devops` `infrastructure` `jenkins`

- [jenkins-shared-libs](../devops/jenkins-shared-libs/) — Jenkins shared libraries — reusable pipeline code, Groovy vars, resources, global pipeline libraries. Use when working with jenkins shared libs.
  `ci-cd` `devops` `infrastructure` `jenkins` `libs`

- [kustomize-config](../devops/kustomize-config/) — Kustomize Kubernetes configuration — bases, overlays, patches, generators, transformers. Use when working with kustomize config.
  `ci-cd` `config` `devops` `infrastructure` `kubernetes`

- [linkerd-mesh](../devops/linkerd-mesh/) — Linkerd service mesh — lightweight Kubernetes mesh, mTLS, traffic splitting, observability. Use when working with linkerd mesh.
  `ci-cd` `devops` `infrastructure` `kubernetes` `linkerd`

- [nomad-scheduler](../devops/nomad-scheduler/) — HashiCorp Nomad — job scheduling, task drivers, allocations, scaling, federation. Use when working with nomad scheduler.
  `ci-cd` `devops` `infrastructure` `nomad` `scheduler`

- [observability](../devops/observability/) — Observability stack — Prometheus, Grafana, Loki, OpenTelemetry. Metrics, logs, traces, alerting, SLO monitoring. Use when working with observability.
  `ci-cd` `devops` `infrastructure` `monitoring` `observability`

- [packer-images](../devops/packer-images/) — HashiCorp Packer — machine image building, builders, provisioners, post-processors for AWS/GCP/Azure. Use when working with packer images.
  `aws` `azure` `ci-cd` `devops` `gcp`

- [serverless](../devops/serverless/) — Serverless architecture — AWS Lambda, Cloudflare Workers, Vercel Edge. Event-driven design, cold start optimization. Use when working with serverless.
  `aws` `ci-cd` `devops` `infrastructure` `serverless`

- [tekton-pipelines](../devops/tekton-pipelines/) — Tekton CI/CD pipelines — Tasks, Pipelines, Triggers, Workspaces for Kubernetes-native CI. Use when working with tekton pipelines.
  `ci-cd` `devops` `infrastructure` `kubernetes` `pipeline`

- [terraform-iac](../devops/terraform-iac/) — Infrastructure as Code with Terraform — providers, modules, state management, workspaces, multi-cloud deployments. Use when working with terraform iac.
  `ci-cd` `devops` `iac` `infrastructure` `terraform`

- [vault-pki](../devops/vault-pki/) — Vault PKI secrets engine — certificate authority, dynamic certificates, certificate rotation. Use when working with vault pki.
  `ci-cd` `devops` `infrastructure` `pki` `vault`

- [vault-secrets](../devops/vault-secrets/) — HashiCorp Vault — secrets management, dynamic secrets, encryption, auth methods, policies. Use when working with vault secrets.
  `ci-cd` `devops` `infrastructure` `secrets` `vault`

### Financial (financial/)

_Total: 18 skills_

Browse in [`financial/_index.md`](../financial/_index.md).

- [ai-readiness](../financial/ai-readiness/) — Assess portfolio company AI readiness, AI adoption maturity. Use when user says "AI readiness", "AI maturity", "assess AI adoption".
  `analysis` `finance` `investment` `readiness`

- [all-in-one-finance](../financial/all-in-one-finance/) — Use when user mentions ticker symbols, tokens, forex pairs, commodities, portfolio, trade, DCF, valuation, technical analysis, on-chain metrics, risk management, position sizing, financial.
  `finance` `trading` `investing` `crypto` `equities`

- [earnings-viewer](../financial/earnings-viewer/) — Analyzes earnings calls + SEC filings, updates financial models, and drafts earnings notes. Use when user says "analyze earnings", "earnings call", "update model after earnings".
  `analysis` `earnings` `finance` `investment` `viewer`

- [finance-tracker](../financial/finance-tracker/) — Track real-time revenue across 5 income streams, monitor cashflow and runway, detect revenue gaps, and send threshold alerts via Telegram. Use when tracking real-time revenue across 5 income streams, monitor cashflow and.
  `analysis` `finance` `investment` `tracker`

- [gl-reconciler](../financial/gl-reconciler/) — Finds breaks, traces root cause, routes for sign-off. Use when user says "reconcile GL", "find breaks", "trace accounting error".
  `analysis` `finance` `investment` `reconciler`

- [investment-bottleneck](../financial/investment-bottleneck/) — Use when find bottleneck companies — the critical constraint in supply chains that have pricing power, low competition, and high returns. Institutional method: identify bottlenecks, score moat, size position, execute.
  `investment` `bottleneck` `finance`

- [investment-earnings](../financial/investment-earnings/) — Use when trade earnings reports for profit — pre-earnings positioning, post-earnings momentum, and management quality scoring. Systematic framework for the highest-alpha event in equity markets.
  `investment` `earnings` `finance`

- [investment-industry](../financial/investment-industry/) — Use when industry research and sector rotation for portfolio alpha — TAM/SAM/SOM analysis, competitive dynamics, regulatory tailwinds, and sector timing to beat the market by 5-15% annually.
  `investment` `industry` `finance`

- [kyc-screener](../financial/kyc-screener/) — Parses onboarding docs, runs rules engine, flags compliance gaps. Use when user says "KYC check", "onboard client", "screen company".
  `analysis` `compliance` `finance` `investment` `kyc`

- [meeting-prep](../financial/meeting-prep/) — Prepares briefing pack before client/investor meetings. Use when user says "prep for meeting", "briefing pack", "client meeting".
  `analysis` `finance` `investment` `meeting` `prep`

- [model-builder](../financial/model-builder/) — Builds and updates DCF, LBO, and 3-statement financial models in Excel with live data connections. Use when user says "build DCF", "create LBO model", "populate 3-statement model".
  `analysis` `builder` `finance` `investment` `model`

- [month-end-closer](../financial/month-end-closer/) — Accruals, roll-forwards, variance commentary. Use when user says "month-end close", "accruals", "roll-forward".
  `analysis` `closer` `end` `finance` `investment`

- [pitch-deck](../financial/pitch-deck/) — Populates branded pitch deck templates with financial data and market comps. Use when user says "create pitch deck", "pitch for investors", "populate pitchbook".
  `analysis` `deck` `finance` `investment` `pitch`

- [portfolio-monitor](../financial/portfolio-monitor/) — Track portfolio company KPIs, variances, returns analysis. Use when user says "monitor portfolio", "track KPIs", "portfolio returns".
  `analysis` `finance` `investment` `monitor` `portfolio`

- [statement-auditor](../financial/statement-auditor/) — Audits LP statements before distribution. Use when user says "audit statement", "review LP package", "distribution check".
  `analysis` `auditor` `finance` `investment` `statement`

- [tax-loss-harvesting](../financial/tax-loss-harvesting/) — Identify TLH opportunities, manage wash sales. Use when user says "tax loss harvest", "TLH", "wash sale check".
  `analysis` `finance` `harvesting` `investment` `loss`

- [valuation-reviewer](../financial/valuation-reviewer/) — Ingests GP packages, runs valuation template, stages LP reporting. Use when user says "review valuation", "LP reporting", "GP package".
  `analysis` `finance` `investment` `reviewer` `valuation`

- [wolf-finance](../financial/wolf-finance/) — ACTIVATE for ANY finance, investment, trading, or market query. Comprehensive value investing framework combining Buffett, Munger, Duan Yongping, and Li Lu methodologies. Use when making investment decisions.
  `analysis` `crypto` `finance` `investment` `testing`

### Integrations (integrations/)

_Total: 26 skills_

Browse in [`integrations/_index.md`](../integrations/_index.md).

- [bigquery-integration](../integrations/bigquery-integration/) — Integrate Google BigQuery for large-scale data analytics. Write SQL queries, manage datasets, export results, and build data pipelines. Use when integrateing google bigquery for large-scale data analytics. write sql queries,.
  `bigquery` `google-cloud` `sql` `analytics` `data-warehouse`

- [cloud-mcp](../integrations/cloud-mcp/) — MCP servers for cloud infrastructure. Connect AI agents to AWS, GCP, and Azure for deployment, management, and infrastructure automation. Use when working with cloud mcp.
  `ai-agent` `api` `aws` `azure` `cloud`

- [communication-mcp](../integrations/communication-mcp/) — MCP servers for team communication. Connect AI agents to Slack, Discord, and Telegram for notifications, messaging, and channel management. Use when working with communication mcp.
  `ai-agent` `api` `communication` `discord` `integrations`

- [database-mcp](../integrations/database-mcp/) — MCP server for SQL databases. Connect AI agents to PostgreSQL, MySQL, MariaDB, and SQLite for natural language queries, schema management, and data operations. Use when working with database mcp.
  `ai-agent` `api` `database` `integrations` `mcp`

- [discord](../integrations/discord/) — Use when discord Automation Hub — Bot and Webhooks for community management, DevOps notifications, and interactive servers. Monetize through community infrastructure-as-a-service.
  `api` `automation` `bot` `community` `discord`

- [free-saas-toolkit](../integrations/free-saas-toolkit/) — Recommend free-tier SaaS tools for teams -- collaboration, project management, analytics, forms, payments, and email marketing. Use when choosing free team tools, setting up a startup.
  `free-tier` `saas` `team-tools` `collaboration` `analytics`

- [github](../integrations/github/) — Use when gitHub Automation Hub — Actions, Issues, and PR management for CI/CD, project tracking, and code review workflows. Monetize through automation-as-a-service.
  `api` `automation` `ci-cd` `github` `integrations`

- [kalodata-dashboard](../integrations/kalodata/dashboard/) — Use when generating CLI-based visual reports from Kalodata product research data, including ASCII trend charts, product cards, interactive dashboards, and markdown exports.
  `api` `dashboard` `integrations` `kalodata` `third-party`

- [kalodata-integrations](../integrations/kalodata/integrations/) — Multi-platform integrations for Kalodata research. Connect Shopify for product listings, Notion for research reports, and Slack for alerts + daily digests. CLI-friendly with config-based API key management. Use when working with kalodata integrations.
  `api` `integrations` `kalodata` `notion` `slack`

- [kalodata-monitor](../integrations/kalodata/monitor/) — Scheduled research runs with auto-alerts for NEW viral products. Runs on configurable schedule (hourly/daily/weekly), detects new products by comparing with previous runs, alerts on revenue threshold crossings, and sends notifications via Slack webhook. Use when working with kalodata monitor.
  `api` `integrations` `kalodata` `monitor` `slack`

- [kalodata-product-research](../integrations/kalodata/product-research/) — Query and analyze TikTok Shop products by category with intelligent filtering, sorting, and AI-powered research goal detection. Use when researching trending products, finding emerging winners, analyzing competition, or building product intelligence reports.
  `api` `integrations` `kalodata` `product` `research`

- [kalodata-research-automation](../integrations/kalodata/research-automation/) — End-to-end competitive analysis automation that combines product research, video analysis, and storyboard extraction into a single workflow. Accepts product search criteria and returns complete competitive analysis with viral product insights, video breakdowns, and content replication guides. Use when working with kalodata research automation.
  `api` `integrations` `kalodata` `research` `third-party`

- [kalodata-storyboard-extract](../integrations/kalodata/storyboard-extract/) — Use when extracting AI-generated storyboards from viral TikTok Shop videos, including scene breakdowns, visual descriptions, camera work analysis, and auto-generating content ideas for replication.
  `api` `extract` `integrations` `kalodata` `storyboard`

- [kalodata-video-analysis](../integrations/kalodata/video-analysis/) — Get videos associated with products, extract video metadata, get downloadable video URLs, and identify top-performing videos for competitive analysis. Use when analyzing video marketing strategies, finding best-performing creative assets, or building video intelligence reports.
  `api` `integrations` `kalodata` `third-party` `video`

- [linear-api](../integrations/linear-api/) — Linear API integration — issue tracking, project management, cycle planning, team workflows via GraphQL API. Use when working with linear api.
  `api` `graphql` `integrations` `linear` `third-party`

- [notion-integration](../integrations/notion-integration/) — Use when notion Automation Hub — API, Database, and Page management for knowledge bases, project trackers, and content systems. Monetize through workspace automation-as-a-service.
  `api` `automation` `integrations` `notion` `third-party`

- [oh-my-opencode](../integrations/oh-my-opencode/) — Use when working with OpenCode AI coding agent and oh-my-opencode harness to install, configure, and leverage its advanced features including Sisyphus, Hephaestus, Oracle, Librarian, and Explore agents
  `ai-agent` `api` `integrations` `opencode` `third-party`

- [oh-my-opencode-agents](../integrations/oh-my-opencode/oh-my-opencode-agents/) — Deep dive into each oh-my-opencode agent - Sisyphus, Hephaestus, Oracle, Librarian, Explore - their characteristics, use cases, and when to use each. Use when working with oh my opencode agents.
  `agents` `ai-agent` `api` `integrations` `opencode`

- [oh-my-opencode-configuration](../integrations/oh-my-opencode/oh-my-opencode-configuration/) — Comprehensive configuration guide for oh-my-opencode including agent settings, MCP servers, hooks, categories, and advanced options. Use when working with oh my opencode configuration.
  `ai-agent` `api` `configuration` `integrations` `opencode`

- [oh-my-opencode-features](../integrations/oh-my-opencode/oh-my-opencode-features/) — Complete reference of all oh-my-opencode features including agents, tools, MCPs, hooks, workflow automation, and productivity enhancements. Use when working with oh my opencode features.
  `ai-agent` `api` `features` `integrations` `opencode`

- [oh-my-opencode-installation](../integrations/oh-my-opencode/oh-my-opencode-installation/) — Smart installation and configuration for OpenCode with oh-my-opencode harness - detects existing installation and only installs if needed. Use when working with oh my opencode installation.
  `api` `installation` `integrations` `opencode` `third-party`

- [oh-my-opencode-usage](../integrations/oh-my-opencode/oh-my-opencode-usage/) — Daily usage patterns for oh-my-opencode including workflow commands, session management, agent invocation, and productivity tips. Use when working with oh my opencode usage.
  `ai-agent` `api` `integrations` `opencode` `third-party`

- [slack](../integrations/slack/) — Use when slack Automation Hub — Bot, Notifier, and Slash Commands for team communication, DevOps alerts, and workflow automation. Monetize through integration-as-a-service.
  `api` `automation` `bot` `integrations` `notifications`

- [storage-mcp](../integrations/storage-mcp/) — MCP servers for cloud storage. Connect AI agents to S3, Google Drive, Dropbox, and file storage for automated backup, sync, and management.
  `ai-agent` `api` `integrations` `mcp` `storage`

- [stripe-integration](../integrations/stripe-integration/) — Integrate Stripe for payments, subscriptions, invoicing, and billing. Handle checkout sessions, webhooks, customer management, and payment method handling. Use when integrateing stripe for payments, subscriptions, invoicing, and billing. handle checkout.
  `payments` `stripe` `billing` `subscriptions` `checkout`

- [webhook-patterns](../integrations/webhook-patterns/) — Webhook design and handling — signature verification, retry logic, idempotency, event routing, testing. Use when working with webhook patterns.
  `api` `integrations` `patterns` `testing` `third-party`

### Marketing (marketing/)

_Total: 42 skills_

Browse in [`marketing/_index.md`](../marketing/_index.md).

- [ad-creative](../marketing/ad-creative/) — Ad creative production — visual briefs, copy variations, and A/B testing frameworks for performance advertising. Use when working with ad creative.
  `creative` `growth` `marketing` `seo` `testing`

- [adcp-advertising](../marketing/adcp-advertising/) — Automate ad campaigns via AdCP protocol — create ads, buy media, manage budgets, and optimize performance across display, video, CTV, and social channels.
  `adcp` `advertising` `growth` `marketing` `seo`

- [ads-manager](../marketing/ads-manager/) — Research trending ads, analyze competitor strategies, and clone successful ad patterns using integrated MCP servers. Use when working with ads manager.
  `advertising` `competitive-analysis` `marketing` `mcp` `google-ads`

- [affiliate-manager](../marketing/affiliate-manager/) — Automated discovery of affiliate programs, partnership opportunities, and cross-promotion deals with outreach, commission tracking, and placement optimization
  `affiliate` `growth` `manager` `marketing` `seo`

- [affiliate-marketing](../marketing/affiliate-marketing/) — AI-powered affiliate marketing automation. Research products, generate content, optimize conversions, and build passive income through automated affiliate campaigns.
  `affiliate` `growth` `marketing` `seo`

- [ai-content-agency-v2](../marketing/ai-content-agency-v2/) — 9-workflow, 6-phase AI content agency blueprint — generates ads, videos, images, and landing pages from product info using LLM ideation through multi-provider rendering.
  `agency` `content` `growth` `marketing` `seo`

- [ai-digital-products](../marketing/ai-digital-products/) — Create and sell AI-powered digital products. Build templates, prompt libraries, workflows, and Notion systems. Generate $500-5K/month passive income.
  `digital` `growth` `marketing` `notion` `products`

- [ai-seo](../marketing/ai-seo/) — Optimize for AI search engines — Perplexity, ChatGPT Search, Google AI Overviews, answer engine optimization. Use when adapting SEO strategy for AI-powered search, optimizing for featured snippets, or building AI-friendly content.
  `growth` `marketing` `seo` `money`

- [analytics-dashboard](../marketing/analytics-dashboard/) — Track performance across all platforms. Monitor social media metrics, ad performance, website analytics, and revenue. Generate automated reports and identify trends for data-driven decisions.
  `analytics` `dashboard` `growth` `marketing` `seo`

- [build-in-public](../marketing/build-in-public/) — Document and share your startup journey, revenue, and learnings on social media. Build audience, attract customers, and find co-founders through transparent sharing. Use when working with build in public.
  `build` `growth` `marketing` `public` `seo`

- [buzzer-engagement-army](../marketing/buzzer-engagement-army/) — Multi-account engagement booster across TikTok, Instagram, and Facebook — automates likes, comments, and warmup schedules to beat algorithm suppression on new posts.
  `army` `buzzer` `engagement` `growth` `marketing`

- [canva](../marketing/canva/) — Create, export, and manage Canva designs via the Connect API. Generate social posts, carousels, and graphics programmatically.
  `api` `canva` `growth` `marketing` `seo`

- [churn-prevention](../marketing/churn-prevention/) — Retention messaging, cancellation flows, win-back campaigns, and customer health scoring. Use when reducing churn rates, designing retention campaigns, or implementing cancellation flows.
  `churn` `growth` `marketing` `prevention` `seo`

- [cold-email](../marketing/cold-email/) — Outbound email with personalization, deliverability optimization, follow-up sequences, and compliance. Use when building cold email campaigns, improving email deliverability, or designing outreach sequences.
  `cold` `compliance` `email` `growth` `marketing`

- [competitor-alternatives](../marketing/competitor-alternatives/) — Competitive comparison page strategy — alternative to pages, positioning, differentiation messaging. Use when creating competitive positioning content.
  `alternatives` `competitor` `growth` `marketing` `seo`

- [content-analytics-engine](../marketing/content-analytics-engine/) — Collect content performance data from PostBridge API and generate daily/weekly reports tracking the full revenue funnel — views, engagement, clicks, and sales.
  `analytics` `api` `content` `engine` `growth`

- [content-creator](../marketing/content-creator/) — Use when generating multi-platform content via browser automation - social media, blogs, articles, video scripts, and images.
  `content` `creator` `growth` `marketing` `seo`

- [content-scheduler](../marketing/content-scheduler/) — Schedule and manage content publishing across platforms with Notion calendar. Use when scheduleing and manage content publishing across platforms with notion calendar.
  `content` `growth` `marketing` `notion` `scheduler`

- [email-marketing](../marketing/email-marketing/) — Create and send email campaigns, newsletters, and drip sequences. Build email lists, design templates, automate follow-ups, and track email performance for customer nurturing.
  `email` `growth` `marketing` `seo`

- [email-sequences](../marketing/email-sequences/) — Automated email sequence design — welcome series, nurture funnels, re-engagement, transactional flows. Use when building email automation systems.
  `email` `growth` `marketing` `sequences` `money`

- [growth-engine](../marketing/growth-engine/) — Autonomous marketing experiment framework — design A/B tests, score hypotheses with ICE, validate results with statistical significance, and run automated optimization loops.
  `engine` `growth` `marketing` `seo` `money`

- [influencer-outreach](../marketing/influencer-outreach/) — Influencer and creator partnership management — discovery, outreach, negotiation, campaign tracking. Use when running influencer marketing campaigns.
  `growth` `influencer` `marketing` `outreach` `seo`

- [launch-strategy](../marketing/launch-strategy/) — Go-to-market planning — launch sequencing, channel strategy, audience building, PR outreach. Use when planning product launches, building launch checklists, or coordinating multi-channel campaigns.
  `growth` `launch` `marketing` `seo` `strategy`

- [lead-magnets](../marketing/lead-magnets/) — Lead magnet design and creation — ebooks, templates, calculators, quizzes matched to audience intent. Use when building lead generation funnels.
  `growth` `lead` `magnets` `marketing` `money`

- [lynk](../marketing/lynk/) — LYNK - Complete Affiliate Link Management with Browser Automation. Use when relevant to this domain.
  `growth` `lynk` `marketing` `seo`

- [market-research](../marketing/market-research/) — Conduct market research, competitive analysis, and industry insights with Exa and Firecrawl. Use when conducting market research, competitive analysis, and industry insights with exa.
  `growth` `market` `marketing` `research` `seo`

- [marketing-ops](../marketing/ops/) — >
  Complete AI-powered marketing & sales operating system for solo founders.
  Covers the full revenue lifecycle: customer research, content creation,
  SEO/GEO/SMO optimization, paid ads, email sequences, sales enablement,
  CRO, pricing, retention, analytics, automation, and global expansion.
  Includes stage-based playbooks ($0→$100K MRR), AI agent orchestration,
  PLG frameworks, Indonesia e-commerce, and decision-making infrastructure.
  `ai-agent` `email` `growth` `marketing` `ops`

- [marketing-strategy](../marketing/strategy/) — Use when doing social media automation, content scheduling, analytics tracking, and campaign management.
  `growth` `marketing` `seo` `social-media` `strategy`

- [paid-ads](../marketing/paid-ads/) — Paid advertising for Google, Meta, LinkedIn — ad copy, audience targeting, budget optimization, conversion tracking. Use when setting up ad campaigns, optimizing ad spend, or designing ad creative.
  `ads` `growth` `marketing` `paid` `money`

- [pricing-strategy](../marketing/pricing-strategy/) — Pricing page design, tier structuring, anchoring psychology, conversion optimization. Use when designing pricing pages, setting up tier structures, or optimizing pricing conversion rates.
  `growth` `marketing` `pricing` `seo` `strategy`

- [referral-program](../marketing/referral-program/) — Referral program design and automation — incentive structures, tracking, viral loops, reward fulfillment. Use when building referral or affiliate programs. Use when working with referral program.
  `growth` `marketing` `program` `referral` `seo`

- [schema-markup](../marketing/schema-markup/) — Structured data markup for rich results and AI search visibility — JSON-LD, FAQ, HowTo, Product schemas. Use when implementing structured data for SEO. Use when working with schema markup.
  `growth` `marketing` `markup` `schema` `seo`

- [seo-auditor](../marketing/seo-auditor/) — SEO analysis and optimization automation for websites. Use when conducting technical SEO audits, tracking keyword rankings, analyzing competitor SEO, monitoring backlink profiles, optimizing existing content, improving local SEO visibility, generating SEO reports for clients, or automating website health checks.
  `auditor` `growth` `marketing` `monitoring` `seo`

- [seo-optimizer](../marketing/seo-optimizer/) — Optimize content for search engines. Perform keyword research, analyze on-page SEO, track rankings, audit technical SEO, and improve organic visibility for sustainable traffic growth. Use when optimizeing content for search engines. perform keyword research, analyze on-page.
  `growth` `marketing` `optimizer` `money` `seo`

- [shopee-optimizer](../marketing/shopee-optimizer/) — Shopee product management automation - listings, pricing, inventory, and order processing. Use when managing Shopee product listings, automating price adjustments based on competitors, syncing inventory across variants, processing orders with templates, tracking analytics, generating SEO-optimized content, or bulk uploading products from CSV files.
  `growth` `marketing` `optimizer` `seo` `shopee`

- [social-growth](../marketing/social-growth/) — Mark Zuckerberg's approach to building massive social platforms through network effects and rapid iteration. Use when working with social growth.
  `api` `growth` `marketing` `seo` `social`

- [social-media-engagement](../marketing/social-media-engagement/) — Automate social media engagement activities including liking, commenting, following, unfollowing, DMing, and replying. Build audience and increase reach across X, Instagram, TikTok, and LinkedIn.
  `engagement` `growth` `marketing` `media` `seo`

- [social-media-upload](../marketing/social-media-upload/) — Distribute content across multiple social media platforms (X, Instagram, TikTok, LinkedIn, Facebook, YouTube). Upload images, videos, and text with platform-specific optimization. Use when working with social media upload.
  `growth` `marketing` `media` `seo` `social`

- [stripe-revenue-bot](../marketing/stripe-revenue-bot/) — Automate posting your Stripe revenue milestones to Twitter/X. Build trust through transparency, attract customers, and join the "build in public" movement.
  `bot` `growth` `marketing` `revenue` `seo`

- [tiktok-marketing](../marketing/tiktok-marketing/) — TikTok marketing automation for the Indonesian market — content upload, carousel creation, engagement, and account management.
  `tiktok` `social-media` `marketing` `content` `automation`

- [twitter-automation](../marketing/twitter-automation/) — Automate Twitter/X presence with AI-powered posting, engagement, and growth. Schedule posts, auto-reply, track analytics, and build audience on autopilot.
  `automation` `growth` `marketing` `seo` `twitter`

- [viral-marketing](../marketing/viral-marketing/) — Gary Vaynerchuk's content machine approach - producing high-volume, authentic content across all platforms. Use when working with viral marketing.
  `growth` `marketing` `seo` `viral`

### Mcp (mcp/)

_Total: 15 skills_

Browse in [`mcp/_index.md`](../mcp/_index.md).

- [agent-reach](../mcp/servers/agent-reach/) — Universal internet scraper for AI agents. Read and search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, LinkedIn, V2EX, RSS, web pages. Zero API fees. Use when agents need real-time social media data, content research, or trend monitoring.
  `agent` `ai-agent` `api` `github` `mcp-server`

- [clients](../mcp/clients/) — Model Context Protocol client hub — connect AI agents to any MCP server for tool discovery, invocation, and ecosystem management. Use when working with MCP clients, discovering MCP servers, or building MCP-based toolchains.
  `mcp` `model-context-protocol` `client` `discover` `tool-integration`

- [codebase-memory-mcp](../mcp/servers/codebase-memory-mcp/) — Index codebases into a persistent knowledge graph for structural code queries, call-chain tracing, and semantic search. Use when navigating unfamiliar repos, understanding architecture, or exploring large codebases.
  `codebase` `mcp` `mcp-server` `memory` `model-context-protocol`

- [github-mcp](../mcp/servers/github-mcp/) — MCP server for GitHub automation. Manage repos, issues, PRs, and workflows through the Model Context Protocol. Use when working with github mcp.
  `github` `mcp` `mcp-server` `model-context-protocol` `tool-integration`

- [linear-mcp](../mcp/servers/linear-mcp/) — Linear Mcp. Use when working with linear mcp in mcp domain.
  `linear` `mcp` `mcp-server` `model-context-protocol` `tool-integration`

- [mcp-client](../mcp/clients/mcp-client/) — Generic MCP client implementation for connecting to any Model Context Protocol server with standardized tool access. Use when working with mcp client.
  `client` `mcp` `mcp-server` `model-context-protocol` `tool-integration`

- [mcp-discover](../mcp/clients/mcp-discover/) — Discover and connect to MCP servers automatically. Browse available tools and register new server endpoints. Use when working with mcp discover.
  `discover` `mcp` `mcp-server` `model-context-protocol` `tool-integration`

- [mcp-server-builder](../mcp/servers/mcp-server-builder/) — Create MCP (Model Context Protocol) servers for any API or service. Auto-generate tools, resources, and prompts that any AI agent can use.
  `ai-agent` `api` `builder` `mcp` `mcp-server`

- [memory-knowledge-graph](../mcp/memory-knowledge-graph/) — Knowledge graph-based persistent memory for AI agents — entities, relations, and semantic retrieval. Use when working with memory knowledge graph.
  `ai-agent` `graph` `knowledge` `mcp-server` `memory`

- [notion-mcp](../mcp/servers/notion-mcp/) — MCP server for Notion databases. Query pages, manage databases, and automate Notion workflows via standardized protocol.
  `mcp` `mcp-server` `model-context-protocol` `notion` `tool-integration`

- [resend-mcp](../mcp/servers/resend-mcp/) — Resend Mcp. Use when working with resend mcp in mcp domain.
  `mcp` `mcp-server` `model-context-protocol` `resend` `tool-integration`

- [sequential-thinking](../mcp/sequential-thinking/) — Dynamic problem-solving through thought sequences — iterative reasoning, hypothesis testing, and solution refinement. Use when working with sequential thinking.
  `mcp-server` `model-context-protocol` `sequential` `testing` `thinking`

- [slack-mcp](../mcp/servers/slack-mcp/) — MCP server for Slack integration. Send messages, manage channels, and automate Slack workflows via standardized protocol.
  `mcp` `mcp-server` `model-context-protocol` `slack` `tool-integration`

- [stripe-mcp](../mcp/servers/stripe-mcp/) — MCP server for Stripe payments. Process payments, manage subscriptions, and handle billing via standardized protocol. Use when working with stripe mcp.
  `mcp` `mcp-server` `model-context-protocol` `stripe` `tool-integration`

- [supabase-mcp](../mcp/servers/supabase-mcp/) — MCP server for Supabase databases. Query tables, manage auth, and handle storage through standardized protocol. Use when working with supabase mcp.
  `mcp` `mcp-server` `model-context-protocol` `supabase` `tool-integration`

### Meta (meta/)

_Total: 13 skills_

Browse in [`meta/_index.md`](../meta/_index.md).

- [auto-evolve](../meta/auto-evolve/) — Continuously monitors system performance identifies improvement opportunities and orchestrates find-skills and create-skills to autonomously evolve capabilities. The brain of the self-evolving system. Use when working with auto evolve.
  `auto` `evolve` `meta-learning` `self-improvement` `skill-evolution`

- [auto-learner](../meta/auto-learner/) — Autonomous learning from execution data. Skills improve themselves by identifying patterns in successful vs failed executions without human intervention. Use when working with auto learner.
  `auto` `learner` `meta-learning` `self-improvement` `skill-evolution`

- [create-skills](../meta/create-skills/) — Use when the system identifies a skill gap and needs to autonomously generate a new skill to fill it. Works with find-skills to ensure no duplicates.
  `create` `meta-learning` `self-improvement` `skill-evolution` `skills`

- [data](../meta/data/) — Raw data storage layer for 1ai-skills. Provides structured data persistence, query interface, and data pipeline support for skill operations. history. Use when working with data.
  `data` `meta-learning` `self-improvement` `skill-evolution`

- [feedback-collector](../meta/feedback-collector/) — Collect, analyze, and route feedback from users and systems. Turn feedback into actionable improvement signals. Use when working with feedback collector.
  `collector` `feedback` `meta-learning` `self-improvement` `skill-evolution`

- [hooks-setup](../meta/hooks-setup/) — Use when user says "install hooks", "setup hooks", "hooks setup", "configure hooks", "/hooks-setup". Installs and configures 1ai-skills auto-evolve hooks for Claude Code.
  `hooks` `meta-learning` `self-improvement` `setup` `skill-evolution`

- [improvement-generator](../meta/improvement-generator/) — Generate specific, actionable improvements for skills based on performance data and feedback. Create improvement plans, not just identify problems.
  `generator` `improvement` `meta-learning` `self-improvement` `skill-evolution`

- [meta-find-skills](../meta/find-skills/) — Automatically discover evaluate and activate community skills when local skills dont cover user needs Includes credibility scoring and safety checks for complete self-sufficiency
  `find` `meta` `meta-learning` `self-improvement` `skill-evolution`

- [meta-skill-datastore](../meta/skill-datastore/) — Centralized database for meta-skill operations. Stores performance metrics, feedback, patterns, and skill evolution history. Use when working with meta skill datastore.
  `datastore` `meta` `meta-learning` `self-improvement` `skill`

- [pattern-recognition](../meta/pattern-recognition/) — Identify patterns in skill execution, errors, and successes. Recognize when situations match previous patterns and apply learned solutions. Use when working with pattern recognition.
  `meta-learning` `pattern` `recognition` `self-improvement` `skill-evolution`

- [performance-monitor](../meta/performance-monitor/) — Track and analyze skill execution performance. Measure latency, success rates, accuracy, and resource usage for continuous improvement. Use when tracking and analyze skill execution performance. measure latency, success rates,.
  `meta-learning` `monitor` `performance` `self-improvement` `skill-evolution`

- [self-assessment](../meta/self-assessment/) — Skills evaluate their own performance, capabilities, and limitations. Honest self-reflection drives improvement. Use when working with self assessment.
  `assessment` `meta-learning` `self` `self-improvement` `skill-evolution`

- [skill-evolution-engine](../meta/skill-evolution-engine/) — Self-improving skill system that auto-extracts patterns from sessions into reusable skills with confidence scoring, skill versioning, import/export, and continuous improvement loops. Use. Use when working with skill evolution engine.
  `self-improvement` `skill-evolution` `confidence-scoring` `continuous-learning` `stocktake`

### Mindset (mindset/)

_Total: 55 skills_

Browse in [`mindset/_index.md`](../mindset/_index.md).

- [active-listening](../mindset/active-listening/) — Master active listening through the HEAR model, reflective listening, and questioning techniques. Use when coaching, resolving conflicts, or building trust.
  `active` `listening` `mindset` `personal-development` `soft-skills`

- [audit](../mindset/ponytail/audit/) — Use when audit repo for over-engineering. Ranked list of what to delete, simplify, or replace with stdlib or native features.
  `audit` `mindset` `ponytail` `simplification`

- [business-model-canvas](../mindset/business-model-canvas/) — Design and analyze business models using the 9 building blocks of the Business Model Canvas. Use when launching, pivoting, or evaluating a business.
  `business` `canvas` `mindset` `model` `personal-development`

- [change-management](../mindset/change-management/) — Lead organizational change using Kotter's 8-step model, ADKAR framework, and stakeholder analysis. Use when rolling out major initiatives or transformations.
  `change` `management` `mindset` `personal-development` `soft-skills`

- [competitive-strategy](../mindset/competitive-strategy/) — Analyze competitors using Porter's Five Forces, positioning maps, and competitive response frameworks. Use when assessing market position or strategic threats.
  `competitive` `mindset` `personal-development` `soft-skills` `strategy`

- [conflict-resolution](../mindset/conflict-resolution/) — Resolve interpersonal and team conflicts using mediation techniques, non-violent communication, and de-escalation. Use when tensions arise between individuals or groups.
  `conflict` `mindset` `personal-development` `resolution` `soft-skills`

- [crisis-management](../mindset/crisis-management/) — Respond to crises using incident command structure, stakeholder communication, and recovery planning. Use during security breaches, PR disasters, or operational failures. Use when working with crisis management.
  `crisis` `mindset` `personal-development` `soft-skills`

- [critical-thinking](../mindset/critical-thinking/) — Use when critical thinking applied to money-making — diagnose starting position, evaluate opportunities by expected value, and execute proven income-generating strategies without asking permission.
  `critical` `mindset` `money` `business` `economics`

- [cross-cultural-communication](../mindset/cross-cultural-communication/) — Navigate cross-cultural communication using Hofstede's dimensions, high/low-context awareness, and async norms. Use when working with global teams or international stakeholders.
  `communication` `cross` `cultural` `mindset` `personal-development`

- [debt](../mindset/ponytail/debt/) — Use when harvest ponytail shortcut comments into one debt ledger so deferrals get tracked instead of forgotten.
  `debt` `mindset` `ponytail` `tracking`

- [decision-frameworks](../mindset/decision-frameworks/) — Apply structured decision frameworks like RICE, ICE, weighted scoring, and pre-mortem analysis. Use when prioritizing features, evaluating options, or making high-stakes decisions.
  `decision` `frameworks` `mindset` `personal-development` `soft-skills`

- [decision-making](../mindset/decision-making/) — Make sound decisions under uncertainty using frameworks like RICE, weighted matrix, decision trees, and pre-mortems. Use when working with decision making.
  `decision` `making` `mindset` `personal-development` `soft-skills`

- [design-thinking](../mindset/design-thinking/) — Solve complex problems through empathy, ideation, prototyping, and testing. Use when tackling ambiguous challenges with user-centered approaches.
  `design` `mindset` `personal-development` `soft-skills` `testing`

- [difficult-conversations](../mindset/difficult-conversations/) — Navigate hard talks like feedback, disagreements, and terminations using SBI, DESC, and the 3-conversations framework. Use when delivering bad news or addressing conflict.
  `conversations` `difficult` `mindset` `personal-development` `soft-skills`

- [email-mastery](../mindset/email-mastery/) — Write effective professional emails using AIDA framework, subject line formulas, and follow-up cadences. Use when crafting cold outreach, negotiation emails, or follow-ups. Use when writeing effective professional emails using aida framework, subject line formulas,.
  `email` `mastery` `mindset` `personal-development` `soft-skills`

- [emotional-intelligence](../mindset/emotional-intelligence/) — Build self-awareness, empathy, and social skills using the EQ model. Use when improving relationships, communication, or leadership effectiveness.
  `emotional` `intelligence` `mindset` `personal-development` `social-media`

- [execution](../mindset/execution/) — Ship projects reliably using goal-setting, progress tracking, and accountability. Use when moving from planning to delivery.
  `execution` `mindset` `personal-development` `soft-skills`

- [executive-presence](../mindset/executive-presence/) — Command rooms, communicate with gravitas, and project confidence. Covers body language, vocal tonality, storytelling, and handling pressure.
  `executive` `mindset` `personal-development` `presence` `soft-skills`

- [financial-literacy](../mindset/financial-literacy/) — Manage personal and business finances including budgeting, cash flow, financial statements, and basic FP&A. Use when manageing personal and business finances including budgeting, cash flow, financial.
  `financial` `literacy` `mindset` `personal-development` `soft-skills`

- [first-principles-thinking](../mindset/first-principles-thinking/) — Decompose problems to fundamental truths using Musk's method. Use when challenging assumptions, solving novel problems, or questioning conventional approaches.
  `first` `mindset` `personal-development` `principles` `soft-skills`

- [fundraising](../mindset/fundraising/) — Pitch investors using 10-slide deck structure, understand term sheets, and manage investor relations. Use when raising capital.
  `api` `fundraising` `mindset` `personal-development` `soft-skills`

- [habit-formation](../mindset/habit-formation/) — Build and maintain habits using cue-routine-reward loops, habit stacking, and environment design. Use when creating new routines or breaking old patterns.
  `formation` `habit` `mindset` `personal-development` `soft-skills`

- [help](../mindset/ponytail/help/) — Use when quick reference for ponytail modes, skills, and commands. One-shot display.
  `help` `mindset` `ponytail` `reference`

- [hiring-playbook](../mindset/hiring-playbook/) — Design jobs, source candidates, run structured interviews, and onboard effectively. Use when hiring for any role.
  `hiring` `mindset` `personal-development` `playbook` `soft-skills`

- [influence-without-authority](../mindset/influence-without-authority/) — Gain buy-in from peers, stakeholders, and executives when you lack direct authority. Covers reciprocity, social proof, and coalition building.
  `authority` `influence` `mindset` `personal-development` `social-media`

- [leadership-essentials](../mindset/leadership-essentials/) — Lead teams through vision-setting, decision-making, delegation, and accountability. Use when stepping into a leadership role or improving team performance.
  `essentials` `leadership` `mindset` `personal-development` `soft-skills`

- [mental-models](../mindset/mental-models/) — Apply 20+ mental models for better decision-making including Circle of Competence, Inversion, Second-Order Thinking, and Margin of Safety. Use when working with mental models.
  `mental` `mindset` `models` `personal-development` `soft-skills`

- [mindfulness](../mindset/mindfulness/) — Practice presence, reduce stress, and improve focus through meditation and awareness techniques. Use daily for mental clarity and emotional regulation. Use when working with mindfulness.
  `mindfulness` `mindset` `personal-development` `soft-skills`

- [negotiation-mastery](../mindset/negotiation-mastery/) — Master negotiation through BATNA analysis, anchoring, and tactical empathy. Use when negotiating deals, resolving conflicts, or structuring agreements.
  `mastery` `mindset` `negotiation` `personal-development` `soft-skills`

- [negotiation-skill](../mindset/negotiation-skill/) — Prepare for, conduct, and close negotiations. Covers separate personalities, interests, needs, BATNA, ZOPA, and effective communication tactics.
  `mindset` `negotiation` `personal-development` `rest-api` `skill`

- [networking](../mindset/networking/) — Build and maintain professional relationships through strategic outreach, events, and follow-up. Use when expanding your professional network or finding opportunities.
  `mindset` `networking` `personal-development` `soft-skills`

- [partnership-development](../mindset/partnership-development/) — Find partners, structure deals, manage co-marketing, and revenue sharing. Use when building strategic alliances or channel partnerships.
  `development` `mindset` `partnership` `personal-development` `soft-skills`

- [personal-productivity](../mindset/personal-productivity/) — Manage time, energy, and focus using GTD, Eisenhower Matrix, time blocking, and deep work. Use when optimizing personal effectiveness.
  `mindset` `personal` `personal-development` `productivity` `soft-skills`

- [persuasion-influence](../mindset/persuasion-influence/) — Apply Cialdini's 6 principles of influence ethically in business contexts. Use when pitching, selling, or driving adoption without formal authority.
  `influence` `mindset` `personal-development` `persuasion` `soft-skills`

- [ponytail](../mindset/ponytail/) — Lazy senior dev mode. Four disciplined mindsets — audit, debt, help, review — that cut complexity, track deferrals, surface reference, and catch over-engineering. Forces YAGNI, stdlib first, no unrequested abstractions. Use when working with ponytail.
  `mindset` `personal-development` `ponytail` `soft-skills` `audit`

- [presentation-design](../mindset/presentation-design/) — Design persuasive presentations using the 10/20/30 rule, slide anatomy principles, and storytelling arcs. Use when creating decks or keynotes. Use when designing persuasive presentations using the 10/20/30 rule, slide anatomy principles,.
  `design` `mindset` `personal-development` `presentation` `soft-skills`

- [pricing-frameworks](../mindset/pricing-frameworks/) — Set prices using value-based, cost-plus, competitive, and subscription models. Includes tiering, anchoring, discounts, and pricing experiments. Use when working with pricing frameworks.
  `frameworks` `mindset` `personal-development` `pricing` `soft-skills`

- [probabilistic-thinking](../mindset/probabilistic-thinking/) — Apply Bayesian updating, base rates, and expected value to decision-making. Use when reasoning under uncertainty or evaluating risks.
  `mindset` `personal-development` `probabilistic` `soft-skills` `thinking`

- [product-market-fit](../mindset/product-market-fit/) — Find and measure product-market fit using surveys, NPS, retention cohorts, and the Mom Test. Use when validating a product's viability.
  `fit` `market` `mindset` `personal-development` `product`

- [public-speaking](../mindset/public-speaking/) — Deliver engaging talks and presentations using narrative structure, audience analysis, and stage presence techniques. Use when working with public speaking.
  `mindset` `personal-development` `public` `soft-skills` `speaking`

- [remote-work](../mindset/remote-work/) — Work effectively remotely including async communication, documentation, video meetings, and self-management in distributed teams. Use when working with remote work.
  `mindset` `personal-development` `remote` `soft-skills` `video`

- [resilience](../mindset/resilience/) — Build mental toughness, recover from setbacks, and adapt to change. Use when navigating failure, crisis, or high-pressure environments.
  `mindset` `personal-development` `resilience` `soft-skills`

- [review](../mindset/ponytail/review/) — Use when review a diff for over-engineering. Finds what to delete — reinvented stdlib, needless deps, speculative abstractions.
  `review` `mindset` `ponytail` `simplification`

- [root-cause-analysis](../mindset/root-cause-analysis/) — Diagnose root causes using 5 Whys, fishbone diagrams, fault trees, and Pareto analysis. Use when troubleshooting recurring problems or post-incident analysis.
  `cause` `mindset` `personal-development` `root` `soft-skills`

- [scenario-planning](../mindset/scenario-planning/) — Plan for uncertainty using best/worst/likely scenarios, war-gaming, and trigger-based pivots. Use when facing high uncertainty or preparing for strategic decisions.
  `mindset` `personal-development` `planning` `scenario` `soft-skills`

- [servant-leadership](../mindset/servant-leadership/) — Lead by serving using Greenleaf's 10 characteristics. Use when empowering teams, removing obstacles, or building trust-based leadership.
  `leadership` `mindset` `personal-development` `servant` `soft-skills`

- [stakeholder-management](../mindset/stakeholder-management/) — Map, engage, and align stakeholders using the power-interest grid, RACI matrix, and communication plans. Use when navigating complex projects or organizational politics. Use when working with stakeholder management.
  `mindset` `personal-development` `rest-api` `soft-skills` `stakeholder`

- [storytelling-frameworks](../mindset/storytelling-frameworks/) — Structure narratives for pitches, content, and communication using Hero's Journey, Before-After-Bridge, and Pixar pitch templates. Use when working with storytelling frameworks.
  `frameworks` `mindset` `personal-development` `soft-skills` `storytelling`

- [strategic-planning](../mindset/strategic-planning/) — Set strategy using OKRs, roadmaps, quarterly planning, and review cadences. Use when defining direction or aligning teams on goals.
  `mindset` `personal-development` `planning` `soft-skills` `strategic`

- [stress-management](../mindset/stress-management/) — Manage stress through breathing techniques, exercise, sleep hygiene, and cognitive reframing. Use when overwhelmed or at risk of burnout.
  `management` `mindset` `personal-development` `soft-skills` `stress`

- [systems-thinking](../mindset/systems-thinking/) — Understand feedback loops, leverage points, and system archetypes to solve complex problems. Use when addressing recurring issues or unintended consequences.
  `mindset` `personal-development` `soft-skills` `systems` `thinking`

- [team-management](../mindset/team-management/) — Manage teams through 1:1s, feedback (SBI model), delegation (70% rule), and performance reviews. Use when leading individual contributors or managers.
  `management` `mindset` `personal-development` `soft-skills` `team`

- [time-management](../mindset/time-management/) — Prioritize tasks, manage schedules, and avoid burnout using Eisenhower Matrix, time blocking, and Pomodoro technique. Use when working with time management.
  `management` `mindset` `personal-development` `soft-skills` `time`

- [trade-off-analysis](../mindset/trade-off-analysis/) — Evaluate opportunity costs and prioritize using Eisenhower Matrix, MoSCoW, and cost of delay. Use when prioritizing with constrained resources.
  `mindset` `off` `personal-development` `soft-skills` `trade`

- [unit-economics](../mindset/unit-economics/) — Calculate CAC, LTV, margins, payback period, and cohort analysis. Use when evaluating business model sustainability or optimizing growth efficiency.
  `economics` `mindset` `personal-development` `soft-skills` `unit`

### Operations (operations/)

_Total: 19 skills_

Browse in [`operations/_index.md`](../operations/_index.md).

- [auth-patterns](../operations/auth-patterns/) — Authentication patterns — OAuth 2.0, JWT, session management, MFA, RBAC, API key management. Use when working with auth patterns.
  `api` `auth` `business-ops` `management` `operations`

- [business-intelligence](../operations/business-intelligence/) — Define and track KPIs across revenue, marketing, and content performance with weekly business reviews and data-driven decisions. Use when working with business intelligence.
  `business` `business-ops` `intelligence` `management` `operations`

- [clickup](../operations/clickup/) — Skill: clickup. See SKILL.md body for details. Use when this domain is relevant.
  `business-ops` `clickup` `management` `operations`

- [contract-manager](../operations/contract-manager/) — Contract lifecycle management — draft, review, negotiate, sign, track, archive. Covers talent agreements, client deals, vendor contracts, employment. Indonesian law compliant (PKS format). Telegram alerts for renewals and breaches.
  `contracts` `legal` `operations` `talent` `indonesian-law`

- [customer-success](../operations/customer-success/) — Automated customer onboarding, health scoring, churn prediction, proactive outreach, and support ticket resolution
  `business-ops` `customer` `management` `operations` `success`

- [finance-ops](../operations/finance-ops/) — Run AI-powered CFO analysis for cost detection, financial modeling, scenario planning, and operational efficiency optimization. Use when working with finance ops.
  `business-ops` `finance` `management` `operations` `ops`

- [financial-automation](../operations/financial-automation/) — AI CFO for solo businesses — invoicing, expense categorization, tax optimization, cash flow forecasting, multi-currency management. Use when working with financial automation.
  `automation` `business-ops` `financial` `management` `operations`

- [governance-team](../operations/governance-team/) — Manage organizational policies, access control, compliance frameworks, and governance processes with radical transparency principles. Use when manageing organizational policies, access control, compliance frameworks, and governance processes.
  `business-ops` `compliance` `governance` `management` `operations`

- [hr-onboarding](../operations/hr-onboarding/) — Design onboarding programs, manage new hire paperwork, and track 30-60-90 day milestones. Use when scaling teams or improving retention.
  `business-ops` `management` `onboarding` `operations`

- [jira](../operations/jira/) — Skill: jira. See SKILL.md body for details. Use when this domain is relevant.
  `business-ops` `jira` `management` `operations`

- [legal-assistant](../operations/legal-assistant/) — Use when legal assistant — contract review checklists, IP protection, business compliance, GDPR/privacy for digital products, DMCA, software licensing, employment law, and dispute resolution. Built for 1-person companies scaling to team.
  `legal` `compliance` `ip` `gdpr` `indonesia`

- [legal-compliance](../operations/legal-compliance/) — Contract generation, terms of service, privacy policies, GDPR/CCPA compliance checks, regulatory monitoring, entity management. Use when working with legal compliance.
  `business-ops` `compliance` `legal` `management` `monitoring`

- [multi-channel-reminder](../operations/multi-channel-reminder/) — Skill: multi-channel-reminder. See SKILL.md body for details. Use when this domain is relevant.
  `business-ops` `channel` `management` `multi` `operations`

- [operations-team](../operations/team/) — Execute SOPs, triage on-call incidents, manage SLA breaches, and drive continuous improvement using lean operations principles. Use when working with operations team.
  `business-ops` `management` `operations` `team`

- [payment-gateways](../operations/payment-gateways/) — Payment gateway integration — Stripe, Paddle, Lemon Squeezy, dunning, subscription management. Use when working with payment gateways.
  `business-ops` `gateways` `management` `operations` `payment`

- [payment-invoicing](../operations/payment-invoicing/) — Process payments and generate invoices using Indonesian payment gateways (TriPay, LYNK.ID, Midtrans). Create payment links, track transactions, and automate invoicing for 1-man company revenue collection.
  `business-ops` `invoicing` `management` `operations` `payment`

- [product-team](../operations/product-team/) — Manage PRD creation, roadmap planning, sprint coordination, and release management with Notion integration. Use when manageing prd creation, roadmap planning, sprint coordination, and release management.
  `business-ops` `management` `notion` `operations` `product`

- [project-management](../operations/project-management/) — Coordinate sprints, track deadlines, manage tasks, and maintain project documentation with Notion and Slack. Use when working with project management.
  `business-ops` `management` `notion` `operations` `project`

- [revenue-team](../operations/revenue-team/) — Manage sales pipelines, forecast revenue, track deals, and optimize sales velocity with HubSpot and Notion integration. Use when manageing sales pipelines, forecast revenue, track deals, and optimize sales.
  `business-ops` `management` `notion` `operations` `pipeline`

### Productivity (productivity/)

_Total: 10 skills_

Browse in [`productivity/_index.md`](../productivity/_index.md).

- [calendar-management](../productivity/calendar-management/) — Advanced calendar management, scheduling, and meeting automation with Google Calendar MCP. Use when working with calendar management.
  `calendar` `management` `productivity` `time-management` `tools`

- [career-ops](../productivity/career-ops/) — AI-powered job search system — CV optimization, ATS scanning, interview prep, application tracking. Use when job searching, writing CVs, preparing for interviews, tracking applications,.
  `career` `job-search` `cv` `resume` `interview`

- [email-automation](../productivity/email-automation/) — Automate email workflows, templates, and campaigns with Gmail MCP integration
  `email` `productivity` `time-management` `tools` `workflow`

- [focus-time-management](../productivity/focus-time-management/) — Deep work scheduling, time blocking, Pomodoro technique, distraction management, and energy-aware productivity. Use when optimizing focus time, building work schedules, or managing distractions.
  `focus` `deep-work` `time-blocking` `pomodoro` `productivity`

- [google-canvas](../productivity/google-canvas/) — Use when creating, opening, reading, editing, or collaborating on Google Canvas documents and Gemini Canvas shared applications through browser automation.
  `canvas` `google` `productivity` `time-management` `tools`

- [google-flow](../productivity/google-flow/) — Use when navigating and operating Google Flow (labs.google/fx/tools/flow) - an AI video generation tool. Helps with project management, scenebuilder interface, prompt entry, preset selection, model configuration, and video generation workflow.
  `flow` `google` `productivity` `time-management` `tools`

- [google-workspace](../productivity/google-workspace/) — Integrate with Google Workspace (Docs, Sheets, Drive, Calendar) using MCP servers. Use when integrateing with google workspace (docs, sheets, drive, calendar) using mcp.
  `google` `productivity` `time-management` `tools` `workspace`

- [meeting-management](../productivity/meeting-management/) — AI-powered meeting management — agenda creation, note-taking, action item extraction, follow-up tracking. Use when planning meetings, capturing decisions, or tracking meeting outcomes.
  `meetings` `notes` `action-items` `agenda` `follow-up`

- [nocode-orchestrator](../productivity/nocode-orchestrator/) — Build and manage automations across Make.com, n8n, Zapier, and Pipedream — onboarding, support tickets, content approval, invoice processing. Use when building and manage automations across make.com, n8n, zapier, and pipedream.
  `api` `nocode` `orchestrator` `productivity` `time-management`

- [notion](../productivity/notion/) — Automate Notion workflows including database CRUD, page creation, content publishing, and workspace management via API.
  `api` `notion` `productivity` `time-management` `tools`

### Research (research/)

_Total: 23 skills_

Browse in [`research/_index.md`](../research/_index.md).

- [ai-research-agent](../research/ai-research-agent/) — Autonomous research agent that monitors trends, discovers income opportunities, and creates new skills — runs daily research cycles to keep the one-man-company evolving. Use when working with ai research agent.
  `agent` `ai-agent` `analysis` `investigation` `research`

- [best-hacker](../research/best-hacker/) — Apply hacker mindset to find vulnerabilities, break assumptions, and stress-test systems before attackers do. Use when working with best hacker.
  `analysis` `best` `hacker` `investigation` `research`

- [competitive-intelligence](../research/competitive-intelligence/) — Continuous competitor monitoring — pricing changes, feature launches, job postings, ad spend, SEO rankings, social media activity — with weekly intelligence briefs and strategic recommendations. Use when working with competitive intelligence.
  `analysis` `competitive` `intelligence` `investigation` `monitoring`

- [continuous-learning](../research/continuous-learning/) — Transform session insights into actionable skills with confidence-weighted scoring — captures patterns, analyzes outcomes, and integrates learnings to improve agent performance. Use when working with continuous learning.
  `ai-agent` `analysis` `continuous` `investigation` `learning`

- [data-pipeline-engine](../research/data-pipeline-engine/) — ETL pipelines that pull data from multiple sources (APIs, databases, web scraping), transform it, and produce actionable dashboards and reports. Use when working with data pipeline engine.
  `analysis` `api` `data` `engine` `investigation`

- [dispatching-parallel-agents](../research/dispatching-parallel-agents/) — Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
  `agents` `analysis` `dispatching` `investigation` `parallel`

- [feynman-science](../research/feynman-science/) — Explain complex concepts simply using Feynman's technique: teach, identify gaps, simplify, and analogize. Use when working with feynman science.
  `analysis` `feynman` `investigation` `learning` `teaching`

- [finance-trading](../research/finance-trading/) — Analyze financial markets using technical indicators, fundamental analysis, and macro trends. Use for investment research.
  `analysis` `finance` `investigation` `research` `trading`

- [grok-browser](../research/grok-browser/) — Use Grok's browser capabilities to search the web, analyze pages, and synthesize real-time information. Use when working with grok browser.
  `analysis` `browser` `grok` `investigation` `research`

- [maybe-hft](../research/maybe-hft/) — Hedging EA dengan sistem trailing stop dan pending order otomatis. Converted dari MQL5, cross-platform (Windows/Linux/Mac). Compatible dengan mt5linux Docker. Use when working with maybe hft.
  `analysis` `docker` `hft` `investigation` `maybe`

- [mckinsey-research](../research/mckinsey-research/) — Use when running McKinsey-level market research and strategy analysis - competitive analysis, TAM analysis, pricing strategy, go-to-market planning, and business strategy.
  `analysis` `investigation` `mckinsey` `research`

- [musk-first-principles](../research/musk-first-principles/) — Break problems down to fundamental truths and reason up using Elon Musk's first-principles methodology. Use when working with musk first principles.
  `analysis` `first` `investigation` `musk` `principles`

- [opportunity-exploitation](../research/opportunity-exploitation/) — Identify and evaluate market opportunities using Jeff Bezos' customer-obsession and long-term thinking frameworks. Use when working with opportunity exploitation.
  `analysis` `bezos` `customer-obsession` `exploitation` `flywheel`

- [polymarket-analyst](../research/polymarket-analyst/) — Analyze Polymarket prediction markets for expected value, market inefficiencies, and trading opportunities. Use when analyzeing polymarket prediction markets for expected value, market inefficiencies, and.
  `analysis` `analyst` `investigation` `polymarket` `research`

- [rockefeller-wealth](../research/rockefeller-wealth/) — Apply Rockefeller's systematic wealth-building strategies: vertical integration, capital allocation, and monopoly thinking. . Use when working with rockefeller wealth.
  `analysis` `api` `investigation` `research` `rockefeller`

- [rothschild-investment](../research/rothschild-investment/) — Apply Rothschild dynasty principles for long-term wealth preservation, diversification, and generational planning. Use when working with rothschild investment.
  `analysis` `investigation` `investment` `research` `rothschild`

- [sherlock-research](../research/sherlock-research/) — Investigate problems systematically using Sherlock Holmes' method: observe, deduce, hypothesize, and verify. . Use when working with sherlock research.
  `analysis` `investigation` `research` `sherlock`

- [social-intelligence](../research/social-intelligence/) — Cross-platform social media intelligence gathering using Agent Reach. Research trends, sentiment, competitive intel, and user insights from Twitter, Reddit, YouTube, XiaoHongShu across 35+ platforms. Use when researching social proof, market sentiment, viral content patterns, or competitive positioning.
  `social-media` `research` `sentiment-analysis` `competitive-intelligence` `trend-monitoring`

- [steve-jobs-product](../research/steve-jobs-product/) — Design products using Steve Jobs' philosophy: simplicity, user experience, intersection of technology and liberal arts. . Use when working with steve jobs product.
  `analysis` `investigation` `jobs` `product` `research`

- [super-browser](../research/super-browser/) — The ultimate browser automation framework combining the best of 8 top-rated browser skills for unified local or cloud-based web task automation. Use when working with super browser.
  `analysis` `browser` `investigation` `research` `super`

- [trendradar](../research/trendradar/) — AI-powered trending topic monitoring from 35+ platforms. Aggregate trends, analyze sentiment, and get real-time notifications. Based on TrendRadar MCP server (4.5K+ stars). Use when working with trendradar.
  `analysis` `investigation` `monitoring` `research` `trendradar`

- [value-investing](../research/value-investing/) — Evaluate stocks using Warren Buffett's value investing: intrinsic value, margin of safety, and long-term moats. . Use when working with value investing.
  `analysis` `investigation` `investing` `research` `value`

- [zhive](../research/zhive/) — Skill: zhive. See SKILL.md body for details. Use when this domain is relevant.
  `analysis` `investigation` `research` `zhive`

### Sales (sales/)

_Total: 13 skills_

Browse in [`sales/_index.md`](../sales/_index.md).

- [ai-agent-development](../sales/ai-agent-development/) — Build and sell custom AI agents as services or products. Create vertical-specific AI solutions for clients and generate $2K-$8K/month recurring revenue.
  `agent` `ai-agent` `business-development` `revenue` `sales`

- [ai-consulting](../sales/ai-consulting/) — Offer fractional AI engineering and consulting services. Act as a part-time AI executive for companies that can't afford full-time AI staff. Generate $3K-10K/month.
  `business-development` `consulting` `revenue` `sales`

- [ai-lead-generation](../sales/ai-lead-generation/) — Automated AI-powered lead generation and prospecting. Find ideal customers, enrich data, personalize outreach, and book meetings without manual effort. Use when generating B2B leads at scale.
  `business-development` `generation` `lead` `revenue` `sales`

- [ai-marketplace](../sales/ai-marketplace/) — Sell AI-powered services on Fiverr, Upwork, and Toptal. Offer automation, content, and development services. Build recurring clients and generate $2K-10K/month.
  `business-development` `marketplace` `revenue` `sales`

- [b2b-sales-automation](../sales/b2b-sales-automation/) — |
  >
    Full B2B sales pipeline automation — from cold prospect to onboarded client.
    Covers ICP definition, lead sourcing, outreach sequences, proposal generation, CRM tracking,
    and deal alerts via   Telegram. Targets SMEs needing AI automation, digital products,
    and content services.

  `sales` `b2b` `crm` `outreach` `proposal`

- [business-development](../sales/business-development/) — Generate leads, research prospects, and manage outreach sequences with HubSpot and Exa integration. Use for B2B pipeline building.
  `business` `business-development` `pipeline` `revenue` `sales`

- [customer-support](../sales/customer-support/) — Use when handling customer support via browser - email responses, chat interactions, ticket management, and escalation workflows.
  `business-development` `customer` `email` `revenue` `sales`

- [high-ticket-closing](../sales/high-ticket-closing/) — Jordan Belfort's Straight Line System - closing high-value deals through persuasion and psychology. Use when working with high ticket closing.
  `business-development` `closing` `high` `revenue` `sales`

- [influencer-scouting](../sales/influencer-scouting/) — |
  >
    Full influencer scouting, outreach, and performance tracking system.
    Covers   platform search across TikTok, Instagram, and YouTube for creators,
    scoring/qualification, DM outreach,   negotiation, deal tracking, and ROI measurement.
    Integrates with Kalodata for TikTok analytics.

  `influencer` `marketing` `tiktok` `instagram` `youtube`

- [sales-pipeline](../sales/pipeline/) — AI-powered sales pipeline inside 1ai-social. Track leads, qualify with BANT, generate proposals, schedule follow-ups, and get daily sales analytics. Use when managing B2B sales pipelines.
  `sales` `pipeline` `crm` `lead-scoring` `proposals`

- [sales-strategy](../sales/strategy/) — Build sales playbooks, define pipeline stages, and optimize conversion rates. Use when designing or improving the sales process.
  `business-development` `pipeline` `revenue` `sales` `strategy`

- [shopee-review-downloader](../sales/shopee-review-downloader/) — Download and analyze Shopee product reviews in bulk for competitive research, sentiment analysis, and market intelligence. Use when working with shopee review downloader.
  `business-development` `downloader` `revenue` `review` `sales`

- [talent-crm](../sales/talent-crm/) — Manage talent pipeline with candidate tracking, outreach automation, and interview scheduling. Use for recruiting CRM.
  `business-development` `crm` `pipeline` `revenue` `sales`

### Trading (trading/)

_Total: 19 skills_

Browse in [`trading/_index.md`](../trading/_index.md).

- [alphaear-strategy](../trading/alphaear-strategy/) — Score trading setups using AlphaEar multi-factor analysis (momentum, volume, sentiment). Use when evaluating entry/exit signals.
  `algorithms` `alphaear` `markets` `money` `strategy`

- [black-edge](../trading/black-edge/) — Apply institutional trading edge using order flow analysis, market microstructure, and dark pool signals. Use when working with black edge.
  `algorithms` `black` `edge` `markets` `trading`

- [crypto-trading-bot](../trading/crypto-trading-bot/) — 加密貨幣交易機器人開發 - 幫你整自動交易Bot，支持Pine Script、Python、CCXT API對接。適用於：(1)整TradingView信號Bot (2)CEX/DEX API自動化 (3)套利機器人 (4)止盈止損策略. Use when working with crypto trading bot.
  `algorithms` `api` `bot` `crypto` `markets`

- [crypto-wallet](../trading/crypto-wallet/) — Skill: crypto-wallet. See SKILL.md body for details. Use when this domain is relevant.
  `algorithms` `crypto` `markets` `trading` `wallet`

- [defi-protocols](../trading/defi-protocols/) — Skill: defi-protocols. See SKILL.md body for details. Use when this domain is relevant.
  `algorithms` `defi` `markets` `protocols` `trading`

- [investing-algorithm-framework](../trading/investing-algorithm-framework/) — Build algorithmic investing strategies with backtesting, signal generation, and portfolio optimization frameworks. Use when building algorithmic investing strategies with backtesting, signal generation, and portfolio.
  `algorithm` `algorithms` `framework` `investing` `markets`

- [nft-marketplace](../trading/nft-marketplace/) — Skill: nft-marketplace. See SKILL.md body for details. Use when this domain is relevant.
  `algorithms` `marketplace` `markets` `nft` `trading`

- [polymarket](../trading/polymarket/) — Natural-language interface to Polymarket prediction markets. Ask questions about event probabilities, market odds, price movements, and betting strategies in plain English. event probabilities, or when user asks about Polymarket data. Use when working with polymarket.
  `algorithms` `markets` `polymarket` `trading`

- [polymarket-fast-loop](../trading/polymarket-fast-loop/) — Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API. Default signal is Binance BTC/USDT klines. Use when user wants to trade sprint/fast markets, automate short-term crypto trading, or use CEX momentum as a Polymarket signal.
  `algorithms` `api` `crypto` `fast` `loop`

- [polymarket-weather-trader](../trading/polymarket-weather-trader/) — Trade Polymarket weather markets using NOAA forecasts via Simmer API. Inspired by gopfan2's $2M+ strategy. Use when user wants to trade temperature markets, automate weather bets, check NOAA forecasts, or run gopfan2-style trading.
  `algorithms` `api` `markets` `polymarket` `trader`

- [portfolio-manager](../trading/portfolio-manager/) — Use when portfolio manager — capital allocation, risk management, and performance metrics tracking for trading strategies.
  `algorithms` `manager` `markets` `portfolio` `trading`

- [smart-contract-dev](../trading/smart-contract-dev/) — Skill: smart-contract-dev. See SKILL.md body for details. Use when this domain is relevant.
  `algorithms` `contract` `dev` `markets` `smart`

- [trading-executor](../trading/executor/) — Execute trades via API with position sizing, order management, and slippage monitoring. Use when placing orders on exchanges.
  `algorithms` `api` `executor` `markets` `monitoring`

- [trading-orchestrator](../trading/orchestrator/) — Coordinate multi-strategy trading workflows by routing signals to the right executor and managing risk limits. Use when working with trading orchestrator.
  `algorithms` `markets` `orchestrator` `trading` `workflow`

- [trading-researcher](../trading/researcher/) — Research market conditions, on-chain data, and sentiment to identify trading opportunities. Use for market analysis.
  `algorithms` `markets` `researcher` `trading`

- [trading-risk-manager](../trading/risk-manager/) — Monitor portfolio risk, enforce position limits, and trigger stop-losses. Use when managing exposure across strategies.
  `algorithms` `manager` `markets` `risk` `trading`

- [trading-strategist](../trading/strategist/) — Design and backtest trading strategies using technical indicators, fundamental analysis, and statistical models. Use when designing and backtesting trading strategies.
  `algorithms` `markets` `strategist` `trading` `money`

- [tushare-finance](../trading/tushare-finance/) — 获取中国金融市场数据（A股、港股、美股、基金、期货、债券）。支持220+个Tushare Pro接口：股票行情、财务报表、宏观经济指标。当用户请求股价数据、财务分析、指数行情、GDP/CPI等宏观数据时使用。. Use when working with tushare finance.
  `algorithms` `finance` `markets` `trading` `tushare`

- [xauusd-asia-7c-breakout](../trading/xauusd-asia-7c-breakout/) — XAUUSD Asia 7-Candle Breakout strategy with backtest, paper trade, and real trade modes. Use when trading gold on the Asia session breakout strategy, running historical backtests, setting up paper trading simulations, or executing live trades with the 7-candle breakout system.
  `algorithms` `asia` `breakout` `markets` `money`

---
_Generated from 1306 skills across 19 categories._
