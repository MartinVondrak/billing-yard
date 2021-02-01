import os

import click

from .billingyard import BillingYard
from .models import Invoice


@click.group('billingyard')
@click.option('-s', '--sender', type=str, default='sender.json')
@click.option('-t', '--template', type=str, default=f'{os.path.dirname(__file__)}/templates/invoice.html')
@click.pass_context
def cli(ctx, sender: str, template: str):
    ctx.obj = BillingYard(sender, template)


pass_billing_yard = click.make_pass_decorator(BillingYard)


@cli.command()
@click.option('-r', '--receiver', type=str)
@click.option('-i', '--invoice', type=str)
@pass_billing_yard
def issue_invoice(billing_yard: BillingYard, receiver: str, invoice: str):
    invoice: Invoice = billing_yard.create_invoice(invoice, receiver)
    billing_yard.print_invoice(invoice)
