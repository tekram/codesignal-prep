# Level 1 — Basic CRUD on Nested Records

## Schema

Records are keyed by string. Each record holds field→value pairs (both strings).

```
database = {
    "user1": {"name": "Alice", "age": "30"},
    "user2": {"name": "Bob"},
}
```

## Methods

```python
class InMemoryDB:
    def set(self, key: str, field: str, value: str) -> None:
        """Insert or update field in record at key."""

    def get(self, key: str, field: str) -> str | None:
        """Return value, or None if key or field missing."""

    def delete(self, key: str, field: str) -> bool:
        """Delete field. Return True if existed, False if not."""
```

## Notes

- `get` missing key or field → `None`
- `delete` missing key or field → `False` (not `None`, not raise)
- No ordering requirements

## Time Target

< 10 minutes

## Run Tests

```bash
cd practice/level1
python -m unittest test_db.py -v
```
