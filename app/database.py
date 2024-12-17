from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./flipcards.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
