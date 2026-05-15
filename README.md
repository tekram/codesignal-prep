# codesignal-prep

Prep for the Anthropic Fellows Program CodeSignal assessment — 90 min, **6 levels**, in-memory database in Python.

## Problem Structure

Nested record store: `database[key][field] = value`.

| Level | Concept | Time |
|-------|---------|------|
| 1 | Basic CRUD: `set/get/delete(key, field, value)` | ~10 min |
| 2 | Scans: `scan(key)` → `["field(value)", ...]` sorted | ~10 min |
| 3 | Timestamps + TTL: `_at` methods, half-open `[t, t+ttl)` | ~20 min |
| 4 | Backup/Restore with TTL recalculation | ~20 min |
| 5 | Thread-safe: `threading.RLock` wrapping all ops | ~15 min |
| 6 | Advanced concurrency: async batch, read-write lock, or worker queue | ~15 min |

## How to Practice

```bash
# read the spec first:
cat level1/prompt.md

# implement in the blank template:
# edit practice/level1/db.py

# run tests:
cd practice/level1
python -m unittest test_db.py -v
```

## With Claude Code

```bash
cd codesignal-prep
claude
```

Claude reads `CLAUDE.md` and coaches you through each level — hints only, no handouts.

## Repo Layout

```
levelN/prompt.md             spec for each level
levelN/test_db.py            reference tests
practice/levelN/db.py        blank template — write your code here
practice/levelN/test_db.py   tests to run
solutions/levelN/db.py       reference solutions (don't peek during practice)
```

## Key Gotchas

- TTL half-open: field expires **at** `t + ttl` — check `expires_at > timestamp` (strict `>`)
- Scan format: exactly `"field(value)"` — no spaces, sorted by field name
- `delete` returns `False` (not `None`) for missing/expired fields
- `backup` count = records with ≥1 alive field, not total fields
- Design L1 with L3 in mind: store `{"value": v, "expires_at": float('inf')}`
- Concurrency: use `threading.RLock` (re-entrant) so methods can call each other safely
