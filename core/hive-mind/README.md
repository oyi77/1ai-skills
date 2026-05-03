# Hive Mind 🐝

Sync memories across multiple agents using a shared TiDB Zero database.

## What It Does

Hive Mind provides a shared configuration store for AI agents, acting like an "iCloud Keychain" for agent settings. Key features:
- Store and retrieve persistent key-value preferences
- Sync settings across multiple devices and agents
- Survives container restarts and clean reinstalls
- Team collaboration by sharing configuration

## Quick Usage Example

```bash
# Set a user preference
python skills/hive-mind/run.py --action set --key "theme" --value "dark"

# Get a preference
python skills/hive-mind/run.py --action get --key "theme"
# Output: dark

# List all preferences
python skills/hive-mind/run.py --action list
# Output:
# theme: dark
# user.timezone: UTC
# notifications.enabled: true
```

## Key Features

- ✅ Persistent key-value storage
- ✅ Cross-device synchronization
- ✅ Two provisioning modes:
  - BYO Database (provide TIDB_* credentials)
  - Auto-Provisioning (free ephemeral database via TiDB Zero API)
- ✅ Team collaboration support
- ✅ Simple CLI interface (set, get, list)
- ✅ Survives container restarts

## Requirements

- TiDB Zero serverless cluster
- Python 3
- curl

## Environment Variables (Optional for BYO DB)

- `TIDB_HOST` - TiDB Zero host
- `TIDB_PORT` - TiDB Zero port
- `TIDB_USER` - TiDB Zero username
- `TIDB_PASSWORD` - TiDB Zero password

If not provided, auto-provisioning creates a free ephemeral database.