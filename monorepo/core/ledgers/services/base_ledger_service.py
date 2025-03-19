from monorepo.core.db.ledger_repository import LedgerRepository
from monorepo.core.db.models.LedgerEntryModel import LedgerEntryModel
from monorepo.core.ledgers.schemas import SharedLedgerOperation

LEDGER_OPERATION_CONFIG = {
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}


class BaseLedgerService:
    def __init__(self, ledger_repo: LedgerRepository):
        self.ledger_repo = ledger_repo

    def update_balance(self, operation: SharedLedgerOperation, owner_id: str, nonce: str):
        if self.is_duplicate_nonce(owner_id, nonce):
            raise ValueError("Duplicate transaction detected!")

        balance = self.ledger_repo.get_balance(owner_id)
        required_amount = self.get_required_amount(operation)

        if operation == SharedLedgerOperation.CREDIT_SPEND and balance < required_amount:
            raise ValueError("Insufficient balance!")

        self.add_entry(owner_id, operation, nonce)
        self.ledger_repo.update_balance(owner_id, required_amount)

        return {"message": "Transaction recorded successfully"}

    def is_duplicate_nonce(self, owner_id: str, nonce: str) -> bool:
        existing_entry = self.ledger_repo.get_by_nonce(owner_id, nonce)
        return existing_entry is not None

    def get_required_amount(self, operation: SharedLedgerOperation) -> int:
        return LEDGER_OPERATION_CONFIG.get(operation.value, 0)

    def add_entry(self, owner_id: str, operation: SharedLedgerOperation, nonce: str):
        new_entry = LedgerEntryModel(owner_id=owner_id, operation=operation.value, nonce=nonce)
        self.ledger_repo.add(new_entry)

    def get_balance(self, owner_id: str) -> int:
        entries = self.ledger_repo.get_all_entries(owner_id)
        balance = sum(LEDGER_OPERATION_CONFIG.get(entry.operation, 0) for entry in entries)
        return balance

    def has_sufficient_balance(self, owner_id: str, operation: SharedLedgerOperation) -> bool:
        return self.get_balance(owner_id) >= self.get_required_amount(operation)
