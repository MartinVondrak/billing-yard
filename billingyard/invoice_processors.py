import os
from abc import ABC, abstractmethod
from typing import IO

from jinja2 import Environment, Template
from weasyprint import HTML

from .models import Subject, Invoice, InvoiceVat
from .parser import Parser


def format_price(value: float) -> str:
    return '{:,.2f}'.format(value).replace(',', ' ').replace('.', ',')


class InvoiceProcessorError(Exception):
    pass


class BaseInvoiceProcessor(ABC):
    def __init__(self, template_path: str):
        self.environment: Environment = Environment()
        self.environment.filters['price'] = format_price
        try:
            template_file: IO = open(template_path)
            self.template: Template = self.environment.from_string(template_file.read())
        except OSError as error:
            raise InvoiceProcessorError(error)

    @abstractmethod
    def create_invoice(self, invoice_path: str, receiver_path: str) -> Invoice:
        pass

    @abstractmethod
    def print_invoice(self, invoice: Invoice) -> None:
        pass


class InvoiceProcessor(BaseInvoiceProcessor):
    def __init__(self, template_path: str):
        if template_path is None:
            template_path = f'{os.path.dirname(__file__)}/templates/invoice.html'
        super().__init__(template_path)

    def create_invoice(self, invoice_path: str, receiver_path: str) -> Invoice:
        receiver: Subject = Parser.parse_subject(receiver_path)
        invoice: Invoice = Parser.parse_invoice(invoice_path)
        invoice.receiver = receiver
        return invoice

    def print_invoice(self, invoice: Invoice) -> None:
        html: str = self.template.render(invoice=invoice, total_price=invoice.get_total_price())
        HTML(string=html).write_pdf(f'{invoice.invoice_number}.pdf')


class VatInvoiceProcessor(BaseInvoiceProcessor):
    def __init__(self, template_path: str):
        if template_path is None:
            template_path = f'{os.path.dirname(__file__)}/templates/vat_invoice.html'
        super().__init__(template_path)

    def create_invoice(self, invoice_path: str, receiver_path: str) -> InvoiceVat:
        receiver: Subject = Parser.parse_subject(receiver_path)
        invoice: InvoiceVat = Parser.parse_vat_invoice(invoice_path)
        invoice.receiver = receiver
        return invoice

    def print_invoice(self, invoice: InvoiceVat) -> None:
        html: str = self.template.render(invoice=invoice, vat_summary=invoice.get_vat_summary(),
                                         total_price=invoice.get_total_price())
        HTML(string=html).write_pdf(f'{invoice.invoice_number}.pdf')
