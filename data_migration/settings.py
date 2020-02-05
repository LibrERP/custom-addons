# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2013-2016 Didotech srl (info at didotech.com)
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
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

# DEBUG = True
DEBUG = False


class FormatOne():
    # R.
    HEADER_CUSTOMER = (u'Codice', u'Ragione Sociale', u'Nome', u'Indirizzo', u'CAP', u'Località', u'Provincia', u'Indirizzo AM', u'CAP AM', u'Località AM', u'Provincia AM', u'Nazione', u'Partita IVA', u'Codice Fiscale', u'E-Mail', u'Category')
    #header_supplier = ('Codice', 'Ragione Sociale', 'Nome', 'Indirizzo', 'CAP', 'Località', 'Provincia', 'Indirizzo AM', 'CAP AM', 'Località AM', 'Provincia AM', 'Nazione', 'Partita IVA', 'Codice Fiscale', 'E-Mail')
    #Codice	Denominazione / Cognome	Nome	Sede legale: indirizzo	SL: CAP	SL: località	SL: Prov.	Sede amministrativa: indirizzo	SA: CAP	SA: località	SA: Prov.	Nazione	PI	CF	e-mail
    # Telefono, Cellulare, Fax e PEC
    COLUMNS = "code, name, person_name, street_default, zip_default, city_default, province_default, street_invoice, zip_invoice, city_invoice, province_invoice, country_code, vat, fiscalcode, email, category"
    REQUIRED = ['name', 'code']
    ADDRESS_TYPE = ('default', 'invoice',)
    # Unique fields to be used to look for partner in database
    PARTNER_SEARCH = ('name', 'vat')

    REQUIRED_PRODUCT = ['ean13', 'name']

    HEADER_PRODUCT = ('Codice', 'Descrizione', 'UMC', 'UMT', 'PesoN', 'CostoStd', 'CostoUltimo')
    COLUMNS_PRODUCT = "default_code, name, uom, uom2, weight_net, standard_price, last_standard_price"
    PRODUCT_SEARCH = ['default_code', 'name']
    REQUIRED_PRODUCT = ['default_code', 'name']
    PRODUCT_WARNINGS = ['standard_price']
    PRODUCT_ERRORS = []

    # Default values
    PRODUCT_DEFAULTS = {
        'uom_id': 'Unit(s)',
        'type': 'product',
        # 'supply_method': 'buy',
        # 'procure_method': 'make_to_stock',
        'cost_method': 'standard',
    }


class FormatTwo():
    # IB.
    HEADER_CUSTOMER = (u'Codice', u'Denominazione / Cognome', u'Nome', u'Sede legale: indirizzo', u'SL: CAP', u'SL: località', u'SL: Prov.', u'Telefono', u'Fax', u'e-mail', u'Sede amministrativa: indirizzo 1', u'Sede amministrativa: indirizzo 2', u'SA: CAP', u'SA: località', u'SA: Prov.', u'Nazione', u'PI', u'CF', u'category', u'Note')
    # COLUMNS = "code, name, person_name, street_default, zip_default, city_default, province_default, phone_default, fax_default, email_default, street_invoice, street2_invoice, zip_invoice, city_invoice, province_invoice, country_code, vat, fiscalcode, category, comment"
    COLUMNS = "code, name, person_name, street_invoice, zip_invoice, city_invoice, province_invoice, phone_invoice, fax_invoice, email_invoice, street_delivery, street2_delivery, zip_delivery, city_delivery, province_delivery, country_code, vat, fiscalcode, category, comment"
    REQUIRED = ('name', 'code')
    ADDRESS_TYPE = ('invoice', 'delivery')
    # Unique fields to be used to look for partner in database
    PARTNER_SEARCH = ['name', 'vat']

    # HEADER_PRODUCT = ('Codice', 'Descrizione', 'UMC', 'UMT', 'PesoN', 'CostoStd', 'CostoUltimo')
    # COLUMNS_PRODUCT = "default_code, name, uom0, uom2, weight_net, standard_price, last_standard_price"
    # PRODUCT_SEARCH = ('default_code', 'name')
    # REQUIRED_PRODUCT = ['default_code', 'name']
    # PRODUCT_WARNINGS = ['standard_price']
    # PRODUCT_ERRORS = []


