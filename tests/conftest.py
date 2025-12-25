"""
Pytest configuration and fixtures.

Fixtures are reusable test setup code. They run before your tests
and provide objects/data that your tests need.
"""

import os
import tempfile
from pathlib import Path

import pytest
import pytest_asyncio

from bot.db import Database


@pytest_asyncio.fixture
async def test_db():
    """
    Provides a fresh test database for each test.

    This fixture:
    1. Creates a temporary SQLite database file
    2. Connects to it and initializes the schema
    3. Yields it to your test
    4. Cleans up (closes connection and deletes file) after the test

    Usage in tests:
        async def test_something(test_db):
            # test_db is a connected Database instance
            # Do stuff with test_db
    """
    # Create a temporary file for the test database
    temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(temp_fd)  # Close the file descriptor, we just need the path

    # Create and connect a Database instance
    db = Database(path=temp_path)
    await db.connect()

    # Yield to the test - this is where your test runs
    yield db

    # Cleanup after test
    await db.close()
    Path(temp_path).unlink(missing_ok=True)
