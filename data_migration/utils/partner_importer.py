# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015-2016 Didotech srl (info at didotech.com)
#
#                          All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import _
from odoo.addons.data_migration import settings
from .utils import BaseImport
from collections import namedtuple
# from openerp import exceptions
from pprint import pprint
from odoo.addons.base_iban.models.res_partner_bank import normalize_iban as format_iban
from odoo.addons.base_iban.models.res_partner_bank import pretty_iban as pretty_iban


import vatnumber

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

COUNTRY_CODES = settings.COUNTRY_CODES
DEBUG = settings.DEBUG

if DEBUG:
    import pdb
    _logger.setLevel(logging.DEBUG)
else:
    _logger.setLevel(logging.INFO)

PROPERTY_REF_MAP = {
    'supplier': 'property_supplier_ref',
    'customer': 'property_customer_ref'
}

UPDATE_ON_CODE = True
DONT_STOP_ON_WRONG_VAT = True


class ImportFile(BaseImport):
    def __init__(self, env, import_record_id):
        # Inizializzazione superclasse
        BaseImport.__init__(self, env, import_record_id, import_model='partner.import')

        self.message_title = _("Importazione partner")
        self.partner_obj = self.env['res.partner']
        self.category_obj = self.env['res.partner.category']
        self.l18n_base_data_it = self.env['ir.module.module'].search([
            ('name', '=', 'l18n_base_data_it'), ('state', '=', 'installed')]) and True or False
        if self.l18n_base_data_it:
            self.city_obj = self.env['res.city.it.code']
            self.province_obj = self.env['res.province']

        self.state_obj = self.env['res.country.state']
        self.account_fiscal_position_obj = self.env['account.fiscal.position']

        config = getattr(settings, self.import_record.file_format)
        self.HEADER = config.HEADER_PARTNER
        self.REQUIRED = config.REQUIRED_PARTNER
        self.PARTNER_SEARCH = config.PARTNER_SEARCH
        self.ADDRESS_TYPE = config.ADDRESS_TYPE
        self.DEFAULT_COUNTRY = config.DEFAULT_COUNTRY
        self.Record = namedtuple('Record', config.COLUMNS_PARTNER)
        self.partner_type = self.import_record.partner_type
        self.strict = self.import_record.strict

        self.parent_id = False

        # self.partner_template = self.env['partner.import.template']
        # self.partner_template_id = self.partnerImportRecord.partner_template_id
        # self.partnerImportID = ids[0]

        self.partner_subaccount = self.env['ir.module.module'].search([
            ('name', '=', 'partner_subaccount'), ('state', '=', 'installed')]) and True or False

    def _find_partner(self, vals_partner):
        partner_clone = set()
        for field in self.PARTNER_SEARCH:
            if vals_partner.get(field, False):
                _logger.info(u"{0} = {1}".format(field, vals_partner[field]))
                partner_ids = self.partner_obj.search([(field, '=', vals_partner[field])])
                if len(partner_ids) == 1:
                    if self.strict:
                        partner_clone.add(partner_ids[0])
                    else:
                        return partner_ids[0]
                elif len(partner_ids) > 1:
                    error = u'Riga {line}: Trovati più clienti con {field} = {name}'.format(line=self.processed_lines, field=field, name=vals_partner[field])
                    _logger.debug(error)
                    self.error.append(error)
                    return -1

        if len(partner_clone) == 1:
            partner_id = partner_clone.pop()
            partner = self.partner_obj.browse(partner_id)
            for field in self.PARTNER_SEARCH:
                if vals_partner.get(field, False) and not vals_partner[field] == getattr(partner, field):
                    error = u'Riga {line}: Trovati più cloni del cliente {name}'.format(line=self.processed_lines, name=partner.name)
                    _logger.debug(error)
                    self.error.append(error)
                    
                    error = u'Riga {line}: ----------------------------- {name} {vat}'.format(line=self.processed_lines, name=vals_partner['name'], vat=vals_partner.get('vat', ''))
                    _logger.debug(error)
                    self.error.append(error)
                    return -1
            return partner_id
        elif len(partner_clone) > 1:
            error = u'Riga {line}: Trovati più cloni del cliente {name}'.format(line=self.processed_lines, name=vals_partner['name'])
            _logger.debug(error)
            self.error.append(error)
            return -1
        return False

    def _contry_by_code(self, code, lang):
        countries = self.env['res.country'].with_context(lang=lang).search([('code', '=', code)])
        if countries:
            return countries[0]
        else:
            return False

    def get_or_create_bank(self, iban, partner):
        bank_obj = self.env['res.partner.bank']

        if bank_obj.is_iban_valid(iban):
            formatted_iban = format_iban(iban)
            formatted_iban = pretty_iban(formatted_iban)
            banks = bank_obj.search([('acc_number', '=', formatted_iban), ('state', '=', 'iban')])

            if banks:
                return banks.ids
            else:
                bank = bank_obj.create({
                    'acc_number': iban,
                    'state': 'iban',
                    'partner_id': partner.id,
                    'owner_name': partner.name,
                    'street': partner.street,
                    'zip': partner.zip,
                    'city': partner.city,
                    'state_id': partner.state_id and partner.state_id.id,
                    'country_id': partner.country_id and partner.country_id.id
                })
                return [bank.id]
        else:
            error = u"Riga {0}: IBAN {iban} is not valid. IBAN viene ignorato.".format(self.processed_lines, iban=iban)
            _logger.debug(error)
            self.warning.append(error)

    def get_state(self, city_name, state_code, country_code, country_id):
        if country_code == 'IT':
            module = self.env['ir.module.module'].search([('name', '=', 'l10n_it_fiscalcode'), ('state', '=', 'installed')])
            if module:
                city = self.env['res.city.it.code'].search([('name', '=', city_name.upper())])
                if city:
                    city = city[0]
                    state = self.env['res.country.state'].search([('code', '=', city.province), ('country_id', '=', country_id)])
                    if not state:
                        state = self.env['res.country.state'].create({
                            'code': city.province,
                            'name': city_name.lower().capitalize(),
                            'country_id': country_id
                        })
                    return state.id
        else:
            state = self.env['res.country.state'].search([('code', '=', state_code)])
            if state:
                return state.id

        return False

    # def write_address(self, address_type, partner_id, record, vals_partner, country_code, force_default=False):
    #     vals_address = {
    #         'partner_id': partner_id,
    #         'name': vals_partner['name'],
    #         'type': address_type,
    #         'active': True
    #     }
    #
    #     if force_default:
    #         vals_address['type'] = 'default'
    #
    #     for field in ('street', 'street2', 'city', 'zip', 'country', 'email', 'phone', 'fax'):
    #         if hasattr(record, field + '_' + address_type) and getattr(record, field + '_' + address_type):
    #             vals_address[field] = getattr(record, field + '_' + address_type)
    #
    #     if len(record.fiscalcode) == 16 and not record.person_name:
    #         vals_address['name'] = ''
    #
    #     # Excel treats all numbers as floats
    #     vals_address['zip'] = vals_address.get('zip') and self.simple_string(vals_address['zip'], as_integer=True) or ''
    #
    #     if vals_address.get('zip') or vals_address.get('city'):
    #         city_ids = []
    #         # Not always we can get a city by zip code. A city can have more than one.
    #         if vals_address.get('city'):
    #             city_ids = self.city_obj.search([('name', '=ilike', vals_address['city'])])
    #
    #         if vals_address.get('zip') and not city_ids:
    #             city_ids = self.city_obj.search([('zip', '=', vals_address['zip'])])
    #
    #         if city_ids:
    #             city_data = self.city_obj.browse(city_ids[0])
    #             vals_address['city'] = city_data.name
    #             vals_address['zip'] = city_data.zip
    #             pdb.set_trace()
    #             vals_address['province'] = city_data.province_id.id
    #             vals_address['region'] = city_data.province_id.region.id
    #             vals_address['country_id'] = city_data.province_id.region.country_id.id
    #
    #     if not vals_address.get('province'):
    #         if hasattr(record, 'province_' + address_type):
    #             province_ids = self.province_obj.search([('code', '=', getattr(record, 'province_' + address_type))])
    #             if province_ids:
    #                 vals_address['province'] = province_ids[0]
    #                 province_data = self.province_obj.browse(province_ids[0])
    #                 vals_address['region'] = province_data.region.id
    #                 vals_address['country_id'] = province_data.region.country_id.id
    #             else:
    #                 state_ids = self.state_obj.search([('code', '=', getattr(record, 'province_' + address_type))])
    #                 if state_ids:
    #                     vals_address['state_id'] = state_ids[0]
    #
    #     if record.country_code and not vals_address.get('country_id'):
    #         vals_address['country_id'] = self._contry_by_code(country_code)
    #
    #     if DEBUG:
    #         pprint(vals_address)
    #
    #     if vals_address.get('country_id'):
    #         address_ids = self.address_obj.search([('partner_id', '=', vals_address['partner_id']), ('type', '=', vals_address['type'])])
    #         if address_ids:
    #             address_id = address_ids[0]
    #             self.address_obj.write(address_id, vals_address)
    #         else:
    #             self.address_obj.create(vals_address)
    #
    #     return True

    def import_row(self, row_list):
        if not len(row_list) == len(self.HEADER):
            error = u'Riga {0} non importata. Colonne non corrsipondono al Header definito'.format(self.processed_lines)
            _logger.debug(error)
            self.error.append(error)
            return False

        if DEBUG:
            # pprint(row_list)
            row_str_list = [self.to_string(value) for value in row_list]
            pprint(zip(self.HEADER, row_str_list))

        record = self.Record._make([self.to_string(value) for value in row_list])

        if self.first_row:
            if not record.name:
                warning = u'Riga {0}: Trovato Header'.format(self.processed_lines)
                _logger.debug(warning)
                self.warning.append(warning)
                return True
            else:
                for column in record:
                    if column in self.HEADER:
                        warning = u'Riga {0}: Trovato Header'.format(self.processed_lines)
                        _logger.debug(warning)
                        self.warning.append(warning)
                        return True

        self.first_row = False

        for field in self.REQUIRED:
            if not getattr(record, field):
                error = u"Riga {0}: Manca il valore della {1}. La riga viene ignorata.".format(self.processed_lines, field)
                _logger.debug(error)
                self.error.append(error)
                return False

        # manage partners
        vals_partner = {
            'name': record.name,
            #'fiscalcode': record.fiscalcode,
            self.partner_type: True
        }

        if 'supplier' in vals_partner:
            vals_partner['customer'] = False

        if hasattr(record, 'person_name') and record.person_name:
            vals_partner['name'] += ' {0}'.format(record.person_name)

        if record.country_code:
            country_code = COUNTRY_CODES.get(record.country_code.lower(), record.country_code)
        else:
            country_code = COUNTRY_CODES.get(self.DEFAULT_COUNTRY.lower())

        if country_code:
            country = self._contry_by_code(country_code, lang='it_IT')
            if country:
                fiscal_positions = self.account_fiscal_position_obj.search([('name', '=ilike', country.name)])

                if fiscal_positions and len(fiscal_positions) == 1:
                    vals_partner['property_account_position'] = fiscal_positions.id
                else:
                    warning = u"Riga {0}: Fiscal position can't be determined for partner {1}, using '{2}' as default value".format(
                        self.processed_lines, vals_partner['name'], self.DEFAULT_COUNTRY)
                    _logger.debug(warning)
                    self.warning.append(warning)
                    fiscal_positions = self.account_fiscal_position_obj.search([('name', '=ilike', self.DEFAULT_COUNTRY)])
                    vals_partner['property_account_position'] = fiscal_positions.id

                vals_partner['country_id'] = country.id
            else:
                error = u"Riga {0}: Country code '{1}' non è riconosciuto. La riga viene ignorata.".format(self.processed_lines, country_code)
                _logger.debug(error)
                self.error.append(error)
                return False

        if hasattr(record, 'fiscal_position') and record.fiscal_position:
            fiscal_position = self.partner_template.map_account_fiscal_position(self.partner_template_id, record.fiscal_position)
            if fiscal_position:
                vals_partner['property_account_position'] = fiscal_position

        if hasattr(record, 'payment_term') and record.payment_term:
            vals_payment = self.partner_template.map_payment_term(self.partner_template_id, record.payment_term)
            if vals_payment.get('property_payment_term', False):
                vals_partner['property_payment_term'] = vals_payment['property_payment_term']
            if vals_payment.get('company_bank_id', False):
                vals_partner['company_bank_id'] = vals_payment['company_bank_id']

        if record.vat and len(record.vat) > 3:
            vals_partner['vat_subjected'] = True
            vals_partner['individual'] = False
            vals_partner['is_company'] = True

            if not country_code == record.vat[:2]:
                vals_partner['vat'] = country_code + record.vat
            else:
                vals_partner['vat'] = record.vat.replace(' ', '')

            #if not self.partner_obj.simple_vat_check(cr, uid, country_code.lower(), vals_partner['vat'][2:], None):
            if not vatnumber.check_vat(vals_partner['vat']):
                error = u"Riga {line}: Partner '{record.code} {record.name}'; Partita IVA errata: {record.vat}".format(line=self.processed_lines, record=record)
                _logger.debug(error)
                self.error.append(error)
                if DONT_STOP_ON_WRONG_VAT:
                    del vals_partner['vat']
                else:
                    return False

            if vals_partner.get('vat') and record.vat == record.fiscalcode:
                vals_partner['fiscalcode'] = record.fiscalcode

        if record.fiscalcode:
            fiscalcode = record.fiscalcode.replace(' ', '')

        if record.fiscalcode and not record.fiscalcode == record.vat and not len(fiscalcode) == 16 and fiscalcode.isdigit():
            vals_partner['fiscalcode'] = fiscalcode
        elif record.fiscalcode and record.vat and not fiscalcode.isdigit() and len(fiscalcode) == 16:
            # Ditta individuale
            vals_partner['fiscalcode'] = fiscalcode
        elif record.fiscalcode and not record.vat and not fiscalcode.isdigit() and len(fiscalcode) == 16:
            vals_partner['individual'] = True
            vals_partner['fiscalcode'] = fiscalcode
            vals_partner['is_company'] = False
        elif record.fiscalcode and not vals_partner.get('fiscalcode'):
            error = u"Riga {0}: Codice Fiscale {1} errato".format(self.processed_lines, record.fiscalcode)
            _logger.debug(error)
            self.error.append(error)

        if record.fiscalcode and len(vals_partner.get('fiscalcode', '')) == 10:
            vals_partner['fiscalcode'] = '0' + vals_partner['fiscalcode']

        # if country_code == 'IT':
        #    vals_partner['property_account_position'] = self.italy_fiscal_position_id
        #    if record.vat:
        #        pdb.set_trace()
        #        old_vat = vals_input['Partita IVA']
        #        if len(vals_input['Partita IVA']) < 11:
        #            zero_add = 11 - len(vals_input['Partita IVA'])
        #            for zero in range(0, zero_add):
        #                vals_input['Partita IVA'] = '0' + vals_input['Partita IVA']

        if hasattr(record, 'comment') and record.comment:
            vals_partner['comment'] = record.comment

        if self.partner_subaccount:
            record_code = self.to_string(record.code)
            code_partners = self.partner_obj.search([(PROPERTY_REF_MAP[self.partner_type], '=', record_code)])

            if code_partners and not UPDATE_ON_CODE:
                code_partner = code_partners[0]
                if vals_partner.get('vat', False) and not code_partner.vat == vals_partner['vat']:
                    error = u"Riga {0}: Partner '{1} {2}'; codice gia utilizzato per partner {3}. La riga viene ignorata.".format(self.processed_lines, record_code, vals_partner['name'], code_partner.name)
                    _logger.debug(error)
                    self.error.append(error)
                    return False
                elif vals_partner.get('fiscalcode', False) and not code_partner.fiscalcode == vals_partner['fiscalcode']:
                    error = u"Riga {0}: Partner '{1} {2}'; codice gia utilizzato per partner {3}. La riga viene ignorata.".format(self.processed_lines, record_code, vals_partner['name'], code_partner.name)
                    _logger.debug(error)
                    self.error.append(error)
                    return False
            elif code_partners and UPDATE_ON_CODE:
                vals_partner[PROPERTY_REF_MAP[self.partner_type]] = record_code
                if PROPERTY_REF_MAP[self.partner_type] not in self.PARTNER_SEARCH:
                    self.PARTNER_SEARCH.insert(0, PROPERTY_REF_MAP[self.partner_type])
            else:
                vals_partner[PROPERTY_REF_MAP[self.partner_type]] = record_code

        if hasattr(record, 'category') and record.category:
            categories = self.category_obj.search([('name', 'ilike', record.category)])

            if len(categories) == 1:
                vals_partner['category_id'] = [(6, 0, categories.ids)]
            else:
                new_category = self.category_obj.create({
                    'name': record.category,
                    'active': True
                })
                vals_partner['category_id'] = [(6, 0, [new_category.id])]

        # Compile address info
        if hasattr(record, 'type'):
            vals_partner['type'] = record.type or 'default'

            if self.parent_id:
                if vals_partner['type'] == 'default':
                    self.parent_id = False
                elif vals_partner['type'] == 'delivery':
                    vals_partner['delivery_address'] = True
                    vals_partner['parent_id'] = self.parent_id
                else:
                    vals_partner['parent_id'] = self.parent_id

            vals_partner['street'] = getattr(record, 'street')
            vals_partner['zip'] = getattr(record, 'zip')
            vals_partner['city'] = getattr(record, 'city')
            if vals_partner['city'] and vals_partner['country_id']:
                vals_partner['state_id'] = self.get_state(
                    vals_partner['city'],
                    hasattr(record, 'state') and record.state or False,
                    country_code,
                    vals_partner['country_id']
                )

            vals_partner['website'] = getattr(record, 'website')
            vals_partner['phone'] = getattr(record, 'phone')
            vals_partner['fax'] = getattr(record, 'fax')
            vals_partner['email'] = getattr(record, 'email')
        else:
            address_type = self.ADDRESS_TYPE[0]
            vals_partner['type'] = address_type

            vals_partner['street'] = getattr(record, 'street_{address_type}'.format(address_type=address_type))
            vals_partner['zip'] = getattr(record, 'zip_{address_type}'.format(address_type=address_type))
            vals_partner['city'] = getattr(record, 'city_{address_type}'.format(address_type=address_type))
            if vals_partner['city'] and vals_partner['country_id']:
                vals_partner['state_id'] = self.get_state(
                    vals_partner['city'],
                    getattr(record, 'state_{address_type}'.format(address_type=address_type)),
                    country_code,
                    vals_partner['country_id']
                )

            vals_partner['website'] = record.website
            vals_partner['phone'] = getattr(record, 'phone_{address_type}'.format(address_type=address_type))
            vals_partner['fax'] = getattr(record, 'fax_{address_type}'.format(address_type=address_type))
            vals_partner['email'] = getattr(record, 'email_{address_type}'.format(address_type=address_type))

        partner = self._find_partner(vals_partner)
        if partner:
            if isinstance(partner, int) and int(partner) == -1:
                return False
            else:
                partner.write(vals_partner)
                self.updated += 1
        else:
            partner = self.partner_obj.with_context(import_ctx=True).create(vals_partner)
            self.new += 1

        if hasattr(record, 'iban') and record.iban:
            self.get_or_create_bank(record.iban, partner)

        if hasattr(record, 'type'):
            if vals_partner['type'] == 'default':
                self.parent_id = partner.id
        else:
            address_type = self.ADDRESS_TYPE[1]
            has_email = hasattr(record, 'email_{address_type}'.format(address_type=address_type))
            has_phone = hasattr(record, 'phone_{address_type}'.format(address_type=address_type))
            if has_email and not vals_partner['email'] == getattr(record, 'email_{address_type}'.format(address_type=address_type)):
                address = self.env['res.partner'].search([('parent_id', '=', partner.id), ('type', '=', address_type)])
                if address:
                    address.email = getattr(record, 'email_{address_type}'.format(address_type=address_type))
                    if has_phone:
                        address.phone = getattr(record, 'phone_{address_type}'.format(address_type=address_type))
                else:
                    self.env['res.partner'].create({
                        'name': u'{} - {}'.format(partner.name, address_type),
                        'parent_id': partner.id,
                        'type': address_type,
                        'use_parent_address': True,
                        'email': getattr(record, 'email_{address_type}'.format(address_type=address_type)),
                        'phone': has_phone and getattr(record, 'phone_{address_type}'.format(address_type=address_type)) or False
                    })
        return partner
