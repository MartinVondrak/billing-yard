from .invoice_processors import InvoiceProcessor, BaseInvoiceProcessor, VatInvoiceProcessor
from .models import Invoice, Subject
from .parser import Parser
from .qrcode_generator import QRCodeGenerator


class BillingYard:
    def __init__(self, sender_path: str, user_template_path: str):
        self.sender: Subject = Parser.parse_subject(sender_path)
        self.user_template_path: str = user_template_path
        self.invoice_processor: BaseInvoiceProcessor = InvoiceProcessor(self.user_template_path)

    def create_invoice(self, invoice_path: str, receiver_path: str) -> Invoice:
        invoice: Invoice = self.invoice_processor.create_invoice(invoice_path, receiver_path)
        invoice.sender = self.sender
        return invoice

    def print_invoice(self, invoice: Invoice):
        qr_code = QRCodeGenerator.generate_qr_code(invoice)
        self.invoice_processor.print_invoice(invoice, qr_code)

    def set_invoice_processor(self):
        self.invoice_processor = InvoiceProcessor(self.user_template_path)

    def set_vat_invoice_processor(self):
        self.invoice_processor = VatInvoiceProcessor(self.user_template_path)
