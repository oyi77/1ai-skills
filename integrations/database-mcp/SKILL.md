---
name: database-mcp
description: MCP server for SQL databases. Connect AI agents to PostgreSQL, MySQL, MariaDB, and SQLite for natural language queries, schema management, and data operations.
---

# Database MCP Skill

## Overview

MCP server for SQL databases enabling AI agents to interact with PostgreSQL, MySQL, MariaDB, and SQLite through natural language. Provides 12+ MCP tools for query execution, schema inspection, and database management.

**Source**: [guyinwonder168/database-mcp](https://github.com/guyinwonder168)  
**Supported**: PostgreSQL, MySQL, MariaDB, SQLite  
**Tools**: 12+ MCP tools

---

## When to Use

- Query databases with natural language
- Inspect and explore database schemas
- Generate SQL queries
- Analyze database performance
- Manage database migrations
- Data analysis and reporting

---

## MCP Setup

### Installation
```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sql"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### PostgreSQL (Anthropic Official)
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@host/db"
      }
    }
  }
}
```

---

## Available Tools

### 1. Query Execution
```typescript
// Execute SQL query
executeQuery({
  sql: "SELECT * FROM users WHERE created_at > NOW() - INTERVAL '7 days'",
  database: "production"
})
```

### 2. Schema Inspection
```typescript
// Get table schema
getSchema({
  table: "users",
  database: "production"
})
```

### 3. List Tables
```typescript
// List all tables
listTables({
  database: "production",
  schema: "public"
})
```

### 4. Query Analysis
```typescript
// Analyze query performance
explainQuery({
  sql: "SELECT * FROM orders WHERE status = 'pending'",
  database: "production"
})
```

### 5. Create Table
```typescript
// Create new table
createTable({
  name: "products",
  columns: [
    { name: "id", type: "SERIAL PRIMARY KEY" },
    { name: "name", type: "VARCHAR(255)" },
    { name: "price", type: "DECIMAL(10,2)" }
  ],
  database: "production"
})
```

### 6. Insert Data
```typescript
// Insert rows
insert({
  table: "users",
  data: { name: "John", email: "john@example.com" },
  database: "production"
})
```

### 7. Update Data
```typescript
// Update rows
update({
  table: "users",
  data: { status: "active" },
  where: "id = 1",
  database: "production"
})
```

### 8. Delete Data
```typescript
// Delete rows
delete({
  table: "users",
  where: "status = 'inactive' AND created_at < NOW() - INTERVAL '1 year'",
  database: "production"
})
```

---

## Database-Specific Tools

### PostgreSQL
| Tool | Description |
|------|-------------|
| list_indexes | List all indexes |
| get_table_size | Get table size |
| vacuum_analyze | Optimize table |
| backup | Create backup |

### MySQL
| Tool | Description |
|------|-------------|
| show_processlist | Show running queries |
| kill_query | Kill long-running query |
| analyze_table | Analyze table |
| optimize_table | Optimize table |

---

## Use Cases

### 1. Data Analysis
```
- Query customer data
- Generate reports
- Calculate metrics
- Export results
```

### 2. Schema Management
```
- Explore existing schemas
- Create new tables
- Modify columns
- Add indexes
```

### 3. Debugging
```
- Find slow queries
- Check connections
- Analyze locks
- Monitor performance
```

### 4. Migrations
```
- Generate migration scripts
- Apply schema changes
- Rollback if needed
```

---

## Integration with 1ai-skills

### With Development
```
code-reviewer → database-mcp → query-analysis
    ↓              ↓
Review code    Optimize schemas
```

### With Analytics
```
database-mcp → analytics-dashboard → reporting
    ↓              ↓
Extract data   Visualize
```

---

## Security Best Practices

### Do's
✅ Use read-only connections when possible  
✅ Parameterize queries  
✅ Limit table access with separate users  
✅ Enable query logging  
✅ Regular backups  

### Don'ts
❌ Don't expose admin credentials  
❌ Don't run without limits  
❌ Don't skip connection pooling  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - PostgreSQL, MySQL, SQLite support
  - 12+ MCP tools

---

## Related Skills

- [code-reviewer](/skills/code-reviewer) - Code review
- [analytics-dashboard](/skills/analytics-dashboard) - Data visualization
- [automation](/skills/automation) - Workflow automation
