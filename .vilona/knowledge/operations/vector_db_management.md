# Vector Database Management - Operational Knowledge

## Last Updated: 2026-03-08

## Crisis Mode Note
**Priority Trade-Off:** In emergency crisis mode (revenue gap, PostBridge down), vector DB sync frequency should be **reduced** to conserve resources for revenue-generating activities. Current recommendation: 1x daily at 09:00 only (instead of 4x daily).

---

## Known Issues

### Process Hang During Model Loading

**Symptoms:**
- vector_db_sync.py process hangs during XLMRobertaModel loading
- Process requires manual SIGTERM kill
- Occurs intermittently (1 out of 3 attempts)

**Technical Details:**
- API Error: 'Client' object has no attribute 'persist'
- Affected Engines: PageIndex, Ruvector (ZVec works fine)
- Loading Phase: Sentence-BERT weights (391 parameters ~800MB)

**Root Causes:**
1. **API Incompatibility**: Different vector DB clients expect different API methods
2. **Resource Starvation**: Model loading may compete with other processes
3. **Timeout Absence**: No built-in timeout for long-running operations

**Resolution Pattern:**
1. Kill hanging process via `process kill <session-id>`
2. Wait 5-10 seconds
3. Re-run vector_db_sync.py
4. Works on subsequent attempt (client cache pre-loaded)

**Permanent Fix Needed:**
```python
# Add timeout wrapper in vector_db_sync.py
import signal

class TimeoutException(Exception): pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

def safe_vector_sync():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(120)  # 2 minute timeout

    try:
        # Vector DB sync code
        pass
    except TimeoutException:
        logging.warning("Vector DB sync timed out, retrying...")
        signal.alarm(0)
        return retry_vector_sync()
    finally:
        signal.alarm(0)
```

## Client API Methods

### ZVec
- ✅ `persist()` method supported
- Works correctly

### PageIndex
- ❌ `persist()` method NOT supported
- Error: 'Client' object has no attribute 'persist'
- Workaround: Skip persist or use different method

### Ruvector
- ❌ `persist()` method NOT supported
- Same as PageIndex
- Workaround: Skip persist or use different method

## Sync Frequency

**Current Schedule:** Every 30 minutes via cron heartbeat
**Actual Execution:** ~4 times per day (6:00, 9:00, 12:00, 15:00)

**Recommendation:**
- Reduce frequency to 2x daily (9:00, 18:00) to prevent resource contention
- Only sync when new documents are added

## Performance Metrics

| Time | Operation | Duration | Result |
|------|-----------|----------|--------|
| 06:00 | Sync | Hung (Killed) | Failed |
| 09:00 | Sync | Hung (Killed) | Failed |
| 12:00 | Sync | ~60s | Success |

## Maintenance Checklist

- [ ] Debug PageIndex/Ruvector `persist()` alternative
- [ ] Add timeout handling (2 minutes recommended)
- [ ] Implement retry logic with exponential backoff
- [ ] Reduce sync frequency to 2x daily
- [ ] Add memory usage monitoring during sync
- [ ] Consider using lighter model for indexing

## Related Scripts

- `/home/openclaw/.openclaw/workspace/scripts/vector_db_sync.py`
- `/home/openclaw/.openclaw/workspace/vector_db_startup.py`
- `/home/openclaw/.openclaw/workspace/.vilona/core/vilona_cli.py`