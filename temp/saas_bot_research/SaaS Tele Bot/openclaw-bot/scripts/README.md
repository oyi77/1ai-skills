# Scripts

This directory contains utility scripts for the OpenClaw Bot.

## 📁 Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `setup.sh` | Initial setup for development | `bash scripts/setup.sh` |
| `deploy.sh` | Deploy to staging/production | `bash scripts/deploy.sh -e production` |
| `health-check.sh` | Check system health | `bash scripts/health-check.sh` |
| `backup.sh` | Backup database and files | `bash scripts/backup.sh [postgres\|redis\|all]` |

## 🚀 Quick Start

### Setup Development Environment

```bash
bash scripts/setup.sh
```

### Deploy to Production

```bash
bash scripts/deploy.sh -e production -v 3.0.1
```

### Check System Health

```bash
bash scripts/health-check.sh
```

### Backup Database

```bash
# Backup PostgreSQL only
bash scripts/backup.sh postgres

# Backup everything
bash scripts/backup.sh all

# Cleanup old backups
bash scripts/backup.sh cleanup
```

## 📝 Adding New Scripts

1. Create script file with `.sh` extension
2. Make it executable: `chmod +x scripts/your-script.sh`
3. Add to this README
4. Follow existing script patterns

---

*See individual scripts for detailed usage information*
