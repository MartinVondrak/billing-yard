from datetime import datetime
from typing import Optional


class Subject:
    def __init__(self, company: str, street: str, city: str, zip_code: str, country: str, company_id: str,
                 is_vat_payer=False, vat_id: Optional[str] = None):
        self.company = company
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country
        self.company_id = company_id
        self.is_vat_payer = is_vat_payer
        self.vat_id = vat_id


class InvoiceLine:
    def __init__(self, description: str, quantity: float, unit: str, unit_price: float):
        self.description = description
        self.quantity = quantity
        self.unit = unit
        self.unit_price = unit_price
        self.price = quantity * unit_price


class Invoice:
    def __init__(self, invoice_number: int, issue_date: datetime, due_date: datetime, currency: str, bank: str,
                 bank_account: str, payment_method: str, register_info: str):
        self.invoice_number = invoice_number
        self.issue_date = issue_date
        self.due_date = due_date
        self.currency = currency
        self.bank = bank
        self.bank_account = bank_account
        self.payment_method = payment_method
        self.register_info = register_info
        self._sender: Optional[Subject] = None
        self._receiver: Optional[Subject] = None
        self._invoice_lines: list[InvoiceLine] = list()

    @property
    def sender(self) -> Subject:
        return self._sender

    @sender.setter
    def sender(self, sender: Subject):
        self._sender = sender

    @property
    def receiver(self) -> Subject:
        return self._receiver

    @receiver.setter
    def receiver(self, receiver: Subject):
        self._receiver = receiver

    @property
    def invoice_lines(self) -> list[InvoiceLine]:
        return self._invoice_lines

    def add_invoice_line(self, invoice_line: InvoiceLine):
        self._invoice_lines.append(invoice_line)

    def get_total_price(self) -> float:
        total_price: float = 0
        for invoice_line in self.invoice_lines:
            total_price += invoice_line.price
        return total_price
