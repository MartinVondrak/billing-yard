import json
from datetime import datetime
from typing import IO

from .models import Subject, Invoice, InvoiceLine, InvoiceVat, InvoiceLineVat


class ParserError(Exception):
    pass


class Parser:
    @classmethod
    def parse_subject(cls, subject_file_path: str) -> Subject:
        try:
            subject_json: dict = cls.load_json_file(subject_file_path)
            subject: Subject = Subject(subject_json['company'], subject_json['street'], subject_json['city'],
                                       subject_json['zip_code'], subject_json['country'], subject_json['company_id'],
                                       subject_json['vat_id'])
        except IOError as error:
            raise ParserError(error)
        return subject

    @classmethod
    def parse_invoice(cls, invoice_file_path: str) -> Invoice:
        try:
            invoice_json: dict = cls.load_json_file(invoice_file_path)
            issue_date: datetime = cls.get_optional_datetime('issue_date', invoice_json)
            due_date: datetime = datetime.strptime(invoice_json['due_date'], '%d. %m. %Y')
            invoice: Invoice = Invoice(invoice_json['invoice_number'], issue_date, due_date, invoice_json['currency'],
                                       invoice_json['bank'], invoice_json['bank_account'],
                                       invoice_json['payment_method'], invoice_json['register_info'])
            for invoice_line in invoice_json['invoice_lines']:
                invoice.add_invoice_line(
                    InvoiceLine(invoice_line['description'], invoice_line['quantity'], invoice_line['unit'],
                                invoice_line['unit_price']))
        except IOError as error:
            raise ParserError(error)
        return invoice

    @classmethod
    def parse_vat_invoice(cls, invoice_file_path: str) -> InvoiceVat:
        try:
            invoice_json: dict = cls.load_json_file(invoice_file_path)
            issue_date: datetime = cls.get_optional_datetime('issue_date', invoice_json)
            supply_date: datetime = cls.get_optional_datetime('supply_date', invoice_json)
            due_date: datetime = datetime.strptime(invoice_json['due_date'], '%d. %m. %Y')
            invoice: InvoiceVat = InvoiceVat(invoice_json['invoice_number'], issue_date, due_date,
                                             invoice_json['currency'], invoice_json['bank'],
                                             invoice_json['bank_account'],
                                             invoice_json['payment_method'], invoice_json['register_info'], supply_date)
            for invoice_line in invoice_json['invoice_lines']:
                invoice.add_invoice_line(
                    InvoiceLineVat(invoice_line['description'], invoice_line['quantity'], invoice_line['unit'],
                                   invoice_line['unit_price'], invoice_line['vat_rate']))
        except IOError as error:
            raise ParserError(error)
        return invoice

    @classmethod
    def load_json_file(cls, file_path: str) -> dict:
        invoice_file_content: IO = open(file_path)
        return json.load(invoice_file_content)

    @classmethod
    def get_optional_datetime(cls, key: str, json_content: dict) -> datetime:
        if key in json_content:
            value: datetime = datetime.strptime(json_content[key], '%d. %m. %Y')
        else:
            value: datetime = datetime.now()
        return value
