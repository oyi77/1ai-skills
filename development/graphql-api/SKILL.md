---
name: graphql-api
description: Use when graphQL API development — schema design, resolvers, subscriptions,
  federation. Apollo, Relay, performance optimization. Use when working with graphql
  api.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- api
- coding
- graphql
- software-engineering
- testing
version: 1.0.0
category: development
---



## Overview

GraphQL provides a flexible query language for APIs that lets clients request exactly the data they need. This skill covers schema design, resolver implementation, real-time subscriptions, and performance optimization patterns for production GraphQL APIs.

## Capabilities

- Design type-safe GraphQL schemas with SDL
- Implement resolvers with DataLoader for N+1 prevention
- Build real-time subscriptions over WebSocket
- Set up Apollo Server/Client for full-stack GraphQL
- Implement authentication and authorization at the resolver level
- Optimize query performance with persisted queries and caching
- Test GraphQL APIs with operation-level assertions

## When to Use
**Trigger phrases:**
- "graphql api"
- "GraphQL API development — schema design, resolvers, subscriptions, federation"


- Building APIs where clients need flexible data fetching
- Mobile apps requiring bandwidth-efficient queries
- Microservices needing a unified API gateway
- Real-time features like chat, notifications, live dashboards
- Replacing multiple REST endpoints with a single GraphQL endpoint

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The graphql-api workflow follows a standard pipeline pattern.

Core flow:
```
# graphql-api primary flow
input = prepare(raw_data)
result = process(input, config={api, apollo, design, development, federation})
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


### Schema Design
```graphql
# schema.graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, limit: Int): [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}

type Subscription {
  userCreated: User!
  messageSent(channelId: ID!): Message!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!       # Resolved via DataLoader
  createdAt: DateTime!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

### Resolver with DataLoader (N+1 Prevention)
```javascript
// resolvers/user.js
const DataLoader = require('dataloader');

// Batch function: loads users by IDs in single query
const userLoader = new DataLoader(async (userIds) => {
  const users = await db.users.findByIds(userIds);
  return userIds.map(id => users.find(u => u.id === id) || null);
});

const resolvers = {
  Query: {
    user: (_, { id }) => userLoader.load(id),
    users: (_, { filter, limit }) => db.users.find({ ...filter, limit }),
  },
  User: {
    // DataLoader prevents N+1 when querying nested posts
    posts: (parent, _, { loaders }) => loaders.postLoader.load(parent.id),
  },
  Mutation: {
    createUser: (_, { input }, { auth }) => {
      requireAuth(auth);
      return db.users.create(input);
    },
  },
};
```

### Apollo Server Setup
```javascript
// server.js
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const { makeExecutableSchema } = require('@graphql-tools/schema');
const { WebSocketServer } = require('ws');
const { useServer } = require('graphql-ws/lib/use/ws');

const schema = makeExecutableSchema({ typeDefs, resolvers });

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({ server: httpServer, path: '/graphql' });
const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    // Proper shutdown
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});

await server.start();
app.use('/graphql', expressMiddleware(server, {
  context: async ({ req }) => ({
    auth: await authenticate(req.headers.authorization),
    loaders: createLoaders(),
  }),
}));
```

### Subscriptions
```javascript
// resolvers/chat.js
const { PubSub } = require('graphql-subscriptions');
const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    sendMessage: async (_, { channelId, text }, { auth, loaders }) => {
      requireAuth(auth);
      const message = await db.messages.create({ channelId, text, userId: auth.id });
      pubsub.publish(`MESSAGE_SENT_${channelId}`, { messageSent: message });
      return message;
    },
  },
  Subscription: {
    messageSent: {
      subscribe: withFilter(
        () => pubsub.asyncIterator('MESSAGE_SENT_*'),
        (payload, variables) => payload.messageSent.channelId === variables.channelId,
      ),
    },
  },
};
```

### Persisted Queries (Performance)
```javascript
// Client: automatic persisted queries
import { ApolloClient, InMemoryCache, createPersistedQueryLink } from '@apollo/client';
import { createHttpLink } from '@apollo/client/link/http';

const client = new ApolloClient({
  link: createPersistedQueryLink().concat(createHttpLink({ uri: '/graphql' })),
  cache: new InMemoryCache(),
});

// Server: enable APQ
const server = new ApolloServer({
  schema,
  persistedQueries: { ttl: 900 }, // Cache for 15 min
});
```

## Production Rules

- **Schema first.** Write SDL before resolvers; treat removals/renames as breaking changes.
- **N+1 prevention.** Batch nested loads with DataLoader keyed per request; never issue one DB query per parent row.
- **Authorization at the field.** Use directives/middleware plus resolver ownership checks; never trust client IDs.
- **Bounded queries.** Require pagination arguments with max page size; cap query depth/complexity; reject introspection in production if not needed.
- **Errors.** Return GraphQL errors with stable codes; never leak SQL, stack traces, or internal IDs.
- **Persisted queries.** Prefer allowlisted persisted queries in production; reject arbitrary documents from untrusted clients.
- **Subscriptions.** Authenticate on connect, authorize channel membership, enforce backpressure, and clean up on disconnect.

### Authorization Directive
```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION

enum Role { USER ADMIN }

type Query {
  publicData: String
  myProfile: User! @auth(requires: USER)
  adminDashboard: Dashboard! @auth(requires: ADMIN)
}
```

### Error Handling
```javascript
const { GraphQLError } = require('graphql');

// In resolver
if (!user) {
  throw new GraphQLError('User not found', {
    extensions: { code: 'NOT_FOUND', http: { status: 404 } },
  });
}
```

### Pagination (Cursor-based)
```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}

type Query {
  users(first: Int, after: String): UserConnection!
}
```

## Verification

- [ ] Schema compiles; breaking changes are additive-only
- [ ] Every query/mutation/subscription has operation-level tests
- [ ] DataLoader or equivalent batching eliminates N+1 on nested fields
- [ ] Field authorization and ownership checks tested for each role
- [ ] Query depth/complexity/pagination limits enforced
- [ ] Error responses carry stable codes; no internal detail leaks
- [ ] Persisted-query allowlist or equivalent document control in production
- [ ] Subscription connect auth and channel authorization tested