# Copyright 2019 ForgeFlow, S.L.
# Copyright 2020 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo import exceptions

from datetime import datetime
from decimal import Decimal
from io import BytesIO
from os import path
import itertools

import logging
_logger = logging.getLogger(__name__)


class AccountBankStatementImportSheetParser(models.TransientModel):
    _name = 'account.bank.statement.import.sheet.parser'
    _description = 'Account Bank Statement Import Sheet Parser'

    @api.model
    def parse_header(self, data_file, filename, encoding, csv_options):
        Parser = self.env['account.bank.statement.import.sheet.parser']
        csv_or_xlsx = Parser.read_table(data_file, filename, encoding, csv_options)
        return [str(value) for value in next(csv_or_xlsx)]

    @api.model
    def parse(self, mapping, data_file, filename):
        journal = self.env['account.journal'].browse(
            self.env.context.get('journal_id')
        )
        currency_code = (
            journal.currency_id or journal.company_id.currency_id
        ).name
        account_number = journal.bank_account_id.acc_number

        name = _('%s: %s') % (
            journal.code,
            path.basename(filename),
        )
        lines = self._parse_lines(mapping, data_file, filename, currency_code)
        if not lines:
            return currency_code, account_number, [{
                'name': name,
                'transactions': [],
            }]

        lines = list(sorted(
            lines,
            key=lambda line: line['timestamp']
        ))
        first_line = lines[0]
        last_line = lines[-1]
        data = {
            'name': name,
            'date': first_line['timestamp'].date(),
        }

        if mapping.balance_column:
            balance_start = first_line['balance']
            balance_start -= first_line['amount']
            balance_end = last_line['balance']
            data.update({
                'balance_start': float(balance_start),
                'balance_end_real': float(balance_end),
            })

        transactions = list(itertools.chain.from_iterable(map(
            lambda line: self._convert_line_to_transactions(line),
            lines
        )))
        data.update({
            'transactions': transactions,
        })

        return currency_code, account_number, [data]

    def import_sheet_generator(self, data_file, filename, encoding, csv_options, start_from=0):
        name, file_type = filename.lower().rsplit('.', 1)
        if file_type in ('xls', 'xlsb'):
            import xlrd
            from xlrd.xldate import xldate_as_datetime
            try:
                book = xlrd.open_workbook(
                    file_contents=data_file,
                    encoding_override=(
                        encoding if encoding else None
                    )
                )
            except UnicodeDecodeError:
                pass

            sh = book.sheet_by_index(0)

            for rx in range(start_from-1, sh.nrows):
                row = []
                for cx in range(sh.ncols):
                    cell = sh.cell(rowx=rx, colx=cx)
                    if cell.ctype == xlrd.XL_CELL_DATE:
                        cell_value = xldate_as_datetime(cell.value, book.datemode)
                    else:
                        cell_value = cell.value

                    row.append(cell_value)
                yield row

        elif file_type in ('xlsx', 'xlsm', 'xltx', 'xltm'):
            from openpyxl import load_workbook

            ## Create virtual File:
            virtual_file = BytesIO(data_file)
            # book = load_workbook(virtual_file, read_only=True)
            book = load_workbook(virtual_file, read_only=False)

            sh = book.worksheets[0]
            max_column = sh.max_column

            for count, shrow in enumerate(sh.rows, 1):
                if count >= start_from:
                    lrrow = list(shrow)
                    for cx in range(max_column - 1, 0, -1):
                        if lrrow[cx].value:
                            max_column = cx + 1
                            # Evaluates max columns to use in range
                            break
                    break

            for count, shrow in enumerate(sh.rows, 1):
                if count >= start_from:
                    row = []
                    lrrow = list(shrow)
                    for cx in range(0, max_column):
                        row.append(lrrow[cx].value)

                    if all(c is None for c in row):
                        break
                    yield row
        elif file_type == 'csv':
            import csv

            def unicode_csv_reader(unicode_csv_data,  delimiter, start_from, dialect=csv.excel, **kwargs):
                # csv.py doesn't do Unicode; encode temporarily as UTF-8:
                # csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                csv_reader = csv.reader(
                    table_reader(unicode_csv_data, start_from),
                    delimiter=delimiter,
                    dialect=dialect, **kwargs)
                for row in csv_reader:
                    # decode UTF-8 back to Unicode, cell by cell:
                    # yield [str(cell, 'utf-8') for cell in row]
                    yield row

            def table_reader(virtual_file_utf8, start_from):
                for count, line in enumerate(virtual_file_utf8, 1):
                    if count >= start_from:
                        yield line.decode('utf-8')

            ## Create virtual File
            # virtual_file = BytesIO(data_file)
            virtual_file_utf8 = BytesIO(data_file)

            ## Process CSV file:
            # sample = virtual_file.read(512)
            # virtual_file.seek(0)

            for row in unicode_csv_reader(virtual_file_utf8, csv_options.get('delimiter', None), start_from):
                yield row

        else:
            raise exceptions.Warning(_('Error: Unknown file extension'))

    def read_table(self, data_file, filename, encoding, csv_options, start_from):
        # table = list(self.import_sheet_generator(data_file, filename, encoding, csv_options))
        table = self.import_sheet_generator(data_file, filename, encoding, csv_options, start_from=start_from)
        return table

    def _parse_lines(self, mapping, data_file, filename, currency_code):
        csv_options = {}
        csv_delimiter = mapping._get_column_delimiter_character()
        if csv_delimiter:
            csv_options['delimiter'] = csv_delimiter
        if mapping.quotechar:
            csv_options['quotechar'] = mapping.quotechar
        if mapping.start_from:
            start_from = mapping.start_from
        else:
            start_from = 0
        csv_or_xlsx = self.read_table(data_file, filename, mapping.file_encoding, csv_options, start_from)

        # header = [str(value) for value in csv_or_xlsx.pop(0)]
        header = [str(value) for value in next(csv_or_xlsx)]

        timestamp_column = header.index(mapping.timestamp_column)
        currency_column = header.index(mapping.currency_column) \
            if mapping.currency_column else None
        amount_column = header.index(mapping.amount_column)
        debit_column = header.index(mapping.debit_column) \
            if mapping.debit_column else None
        balance_column = header.index(mapping.balance_column) \
            if mapping.balance_column else None
        original_currency_column = (
            header.index(mapping.original_currency_column)
            if mapping.original_currency_column else None
        )
        original_amount_column = (
            header.index(mapping.original_amount_column)
            if mapping.original_amount_column else None
        )
        debit_credit_column = header.index(mapping.debit_credit_column) \
            if mapping.debit_credit_column else None
        transaction_id_column = header.index(mapping.transaction_id_column) \
            if mapping.transaction_id_column else None
        description_column = header.index(mapping.description_column) \
            if mapping.description_column else None
        notes_column = header.index(mapping.notes_column) \
            if mapping.notes_column else None
        reference_column = header.index(mapping.reference_column) \
            if mapping.reference_column else None
        partner_name_column = header.index(mapping.partner_name_column) \
            if mapping.partner_name_column else None
        bank_name_column = header.index(mapping.bank_name_column) \
            if mapping.bank_name_column else None
        bank_account_column = header.index(mapping.bank_account_column) \
            if mapping.bank_account_column else None

        # if isinstance(csv_or_xlsx, tuple):
        #     rows = range(1, csv_or_xlsx[1].nrows)
        # else:
        rows = csv_or_xlsx

        lines = []
        for row in rows:
            if row and any(row):
                values = list(row)

                timestamp = values[timestamp_column]
                currency = values[currency_column] \
                    if currency_column is not None else currency_code
                amount = values[amount_column] or values[debit_column]
                balance = values[balance_column] \
                    if balance_column is not None else None
                original_currency = values[original_currency_column] \
                    if original_currency_column is not None else None
                original_amount = values[original_amount_column] \
                    if original_amount_column is not None else None
                debit_credit = values[debit_credit_column] \
                    if debit_credit_column is not None else None
                transaction_id = values[transaction_id_column] \
                    if transaction_id_column is not None else None
                description = values[description_column] \
                    if description_column is not None else None
                notes = values[notes_column] \
                    if notes_column is not None else None
                reference = values[reference_column] \
                    if reference_column is not None else None
                partner_name = values[partner_name_column] \
                    if partner_name_column is not None else None
                bank_name = values[bank_name_column] \
                    if bank_name_column is not None else None
                bank_account = values[bank_account_column] \
                    if bank_account_column is not None else None

                if currency.upper() == currency_code.upper():
                    if isinstance(timestamp, str):
                        timestamp = datetime.strptime(
                            timestamp,
                            mapping.timestamp_format
                        )

                    amount = self._parse_decimal(amount, mapping)
                    if balance:
                        balance = self._parse_decimal(balance, mapping)
                    else:
                        balance = None

                    if debit_credit:
                        amount = amount.copy_abs()
                        if debit_credit == mapping.debit_value:
                            amount = -amount

                    if not original_currency:
                        original_currency = currency
                        original_amount = amount
                    elif original_currency == currency:
                        original_amount = amount

                    if original_amount:
                        original_amount = self._parse_decimal(
                            original_amount,
                            mapping
                        ).copy_sign(amount)
                    else:
                        original_amount = 0.0

                    line = {
                        'timestamp': timestamp,
                        'amount': amount,
                        'currency': currency,
                        'original_amount': original_amount,
                        'original_currency': original_currency,
                    }
                    if balance is not None:
                        line['balance'] = balance
                    if transaction_id is not None:
                        line['transaction_id'] = transaction_id
                    if description is not None:
                        line['description'] = description
                    if notes is not None:
                        line['notes'] = notes
                    if reference is not None:
                        line['reference'] = reference
                    if partner_name is not None:
                        line['partner_name'] = partner_name
                    if bank_name is not None:
                        line['bank_name'] = bank_name
                    if bank_account is not None:
                        line['bank_account'] = bank_account
                    lines.append(line)
                else:
                    _logger.warning('Wrong currency')
            else:
                break
        return lines

    @api.model
    def _convert_line_to_transactions(self, line):
        """Hook for extension"""
        timestamp = line['timestamp']
        amount = line['amount']
        currency = line['currency']
        original_amount = line['original_amount']
        original_currency = line['original_currency']
        transaction_id = line.get('transaction_id')
        description = line.get('description')
        notes = line.get('notes')
        reference = line.get('reference')
        partner_name = line.get('partner_name')
        bank_name = line.get('bank_name')
        bank_account = line.get('bank_account')

        transaction = {
            'date': timestamp,
            'amount': str(amount),
        }
        if currency != original_currency:
            original_currency = self.env['res.currency'].search(
                [('name', '=', original_currency)],
                limit=1,
            )
            if original_currency:
                transaction.update({
                    'amount_currency': str(original_amount),
                    'currency_id': original_currency.id,
                })

        if transaction_id:
            transaction['unique_import_id'] = '%s-%s' % (
                transaction_id,
                int(timestamp.timestamp()),
            )

        transaction['name'] = description or _('N/A')
        if reference:
            transaction['ref'] = reference

        note = ''
        if bank_name:
            note += _('Bank: %s; ') % (
                bank_name,
            )
        if bank_account:
            note += _('Account: %s; ') % (
                bank_account,
            )
        if transaction_id:
            note += _('Transaction ID: %s; ') % (
                transaction_id,
            )
        if note and notes:
            note = '%s\n%s' % (
                note,
                note.strip(),
            )
        elif note:
            note = note.strip()
        if note:
            transaction['note'] = note

        if partner_name:
            transaction['partner_name'] = partner_name
        if bank_account:
            transaction['account_number'] = bank_account

        return [transaction]

    @api.model
    def _parse_decimal(self, value, mapping):
        if isinstance(value, Decimal):
            return value
        elif isinstance(value, (float, int)):
            return Decimal(value)
        else:
            thousands, decimal = mapping._get_float_separators()
            value = value.replace(thousands, '')
            value = value.replace(decimal, '.')
            return Decimal(value)
