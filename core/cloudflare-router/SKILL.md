---
name: cloudflare-router
description: Manage Cloudflare DNS, CDN, and security rules via API. Use when configuring domains, SSL, WAF, or edge caching.
domain: core
tags:
- api
- cloudflare
- infrastructure
- memory
- router
- self-improvement
persona:
  name: Matthew Prince
  title: The Edge Network Expert - Master of Global Routing
  expertise:
  - Edge Computing
  - CDN
  - Network Security
  - Global Routing
  philosophy: The network is the computer.
  credentials:
  - CEO of Cloudflare
  - Built one of the largest edge networks
  - Pioneer of serverless edge
  principles:
  - Route to nearest edge
  - Cache aggressively
  - Secure by default
  - Scale globally
---
# Cloudflare Router

## When to Use

- Adding new subdomains pointing to local services
- Managing Cloudflare Tunnel ingress rules
- Generating nginx reverse proxy configs
- Deploying DNS records to Cloudflare
- Monitoring service health and status

## Overview

Cloudflare Router is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

