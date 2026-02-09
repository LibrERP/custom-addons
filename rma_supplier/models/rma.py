# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models


class Rma(models.Model):
    _inherit = "rma"

    inventory_state = fields.Many2one(comodel_name="rma.inventory.state", string="Stato Magazzino", required=False, )
    supplier_id = fields.Many2one(comodel_name="res.partner", string="Fornitore", required=False)
    supplier_goods_arrival_date = fields.Date(string="Data Arrivo Merce", required=False)
    supplier_return_document = fields.Char(string="Documento di Reso", required=False)
    supplier_credit_note = fields.Char(string="Nota Accredito Fornitore", required=False)
    supplier_transportation_document = fields.Char(string="DDT Fornitore", required=False)


class RmaInventoryState(models.Model):
    _name = 'rma.inventory.state'
    _description = 'RMA Stage'
    _order = 'name, id'

    name = fields.Char(string="Name", required=False)
