# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
"""
create_account_files.py:

    -F <csv_file>
    -h - help

Ex:
    create_account_files.py -F <csv_file>

"""

import getopt
import sys
import re
from dataclasses import dataclass
import csv


@dataclass
class R:
    id: int = 0
    B: int = 1
    name: int = 2
    account_type: int = 3
    reconcile: int = 4
    F: int = 5
    G: int = 6

group_record_template = """
        <record id="account_group_{id}" model="account.group">
            <field name="code_prefix_start">{id}</field>
            <field name="code_prefix_end">{end}</field>
            <field name="name">{name}</field>
            {parent}
        </record>"""

parent_template = '<field name="parent_id" ref="l10n_it.account_group_{parent}"/>'

# group_template = """<?xml version="1.0" encoding="utf-8"?>
# <odoo>
#     <data noupdate="1">
#         {records}
#     </data>
# </odoo>
# """

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    # csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
    delimiter = ','
    csv_reader = csv.reader(
        table_reader(unicode_csv_data),
        delimiter=delimiter,
        dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        # yield [str(cell, 'utf-8') for cell in row]
        yield row

# def utf_8_encoder(unicode_csv_data):
#     for line in unicode_csv_data:
#         yield line.encode('utf-8')

def table_reader(virtual_file_utf8):
    for line in virtual_file_utf8:
        # yield line.decode('utf-8')
        yield line

def sanitize(name):
    name = name.replace('&', '&amp;')
    return name

def script_help():
    import __main__
    return __main__.__doc__


if __name__ == '__main__':
    # LOCAL VERSION
    file_path = False
    test = False

    options, remainder = getopt.getopt(sys.argv[1:], 'F:h:t',
                                       [
                                           'file='
                                           'help',
                                           'test'
                                       ])

    print(options)
    for opt, arg in options:
        if opt in ('-F', '--file'):
            file_path = arg
        elif opt in ('-t', '--test'):
            test = True
        elif opt in ('-h', '--help'):
            print(script_help())
            sys.exit()
        else:
            print(script_help())
            sys.exit()

    if not all([file_path,]):
        print(script_help())
        sys.exit()

    with open(file_path, 'r') as data_file:
        with open('account_group-it.xml', 'w') as groups:
            with open('account.account-it.csv', 'w') as coa:
                groups.write("""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">""")

                coa_writer = csv.writer(
                    coa, delimiter=',',
                    quotechar='"',
                    # quoting=csv.QUOTE_MINIMAL
                    quoting=csv.QUOTE_ALL
                )

                coa_writer.writerow(["id", "code", "name", "account_type", "reconcile", "tag_ids", "name@it"])

                for counter, row in enumerate(unicode_csv_reader(data_file), start=1):
                    if counter > 1:
                        print(row)
                        name = sanitize(row[R.name])
                        if len(row[R.id]) == 2:
                            group = group_record_template.format(id=row[R.id], name=name, end=row[R.id], parent='')
                        elif len(row[R.id]) == 4:
                            parent = parent_template.format(parent=row[R.id][:2])
                            group = group_record_template.format(id=row[R.id], name=name, end=int(row[R.id]), parent=parent)
                        elif len(row[R.id]) == 6:
                            parent = parent_template.format(parent=row[R.id][:4])
                            group = group_record_template.format(id=row[R.id], name=name, end=int(row[R.id]), parent=parent)
                        else:
                            group = False
                            coa_writer.writerow(['urmet_ate_coa_' + row[R.id], row[R.id], name, row[R.account_type], row[R.reconcile], "", name])

                        if group:
                            print(group)
                            groups.write('\n' + group)

                groups.write("""
    </data>
</odoo>
""")