# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2013-2016 Andrei Levin (andrei.levin at didotech.com)
#
#                          All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import _
from odoo.addons.barcodes.models.barcodes import BarcodeNomenclature
from odoo.addons.data_migration import settings
from .utils import BaseImport
from collections import namedtuple
from odoo import exceptions
from pprint import pprint
import logging
_logger = logging.getLogger(__name__)
DEBUG = settings.DEBUG

if DEBUG:
    import pdb
    _logger.setLevel(logging.DEBUG)
else:
    _logger.setLevel(logging.INFO)


class ProductVersion(object):
    def __init__(self, env, product_defaults):
        # self.attributes = env['product.attribute']
        self.attribute_values = env['product.attribute.value']
        self.product_obj = env['product.product']
        self.supplierinfo_obj = env['product.supplierinfo']
        self.values = {}
        self.PRODUCT_DEFAULTS = product_defaults
        # variant_code - attributes
        self.variants = []
        self.processed_lines = 0

    def add_attribute_value(self, attribute_values):
        for a_value in attribute_values:
            if a_value.id not in self.attribute_values.ids:
                self.attribute_values += a_value

    def set_attribute_line_ids(self, old_attribute_line_ids=False):
        """
        {'attribute_line_ids': [[1, 5, {'value_ids': [[6, False, [17, 18, 19]]]}]]}

        {'attribute_line_ids': [[1, 5, {'value_ids': [[6, False, [17, 18, 19, 22]]]}],
                        [0,
                         False,
                         {'attribute_id': 3,
                          'value_ids': [[6, False, [20, 21]]]}]]}

        attribute_id - product attribute
        value_ids - product_attribute_value

        """

        attribute_value_ids = {}

        for attribute_value in self.attribute_values:
            if not attribute_value_ids.get(attribute_value.attribute_id.id):
                attribute_value_ids[attribute_value.attribute_id.id] = []

            attribute_value_ids[attribute_value.attribute_id.id].append(attribute_value.id)

        attribute_line_ids = []

        if old_attribute_line_ids:
            attribute_ids = {line.attribute_id.id: line.id for line in old_attribute_line_ids}
        else:
            attribute_ids = {}

        for attribute_id, value_ids in attribute_value_ids.items():
            if attribute_id in attribute_ids:
                attribute_line_ids.append([
                    1, attribute_ids[attribute_id], {
                        'value_ids': [[6, False, value_ids]]
                    }
                ])
            else:
                attribute_line_ids.append([
                    0, False, {
                        'attribute_id': attribute_id,
                        'value_ids': [[6, False, value_ids]]
                    }
                ])

        self.values['attribute_line_ids'] = attribute_line_ids
        return True

    def get_variant_names(self):
        return [v['name'] for v in self.variants]

    def clean_versions(self, variants):
        """
        'seller_ids': [[4, 33, False],
                [4, 25, False],
                [4, 82, False],
                [1, 83, {'min_qty': 1}],
                [0,
                 False,
                 {'company_id': 1,
                  'delay': 1,
                  'min_qty': 0,
                  'name': 109,
                  'pricelist_ids': [],
                  'product_code': 'FF_MRL1',
                  'product_name': False,
                  'sequence': 1}]]}
        """
        active_variants = {v['attribute_values']: v for v in self.variants}
        for variant in variants:
            if variant.attribute_value_ids in active_variants:
                seller_ids = []

                if active_variants[variant.attribute_value_ids].get('supplier_info'):
                    seller_id = self.supplierinfo_obj.search([
                        ('name', '=', active_variants[variant.attribute_value_ids]['supplier_info']['name']),
                        ('product_id', '=', variant.id),
                    ])
                    if seller_id:
                        seller_ids.append([1, seller_id[0].id, {
                            'min_qty': active_variants[variant.attribute_value_ids]['supplier_info']['min_qty'],
                            'product_code': active_variants[variant.attribute_value_ids]['supplier_info']['product_code']
                        }])
                    else:
                        seller_ids.append([0, False, active_variants[variant.attribute_value_ids]['supplier_info']])
                else:
                    seller_id = False

                for seller_info in variant.seller_ids:
                    if not seller_id or not seller_id[0].id == seller_info.id:
                        seller_ids.append([4, seller_info.id, False])

                variant_values = {
                    'active': True,
                    'default_code': active_variants[variant.attribute_value_ids]['name'],
                    'seller_ids': seller_ids,
                    'description': active_variants[variant.attribute_value_ids]['description']
                }

                if active_variants[variant.attribute_value_ids].get('product_uib'):
                    variant_values['product_uib'] = float(active_variants[variant.attribute_value_ids]['product_uib'])

                variant.write(variant_values)
            else:
                variant.active = False


