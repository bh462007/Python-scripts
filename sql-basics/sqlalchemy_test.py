from sqlalchemy import create_engine, String, Float, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine("sqlite:///reconciliation.db")
print("Database connected")

class Base(DeclarativeBase):
    pass

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[str] = mapped_column(String, primary_key=True)
    vendor: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String)

Base.metadata.create_all(engine)

# 1. CREATE / INSERT
with Session(engine) as session:
    existing_invoice = session.get(Invoice, "INV001")
    if existing_invoice is None:
        invoice = Invoice(invoice_id="INV001", vendor="abc ltd", amount=5000, date="2026-09-20")
        session.add(invoice)
        session.commit()
        print("Invoice inserted")
    else:
        print("Invoice already exists")

# 2. UPDATE
with Session(engine) as session:
    invoice = session.get(Invoice, "INV001")
    if invoice:
        invoice.amount = 5500
        session.commit()
        print("Invoice updated")

# 3. READ / PRINT (Moved up here so it actually finds data!)
with Session(engine) as session:
    statement = select(Invoice).where(Invoice.invoice_id == "INV001")
    result = session.execute(statement)
    invoice = result.scalar_one()

    print(f"\n--- Current Database Record ---")
    print(f"ID: {invoice.invoice_id}")
    print(f"Vendor: {invoice.vendor}")
    print(f"Amount: {invoice.amount}")
    print(f"Date: {invoice.date}\n")

# 4. DELETE
with Session(engine) as session:
    invoice = session.get(Invoice, "INV001")
    if invoice:
        session.delete(invoice)
        session.commit()
        print("Invoice deleted")

# 5. SAFE VERIFICATION (Verifying it is truly gone)
with Session(engine) as session:
    invoice = session.get(Invoice, "INV001")
    if invoice is None:
        print("Verification: Invoice 'INV001' no longer exists in the database.")
