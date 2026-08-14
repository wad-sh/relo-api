from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine,autoflush=False)

Base = declarative_base()

def get_db () :
    try:
        db = sessionLocal()
        yield db
    finally :
        db.close()
