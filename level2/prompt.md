# Level 2 — Filtered Scans

Extends Level 1. Add two scan methods.

## New Methods

```python
def scan(self, key: str) -> list[str]:
    """
    Return all fields in record at key as ["field(value)", ...]
    sorted lexicographically by field name.
    Return [] if key missing.
    """

def scan_by_prefix(self, key: str, prefix: str) -> list[str]:
    """
    Same as scan(), but only fields whose name starts with prefix.
    prefix="" matches all fields (same as scan).
    """
```

## Output Format — CRITICAL

Each item must be exactly `"field(value)"` — no spaces.

```python
# db has key="user1", field="name", value="Alice"
db.scan("user1")  # → ["name(Alice)"]
```

Sort is by **field name**, lexicographically. Not by value, not by insertion order.

## Notes

- `scan` on missing key → `[]` not `None`
- Helper: `f"{field}({value})"` — memorize this pattern
- Helper: `sorted(fields.items())` gives `(field, entry)` pairs sorted by field

## Time Target

< 10 minutes on top of Level 1

## Run Tests

```bash
cd practice/level2
python -m unittest test_db.py -v
```
