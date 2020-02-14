# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2014-2016 Didotech SRL (info at didotech.com)
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

from odoo import models, fields, api, _
# from data_migration.utils import partner_importer
from odoo.addons.data_migration.utils import product_importer
from odoo.addons.data_migration.utils import category_importer
from odoo.addons.data_migration.utils import partner_importer
import base64
from odoo import exceptions


class FiledataImport(models.Model):
    _name = "filedata.import"

    # State of this wizard
    state = fields.Selection((
        ('import', 'import'),
        ('preview', 'preview'),
        ('end', 'end')
    ), 'state', required=True, translate=False, readonly=True, default='import')

    # Data of file, in code BASE64
    content_base64 = fields.Binary('Data File path', required=False, translate=False)
    file_name = fields.Char('File Name', size=256)
    # Data of file, in code text
    content_text = fields.Binary('File Partner', required=False, translate=False)
    preview_text_original = fields.Binary('Preview text original', required=False, translate=False, readonly=True)
    # problem's row of product. decoded
    preview_text_decoded = fields.Text('Preview text decoded', required=False, translate=False, readonly=True)
    progress_indicator = fields.Integer('Progress import ', size=3, translate=False, readonly=True, default=0)

    
    # # # # # # # # # # # # # #
    # action of button click  #
    # # # # # # # # # # # # # #
    @api.one
    def action_check_encoding(self):
        # Extraction file content, encoded in base64
        content_base64 = self.content_base64

        # Check if user supplied the data, if data was not supplied show a message
        if not content_base64:
            # Send a message to the user telling that there is a missing field
            raise exceptions.Warning('Attenzione!\n Non è stato selezionato il file da importare')
            
        # Decoding content of file and store the resulting text in object
        decoded_text = base64.decodestring(content_base64)

        self.write({
            'content_text': decoded_text,
            'file_name': self.file_name,
        })

        self.action_start_import()
        return {'type': 'ir.actions.act_window_close'}

    @api.one
    def action_start_import(self):
        # Set 'end' as a next state
        # self.write({'state': 'end'})
        self.state = 'end'

        # from OE 6.1 memory object not move data in other thread - move data in parameters
        self._cr.commit()
        # Start import
        data_importer = self.importer.ImportFile(self.env, self.id)
        # data_importer.start()
        data_importer.run()

        return False


class CategoryImport(FiledataImport):
    _name = "category.import"
    _description = "Import products from file in .csv format."

    importer = category_importer
    _rec_name = 'file_name'

    def _get_root_category(self):
        root_categories = self.env['product.category'].search([('parent_id', '=', False)])
        return [(str(category.id), category.name) for category in root_categories]

    header = fields.Boolean('Header', help="Start from second row")
    root_category = fields.Selection(selection='_get_root_category', string='Root Category', required=True)


class ProductImport(FiledataImport):
    _name = "product.import"
    _description = "Import products from file in .csv format."

    importer = product_importer

    @api.model
    def _get_language(self):
        languages = self.env['res.lang'].search([])
        return [(language.code, language.name) for language in languages]

    file_format = fields.Selection((
        ('FormatOne', _('Format One')),
        # ('FormatTwo', _('Format Two')),
        ('FormatThree', _('Format Three')),
        ('FormatFour', _('Format Four')),
        ('FormatEcommerce', 'eCommerce'),
        ('ProductVariants', 'Products & Variants')
    ), 'Formato Dati', required=True, readonly=False)
    language = fields.Selection(_get_language, required=True)
    update_product_name = fields.Boolean('Update Product Name', help="If set, overwrite product name")
    update_public_category = fields.Boolean('Update Public Category', help="If set, overwrite category sequence")


class PartnerImport(FiledataImport):
    _name = "partner.import"
    _description = "Import partner from a file in .csv, .ods or .xls format."

    importer = partner_importer

    file_format = fields.Selection((
        ('FormatEcommerce', 'eCommerce'),
        ('ExtendedPartner', 'Unlimited Addresses')
    ), 'Formato Dati', required=True, readonly=False)
    partner_type = fields.Selection((
        ('customer', 'Customer'),
        ('supplier', 'Supplier')
    ), 'Partner Type', required=True)
    strict = fields.Boolean(_('Strict'), help="Use more strict (and more slow) data check", default=False)
