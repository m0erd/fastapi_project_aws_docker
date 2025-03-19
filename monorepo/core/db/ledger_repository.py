from fastapi import HTTPException
from sqlalchemy.orm import Session

from monorepo.core.db.models.LedgerEntryModel import LedgerEntryModel
from monorepo.core.db.models.LedgerEntryModel import LedgerEntryCreate

LEDGER_OPERATION_CONFIG = {
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}


class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, entry: LedgerEntryModel):
        self.db.add(entry)
        self.db.commit()

    def get_balance(self, owner_id: str) -> int:
        result = self.db.query(LedgerEntryModel).filter_by(owner_id=owner_id).all()
        return sum(entry.amount for entry in result)

    def get_by_nonce(self, owner_id: str, nonce: str):
        return self.db.query(LedgerEntryModel).filter_by(owner_id=owner_id, nonce=nonce).first()

    def get_all_entries(self, owner_id: str):
        return self.db.query(LedgerEntryModel).filter_by(owner_id=owner_id).all()

    def get_next_nonce(self, owner_id: str) -> str:
        latest_entry = (
            self.db.query(LedgerEntryModel)
            .filter_by(owner_id=owner_id)
            .order_by(LedgerEntryModel.id.desc())
            .first()
        )
        return str(int(latest_entry.nonce) + 1) if latest_entry else "1"

    def create_ledger_entry(self, ledger_entry: LedgerEntryCreate):
        if ledger_entry.operation not in LEDGER_OPERATION_CONFIG:
            raise ValueError("Invalid operation")

        amount = LEDGER_OPERATION_CONFIG[ledger_entry.operation]

        current_balance = self.get_balance(ledger_entry.owner_id)

        if amount < 0 and current_balance + amount < 0:
            raise HTTPException(status_code=400, detail="Insufficient balance for this operation.")

        db_ledger = LedgerEntryModel(
            operation=ledger_entry.operation,
            amount=amount,
            nonce=self.get_next_nonce(ledger_entry.owner_id),
            owner_id=ledger_entry.owner_id
        )
        self.db.add(db_ledger)
        self.db.commit()
        self.db.refresh(db_ledger)
        return db_ledger
