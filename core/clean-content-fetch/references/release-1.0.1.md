# Scrapling Web Fetch 1.0.1

## 中文功能描述

Scrapling Web Fetch 是一个面向现代网页正文提取的 OpenClaw Skill，默认使用 **Scrapling + html2text** 管线获取网页内容。

### 主要特点
- **支持微信公众号文章抓取**：可抓取 `mp.weixin.qq.com` 文章正文。
- **自动清洗微信公众号尾部噪音**：会去掉“继续滑动看下一个”“轻触阅读原文”“扫码打开”“小程序提示”“Allow/Cancel/Got It”等无用容器内容。
- **节省 token**：是的，**清洗无用信息本质上会节省 token**，因为输出内容更短、更聚焦正文，后续总结/分析时上下文占用更低。
- **适合很多有反爬的网站**：依赖 Scrapling 的现代网页抓取能力，适合处理普通 requests/fetch 不稳定、页面结构复杂、存在一定反爬/动态渲染干扰的网页。
- **正文提取更稳**：按 `article → main → .post-content → [class*="body"] → body` 的顺序优先提取正文。
- **支持 Markdown 输出**：抓取后直接转成 Markdown，更适合总结、归档、二次处理。
- **支持 JSON 输出**：方便程序化接入。
- **支持批量抓取**：可一次抓多个 URL。
- **支持站点级 selector 覆盖**：可为特定网站定制正文 selector。
- **内置基础质量评分**：方便判断抓到的是不是高质量正文。

### 适用场景
- 抓取新闻、博客、公告、公众号文章正文
- 把网页内容转成 Markdown 供总结/翻译/分析
- 对抗普通 fetch 难以稳定获取内容的现代网页
- 做批量资讯采集与清洗

## English Description

Scrapling Web Fetch is an OpenClaw skill for extracting readable main content from modern web pages using a **Scrapling + html2text** pipeline.

### Key Features
- **WeChat article support**: Can fetch content from `mp.weixin.qq.com` pages.
- **Automatic WeChat tail-noise cleanup**: Removes common noisy footer/UI artifacts such as “continue scrolling”, “read original”, QR/open-in-WeChat prompts, mini-program prompts, and modal button text like Allow / Cancel / Got It.
- **Token saving**: Yes — **cleaning noisy content reduces token usage** because the final output is shorter and more focused on the actual article body.
- **Works well on many anti-bot / hard-to-fetch pages**: Built on Scrapling, which is better suited for modern pages with anti-bot friction, dynamic markup, and unstable generic fetch results.
- **Stable body extraction strategy**: Uses the selector priority `article → main → .post-content → [class*="body"] → body`.
- **Markdown output by default**: Better for summarization, archiving, and downstream processing.
- **JSON output available**: Easy to integrate programmatically.
- **Batch mode**: Fetch multiple URLs in one run.
- **Site-specific selector overrides**: Customize extraction rules per domain.
- **Basic quality scoring**: Helps estimate whether the extracted content looks like a real article body.

### Good For
- News/blog/article extraction
- WeChat article cleanup
- Converting pages into markdown for AI summarization
- Batch content collection pipelines
- Pages where simple requests/fetch often fail or produce noisy output