class FormatThree():
    # TP
    HEADER_CUSTOMER = (u'Codice', u'Denominazione / Cognome', u'Nome', u'Sede legale: indirizzo', u'SL: CAP', u'SL: località', u'SL: Prov.', u'Telefono', u'Fax', u'e-mail', u'Sede amministrativa: indirizzo 1', u'Sede amministrativa: indirizzo 2', u'SA: CAP', u'SA: località', u'SA: Prov.', u'Nazione', u'PI', u'CF', u'category')
    COLUMNS = "code, name, person_name, street_default, zip_default, city_default, province_default, phone_default, fax_default, email_default, street_invoice, street2_invoice, zip_invoice, city_invoice, province_invoice, country_code, vat, fiscalcode, category"
    #COLUMNS = "code, name, person_name, street_invoice, zip_invoice, city_invoice, province_invoice, phone_invoice, fax_invoice, email_invoice, street_delivery, street2_delivery, zip_delivery, city_delivery, province_delivery, country_code, vat, fiscalcode, email2, category"
    REQUIRED = ('name', 'code')
    ADDRESS_TYPE = ('default', 'invoice',)
    # Unique fields to be used to look for partner in database
    PARTNER_SEARCH = ['name', 'vat']

    HEADER_PRODUCT = ('codice', 'nome', 'categoria', 'uom', 'codiva_acq', 'codiva_cen', 'list_price', 'ean13', 'fornitore', 'cod__prod__forn_', 'prezzo_forn_', 'active', 'available_in_pos', 'sale_ok', 'assupply_method', 'type', 'procure_method', 'cost_method')
    COLUMNS_PRODUCT = "default_code, name, category, uom, tax_in, tax_out, list_price, ean13, supplier, supplier_product_code, standard_price, active, null, sale_ok, supply_method, type, procure_method, cost_method"
    PRODUCT_SEARCH = ('default_code', 'name')
    REQUIRED_PRODUCT = ['default_code', 'name']
    PRODUCT_WARNINGS = []
    PRODUCT_ERRORS = []

    # Default values
    PRODUCT_DEFAULTS = {
        'supply_method': 'buy',
        'uom': 'PCE',
        'type': 'consu',
        #'type': 'product',
        'procure_method': 'make_to_stock',
        'cost_method': 'standard',
        'sale_ok': True
    }


class FormatFour():
    # TP Extended (differs only for product import)
    HEADER_CUSTOMER = (u'Codice', u'Denominazione / Cognome', u'Nome', u'Sede legale: indirizzo', u'SL: CAP', u'SL: località', u'SL: Prov.', u'Telefono', u'Fax', u'e-mail', u'Sede amministrativa: indirizzo 1', u'Sede amministrativa: indirizzo 2', u'SA: CAP', u'SA: località', u'SA: Prov.', u'Nazione', u'PI', u'CF', u'category')
    COLUMNS = "code, name, person_name, street_default, zip_default, city_default, province_default, phone_default, fax_default, email_default, street_invoice, street2_invoice, zip_invoice, city_invoice, province_invoice, country_code, vat, fiscalcode, category"
    #COLUMNS = "code, name, person_name, street_invoice, zip_invoice, city_invoice, province_invoice, phone_invoice, fax_invoice, email_invoice, street_delivery, street2_delivery, zip_delivery, city_delivery, province_delivery, country_code, vat, fiscalcode, email2, category"
    REQUIRED = ('name', 'code')
    ADDRESS_TYPE = ('default', 'invoice',)
    # Unique fields to be used to look for partner in database
    PARTNER_SEARCH = ['name', 'vat']

    HEADER_PRODUCT = ('codice', 'nome', 'categoria', 'brand', 'descrizione vendita', 'uom_i', 'codiva_acq', 'codiva_cen', 'list_price', 'ean13', 'fornitore', 'cod__prod__forn_', 'prezzo_forn_', 'active', 'available_in_pos', 'sale_ok', 'assupply_method', 'type', 'procure_method', 'cost_method')
    COLUMNS_PRODUCT = "default_code, name, category, brand, description_sale, uom, tax_in, tax_out, list_price, ean13, supplier, supplier_product_code, standard_price, active, null, sale_ok, supply_method, type, procure_method, cost_method"
    PRODUCT_SEARCH = ('default_code', 'name')
    REQUIRED_PRODUCT = ['default_code', 'name']
    PRODUCT_WARNINGS = []
    PRODUCT_ERRORS = []

    # Default values
    PRODUCT_DEFAULTS = {
        'supply_method': 'buy',
        'uom': 'PCE',
        #'type': 'consu',
        'type': 'product',
        'procure_method': 'make_to_stock',
        'cost_method': 'standard',
        'sale_ok': True
    }


