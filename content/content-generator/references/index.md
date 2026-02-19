# Content Generator API Reference

Complete API reference documentation for the Content Generator project.

## Table of Contents

### Providers

| Module | Description |
|--------|-------------|
| [providers/index](./providers/index.md) | Overview of all AI providers |
| [providers/base](./providers/base.md) | AIProvider base classes and interfaces |
| [providers/nvidia](./providers/nvidia.md) | NVIDIA NIM for image generation |
| [providers/byteplus](./providers/byteplus.md) | BytePlus Seedance for video generation |
| [providers/groq](./providers/groq.md) | Groq for fast LLM inference |

### Platforms

| Module | Description |
|--------|-------------|
| [platforms](./platforms.md) | Platform specifications and enums |

### Video Processing

| Module | Description |
|--------|-------------|
| [ffmpeg](./ffmpeg.md) | Basic FFmpeg operations |
| [ffmpeg_editor](./ffmpeg_editor.md) | Advanced FFmpeg editor class |

### Processing

| Module | Description |
|--------|-------------|
| [batch_processor](./batch_processor.md) | Concurrent batch processing |
| [scheduler](./scheduler.md) | Scheduled content posting |

---

## Quick Links

- [Main README](../README.md)
- [CLI Usage](../README.md#cli-usage)
- [Configuration](../README.md#configuration)

---

## Overview

The Content Generator is organized into several key modules:

1. **Providers** - AI content generation backends (NVIDIA, BytePlus, Groq, etc.)
2. **Platforms** - Social media platform specifications (TikTok, YouTube, Instagram, Facebook)
3. **FFmpeg** - Video processing and editing
4. **Batch Processing** - Concurrent job handling
5. **Scheduler** - Automated posting management
