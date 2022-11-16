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

from odoo import api, fields, models, _


class SaleReport(models.Model):
    _name = "sale.stat.report"
    _inherit = "sale.report"
    _description = "Sales Orders Statistics"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'
    # _rec_name = 'date'

    supplier_id = fields.Many2one('res.partner', 'Supplier',
                                  readonly=True, index=True)
    state_id = fields.Many2one('res.country.state', 'Customer State',
                               readonly=True, index=True)
    region_id = fields.Many2one('res.country.region', 'Customer Region',
                                readonly=True, index=True)
    region_group_id = fields.Many2one('res.country.group',
                                       'Customer Region Group',
                                       readonly=True, index=True)
    country_group_id = fields.Many2one('res.country.group',
                                       'Customer Country Group',
                                       readonly=True, index=True)
    country_company_id = fields.Many2one('res.country',
                                         'Company Country',
                                         readonly=True, index=True)
    partner_company_id = fields.Many2one('res.partner',
                                         'Company Partner',
                                         readonly=True, index=True)
    is_foreign = fields.Boolean(readonly=True)

    amount_untaxed_to_deliver = fields.Float("Untaxed Amount To Deliver", digits=(16, 2), readonly=True, group_operator="sum")
    amount_untaxed_delivered = fields.Float("Untaxed Amount Delivered", digits=(16, 2), readonly=True, group_operator="sum")
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', readonly=True)
    margin = fields.Float('Margin')

    def _select(self, other_select=""):
        select_str = """
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
            sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
            sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
            sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
            sum(l.price_total / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_total,
            sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_subtotal,
            sum(l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_to_invoice,
            sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_invoiced,
            sum((l.product_uom_qty - l.qty_delivered) * l.price_unit * (1 - (l.discount) / 100.0) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as amount_untaxed_to_deliver,
            sum(l.qty_delivered * l.price_unit * (1 - (l.discount) / 100.0) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as amount_untaxed_delivered,
            SUM(l.margin / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS margin,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.confirmation_date as confirmation_date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.warehouse_id as warehouse_id,
            company.id as company_id,
            partner_company.id as partner_company_id,
            extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.analytic_account_id as analytic_account_id,
            s.team_id as team_id,
            p.product_tmpl_id as product_tmpl_id,
            partner_state.id as state_id,
            region_state.id as region_id,
            partner_country.id as country_id,
            partner_company.country_id as country_company_id,
            CASE WHEN partner_company.country_id = partner_country.id THEN FALSE ELSE TRUE END as is_foreign,
            rcgrel.res_country_group_id as country_group_id,
            regrel.res_country_group_id as region_group_id,
            partner.commercial_partner_id as supplier_id,
            partner.commercial_partner_id as commercial_partner_id,
            sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
            sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume,
            l.discount as discount,
            sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) as discount_amount,
            s.id as order_id
        """
        select_str += ", {}".format(other_select) if other_select else ""
        return select_str

    def _from(self, other_from=""):
        from_str = """
                sale_order_line l
                    join sale_order s on (l.order_id=s.id)
                    join res_company company on s.company_id = company.id
                        left join res_partner partner_company on (company.partner_id=partner_company.id)
                    join res_partner partner on s.partner_id = partner.id
                    left join res_country partner_country on (partner.country_id=partner_country.id)
                    left join res_country_state partner_state on (partner.state_id=partner_state.id)
                        left join res_country_region region_state on (partner_state.region_id=region_state.id)
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
                    left join res_country_res_country_group_rel rcgrel on (partner_country.id = rcgrel.res_country_id)
                    left join res_country_region_id regrel on (region_state.id = regrel.res_country_region_id)
        """
        from_str += ", {}".format(other_from) if other_from else ""
        return from_str

    def _group_by(self, other_groups=""):
        group_by_str = """
            l.product_id,
            l.order_id,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.confirmation_date,
            s.partner_id,
            s.user_id,
            s.state,
            s.warehouse_id,
            company.id,
            s.pricelist_id,
            s.analytic_account_id,
            s.team_id,
            p.product_tmpl_id,
            partner_state.id,
            region_state.id,
            partner_country.id,
            partner.commercial_partner_id,
            partner_company.id,
            partner_company.country_id,
            rcgrel.res_country_group_id,
            regrel.res_country_group_id,
            l.discount,
            s.id
        """
        group_by_str += ", {}".format(other_groups) if other_groups else ""
        return group_by_str

    def _index_fields(self, other_fields=[]):
        fields = [
            'id',
            'order_id',
            'product_id',
            'product_tmpl_id',
            'product_uom',
            'date',
            'confirmation_date',
            'partner_id',
            'user_id',
            'company_id',
            'state',
            'categ_id',
            'pricelist_id',
            'warehouse_id',
            'analytic_account_id',
            'team_id',
            'state_id',
            'region_id',
            'country_id',
            'supplier_id',
            'commercial_partner_id',
            'country_company_id',
        ]
        fields.extend(other_fields)
        return fields

    def _cleanup(self):
        cr = self._cr
        ret = False
        try:
            cr.execute('SAVEPOINT creatematerialview')
            cr.execute("DROP MATERIALIZED VIEW IF EXISTS {table} CASCADE".format(table=self._table))
            cr.execute('RELEASE SAVEPOINT creatematerialview')
        except:
            try:
                cr.execute('ROLLBACK TO SAVEPOINT creatematerialview')
                cr.execute('SAVEPOINT creatematerialview2')
                cr.execute("DROP VIEW IF EXISTS {table} CASCADE".format(table=self._table))
                cr.execute('RELEASE SAVEPOINT creatematerialview2')
            except:
                cr.execute('ROLLBACK TO SAVEPOINT creatematerialview2')
                ret = True
        return ret

    def _query(self, with_clause="", other_select="", groupby="", from_clause=""):
        """
            Refreshes Materialized View.
        """
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        select_ = self._select(other_select)
        from_ = self._from(from_clause)
        groupby_ = self._group_by(groupby)

        return '%s (SELECT %s FROM %s GROUP BY %s)' % (with_, select_, from_, groupby_)

    def _create(self, table="", query=""):
        if table and query:
            cr = self._cr
            cr.execute(
                """CREATE MATERIALIZED VIEW {table} as (
                 {query}
                )""" .format(table=table, query=query)
                )

    def _optimize(self, fields=[]):
        """
            Add indexes on Materialized View.
        """
        cr = self._cr
        for field in fields:
            if cr._obj.connection.server_version >= 90500:
                # requires Postgresql 9.5+
                cr.execute(
                    "CREATE INDEX IF NOT EXISTS idx_{field}_{table} ON {table} ({field})".format(table=self._table,
                                                                                                 field=field))
            elif cr._obj.connection.server_version >= 90400:
                # requires Postgresql 9.4+
                # https://dba.stackexchange.com/questions/35616/create-index-if-it-does-not-exist
                cr.execute("""DO
                $$
                BEGIN
                   IF to_regclass('idx_{field}_{table}') IS NULL THEN
                      CREATE INDEX idx_{field}_{table} ON {table} ({field});
                   END IF;
                END
                $$;
                """.format(table=self._table, field=field))
#
#    External methods
#

    def refresh(self, request=None):
        """
            Refreshes Materialized Views, from scheduler.
        """
        cr = self._cr
        cr.execute("REFRESH MATERIALIZED VIEW {table}".format(table=self._table))
        return False

    def init(self):
        """
            Initializes Materialized Views.

            Override to customize it, adding fields to with, select, from and group by
            clauses, to improve / extend analysis objects, calling _query method,
            Index fields can be extended passing a list of fields to add to indexes.

            e.g.
            self._create(self._table, self._query(with_clause, other_select, groupby, from_clause))
            self._optimize(self._index_fields(fields))
       """
        if not self._cleanup():
            self._create(self._table, self._query())
            self._optimize(self._index_fields())
