from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

from healthai.src.api.ledgers.schemas import HealthAILedgerOperation
from monorepo.core.ledgers.schemas import SharedLedgerOperation
from travelai.src.api.ledgers.schemas import TravelAILedgerOperation

Base = declarative_base()

all_enum_values = list(set(
    [op.value for op in SharedLedgerOperation] +
    [op.value for op in HealthAILedgerOperation] +
    [op.value for op in TravelAILedgerOperation]
))


class LedgerEntryModel(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(Enum(*all_enum_values, name="ledgeroperation"), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)


DATABASE_URL = "postgresql://postgres:pass@postgresql_container/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


class LedgerEntryCreate(BaseModel):
    operation: str
    owner_id: str


class LedgerEntry(BaseModel):
    id: int
    operation: str
    amount: int
    nonce: str
    owner_id: str
    created_on: datetime

    class Config:
        from_attributes = True
