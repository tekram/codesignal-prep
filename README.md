# codesignal-prep

Prep for the Anthropic Fellows Program CodeSignal assessment — 90 min, 4 levels, in-memory database in Python.

## Problem Structure

Nested record store: `database[key][field] = value`.

| Level | Concept | Time |
|-------|---------|------|
| 1 | Basic CRUD: `set/get/delete(key, field, value)` | ~10 min |
| 2 | Scans: `scan(key)` → `["field(value)", ...]` sorted | ~10 min |
| 3 | Timestamps + TTL: `_at` methods, half-open `[t, t+ttl)` | ~25 min |
| 4 | Backup/Restore with TTL recalculation | ~25 min |

## How to Practice

```bash
# pick a level, implement in practice/levelN/db.py
# read the spec first:
cat level1/prompt.md

# run tests:
cd practice/level1
python -m unittest test_db.py -v
```

## With Claude Code

```bash
cd codesignal-prep
claude
```

Claude reads `CLAUDE.md` and acts as a coaching tutor — guides without giving away answers.

## Repo Layout

```
levelN/prompt.md         spec for each level
levelN/test_db.py        reference tests
practice/levelN/db.py    blank template — write your code here
practice/levelN/test_db.py   tests to run
solutions/levelN/db.py   reference solutions
```

## Key Gotchas

- TTL half-open: field expires **at** `t + ttl` (not valid at that exact timestamp)
- Scan output format: exactly `"field(value)"` — no spaces, sorted by field name
- `delete` returns `False` (not `None`) for missing fields
- `backup` count = records with ≥1 alive field, not total fields
- Design Level 1 with Level 3 in mind: store `{"value": v, "expires_at": float('inf')}`
