from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "sqlite:///database/database.db"

engine = create_engine(SQLALCHEMY_DB_URL,
                       pool_size=10,
                       max_overflow=-1,  # unlimited que to connect
                       )

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
