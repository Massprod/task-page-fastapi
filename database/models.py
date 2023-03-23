from database.database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship


class DbTasks(Base):
    __tablename__ = "tasks"
    id = Column(primary_key=True)
    name = Column(String(length=50), nullable=True)
    description = Column(String(length=300), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.user_id"), nullable=True)
    status = Column(Boolean(), nullable=False)

    user = relationship("DbUsers", back_populates="user_tasks")


class DbUsers(Base):
    __tablename__ = "users"
    user_id = Column(primary_key=True)
    username = Column(String(length=50), nullable=False)
    password = Column(String(length=50), nullable=False)

    user_tasks = relationship("DbTasks", back_populates="user_id", cascade="all, delete, delete-orphan")
