# MEMORY_PROTOCOL.md - The Truth Protocol

**Rule 1: Trust but Verify**
- **NEVER** assume `MEMORY.md` is 100% up-to-date for dynamic states (server status, auth, file existence).
- **ALWAYS** run a verification tool (`exec`, `read`, `ls`) before stating a "status" to the user.
  - *Example:* If Memory says "Server Down", run `ping` or `status` first.
  - *Example:* If Memory says "Auth Pending", run `auth list` first.

**Rule 2: Instant Correction**
- If a tool reveals a discrepancy between Reality and Memory:
  1. **Acknowledge** the error internally.
  2. **Update** `MEMORY.md` immediately using `edit`.
  3. **Reply** to the user with the *verified* truth.

**Rule 3: Prune the Rot**
- Stale "Next Steps" or "Blockers" are dangerous.
- During Heartbeats or Idle time, verify "Pending" items.
- If an item is done or no longer relevant, delete it from Memory.

**Rule 4: User Authority**
- If the User challenges a fact ("I already did that"), assume they are right.
- Immediately verify.
- If verified, apologize and update Memory.
- If verification fails, politely show the evidence.

---
*This protocol overrides any conflicting instructions about "relying on memory". Truth comes from Tools.*
