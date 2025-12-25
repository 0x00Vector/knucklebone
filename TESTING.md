# Testing Guide

This document explains the testing setup for the Knucklebone Discord bot, what each test does, and how to use them.

## Quick Start

**Install test dependencies:**
```bash
pip install -r requirements-dev.txt
```

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run a specific test file:**
```bash
pytest tests/test_db.py
```

**Run a specific test:**
```bash
pytest tests/test_db.py::TestDatabaseConnection::test_database_connects
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py       # Shared fixtures and test configuration
└── test_db.py        # Database tests
```

## Understanding conftest.py

**What it does:** Provides reusable test setup code called "fixtures."

### Fixtures

#### `test_db` Fixture
```python
async def test_db():
    # Creates a temporary SQLite database
    # Connects and initializes schema
    # Yields to your test
    # Cleans up after test completes
```

**Why it matters:** Every test gets a fresh, isolated database. Tests never interfere with each other or your real data.

**How to use it:**
```python
async def test_something(test_db):
    # test_db is a fully connected Database instance
    # Do your test here
```

## Understanding test_db.py

This file contains all database-related tests, organized into logical groups (classes).

### TestDatabaseConnection

Tests that verify the database connects and initializes correctly.

#### `test_database_connects`
- **Purpose:** Smoke test to verify basic database connection works
- **What it tests:** Database connects and connection is alive
- **Why it matters:** If this fails, everything else will fail too
- **Learning:** Basic assertion patterns with `assert`

#### `test_schema_initialization`
- **Purpose:** Verify the KV table is created
- **What it tests:** SQL schema creation during initialization
- **Why it matters:** Ensures your schema migrations work
- **Learning:** How to query SQLite system tables to verify structure

#### `test_wal_mode_enabled`
- **Purpose:** Verify Write-Ahead Logging is enabled
- **What it tests:** PRAGMA settings are applied correctly
- **Why it matters:** WAL mode allows concurrent reads during writes (important for bots)
- **Learning:** How to check SQLite configuration with PRAGMA statements

### TestKeyValueOperations

Tests that verify CRUD (Create, Read, Update, Delete) operations work.

#### `test_insert_and_retrieve`
- **Purpose:** Test basic INSERT and SELECT operations
- **What it tests:** Can write data and read it back
- **Why it matters:** Most fundamental database operation
- **Learning:** The Arrange-Act-Assert pattern
  - **Arrange:** Insert data
  - **Act:** Query it back
  - **Assert:** Verify it matches

#### `test_update_value`
- **Purpose:** Test UPDATE operations
- **What it tests:** Can modify existing data
- **Why it matters:** You'll need to update user stats, configs, etc.
- **Learning:** How to verify state changes in tests

#### `test_delete_value`
- **Purpose:** Test DELETE operations
- **What it tests:** Can remove data and verify it's gone
- **Why it matters:** Data cleanup, resetting user data, etc.
- **Learning:** Testing for absence (assert result is None)

#### `test_primary_key_constraint`
- **Purpose:** Test that database constraints work
- **What it tests:** Cannot insert duplicate primary keys
- **Why it matters:** Ensures data integrity - critical for preventing bugs
- **Learning:** Testing that errors occur when they should using `pytest.raises()`

**Pattern:**
```python
with pytest.raises(Exception):
    # Code that SHOULD fail
    await db.conn.execute(...)
```

### TestDatabaseHelpers

Placeholder tests for future features (currently skipped).

#### `test_get_user_roll_count` (skipped)
- **Purpose:** Example of Test-Driven Development (TDD)
- **What it will test:** Counting rolls per user (not implemented yet)
- **Why it's here:** Shows you the workflow for adding new features
- **How to use it:**
  1. Remove `@pytest.mark.skip` decorator
  2. Implement the logic in the test
  3. Run test (it will fail)
  4. Implement the feature in `bot/db.py`
  5. Run test again (it should pass)

