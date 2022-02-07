# -*- encoding: utf-8 -*-
############################################################################
#
#    Copyright (C) 2020-2020 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2020-10-23
#    Author : Fabio Colognesi
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
############################################################################


def get_view_id(obj, view_name=""):
    """
        Gets a view id from model data.
    """
    ret = False
    if view_name:
        model_data_model = obj.env['ir.model.data']
        criteria = [('model', '=', 'ir.ui.view'), ('name', '=', view_name)]
        model_data_ids = model_data_model.search(criteria)
        if model_data_ids:
            ret = model_data_ids.res_id
    return ret
