---
name: storage-mcp
description: MCP servers for cloud storage. Connect AI agents to S3, Google Drive, Dropbox, and file storage for automated backup, sync, and management.
---

# Storage MCP Skill

## Overview

MCP servers enabling AI agents to interact with cloud storage services. Automate backups, file sync, data migration, and storage management across S3, Google Drive, and Dropbox.

**Supported**: AWS S3, Google Drive, Dropbox, Azure Blob  
**Use Cases**: Backup, sync, file management, data migration

---

## When to Use

- Automated backups
- File synchronization
- Data migration
- Archive management
- Content distribution

---

## AWS S3 MCP Setup

### Installation
```json
{
  "mcpServers": {
    "s3": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-s3"],
      "env": {
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}"
      }
    }
  }
}
```

### S3 Tools
```typescript
// List buckets
s3.listBuckets()

// List objects
s3.listObjects({
  Bucket: "my-bucket",
  Prefix: "documents/"
})

// Upload file
s3.uploadFile({
  Bucket: "my-bucket",
  Key: "backup/database.sql",
  Body: fileContent,
  ContentType: "application/sql"
})

// Download file
s3.downloadFile({
  Bucket: "my-bucket",
  Key: "data/export.csv"
})

// Copy object
s3.copyObject({
  Bucket: "destination-bucket",
  CopySource: "source-bucket/old-file",
  Key: "new-location/new-file"
})

// Delete old backups
s3.deleteObjects({
  Bucket: "backups",
  Keys: ["old-backup-1.tar", "old-backup-2.tar"]
})
```

---

## Google Drive MCP Setup

### Installation
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

### Google Drive Tools
```typescript
// List files
gdrive.listFiles({
  folderId: "root",
  pageSize: 100
})

// Upload file
gdrive.uploadFile({
  name: "report.pdf",
  parents: ["folder-id"],
  content: pdfBuffer,
  mimeType: "application/pdf"
})

// Create folder
gdrive.createFolder({
  name: "Backups",
  parents: ["root"]
})

// Share file
gdrive.createPermission({
  fileId: "file-id",
  type: "anyone",
  role: "reader"
})

// Get share link
gdrive.getShareLink({
  fileId: "file-id"
})
```

---

## Dropbox MCP Setup

### Installation
```json
{
  "mcpServers": {
    "dropbox": {
      "command": "npx",
      "args": ["-y", "mcp-dropbox"],
      "env": {
        "DROPBOX_ACCESS_TOKEN": "${DROPBOX_ACCESS_TOKEN}"
      }
    }
  }
}
```

### Dropbox Tools
```typescript
// List files
dropbox.listFolder({
  path: "/backups"
})

// Upload file
dropbox.uploadFile({
  path: "/backups/backup.zip",
  contents: fileBuffer
})

// Download file
dropbox.downloadFile({
  path: "/documents/report.pdf"
})

// Create shared link
dropbox.createSharedLink({
  path: "/documents/report.pdf",
  settings: { requested_visibility: "public" }
})

// Move file
dropbox.move({
  from: "/temp/file.txt",
  to: "/archive/file.txt"
})
```

---

## Use Cases

### 1. Automated Backups
```
Schedule: Daily 2 AM
Action:
  1. Database dump
  2. Compress
  3. Upload to S3
  4. Delete local
  5. Notify success
```

### 2. Cross-Cloud Sync
```
Trigger: File change
Action:
  1. Detect change
  2. Upload to S3
  3. Sync to Google Drive
  4. Update metadata
```

### 3. Archive Management
```
Schedule: Monthly
Action:
  1. Find old files
  2. Compress
  3. Move to cold storage
  4. Update index
```

### 4. Content Distribution
```
Trigger: New upload
Action:
  1. Upload to CDN
  2. Generate URLs
  3. Update database
  4. Notify team
```

---

## Backup Strategy

### Incremental Backup
```typescript
async function incrementalBackup() {
  // Get last backup date
  const lastBackup = await getLastBackupTimestamp();
  
  // Get changes since last backup
  const changes = await getChangesSince(lastBackup);
  
  // Upload changes
  for (const change of changes) {
    await s3.uploadFile({
      Bucket: "backups",
      Key: `incremental/${date}/${change.file}`,
      Body: change.content
    });
  }
  
  // Update backup timestamp
  await updateLastBackupTimestamp(Date.now());
}
```

### Versioning
```typescript
// Enable versioning
s3.putBucketVersioning({
  Bucket: "my-bucket",
  VersioningConfiguration: {
    Status: "Enabled"
  }
})
```

---

## Integration with 1ai-skills

### With Database
```
database-mcp → storage-mcp → backup
     ↓              ↓
 Export data    Upload to S3
```

### With Development
```
deployment → storage-mcp → artifacts
     ↓              ↓
 Build        Store binaries
```

---

## Best Practices

### Do's
✅ Enable versioning  
✅ Use lifecycle policies  
✅ Encrypt sensitive data  
✅ Regular test restores  

### Don'ts
❌ Don't store credentials in files  
❌ Don't skip encryption  
❌ Don't ignore retention policies  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - S3, Google Drive, Dropbox support

---

## Related Skills

- [database-mcp](/skills/database-mcp) - Database operations
- [cloud-mcp](/skills/cloud-mcp) - Cloud infrastructure
- [automation](/skills/automation) - Workflow automation
