from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


DATABASE_URL = "postgresql+psycopg2://postgres:pass@postgresql_container:5432/fastapi_db"


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    with engine.connect() as connection:
        print("✅ Database connected successfully!")
except OperationalError as e:
    print(f"❌ OperationalError: {e}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
