# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Andrei Levin (andrei.levin at didotech.com)
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

from odoo import models, fields, api, _
from odoo.addons.data_migration import settings
from .utils import BaseImport
import logging
_logger = logging.getLogger(__name__)
DEBUG = settings.DEBUG

if DEBUG:
    import pdb
    _logger.setLevel(logging.DEBUG)
else:
    _logger.setLevel(logging.INFO)


class ImportFile(BaseImport):
    def __init__(self, env, import_record_id):
        # Inizializzazione superclasse
        BaseImport.__init__(self, env, import_record_id, import_model='category.import')
# class ImportFile(ThreadingImport):
#     def __init__(self, env, import_record_id):
#         # Inizializzazione superclasse
#         ThreadingImport.__init__(self, env, import_record_id, import_model='category.import')

        self.message_title = _("Importazione categorie")
        self.category_obj = self.env['product.category']
        self.root_category_id = int(self.import_record.root_category)
        self.header = self.import_record.header
        self.cache = {}

    def get_category(self, categories_list, parent=False):
        if categories_list:
            if DEBUG:
                print(categories_list)

            name = categories_list.pop(0)

            _logger.debug(u'# {lines} {parent}/{name} {categories}'.format(lines=self.processed_lines, parent=parent and parent.name or '', name=name, categories=categories_list))
            key = u'{parent}-{category}'.format(parent=parent and parent.name or '', category=name)
            if self.cache.get(key):
                _logger.debug(u"# Category '{category}' taken from cache".format(category=name))
                categories = [self.cache[key]]
                add_cache = False
            else:
                parent_id = parent and parent.id or False
                categories = self.category_obj.search([('name', '=ilike', name.strip()), ('parent_id', '=', parent_id)])
                add_cache = True

            if len(categories) == 1:
                if add_cache:
                    self.cache[key] = categories[0]
                if categories_list:
                    return self.get_category(categories_list, parent=categories[0])
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
                category_values = {
                    'name': name,
                    'parent_id': parent and parent.id or False
                }
                if hasattr(parent, 'spareparts'):
                    category_values['spareparts'] = parent.spareparts

                category = self.category_obj.create(category_values)
                _logger.debug('Created {category.id}'.format(category=category))
                self.new += 1
                if categories_list:
                    return self.get_category(categories_list, category)
                else:
                    return category
        return False

    def import_row(self, row_list):
        _logger.debug(row_list)

        if self.processed_lines == 1 and self.header:
            _logger.info(u'# Ignoring header')
            return True
        else:
            root_category = self.category_obj.browse(self.root_category_id)
            return self.get_category(row_list, parent=root_category)