class ImportFile(BaseImport):
    def __init__(self, env, import_record_id):
        BaseImport.__init__(self, env, import_record_id, import_model='product.import')

        self.message_title = _("Importazione prodotti")
        self.product_obj = self.env['product.template']
        self.supplierinfo_obj = self.env['product.supplierinfo']
        self.partner_obj = self.env['res.partner']
        self.category_obj = self.env['product.category']

        try:
            self.public_category_obj = self.env['product.public.category']
        except:
            self.public_category_obj = False

        try:
            self.pos_category_obj = self.env['pos.category']
        except:
            self.pos_category_obj = False

        self.uom_obj = self.env['uom.uom']
        self.tax_obj = self.env['account.tax']

        # self.brand_obj = self.env['product.brand']
        self.cache = {}
        
        self.update_product_name = self.import_record.update_product_name
        self.language = self.import_record.language
        self.update_public_category = self.import_record.update_public_category

        config = getattr(settings, self.import_record.file_format)
        self.default_code = ''

        self.HEADER = config.HEADER_PRODUCT
        self.REQUIRED = config.REQUIRED_PRODUCT
        self.PRODUCT_SEARCH = config.PRODUCT_SEARCH
        self.PRODUCT_WARNINGS = config.PRODUCT_WARNINGS
        self.PRODUCT_ERRORS = config.PRODUCT_ERRORS
        # Default values
        self.PRODUCT_DEFAULTS = config.PRODUCT_DEFAULTS
        if not len(self.HEADER) == len(config.COLUMNS_PRODUCT.split(',')):
            pprint(zip(self.HEADER, config.COLUMNS_PRODUCT.split(',')))
            raise exceptions.Warning('Error: wrong configuration!\nThe length of columns and headers must be the same')

        self.RecordProduct = namedtuple('RecordProduct', config.COLUMNS_PRODUCT)

        self.product = False

        self.category_order = self.env['ir.module.module'].search([
            ('name', '=', 'product_public_category_order'), ('state', '=', 'installed')]) and True or False
        if self.category_order:
            self.category_order_obj = env['product.attribute.sequence']

        self.variant_description = self.env['ir.module.module'].search([
            ('name', '=', 'product_description_variant'), ('state', '=', 'installed')]) and True or False

    def get_category(self, categories_list, parent=False, public=False, pos=False):
        if categories_list:
            if DEBUG:
                print(categories_list)

            name = categories_list.pop(0)

            if public:
                _logger.debug(u'# £Public£ {lines} {parent}/{name} {categories}'.format(lines=self.processed_lines, parent=parent and parent.id or '', name=name, categories=categories_list))
                key = u'$PUBLIC-{parent}-{category}'.format(parent=parent and parent.id or '', category=name)
            elif pos:
                _logger.debug(u'# £Pos£ {lines} {parent}/{name} {categories}'.format(lines=self.processed_lines,
                                                                                        parent=parent and parent.id or '',
                                                                                        name=name,
                                                                                        categories=categories_list))
                key = u'$POS-{parent}-{category}'.format(parent=parent and parent.id or '', category=name)
            else:
                _logger.debug(u'# {lines} {parent}/{name} {categories}'.format(lines=self.processed_lines, parent=parent and parent.id or '', name=name, categories=categories_list))
                key = u'{parent}-{category}'.format(parent=parent and parent.id or '', category=name)

            if self.cache.get(key):
                _logger.debug(u"# Category '{category}' taken from cache".format(category=name))
                categories = [self.cache[key]]
                add_cache = False
            else:
                parent_id = parent and parent.id or False
                if public:
                    categories = self.public_category_obj.with_context(strict=True).search([('name', '=ilike', name.strip()), ('parent_id', '=', parent_id)])
                elif pos:
                    categories = self.pos_category_obj.with_context(strict=True).search([('name', '=ilike', name.strip()), ('parent_id', '=', parent_id)])
                else:
                    categories = self.category_obj.search([('name', '=ilike', name.strip()), ('parent_id', '=', parent_id)])
                add_cache = True

            if len(categories) == 1:
                if add_cache:
                    self.cache[key] = categories[0]
                if categories_list:
                    return self.get_category(categories_list, parent=categories[0], public=public, pos=pos)
                else:
                    return categories[0]
            elif len(categories) > 1:
                error = u"Row {0}: Abnormal situation. More than one category '{1}' found".format(self.processed_lines, name)
                _logger.error(error)
                self.error.append(error)
                return False
            else:
                info = u"# Row {0}: Creating category '{1}'...".format(self.processed_lines, name)
                _logger.debug(info)
                # self.error.append(error)
                parent_id = parent and parent.id or False
                if public:
                    category = self.public_category_obj.create({'name': name, 'parent_id': parent_id})
                elif pos:
                    category = self.pos_category_obj.create({'name': name, 'parent_id': parent_id})
                else:
                    category = self.category_obj.create({'name': name, 'parent_id': parent_id})
                self.new += 1
                if categories_list:
                    return self.get_category(categories_list, parent=category, public=public, pos=pos)
                else:
                    return category
        return False

    def get_create_name(self, model, name, search_parameters=False):
        name = name.strip()
        domain = [('name', '=ilike', name)]

        if search_parameters:
            for key, value in search_parameters.items():
                domain.append((key, '=', value))

        results = self.env[model].search(domain)
        if len(results) == 1:
            result = results[0]
        elif len(results) > 1:
            raise exceptions.Warning(_(u"Search for '{}' produced ambiguous results").format(name))
        else:
            values = {'name': name}
            if search_parameters:
                values.update(search_parameters)
            result = self.env[model].create(values)
        return result

    def get_attributes(self, attribute_list):
        attribute_values = self.env['product.attribute.value']
        for attribute_name_value in attribute_list:
            if ':' in attribute_name_value:
                if DEBUG:
                    print(attribute_name_value)

                name, value = attribute_name_value.split(':', 1)
                if ':' in value:
                    raise exceptions.Warning(_(u"Attribute '{}' can't be splitted in unambiguous way").format(attribute_name_value))
                attribute = self.get_create_name('product.attribute', name)
                attribute_values += self.get_create_name('product.attribute.value', value, {'attribute_id': attribute.id})
        return attribute_values

    def get_uom(self, name):
        translate = {
            'm': 'm',
            'kgm': 'kg',
            'unit': 'Unit(s)',
            'litre': 'Liter(s)',
            'LT': 'Litre',
            'lt': 'Litre',
            '20 lt': 'Litre',
            'PCE': 'Unit(s)',
            'Pz.': 'Unit(s)',
            'Pa.': 'Unit(s)',  # Paia
            'Paia': 'Unit(s)',  # Paia
            'PZ': 'Unit(s)',
            'Pz': 'Unit(s)',
            'CF': 'Unit(s)',
            'N.': 'Unit(s)',
            'Mt.': 'Unit(s)',
            'pz': 'Unit(s)',
            'copp': 'Unit(s)',
            'conf': 'Unit(s)',
            'Kit': 'Unit(s)',
            'Pacco': 'Unit(s)',
            'scat': 'Unit(s)',
            'pac': 'Unit(s)',
            'HH': 'Hour',
            'M': 'm',
            'ML.': 'm',
            'mc': 'm',
            'M2': 'mq',
            'mq': 'mq',
            'Kg': 'kg',
            'kg': 'kg',
            'mm': 'mm'
        }
        
        if name and len(name) > 20 and name[:20] == 'product.product_uom_':
            uom_name = name[20:]
        elif name:
            uom_name = name
        else:
            error = u"Row {0}: Can't find valid UOM".format(self.processed_lines)
            _logger.error(error)
            self.error.append(error)
            return False

        uoms = self.uom_obj.with_context(lang='en_EN').search([('name', '=ilike', translate[uom_name])])
        if len(uoms) == 1:
            return uoms[0]
        elif len(uoms) > 1:
            error = u"Row {0}: Abnormal situation. More than one UOM '{1}' found".format(self.processed_lines, uom_name)
            _logger.error(error)
            self.error.append(error)
            return False
        else:
            error = u"Row {0}: UOM '{1}' is missing in database".format(self.processed_lines, uom_name)
            _logger.error(error)
            self.error.append(error)
            return False
        
    def get_taxes(self, description):
        taxes = self.tax_obj.search([('description', '=', description)])
        
        if len(taxes) == 1:
            return taxes
        elif len(taxes) > 1:
            error = u"Row {0}: Abnormal situation. More than one tax '{1}' found".format(self.processed_lines, description)
            _logger.error(error)
            self.error.append(error)
            return False
        else:
            error = u"Row {0}: Tax '{1}' is missing in database".format(self.processed_lines, description)
            _logger.error(error)
            self.error.append(error)
            return False
        
    def get_suppliers(self, names):
        names = names.split(',')
        suppliers = []
        
        for name in names:
            name = name.strip()
            partners = self.partner_obj.search([('name', '=ilike', name), ('supplier', '=', True)])
            
            if len(partners) == 1:
                suppliers += partners
            elif len(suppliers) > 1:
                warning = u"Row {0}: Abnormal situation. More than one supplier '{1}' found".format(self.processed_lines, name)
                _logger.warning(warning)
                self.warning.append(warning)
                return False
            else:
                warning = u"Row {0}: Supplier '{1}' is missing in database".format(self.processed_lines, name)
                _logger.warning(warning)
                self.warning.append(warning)
                return False
        
        return suppliers
    
    def get_brand(self, name):
        brand_obj = self.env['product.brand']
        brands = brand_obj.search([('name', '=ilike', name)])
        
        if len(brands) == 1:
            return brands[0]
        elif len(brands) > 1:
            warning = u"Row {0}: Abnormal situation. More than one brand '{1}' found".format(self.processed_lines, name)
            _logger.warning(warning)
            self.warning.append(warning)
            return False
        else:
            warning = u"Row {0}: No brand '{1}' found".format(self.processed_lines, name)
            _logger.warning(warning)
            self.warning.append(warning)
            return False
            # return brand_obj.create({'name': name})

    def get_public_categories(self, raw_public_categories):
        raw_public_categories = raw_public_categories.split(';')
        public_category = []

        for count, category_line in enumerate(raw_public_categories, start=1):
            if category_line:
                categories = self.split_categories(category_line)
                category = self.get_category(categories, parent=False, public=True)
                # if self.update_public_category:
                #     category.sequence = count
                public_category.append(category.id)
        return public_category

    @staticmethod
    def split_categories(categories):
        if '\\' in categories:
            categories = categories.split('\\')
        elif '/' in categories:
            categories = categories.split('/')
        elif ',' in categories:
            categories = categories.split(',')
        else:
            categories = [categories]
        # Delete empty categories and strip
        categories = [category.strip() for category in categories if category]
        return categories

    def update_product(self, product, vals_product, field):
        _logger.info(u'Row {row}: Updating product {product}...'.format(row=self.processed_lines, product=vals_product[field]))

        if self.update_product_name:
            vals_product['name'] = product.name

        product.with_context(lang=self.language).write(vals_product)
        self.updated += 1
        return product

    def create_product(self, vals_product, field):
        _logger.info(u'Row {row}: Adding product {product}...'.format(row=self.processed_lines, product=vals_product[field]))
        # print(vals)
        # Create new product
        default_vals_product = self.PRODUCT_DEFAULTS.copy()
        if not vals_product.get('uom_id') and default_vals_product.get('uom'):
            vals_product['uom_id'] = self.get_uom(default_vals_product['uom']).id
            vals_product['uom_po_id'] = vals_product['uom_id']
            del default_vals_product['uom']
        elif not vals_product.get('uom_id'):
            vals_product['uom_id'] = self.get_uom('Unit(s)').id
            vals_product['uom_po_id'] = vals_product['uom_id']
        default_vals_product.update(vals_product)

        product = self.product_obj.with_context(lang=self.language).create(default_vals_product)

        self.new += 1
        return product

    def import_row(self, row_list):
        if self.first_row:
            row_str_list = [self.to_string(value) for value in row_list]
            for column in row_str_list:
                # print column
                if column in self.HEADER:
                    _logger.info(u'Riga {0}: Trovato Header'.format(self.processed_lines))
                    return True
            self.first_row = False

        if not len(row_list) == len(self.HEADER):
            row_str_list = [self.to_string(value) for value in row_list]
            if DEBUG:
                if len(row_list) > len(self.HEADER):
                    pprint(zip(self.HEADER, row_str_list[:len(self.HEADER)]))
                else:
                    pprint(zip(self.HEADER[:len(row_list)], row_str_list))

            error = u"""Row {row}: Row_list is {row_len} long. We expect it to be {expected} long, with this columns:
                {keys}
                Instead of this we got this:
                {header}
                """.format(
                    row=self.processed_lines,
                    row_len=len(row_list),
                    expected=len(self.HEADER),
                    keys=self.HEADER,
                    header=', '.join([str(v, 'utf-8') for v in zip(self.HEADER, row_list)]))

            _logger.error(str(row_list, 'utf-8'))
            _logger.error(error)
            self.error.append(error)
            if DEBUG:
                pprint(zip(self.HEADER, row_str_list))
            return False
        elif DEBUG:
            # pprint(row_list)
            row_str_list = [self.to_string(value) for value in row_list]
            pprint(zip(self.HEADER, row_str_list))
        
        # Sometime value is only numeric and we don't want string to be treated as Float
        record = self.RecordProduct._make([self.to_string(value) for value in row_list])

        for field in self.REQUIRED:
            if not getattr(record, field):
                error = u"Riga {0}: Manca il valore della {1}. La riga viene ignorata.".format(self.processed_lines, field)
                _logger.debug(error)
                self.error.append(error)
                return False
        
        vals_product = {'name': record.name}
        
        for field in self.PRODUCT_SEARCH:
            if (hasattr(record, field) and getattr(record, field)) or (hasattr(self, field) and getattr(self, field)):
                vals_product[field] = getattr(record, field) or getattr(self, field)
                break
        else:
            error = u"Row {0}: Can't find valid product key".format(self.processed_lines)
            _logger.error(error)
            self.error.append(error)
            return False

        if hasattr(record, 'version_code') and record.default_code:
            # Create product
            if not self.default_code == record.default_code:
                if self.product:
                    self.create_variants()

                self.default_code = record.default_code
                self.product = False
        
        if hasattr(record, 'category') and record.category:
            categories = self.split_categories(record.category)
            category = self.get_category(categories, parent=False)
            if category:
                vals_product['categ_id'] = category.id
            else:
                return False
            if 'pos_categ_id' in self.product_obj._fields:
                categories = self.split_categories(record.category)
                category = self.get_category(categories, parent=False, pos=True)
                if category:
                    vals_product['pos_categ_id'] = category.id

        public_categ_ids = []

        if hasattr(record, 'menu') and record.menu:
            menu_categories = self.split_categories(record.menu)
            root_menu_category = self.public_category_obj.get_menu()
            menu_category = self.get_category(menu_categories, parent=root_menu_category, public=True)
            if menu_category:
                menu_category_id = menu_category.id
                public_categ_ids.append(menu_category_id)
            else:
                return False

        if hasattr(record, 'product_public_category') and record.product_public_category:
            public_categ_ids += self.get_public_categories(record.product_public_category)

        if public_categ_ids:
            vals_product['public_categ_ids'] = [(6, 0, public_categ_ids)]

        if hasattr(record, 'brand') and record.brand:
            brand = self.get_brand(record.brand)
            vals_product['product_brand_id'] = brand and brand.id or False
        else:
            if 'brand' in self.PRODUCT_WARNINGS:
                warning = u"Row {0}: No brand for product {1}".format(self.processed_lines, vals_product['name'])
                _logger.warning(warning)
                self.warning.append(warning)
        
        if hasattr(record, 'description') and record.description and not self.variant_description:
            vals_product['description'] = record.description
            vals_product['description_sale'] = ''
        
        if hasattr(record, 'uom') and record.uom:
            uom_id = self.get_uom(record.uom)
            if uom_id:
                vals_product['uom_id'] = uom_id.id
                vals_product['uom_po_id'] = vals_product['uom_id']

        if hasattr(record, 'tax_out') and record.tax_out:
            taxes = self.get_taxes(record.tax_out)
            if taxes:
                vals_product['taxes_id'] = [(6, 0, [tax.id for tax in taxes])]
            else:
                error = u"Row {0}: Can't find tax for specified Codice Iva".format(self.processed_lines)
                _logger.error(error)
                self.error.append(error)
        
        if hasattr(record, 'tax_in') and record.tax_in:
            supplier_taxes = self.get_taxes(record.tax_in)
            if supplier_taxes:
                vals_product['supplier_taxes_id'] = [(6, 0, [tax.id for tax in supplier_taxes])]
            else:
                error = u"Row {0}: Can't find tax for specified Codice Iva {1}".format(self.processed_lines, record.tax_in)
                _logger.error(error)
                self.error.append(error)

        if hasattr(record, 'list_price') and record.list_price:
            vals_product['list_price'] = record.list_price
            # if record.list_price.replace('.', '', 1).isdigit():
            #     vals_product['list_price'] = float(record.list_price)
            # else:
            #     error = u"Row {0}: '{1}' is not a valid price value. Product is ignored".format(self.processed_lines, record.list_price)
            #     _logger.error(error)
            #     self.error.append(error)
            #     return False
        else:
            if 'list_price' in self.PRODUCT_WARNINGS:
                warning = u"Row {0}: No list price for product {1}".format(self.processed_lines, vals_product['name'])
                _logger.warning(warning)
                self.warning.append(warning)
        
        if hasattr(record, 'supplier') and record.supplier:
            partner_ids = self.get_suppliers(record.supplier)
        else:
            partner_ids = False
        
        if hasattr(record, 'supplier_product_code') and record.supplier_product_code:
            product_code = record.supplier_product_code
        else:
            product_code = False
                    
        if hasattr(record, 'standard_price') and record.standard_price:
            vals_product['standard_price'] = float(record.standard_price)
        else:
            if 'standard_price' in self.PRODUCT_WARNINGS:
                warning = u"Row {0}: No standard price for product {1}".format(self.processed_lines, vals_product['name'])
                _logger.warning(warning)
                self.warning.append(warning)
        
        if hasattr(record, 'available_in_pos') and record.available_in_pos:
            if record.available_in_pos.lower() == 'true':
                vals_product['available_in_pos'] = True
            else:
                vals_product['available_in_pos'] = False
        
        if hasattr(record, 'sale_ok') and record.sale_ok:
            if record.sale_ok.lower() == 'true':
                vals_product['sale_ok'] = True
            else:
                vals_product['sale_ok'] = False
        
        if hasattr(record, 'ean13') and record.ean13:
            if True:
                vals_product['barcode'] = str(record.ean13)
            else:
                if 'ean13' in self.PRODUCT_ERRORS:
                    error = u"Row {0}: '{1}' is not a valid EAN13 code".format(self.processed_lines, vals_product['barcode'])
                    _logger.error(error)
                    self.error.append(error)
                    return False
        
        if hasattr(record, 'type') and record.type:
            if record.type in ('product', 'consu', 'service'):
                vals_product['type'] = record.type
            else:
                error = u"Row {0}: '{1}' is unknown type".format(self.processed_lines, vals_product['type'])
                _logger.error(error)
                self.error.append(error)

        if hasattr(record, 'weight_net') and record.weight_net:
            vals_product['weight_net'] = record.weight_net

        if hasattr(record, 'version_code'):
            if hasattr(record, 'version_attribute'):
                if not self.product:
                    self.product = ProductVersion(self.env, self.PRODUCT_DEFAULTS)
                    self.product.values.update(vals_product)
                attributes = self.split_categories(record.version_attribute)

                if record.supplier and partner_ids:
                    supplier_info = {
                        'name': partner_ids[0].id,
                        'min_qty': record.supplier_min_qty,
                        'product_code': record.supplier_product_code
                    }
                else:
                    supplier_info = False

                attribute_values = self.get_attributes(attributes)
                variant_values = {
                    'name': record.version_code,
                    'attribute_values': attribute_values,
                    'supplier_info': supplier_info,
                    'product_uib': hasattr(record, 'product_uib') and record.product_uib or 0
                }
                if self.variant_description:
                    variant_values['description'] = record.description

                self.product.variants.append(variant_values)
                self.product.add_attribute_value(attribute_values)
            else:
                error = _(u'Row {row}: version without attributes'.format(row=self.processed_lines))
                _logger.error(error)
                self.error.append(error)
        else:
            products = self.product_obj.search([(field, '=ilike', vals_product[field].replace('\\', '\\\\'))])
            if products:
                _logger.info(u'Row {row}: Updating product {product}...'.format(row=self.processed_lines, product=vals_product[field]))
                product = products[0]
                if self.update_product_name:
                    vals_product['name'] = product.name
                product.with_context(lang=self.language).write(vals_product)
                self.updated += 1
            else:
                _logger.info(u'Row {row}: Adding product {product}...'.format(row=self.processed_lines, product=vals_product[field]))
                # print(vals)
                # Create new product
                default_vals_product = self.PRODUCT_DEFAULTS.copy()
                if not vals_product.get('uom_id') and default_vals_product.get('uom'):
                    uom_id = self.get_uom(default_vals_product['uom'])
                    if uom_id:
                        vals_product['uom_id'] = uom_id.id
                        vals_product['uom_po_id'] = vals_product['uom_id']
                        del default_vals_product['uom']
                elif not vals_product.get('uom_id'):
                    uom_id = self.get_uom('Unit(s)')
                    if uom_id:
                        vals_product['uom_id'] = uom_id.id
                        vals_product['uom_po_id'] = vals_product['uom_id']

                default_vals_product.update(vals_product)

                product = self.product_obj.with_context(lang=self.language).create(default_vals_product)

                self.new += 1

            if public_categ_ids and self.category_order:
                for count, category_id in enumerate(public_categ_ids, start=1):
                    category_order = self.category_order_obj.search([
                        ('product_id', '=', product.id),
                        ('public_category_id', '=', category_id)])
                    if category_order:
                        category_order.sequence = count
                    else:
                        self.category_order_obj.create({
                            'product_id': product.id,
                            'public_category_id': category_id,
                            'sequence': count
                        })

            # TODO: verify this code.
            # Seems to be wrong, because it should be product.product and not product.template
            # This part of the code seems to be unported
            # if partner_ids and product:
            #     for partner_id in partner_ids:
            #         suppliers_info = self.supplierinfo_obj.search([('product_id', '=', product.id), ('name', '=', partner_id)])
            #         if suppliers_info:
            #             _logger.info(u'{0}: Updating supplierinfo for product {1}'.format(self.processed_lines, default_vals_product['name']))
            #             suppliers_info[0].write({
            #                 'name': partner_id,
            #                 'product_name': default_vals_product['name'],
            #                 'product_id': product.id,
            #                 'min_qty': 1,
            #                 'product_code': product_code
            #                 # 'company_id':
            #             })
            #         else:
            #             _logger.info(u'{0}: Creating supplierinfo for product {1}...'.format(self.processed_lines, default_vals_product['name']))
            #             self.supplierinfo_obj.create({
            #                 'name': partner_id,
            #                 'product_name': default_vals_product['name'],
            #                 'product_id': product.id,
            #                 'min_qty': 1,
            #                 'product_code': product_code
            #                 # 'company_id':
            #             })
            # else:
            #     _logger.warning(u'{0}: No supplier for product {1}'.format(self.processed_lines, vals_product['name']))

            return product
            
    def get_product_template_id(self, product_id):
        # Retrive the record associated with the product id
        product_object = self.product_obj.browse(product_id)
        
        # Retrive the template id
        product_template_id = product_object.product_tmpl_id.id
        
        # Return the template id
        return product_template_id

    def create_variants(self):
        field = 'default_code'
        products = self.product_obj.search([(field, 'in', self.product.get_variant_names())])
        if products:
            self.product.set_attribute_line_ids(products[0].attribute_line_ids)
            product = self.update_product(products[0], self.product.values, field)
        else:
            self.product.set_attribute_line_ids()
            product = self.create_product(self.product.values, field)

        self.product.clean_versions(product.product_variant_ids)
        del self.product

    def post_import(self):
        if self.product:
            self.create_variants()