#### `test_store_roll_history` (skipped)
- **Purpose:** Example of future roll history feature
- **What it will test:** Storing and retrieving roll data
- **Why it's here:** Template for when you add this feature
- **Learning:** TDD workflow - write test first, implement feature second

## Testing Philosophy

### What We Test
- **Database operations** - Insert, update, delete, queries
- **Business logic** - Game mechanics, calculations, validations
- **Data integrity** - Constraints, schemas, migrations

### What We Don't Test (Yet)
- **Discord interactions** - Too complex, low ROI for this project
- **Network calls** - Would require mocking
- **UI/UX** - Test manually in Discord

### Why This Approach?

**Fast feedback:** Tests run in ~2 seconds, catch bugs before you deploy

**Confidence:** Know your database code works before testing in Discord

**Documentation:** Tests show how to use your Database class

**Refactoring safety:** Change code confidently, tests catch regressions

## Common Testing Patterns

### Arrange-Act-Assert (AAA)
Every test should follow this structure:

```python
async def test_example(test_db):
    # ARRANGE: Set up test data
    await test_db.conn.execute("INSERT INTO kv VALUES (?, ?)", ("key", "value"))

    # ACT: Perform the action you're testing
    cursor = await test_db.conn.execute("SELECT value FROM kv WHERE key = ?", ("key",))
    result = await cursor.fetchone()

    # ASSERT: Verify the result
    assert result[0] == "value"
```

### Testing Async Functions
Use the `@pytest.mark.asyncio` decorator (or set `asyncio_mode = auto` in pytest.ini):

```python
@pytest.mark.asyncio
async def test_async_operation(test_db):
    result = await some_async_function()
    assert result is not None
```

### Testing Exceptions
Verify that code fails correctly:

```python
with pytest.raises(ExpectedExceptionType):
    # Code that should raise ExpectedExceptionType
    await dangerous_operation()
```

## Writing New Tests

### For Database Features

1. **Add test to `tests/test_db.py`:**
```python
@pytest.mark.asyncio
async def test_your_new_feature(test_db):
    # Arrange
    # Act
    # Assert
```

2. **Run it:** `pytest tests/test_db.py::test_your_new_feature`

3. **Implement the feature in `bot/db.py`**

4. **Run again to verify**

### For Game Logic (e.g., Mork Borg)

1. **Create `tests/test_morkborg.py`:**
```python
import d20

def test_omen_generation():
    """Test that omens are valid."""
    omen = generate_omen()  # Your function
    assert omen in VALID_OMENS
    assert len(omen) > 0

def test_ability_check_critical():
    """Test critical success detection."""
    # Test the logic, not the Discord command
    die_value = 20
    total = 22
    dr = 12

    outcome = determine_outcome(die_value, total, dr)
    assert "CRITICAL" in outcome
```

2. **No `test_db` fixture needed** - pure logic tests

3. **Super fast** - no database, no async

## Debugging Failed Tests

**Verbose output:**
```bash
pytest -vv
```

**Stop on first failure:**
```bash
pytest -x
```

**Show print statements:**
```bash
pytest -s
```

**Run specific test:**
```bash
pytest tests/test_db.py::TestDatabaseConnection::test_database_connects -vv
```

## Test Coverage

**Install coverage tool:**
```bash
pip install pytest-cov
```

**Run with coverage:**
```bash
pytest --cov=bot --cov-report=html
```

**View report:**
Open `htmlcov/index.html` in browser

**Goal:** 80%+ coverage on `bot/db.py` and game logic

## CI/CD Integration (Future)

When you're ready to deploy, add tests to GitHub Actions:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest
```

Now tests run automatically on every commit.

## Next Steps

1. **Run the tests now:** `pytest -v`
2. **Add roll history:** Implement the skipped tests
3. **Test Mork Borg logic:** Create `tests/test_morkborg.py`
4. **Track coverage:** Aim for 80%+ on core code

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [SQLite testing patterns](https://www.sqlite.org/testing.html)

## Questions?

The tests are heavily commented. Read through `tests/test_db.py` to see patterns in action.
