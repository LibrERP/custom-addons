#    Created on : 2020-10-23    Author : Fabio Colognesi
#
# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


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