class ExtendedPartner():
    """Extended:
        permits import of partners with multiple addresses (one address per line)"""
    HEADER_PARTNER = (u'Denominazione / Cognome', u'Tipo indirizzo (default/invoice/delivery)',
                       u'indirizzo', u'indirizzo 2', u'CAP', u'Località', u'Provincia', u'Nazione',
                       u'Telefono', u'Fax', u'E-mail', u'Website', u'P.IVA', u'CF', u'IBAN', u'Note')

    COLUMNS_PARTNER = "name, type, street, street2, zip, city, province, country_code, phone, fax, email, website, vat, fiscalcode, IBAN, note"
    REQUIRED_PARTNER = ('name',)
    ADDRESS_TYPE = ('default', 'invoice', 'delivery')
    # Unique fields to be used to look for partner in database
    PARTNER_SEARCH = ['name', 'vat']
    DEFAULT_COUNTRY = 'Italia'


class FormatEcommerce():
    HEADER_PARTNER = (u'Codice', u'Ragione Sociale', u'Indirizzo', u'CAP', u'Località', u'Provincia', u'Nazione', u'Codice Fiscale', u'Partita IVA', u'Web', u'IBAN', u'note', u'telefono', u'Fax', u'email', u'Email-invoice')
    # HEADER_PARTNER = (u'Codice', u'Denominazione / Cognome', u'Nome', u'Sede legale: indirizzo', u'SL: CAP', u'SL: località', u'SL: Prov.', u'Telefono', u'Fax', u'e-mail', u'Sede amministrativa: indirizzo 1', u'Sede amministrativa: indirizzo 2', u'SA: CAP', u'SA: località', u'SA: Prov.', u'Nazione', u'PI', u'CF', u'category')
    COLUMNS_PARTNER = "code, name, street_default, zip_default, city_default, state_default, country_code, fiscalcode, vat, website, iban, comment, phone_default, fax_default, email_default, email_invoice"
    REQUIRED_PARTNER = ('name', 'code')
    ADDRESS_TYPE = ('default', 'invoice',)
    PARTNER_SEARCH = ['name', 'vat']
    DEFAULT_COUNTRY = 'Italia'

    HEADER_PRODUCT = ('codice', 'Versioni', 'Name', 'Descrizione vendita', 'Type product/consu/service', 'Categoria Interna', 'Prezzo di listino (senza IVA)', 'Fornitore', 'Prezzo fornitore', 'Menu', 'Categorie (Attributi)', 'Brand')
    COLUMNS_PRODUCT = "default_code, version, name, description, type, category, list_price, supplier, standard_price, menu, product_public_category, brand"
    PRODUCT_SEARCH = ['default_code', 'name']
    REQUIRED_PRODUCT = ['default_code', 'name']
    PRODUCT_WARNINGS = ['public_category', 'brand']
    PRODUCT_ERRORS = []

    # Default values
    PRODUCT_DEFAULTS = {
        'supply_method': 'buy',
        'uom': 'PCE',
        'type': 'product',
        'procure_method': 'make_to_stock',
        'cost_method': 'standard',
        'website_published': True
    }


class ProductVariants():
    REQUIRED_PRODUCT = ['version_code']
    HEADER_PRODUCT = ('codice', 'Versioni', 'Attributi delle versioni', 'Peso scatola', 'Nome', 'Descrizione vendita', 'Type product/consu/service', 'Categoria Interna', 'Prezzo di listino (senza IVA)', 'Fornitore', 'Prezzo fornitore', 'Codice fornitore')
    COLUMNS_PRODUCT = "default_code, version_code, version_attribute, product_uib, name, description, type, category, list_price, supplier, supplier_min_qty, supplier_product_code"
    PRODUCT_SEARCH = ['default_code']

    PRODUCT_WARNINGS = []
    PRODUCT_ERRORS = []

    # Default values
    PRODUCT_DEFAULTS = {
        'supply_method': 'buy',
        'uom': 'PCE',
        # 'uom': 'kg',
        'type': 'product',
        'procure_method': 'make_to_stock',
        'cost_method': 'standard'
    }


# Nothing should be changed after this line
# -------------------------------------------------------------------------------

# All in lowercase
COUNTRY_CODES = {
    'italia': 'IT',
    'italy': 'IT',
    'cva': 'IT',
    '20': 'IT',
    '22': 'CZ',
    'spa': 'ES',
    'uh': 'HU',
    'portogallo': 'PT',
    'uk': 'GB',
    'germany': 'DE',
    'svizzera': 'CH'
}
