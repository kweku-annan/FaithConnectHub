from app.models import storage
from app.models.finance import FinancialRecord

finance = FinancialRecord(
    amount=500.00,
    type="Income",
    category="Tithes",
    description="January church tithes",
    date="2025-01-22"
)
finance.save()
print(storage.query(FinancialRecord).all())
