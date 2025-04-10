from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime

from healthai.src.api.ledgers.schemas import HealthAILedgerOperation
from monorepo.core.db.database import Base


class HealthAILedgerEntryModel(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True)
    operation = Column(Enum(HealthAILedgerOperation), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)
