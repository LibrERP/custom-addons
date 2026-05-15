#    Created on : 2020-10-23    Author : Fabio Colognesi
#
# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleReport(models.Model):
    _name = "sale.stat.report"
    _inherit = "sale.report"
    _description = "Sales Orders Statistics"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    supplier_id = fields.Many2one('res.partner', 'Supplier',
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

    amount_untaxed_to_deliver = fields.Float(
        "Untaxed Amount To Deliver", digits=(16, 2), readonly=True,
        aggregator="sum")
    amount_untaxed_delivered = fields.Float(
        "Untaxed Amount Delivered", digits=(16, 2), readonly=True,
        aggregator="sum")
    order_id = fields.Many2one('sale.order', 'Order', readonly=True, index=True)

    # Disable the parent's `_table_query` to use a materialized view managed
    # via `init()` instead of a regular SQL view.
    @property
    def _table_query(self):
        return None

    def _case_value_or_one(self, value):
        return f"CASE COALESCE({value}, 0) WHEN 0 THEN 1.0 ELSE {value} END"

    def _select(self, other_select=""):
        rate = self._case_value_or_one('s.currency_rate')
        select_str = f"""
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
            sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
            sum((l.product_uom_qty - l.qty_delivered) / u.factor * u2.factor) as qty_to_deliver,
            sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
            sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
            avg(l.price_unit / {rate}) as price_unit,
            sum(l.price_total / {rate}) as price_total,
            sum(l.price_subtotal / {rate}) as price_subtotal,
            sum(l.untaxed_amount_to_invoice / {rate}) as untaxed_amount_to_invoice,
            sum(l.untaxed_amount_invoiced / {rate}) as untaxed_amount_invoiced,
            sum((l.product_uom_qty - l.qty_delivered) * l.price_unit * (1 - (l.discount) / 100.0) / {rate}) as amount_untaxed_to_deliver,
            sum(l.qty_delivered * l.price_unit * (1 - (l.discount) / 100.0) / {rate}) as amount_untaxed_delivered,
            sum(l.margin / {rate}) as margin,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.invoice_status as invoice_status,
            l.invoice_status as line_invoice_status,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.warehouse_id as warehouse_id,
            company.id as company_id,
            partner_company.id as partner_company_id,
            s.campaign_id as campaign_id,
            s.medium_id as medium_id,
            s.source_id as source_id,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.team_id as team_id,
            p.product_tmpl_id as product_tmpl_id,
            partner_state.id as state_id,
            region_state.id as region_id,
            partner_country.id as country_id,
            partner.industry_id as industry_id,
            partner.zip as partner_zip,
            partner_company.country_id as country_company_id,
            CASE WHEN partner_company.country_id = partner_country.id THEN FALSE ELSE TRUE END as is_foreign,
            rcgrel.res_country_group_id as country_group_id,
            regrel.country_group_id as region_group_id,
            partner.commercial_partner_id as supplier_id,
            partner.commercial_partner_id as commercial_partner_id,
            sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
            sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume,
            l.discount as discount,
            sum(l.price_unit * l.product_uom_qty * l.discount / 100.0 / {rate}) as discount_amount,
            concat('sale.order', ',', s.id) as order_reference,
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
                    left join res_country_region_country_group_rel regrel on (region_state.id = regrel.region_id)
        """
        from_str += " {}".format(other_from) if other_from else ""
        return from_str

    def _where(self, other_where=""):
        where_str = "l.display_type IS NULL"
        where_str += " AND {}".format(other_where) if other_where else ""
        return where_str

    def _group_by(self, other_groups=""):
        group_by_str = """
            l.product_id,
            l.order_id,
            l.price_unit,
            l.invoice_status,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.partner_id,
            s.user_id,
            s.state,
            s.invoice_status,
            s.warehouse_id,
            company.id,
            s.campaign_id,
            s.medium_id,
            s.source_id,
            s.pricelist_id,
            s.team_id,
            p.product_tmpl_id,
            partner_state.id,
            region_state.id,
            partner_country.id,
            partner.commercial_partner_id,
            partner.industry_id,
            partner.zip,
            partner_company.id,
            partner_company.country_id,
            rcgrel.res_country_group_id,
            regrel.country_group_id,
            l.discount,
            s.id
        """
        group_by_str += ", {}".format(other_groups) if other_groups else ""
        return group_by_str

    def _index_fields(self, other_fields=None):
        fields_ = [
            'id',
            'order_id',
            'product_id',
            'product_tmpl_id',
            'product_uom',
            'date',
            'partner_id',
            'user_id',
            'company_id',
            'state',
            'categ_id',
            'pricelist_id',
            'warehouse_id',
            'team_id',
            'state_id',
            'region_id',
            'country_id',
            'supplier_id',
            'commercial_partner_id',
            'country_company_id',
        ]
        if other_fields:
            fields_.extend(other_fields)
        return fields_

    def _cleanup(self):
        cr = self._cr
        ret = False
        try:
            cr.execute('SAVEPOINT creatematerialview')
            cr.execute("DROP MATERIALIZED VIEW IF EXISTS {table} CASCADE".format(table=self._table))
            cr.execute('RELEASE SAVEPOINT creatematerialview')
        except Exception:
            try:
                cr.execute('ROLLBACK TO SAVEPOINT creatematerialview')
                cr.execute('SAVEPOINT creatematerialview2')
                cr.execute("DROP VIEW IF EXISTS {table} CASCADE".format(table=self._table))
                cr.execute('RELEASE SAVEPOINT creatematerialview2')
            except Exception:
                cr.execute('ROLLBACK TO SAVEPOINT creatematerialview2')
                ret = True
        return ret

    def _query(self, with_clause="", other_select="", groupby="", from_clause="", where_clause=""):
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        select_ = self._select(other_select)
        from_ = self._from(from_clause)
        where_ = self._where(where_clause)
        groupby_ = self._group_by(groupby)
        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s)' % (
            with_, select_, from_, where_, groupby_)

    def _create(self, table="", query=""):
        if table and query:
            cr = self._cr
            cr.execute(
                """CREATE MATERIALIZED VIEW {table} as (
                 {query}
                )""".format(table=table, query=query)
            )

    def _optimize(self, fields_=None):
        if not fields_:
            return
        cr = self._cr
        for field in fields_:
            cr.execute(
                "CREATE INDEX IF NOT EXISTS idx_{field}_{table} "
                "ON {table} ({field})".format(table=self._table, field=field)
            )

    def refresh(self, request=None):
        """ Refreshes Materialized View, called from cron. """
        self._cr.execute(
            "REFRESH MATERIALIZED VIEW {table}".format(table=self._table)
        )
        return False

    def init(self):
        """ Initializes Materialized View.

            Override to customize, adding fields to with, select, from, where
            and group by clauses, to improve / extend analysis objects, calling
            _query method. Index fields can be extended by passing a list of
            additional fields to indexes.
        """
        if not self._cleanup():
            self._create(self._table, self._query())
            self._optimize(self._index_fields())