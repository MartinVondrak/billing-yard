import json
from datetime import datetime
from typing import IO

from .models import Subject, Invoice, InvoiceLine


class ParserError(Exception):
    pass


class Parser:
    @classmethod
    def parse_subject_from_file(cls, subject_file_path: str) -> Subject:
        try:
            subject_file_content: IO = open(subject_file_path)
            subject_json: dict = json.load(subject_file_content)
            subject: Subject = Subject(subject_json['company'], subject_json['street'], subject_json['city'],
                                       subject_json['zip_code'], subject_json['country'], subject_json['company_id'],
                                       subject_json['is_vat_payer'], subject_json['vat_id'])
        except IOError as error:
            raise ParserError(error)
        return subject

    @classmethod
    def parse_invoice_from_file(cls, invoice_file_path: str) -> Invoice:
        try:
            invoice_file_content: IO = open(invoice_file_path)
            invoice_json: dict = json.load(invoice_file_content)
            if 'issue_date' in invoice_json:
                issue_date: datetime = datetime.strptime(invoice_json['issue_date'], '%d. %m. %Y')
            else:
                issue_date: datetime = datetime.now()
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
