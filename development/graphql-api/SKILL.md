---
name: graphql-api
description: GraphQL API development — schema design, resolvers, subscriptions, federation. Apollo, Relay, performance optimization. Use when working with graphql api.
domain: development
tags:
- api
- coding
- graphql
- software-engineering
- testing
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

## Common Patterns

Proven patterns for graphql-api usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


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