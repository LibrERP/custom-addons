# © 2021-2023 Didotech SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
from odoo.addons.report_aeroo.extra_functions import aeroo_util
from odoo.tools.misc import format_date as fd
# from odoo import _


@aeroo_util('italian_number')
def italian_number(report, number, precision=2, no_zero=False):
    if not number and no_zero:
        return ''
    elif not number:
        return '0,00'

    if number < 0:
        sign = '-'
    else:
        sign = ''

    # Requires Python >= 2.7:
    before, after = "{:.{digits}f}".format(number, digits=precision).split('.')
    # Works with Python 2.6:
    # if precision:
    #     before, after = "{0:10.{digits}f}".format(number, digits=precision).strip('- ').split('.')
    # else:
    #     before = "{0:10.{digits}f}".format(number, digits=precision).strip('- ').split('.')[0]
    #     after = ''

    belist = []
    end = len(before)
    for i in range(3, len(before) + 3, 3):
        start = len(before) - i
        if start < 0:
            start = 0
        belist.append(before[start: end])
        end = len(before) - i
    before = '.'.join(reversed(belist))

    if no_zero and int(number) == float(number) or precision == 0:
        return sign + before
    else:
        return sign + before + ',' + after


@aeroo_util('formatDate')
def formatDate(report, object, value, lang_code=False, date_format=False):
    return fd(object.env, value, lang_code, date_format)


@aeroo_util('utente')
def utente(report):
    return report.env.user


@aeroo_util('get_selection_item')
def get_selection_item(report, obj, field, value=None):
    if value is None:
        value = obj.option
    vals = dict(obj.fields_get(allfields=[field])[field]['selection'])
    return vals[value]


@aeroo_util('desc_nocode')
def desc_nocode(self, string):
    return re.compile('\[.*\]\ ').sub('', string)


@aeroo_util('cod_fiscale')
def cod_fiscale(report, o):
    if o.partner_id.fiscalcode:
        return o.partner_id.fiscalcode
    return ''


@aeroo_util('piva')
def piva(report, o):
    if o.partner_id.vat:
        return o.partner_id.vat
    return ''


@aeroo_util('codice_cliente')
def codice_cliente(report, o):
    if o.partner_id.code:
        return o.partner_id.code
    return ''


@aeroo_util('tel_cliente')
def tel_cliente(report, o):
    if o.partner_id.phone:
        return o.partner_id.phone
    return ''


# @aeroo_util('iva')
# def iva(report, o):
#     taxes = []
#     if o.tax_line_ids:
#         for tax in o.tax_line_ids:
#             if tax.tax_id.amount not in taxes:
#                 taxes.append(tax.tax_id.amount)
#     if taxes:
#         taxes = [str(round(i)) for i in taxes]
#     return ' - '.join(taxes)


# @aeroo_util('riga_iva')
# def riga_iva(report, riga):
#     taxes = []
#     if riga.invoice_line_tax_ids:
#         tax = riga.invoice_line_tax_ids[0]
#         if tax.amount not in taxes:
#             taxes.append(tax.amount)
#
#     if taxes:
#         taxes = [round(i) for i in taxes]
#     return ' - '.join(taxes)
