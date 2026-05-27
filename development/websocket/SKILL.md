---
name: websocket
description: WebSocket development — real-time bidirectional communication, Socket.IO, native WebSocket API, scaling patterns
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

- Chat applications and messaging systems
- Live dashboards and real-time data feeds
- Collaborative editing (Google Docs-style)
- Multiplayer games
- Stock/crypto price streaming
- IoT device communication
- Progress bars and live status updates

## Pseudo Code

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
