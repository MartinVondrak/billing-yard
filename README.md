# Billing Yard

Billing Yard is an open source CLI tool written in Python 3 for generating invoices from [JSON](https://www.json.org)
for business entities in the Czech republic. It supports invoices for both VAT payers and non VAT payers.

If you like this software, please [buy me a coffee](https://www.buymeacoffee.com/martinvondrak).

## Installation

First, please note that the software has [WeasyPrint](https://weasyprint.org) as a dependency and WeasyPrint needs some
external third party libraries for correct functioning. The way to install these libraries will differ based on your
operating system. So first you need to install these dependencies according to the manual below, then you can install
Billing Yard itself.

The installation manual below expects you to know and understand how to work with [pip](https://pip.pypa.io)
and [Virtual Environment](https://docs.python.org/3/tutorial/venv.html).

### Linux

Below, you can find how to install external third party libraries on different Linux distributions.

#### Debian

Debian 11 Bullseye or newer

```shell
apt install python3-pip libpango-1.0-0 libpangoft2-1.0-0 libjpeg-dev libopenjp2-7-dev libffi-dev
```

#### Ubuntu

Ubuntu 20.04 Focal Fossa or newer

```shell
apt install python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev
```

#### Fedora

Fedora 34 or newer

```shell
dnf install python3-pip pango gcc python3-devel gcc-c++ zlib-devel libjpeg-devel openjpeg2-devel libffi-devel
```

#### Archlinux

```shell
pacman -S python-pip pango gcc libjpeg-turbo openjpeg2
```

#### Alpine

Alpine Linux 3.14 or newer

```shell
apk add py3-pip gcc musl-dev python3-dev pango zlib-dev jpeg-dev openjpeg-dev g++ libffi-dev
```

### macOS

Installation on macOS is recommended via [Homebrew](https://brew.sh).

```shell
brew install python3 pango libffi
```

### Windows and further support

For installation on Windows or further support, please see the
official [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows). But
please keep in mind that WeasyPrint must be installed as a dependency of Billing Yard and not directly using your OS
package manager.

### Installing Billing Yard

First you need to decide whether you want to use Virtual Environment or install Billing Yard globally. But note that
installing in Virtual Environment is always preferred way. Then just make sure you are using Python 3.9 or newer and
run following command, and you are done.

```shell
pip install billingyard
```

## Basic usage

First step is to create configuration and data source files for generating an invoice. All configuration and data
sources for an invoice are stored in JSON files. There are three schemas of JSON files, one for business entity (sender,
receiver), one for an invoice without VAT and one for an invoice with VAT. Then you can generate the invoice itself.

### Business entity

We create two business entities, sender (entity which issues the invoice) and receiver (entity which pays the invoice).

```json
{
  "company": "Company s.r.o.",
  "street": "Ulice 38",
  "city": "Praha",
  "zip_code": "100 00",
  "country": "Česká republika",
  "company_id": "00011000",
  "vat_id": "CZ00011000"
}
```

* **company** - the business name of the business entity
* **street** - the street in the address of the business entity
* **city** - the city in the address of the business entity
* **zip_code** - the zip code in the address of the business entity
* **country** - the country in the address of the business entity
* **company** - the identifier given by Czech authority of the business entity
* **vat_id** - the identifier for VAT purpose of the business entity
    * optional if business entity is not a VAT payer

### Invoice for a non VAT payer

Below you can find the self explaining example of a non VAT payer invoice with further description.

```json
{
  "invoice_number": "2021001",
  "issue_date": "01. 01. 2021",
  "due_date": "31. 01. 2021",
  "currency": "Kč",
  "bank": "Bank a.s.",
  "bank_account": "1234567890/1234",
  "payment_method": "bank transfer",
  "register_info": "Fyzická osoba zapsaná v živnostenském rejstříku.",
  "invoice_lines": [
    {
      "description": "software development",
      "unit": "hr",
      "quantity": 20,
      "unit_price": 1500
    }
  ]
}
```

* **invoice_number** - a unique identifier of the invoice
    * completely up to you, but keep in mind local policies from government
* **issue_date** - the date of issue of the invoice
    * optional, if not set current date is used
* **due_date** - the last day, when the invoice must be paid
* **currency** - the currency in which is the invoice issued
* **bank** - the bank of the sender business entity
* **bank_account** - the bank account number of the sender business entity
* **payment_method** - the agreed instrument to pay the invoice
    * e.g. bank transfer, cash, credit card
    * this text is directly rendered in the invoice
* **register_info** - the info about record in government registers of the sender business entity
    * the typical examples in Czech are "Fyzická osoba zapsaná v živnostenském rejstříku." or "Společnost je zapsána v
      obchodním rejstříku vedeném u Městského soudu v Praze, oddílu C, vložce 2396."
* **invoice_lines** - the list of items that are invoiced

Each invoice line consists of following properties.

* **description** - the name or more exhaustive description of the invoiced item
* **unit** - the unit which we can use to count the invoiced item
    * e.g. hour, piece, meter, square meter etc
* **quantity** - the amount of invoiced items in previously specified unit
* **unit_price** - the price of the invoiced item for one unit

All dates have `DD. MM. YYYY` format.

### Invoice for a VAT payer

Below you can find the self explaining example of a VAT payer invoice with further description.

```json
{
  "invoice_number": "2021001",
  "issue_date": "01. 01. 2021",
  "supply_date": "01. 01. 2021",
  "due_date": "31. 01. 2021",
  "currency": "Kč",
  "bank": "Bank a.s.",
  "bank_account": "1234567890/1234",
  "payment_method": "bank transfer",
  "register_info": "Fyzická osoba zapsaná v živnostenském rejstříku.",
  "invoice_lines": [
    {
      "description": "software development",
      "unit": "hr",
      "quantity": 20,
      "unit_price": 1500,
      "vat_rate": 0.21
    }
  ]
}
```

* **invoice_number** - a unique identifier of the invoice
    * completely up to you, but keep in mind local policies from government
* **issue_date** - the date of issue of the invoice
    * optional, if not set current date is used
* **supply_date** - the date of taxable supply
    * optional, if not set current date is used
* **due_date** - the last day, when the invoice must be paid
* **currency** - the currency in which is the invoice issued
* **bank** - the bank of the sender business entity
* **bank_account** - the bank account number of the sender business entity
* **payment_method** - the agreed instrument to pay the invoice
    * e.g. bank transfer, cash, credit card
    * this text is directly rendered in the invoice
* **register_info** - the info about record in government registers of the sender business entity
    * the typical examples in Czech are "Fyzická osoba zapsaná v živnostenském rejstříku." or "Společnost je zapsána v
      obchodním rejstříku vedeném u Městského soudu v Praze, oddílu C, vložce 2396."
* **invoice_lines** - the list of items that are invoiced

Each invoice line consists of following properties.

* **description** - the name or more exhaustive description of the invoiced item
* **unit** - the unit which we can use to count the invoiced item
    * e.g. hour, piece, meter, square meter etc
* **quantity** - the amount of invoiced items in previously specified unit
* **unit_price** - the price of the invoiced item for one unit without VAT
* **vat_rate** - the rate of VAT for this invoiced item

All dates have `DD. MM. YYYY` format.

### Generating an invoice

If you installed Billing Yard using Virtual Environment, just activate this environment and run one of the following
commands, depending on whether you are a VAT payer or not. If you installed Billing Yard globally, just run one of the
commands.

```shell
billingyard -s sender.json issue-invoice -i invoice.json -r receiver.json
```

The option `-s` expects path to JSON data file with information about a sender business entity. It can be omitted, if
its name is `sender.json` and it is located in the same directory from which is the command executed.

The option `-i` expects path to JSON data file with the invoice data.

The option `-r` expects path to JSON data file with information about a sender business entity.

```shell
billingyard -s sender.json issue-invoice -i invoice_vat.json -r receiver.json --vat
```

The option `--vat` is used to generate an invoice for a VAT payer sender business entity. Please do not forget, that in
this case, you have to also provide correct invoice JSON data file with all needed attributes.

## License

This software is released under MIT License and use other third party software.

* [Click](https://github.com/pallets/click/blob/main/LICENSE.txt)
* [Jinja2](https://github.com/pallets/jinja/blob/main/LICENSE.txt)
* [WeasyPrint](https://github.com/Kozea/WeasyPrint/blob/master/LICENSE)
