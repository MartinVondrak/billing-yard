from typing import IO

from jinja2 import Template
from weasyprint import HTML

from .models import Invoice, Subject
from .parser import Parser


class BillingYardError(Exception):
    pass


class BillingYard:
    def __init__(self, sender_path: str, template_path: str):
        self.sender: Subject = Parser.parse_subject_from_file(sender_path)
        try:
            template_file: IO = open(template_path)
            self.template: Template = Template(template_file.read())
        except OSError as error:
            raise BillingYardError(error)

    def create_invoice(self, invoice_path: str, receiver_path: str) -> Invoice:
        receiver: Subject = Parser.parse_subject_from_file(receiver_path)
        invoice: Invoice = Parser.parse_invoice_from_file(invoice_path)
        invoice.sender = self.sender
        invoice.receiver = receiver
        return invoice

    def print_invoice(self, invoice: Invoice):
        html: str = self.template.render(invoice=invoice, total_price=invoice.get_total_price())
        HTML(string=html).write_pdf(f'{invoice.invoice_number}.pdf')
