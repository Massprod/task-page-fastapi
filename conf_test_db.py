from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, db_session
from main import app


SQL_URL = "sqlite:///tests/test_database.db"

engine = create_engine(SQL_URL)
TestingSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_db_session():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[db_session] = override_db_session()
