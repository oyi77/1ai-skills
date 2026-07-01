---
name: websocket
description: WebSocket development — real-time bidirectional communication, Socket.IO, native WebSocket API, scaling patterns. Use when working with websocket.
domain: development
tags:
- api
- coding
- software-engineering
- testing
- websocket
---


## Overview

WebSocket enables persistent, full-duplex communication between client and server over a single TCP connection. This skill covers the native WebSocket API, Socket.IO for feature-rich real-time apps, and scaling patterns for production deployments.

## Capabilities

- Build real-time features: chat, live dashboards, notifications, collaborative editing
- Implement WebSocket servers with native `ws` library or Socket.IO
- Handle connection lifecycle: open, heartbeat, reconnect, close
- Authenticate WebSocket connections during the upgrade handshake
- Scale horizontally with Redis adapter for pub/sub across instances
- Implement rooms/namespaces for message routing
- Handle backpressure and message queuing

## When to Use
**Trigger phrases:**
- "websocket"
- "WebSocket development — real-time bidirectional communication, Socket"


- Chat applications and messaging systems
- Live dashboards and real-time data feeds
- Collaborative editing (Google Docs-style)
- Multiplayer games
- Stock/crypto price streaming
- IoT device communication
- Progress bars and live status updates

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The websocket workflow follows a standard pipeline pattern.

Core flow:
```
# websocket primary flow
input = prepare(raw_data)
result = process(input, config={bidirectional, communication, development, native, patterns})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Native WebSocket Server
```javascript
// server.js — using 'ws' library
const { WebSocketServer } = require('ws');
const http = require('http');

const server = http.createServer();
const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
  const userId = authenticateUpgrade(req);
  if (!userId) {
    ws.close(4001, 'Unauthorized');
    return;
  }

  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    // Broadcast to all clients
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({ from: userId, ...msg }));
      }
    });
  });

  ws.on('close', () => console.log(`User ${userId} disconnected`));
});

// Heartbeat to detect dead connections
setInterval(() => {
  wss.clients.forEach(ws => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

server.listen(8080);
```

### Socket.IO with Rooms
```javascript
// server.js — Socket.IO
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const io = new Server(httpServer, {
  cors: { origin: 'https://app.example.com' },
});

// Redis adapter for horizontal scaling
const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();
await Promise.all([pubClient.connect(), subClient.connect()]);
io.adapter(createAdapter(pubClient, subClient));

// Authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  const user = verifyToken(token);
  if (!user) return next(new Error('Unauthorized'));
  socket.user = user;
  next();
});

io.on('connection', (socket) => {
  console.log(`${socket.user.name} connected`);

  // Join a room
  socket.on('join-room', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('user-joined', socket.user.name);
  });

  // Room-scoped messaging
  socket.on('send-message', ({ roomId, text }) => {
    io.to(roomId).emit('new-message', {
      from: socket.user.name,
      text,
      timestamp: Date.now(),
    });
  });

  // Typing indicator
  socket.on('typing', (roomId) => {
    socket.to(roomId).emit('user-typing', socket.user.name);
  });

  socket.on('disconnect', () => {
    io.emit('user-left', socket.user.name);
  });
});
```

### Client-Side (Browser)
```javascript
// client.js
import { io } from 'socket.io-client';

const socket = io('https://api.example.com', {
  auth: { token: getAuthToken() },
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 10,
});

socket.on('connect', () => console.log('Connected:', socket.id));
socket.on('connect_error', (err) => console.error('Connection failed:', err.message));

// Join room and listen
socket.emit('join-room', 'room-123');
socket.on('new-message', (msg) => {
  appendToChat(msg);
});

// Send message
socket.emit('send-message', { roomId: 'room-123', text: 'Hello!' });
```

### Reconnection with Exponential Backoff
```javascript
const socket = io('https://api.example.com', {
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 30000,
  reconnectionAttempts: Infinity,
  // Exponential backoff: 1s, 2s, 4s, 8s... up to 30s
});
```

## Common Patterns

Proven patterns for websocket usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Namespace Isolation
```javascript
// Separate namespaces for different features
const chatNs = io.of('/chat');
const notifNs = io.of('/notifications');

chatNs.on('connection', (socket) => { /* chat logic */ });
notifNs.on('connection', (socket) => { /* notification logic */ });
```

### Binary Data Transfer
```javascript
// Send binary data (images, files)
socket.emit('file-chunk', buffer);

// Receive
socket.on('file-chunk', (buffer) => {
  const blob = new Blob([buffer]);
});
```

### Rate Limiting
```javascript
io.use((socket, next) => {
  const rateLimiter = new Map();
  socket.onAny((event) => {
    const now = Date.now();
    const last = rateLimiter.get(event) || 0;
    if (now - last < 100) return; // 10 events/sec max
    rateLimiter.set(event, now);
  });
  next();
});
```

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |