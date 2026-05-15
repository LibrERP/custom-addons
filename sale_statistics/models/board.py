#    Created on : 2020-10-23    Author : Fabio Colognesi
#
# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .common import get_view_id
from datetime import datetime

from odoo import api, fields, models, _


class BoardCreate(models.TransientModel):
    _name = "board.temporary"
    _description = "Temporary Class"

    choose_0101 = fields.Boolean('From 01/01', default=True)
    choose_3112 = fields.Boolean('To 31/12', default=False)
    date_start = fields.Datetime('Date Order From')
    date_end = fields.Datetime('Date Order To')
    date_confirm_start = fields.Date('Date Confirm Start')
    date_confirm_end = fields.Date('Date Confirm End')
    date_represent = fields.Selection([
            ('none', 'None'),
            ('quarter', 'Quarter'),
            ('month', 'Monthly'),
            ('week', 'Weekly'),
            ('year', 'Yearly')
        ],
        string='Date Representation', default='none')
    choose_year = fields.Boolean('Whole Year', default=False)
    product_id = fields.Many2one('product.product', 'Product')
    product_tmpl_id = fields.Many2one('product.template', 'Product Template')
    partner_id = fields.Many2one('res.partner', 'Partner')
    user_id = fields.Many2one('res.users', 'Salesperson')
    order_id = fields.Many2one('sale.order', 'Sale Order')

    def sale_report_create(self):
        """
            Opens a new Sale Report View, using parameters as filters.
        """
        ret = False
        add_name = ""
        confirmed = False
        base_name = "Sale Report Activities"
        graph_name = 'view_order_product_graph'
        now = datetime.now()

        self.ensure_one()
        oid_fly = self
        report_search_id = get_view_id(self, 'view_order_product_search')

        if oid_fly and report_search_id:
            date_start = oid_fly.date_start if oid_fly.date_start else now
            date_end = oid_fly.date_end if oid_fly.date_end else now

            if date_start == now and oid_fly.date_confirm_start:
                date_start = datetime.combine(oid_fly.date_confirm_start, datetime.min.time())
                confirmed = True
            if date_end == now and oid_fly.date_confirm_end:
                date_end = datetime.combine(oid_fly.date_confirm_end, datetime.min.time())
                confirmed = True

            if oid_fly.choose_0101:
                start_val = date_start.strftime('%Y-01-01 00:00:00')
                date_start = datetime.strptime(start_val, '%Y-%m-%d %H:%M:%S')
            if oid_fly.choose_3112:
                end_val = date_end.strftime('%Y-12-31 00:00:00')
                date_end = datetime.strptime(end_val, '%Y-%m-%d %H:%M:%S')

            date_field = 'date'

            graph_name += "_{}".format(oid_fly.date_represent) if oid_fly.date_represent != 'none' else ""

            report_form_id = get_view_id(self, graph_name)

            if report_form_id:
                if oid_fly.choose_year:
                    start_date = date_start.strftime('%Y-01-01')
                    end_date = date_start.strftime('%Y-12-31')
                    date_start = datetime.strptime(start_date, '%Y-%m-%d')
                    date_end = datetime.strptime(end_date, '%Y-%m-%d')

                criteria = []
                if oid_fly.user_id:
                    criteria = [('user_id', '=', oid_fly.user_id.id)]
                    add_name = _("by Salesman") + ": {}".format(oid_fly.user_id.name)
                if oid_fly.partner_id:
                    criteria = [('partner_id', '=', oid_fly.partner_id.id)]
                    add_name = _("by Customer") + ": {}".format(oid_fly.partner_id.name)
                if oid_fly.order_id:
                    criteria = [('order_id', '=', oid_fly.order_id.id)]
                    add_name = _("by Order") + ": {}".format(oid_fly.order_id.name)
                if oid_fly.product_id:
                    criteria = [('product_id', '=', oid_fly.product_id.id)]
                    add_name = _("by Product") + ": {}".format(oid_fly.product_id.name)
                if oid_fly.product_tmpl_id:
                    criteria = [('product_tmpl_id', '=', oid_fly.product_tmpl_id.id)]
                    add_name = _("by Product Template") + ": {}".format(oid_fly.product_tmpl_id.name)
                if date_start:
                    criteria.append((date_field, '>=', date_start.strftime('%Y-%m-%d')))
                if date_end:
                    criteria.append((date_field, '<', date_end.strftime('%Y-%m-%d')))

                ret = {
                    'name': _('{} {}').format(base_name, add_name),
                    "view_mode": 'graph',
                    'res_model': 'sale.stat.report',
                    'type': 'ir.actions.act_window',
                    'search_view_id': report_search_id,
                    'view_id': report_form_id,
                    'domain': "{}".format(criteria),
                    'context': {
                        'group_by': [],
                        'measures': ['price_total', 'product_uom_qty'],
                    }
                }

        return ret