# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014-2015 Didotech Srl (<http://www.didotech.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################.

from odoo import models, fields, api, _

COLOR_SELECTION = [
    ('aqua', _(u"Aqua")),
    ('black', _(u"Black")),
    ('blue', _(u"Blue")),
    ('brown', _(u"Brown")),
    ('cadetblue', _(u"Cadet Blue")),
    ('darkblue', _(u"Dark Blue")),
    ('fuchsia', _(u"Fuchsia")),
    ('forestgreen', _(u"Forest Green")),
    ('green', _(u"Green")),
    ('grey', _(u"Grey")),
    ('red', _(u"Red")),
    ('orange', _(u"Orange"))
]


class RowColor(models.AbstractModel):
    '''
        <tree colors="aqua:row_color=='aqua';black:row_color=='black';blue:row_color=='blue';brown:row_color=='brown';cadetblue:row_color=='cadetblue';darkblue:row_color=='darkblue';fuchsia:row_color=='fuchsia';forestgreen:row_color=='forestgreen';orange:row_color=='orange';green:row_color=='green';grey:row_color=='grey';red:row_color=='red';">
            <field name="color" />
            <field name="row_color" invisible="1" />
    '''
    
    _name = 'row.color'
    _description = 'Row colors'

    color = fields.Selection(COLOR_SELECTION, _('Color'), select=True, default='black')
    row_color = fields.Char(_('Row color'), compute='_get_color', readonly=True)
    
    @api.one
    @api.depends('color')
    def _get_color(self):
        self.row_color = self.color
