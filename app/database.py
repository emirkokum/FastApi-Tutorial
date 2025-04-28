from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"  # SQLite database file name

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Connection arguments for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create a session for each process(select, insert, update, delete)

Base = declarative_base()