from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "sqlite:///database/task_page.db"

engine = create_engine(SQLALCHEMY_DB_URL)

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine,
                       )

Base = declarative_base()


def db_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
