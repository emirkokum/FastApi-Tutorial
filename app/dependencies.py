from app.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    """
    Dependency to get a database session.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()