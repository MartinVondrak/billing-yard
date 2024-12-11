import base64
from io import BytesIO

import qrcode

from billingyard.models import Invoice


class QRCodeGenerator:
    @classmethod
    def generate_qr_code(cls, invoice: Invoice) -> str | None:
        if invoice.iban is None:
            return None
        total_price = '{:.2f}'.format(invoice.get_total_price())
        qr_code_content = f'SPD*1.0*ACC:{invoice.iban}*AM:{total_price}*CC:{invoice.get_currency_code()}*X-VS:{invoice.invoice_number}'
        qr_code = qrcode.make(qr_code_content)
        buffer = BytesIO()
        qr_code.save(buffer)
        return base64.b64encode(buffer.getvalue()).decode()
