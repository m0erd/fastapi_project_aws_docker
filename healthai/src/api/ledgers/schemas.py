from monorepo.core.ledgers.schemas import BaseLedgerOperation


class HealthAILedgerOperation(BaseLedgerOperation):
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"
