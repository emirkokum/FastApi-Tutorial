from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class TaskDb(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    done = Column(Boolean, default=False)