"""
Database tests.

These tests verify that your Database class works correctly.
Each test function demonstrates a different testing pattern.
"""

import pytest


class TestDatabaseConnection:
    """Tests for database connection and initialization."""

    @pytest.mark.asyncio
    async def test_database_connects(self, test_db):
        """
        Test that the database connects successfully.

        This is a "smoke test" - it just verifies the basic setup works.
        The test_db fixture handles connection, so if we get here, it worked.
        """
        assert test_db.conn is not None
        assert test_db.conn.is_alive()

    @pytest.mark.asyncio
    async def test_schema_initialization(self, test_db):
        """
        Test that the schema is created correctly.

        This verifies the KV table exists with the right columns.
        """
        cursor = await test_db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='kv'"
        )
        result = await cursor.fetchone()
        assert result is not None
        assert result[0] == "kv"

    @pytest.mark.asyncio
    async def test_wal_mode_enabled(self, test_db):
        """
        Test that WAL mode is enabled.

        WAL (Write-Ahead Logging) is important for concurrent access.
        """
        cursor = await test_db.conn.execute("PRAGMA journal_mode")
        result = await cursor.fetchone()
        assert result[0].lower() == "wal"


class TestKeyValueOperations:
    """Tests for basic KV store operations."""

    @pytest.mark.asyncio
    async def test_insert_and_retrieve(self, test_db):
        """
        Test that we can insert and retrieve a value.

        This is the most basic CRUD operation.
        """
        # Insert a value
        await test_db.conn.execute(
            "INSERT INTO kv (key, value) VALUES (?, ?)", ("test_key", "test_value")
        )
        await test_db.conn.commit()

        # Retrieve it
        cursor = await test_db.conn.execute(
            "SELECT value FROM kv WHERE key = ?", ("test_key",)
        )
        result = await cursor.fetchone()

        assert result is not None
        assert result[0] == "test_value"

    @pytest.mark.asyncio
    async def test_update_value(self, test_db):
        """
        Test that we can update an existing value.
        """
        # Insert initial value
        await test_db.conn.execute(
            "INSERT INTO kv (key, value) VALUES (?, ?)", ("counter", "0")
        )
        await test_db.conn.commit()

        # Update it
        await test_db.conn.execute(
            "UPDATE kv SET value = ? WHERE key = ?", ("1", "counter")
        )
        await test_db.conn.commit()

        # Verify the update
        cursor = await test_db.conn.execute(
            "SELECT value FROM kv WHERE key = ?", ("counter",)
        )
        result = await cursor.fetchone()
        assert result[0] == "1"

    @pytest.mark.asyncio
    async def test_delete_value(self, test_db):
        """
        Test that we can delete a value.
        """
        # Insert a value
        await test_db.conn.execute(
            "INSERT INTO kv (key, value) VALUES (?, ?)", ("temp", "data")
        )
        await test_db.conn.commit()

        # Delete it
        await test_db.conn.execute("DELETE FROM kv WHERE key = ?", ("temp",))
        await test_db.conn.commit()

        # Verify it's gone
        cursor = await test_db.conn.execute(
            "SELECT value FROM kv WHERE key = ?", ("temp",)
        )
        result = await cursor.fetchone()
        assert result is None

    @pytest.mark.asyncio
    async def test_primary_key_constraint(self, test_db):
        """
        Test that duplicate keys are rejected.

        This verifies that the PRIMARY KEY constraint works.
        """
        # Insert first value
        await test_db.conn.execute(
            "INSERT INTO kv (key, value) VALUES (?, ?)", ("unique_key", "value1")
        )
        await test_db.conn.commit()

        # Try to insert duplicate key - should raise an error
        with pytest.raises(Exception):  # aiosqlite raises IntegrityError
            await test_db.conn.execute(
                "INSERT INTO kv (key, value) VALUES (?, ?)", ("unique_key", "value2")
            )
            await test_db.conn.commit()


class TestDatabaseHelpers:
    """
    Tests for helper methods you'll add to the Database class.

    These are placeholder tests for methods you haven't written yet.
    This is called "Test-Driven Development" (TDD) - write the test first,
    then implement the feature to make the test pass.
    """

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Not implemented yet - example for future")
    async def test_get_user_roll_count(self, test_db):
        """
        Future test: Get total rolls for a user.

        When you add a get_user_roll_count() method to Database,
        remove the @pytest.mark.skip decorator and this will run.
        """
        # Example of what this test would look like:
        # count = await test_db.get_user_roll_count(user_id=12345)
        # assert count == 0
        pass

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Not implemented yet - example for future")
    async def test_store_roll_history(self, test_db):
        """
        Future test: Store a roll in history.
        """
        # Example:
        # await test_db.store_roll(
        #     user_id=12345,
        #     expression="1d20+5",
        #     result=15
        # )
        # rolls = await test_db.get_user_rolls(user_id=12345)
        # assert len(rolls) == 1
        pass
