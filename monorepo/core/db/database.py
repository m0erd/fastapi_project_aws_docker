from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

import os

# db_password = os.getenv('DB_PASSWORD')
# DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
DATABASE_URL = "postgresql://user:Sometime@postgres:5432/fastapi_db"


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
