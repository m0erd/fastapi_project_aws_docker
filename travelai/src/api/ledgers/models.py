from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime

from monorepo.core.db.database import Base
from travelai.src.api.ledgers.schemas import TravelAILedgerOperation


class TravelAILedgerEntryModel(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True)
    operation = Column(Enum(TravelAILedgerOperation), nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow, nullable=False)
