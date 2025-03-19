from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from monorepo.core.db.database import get_db
from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.db.models.LedgerEntryModel import LedgerEntryCreate
from monorepo.core.ledgers.services.base_ledger_service import BaseLedgerService
from healthai.src.api.ledgers.schemas import HealthAILedgerOperation


class LedgerEntryRequest(BaseModel):
    operation: HealthAILedgerOperation
    amount: int
    nonce: str
    owner_id: str


router = APIRouter()


def get_ledger_service(db: Session = Depends(get_db)):
    return BaseLedgerService(ledger_repo=LedgerRepository(db))


@router.post("/ledger/")
def create_ledger_entry(entry: LedgerEntryCreate, db: Session = Depends(get_db)):
    ledger_repo = LedgerRepository(db)

    existing_entries = ledger_repo.get_all_entries(entry.owner_id)
    if not existing_entries and entry.operation != "SIGNUP_CREDIT":
        raise HTTPException(status_code=400, detail="Account does not exist. Must start with SIGNUP_CREDIT.")

    if entry.operation == "SIGNUP_CREDIT" and existing_entries:
        raise HTTPException(status_code=400, detail="Account already exists.")

    new_entry = ledger_repo.create_ledger_entry(entry)
    return {"message": "Ledger entry created successfully.", "entry": new_entry}


@router.get("/ledger/{owner_id}/")
def get_balance(owner_id: str, db: Session = Depends(get_db)):
    ledger_repo = LedgerRepository(db)
    balance = ledger_repo.get_balance(owner_id)
    return {"owner_id": owner_id, "balance": balance}


@router.get("/ledger/{owner_id}/entries/")
def get_ledger_entries(owner_id: str, db: Session = Depends(get_db)):
    ledger_repo = LedgerRepository(db)
    entries = ledger_repo.get_all_entries(owner_id)
    return {"owner_id": owner_id, "entries": entries}
