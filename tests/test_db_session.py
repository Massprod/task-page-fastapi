from sqlalchemy import inspect
from sqlalchemy.orm.session import Session
from database.database import engine, db_session
from database.models import DbUsers, DbTasks
import pytest


@pytest.mark.asyncio
async def test_get_db_session():
    """Test getting database session from db_session call"""
    assert isinstance(next(db_session()), Session)


@pytest.mark.asyncio
async def test_created_tables():
    """Test creating correct database tables"""
    created_tables = inspect(engine).get_table_names()
    target_tables = [DbUsers.__tablename__, DbTasks.__tablename__]
    for table in target_tables:
        assert table in created_tables
