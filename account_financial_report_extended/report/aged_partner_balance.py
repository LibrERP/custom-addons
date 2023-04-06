# © 2016 Julien Coux (Camptocamp)
# © 2023 Didotech s.r.l.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
# from odoo.addons.account_financial_report.report.aged_partner_balance import AgedPartnerBalanceReportCompute as OriginalAgedPartnerBalanceReportCompute


class AgedPartnerBalanceReport(models.TransientModel):
    """ Here, we just define class fields.
        added hide_totals equal to zero
    """

    _inherit = 'report_aged_partner_balance'

    hide_account_at_0 = fields.Boolean()


class AgedPartnerBalanceReportCompute(models.TransientModel):
    """ Here, we just define methods.
    Override methods to handle the new field
    """

    _inherit = 'report_aged_partner_balance'

    def _prepare_report_open_items(self):
        self.ensure_one()
        res = super()._prepare_report_open_items()
        res['hide_account_at_0'] = self.hide_account_at_0
        return res

    def _inject_line_values(self, only_empty_partner_line=False):
        """ Inject report values for report_aged_partner_balance_line.

        The "only_empty_partner_line" value is used
        to compute data without partner.
        """
        query_inject_line = """
WITH
    date_range AS
        (
            SELECT
                DATE %s AS date_current,
                DATE %s - INTEGER '30' AS date_less_30_days,
                DATE %s - INTEGER '60' AS date_less_60_days,
                DATE %s - INTEGER '90' AS date_less_90_days,
                DATE %s - INTEGER '120' AS date_less_120_days
        )
INSERT INTO
    report_aged_partner_balance_line
    (
        report_partner_id,
        create_uid,
        create_date,
        partner,
        amount_residual,
        current,
        age_30_days,
        age_60_days,
        age_90_days,
        age_120_days,
        older
    )
SELECT
    rp.id AS report_partner_id,
    %s AS create_uid,
    NOW() AS create_date,
      """
        if self.env.context.get('export_cribis'):
            query_inject_line += """
        rp.partner_id,
            """
        else:
            query_inject_line += """
            rp.name,
            """

        query_inject_line += """
    
    SUM(rlo.amount_residual) AS amount_residual,
    SUM(
        CASE
            WHEN rlo.date_due >= date_range.date_current
            THEN rlo.amount_residual
        END
    ) AS current,
    SUM(
        CASE
            WHEN
                rlo.date_due >= date_range.date_less_30_days
                AND rlo.date_due < date_range.date_current
            THEN rlo.amount_residual
        END
    ) AS age_30_days,
    SUM(
        CASE
            WHEN
                rlo.date_due >= date_range.date_less_60_days
                AND rlo.date_due < date_range.date_less_30_days
            THEN rlo.amount_residual
        END
    ) AS age_60_days,
    SUM(
        CASE
            WHEN
                rlo.date_due >= date_range.date_less_90_days
                AND rlo.date_due < date_range.date_less_60_days
            THEN rlo.amount_residual
        END
    ) AS age_90_days,
    SUM(
        CASE
            WHEN
                rlo.date_due >= date_range.date_less_120_days
                AND rlo.date_due < date_range.date_less_90_days
            THEN rlo.amount_residual
        END
    ) AS age_120_days,
    SUM(
        CASE
            WHEN rlo.date_due < date_range.date_less_120_days
            THEN rlo.amount_residual
        END
    ) AS older
FROM
    date_range,
    report_open_items_move_line rlo
INNER JOIN
    report_open_items_partner rpo ON rlo.report_partner_id = rpo.id
INNER JOIN
    report_open_items_account rao ON rpo.report_account_id = rao.id
INNER JOIN
    report_aged_partner_balance_account ra ON rao.code = ra.code
INNER JOIN
    report_aged_partner_balance_partner rp
        ON
            ra.id = rp.report_account_id
        """
        if not only_empty_partner_line:
            query_inject_line += """
        AND rpo.partner_id = rp.partner_id
            """
        elif only_empty_partner_line:
            query_inject_line += """
        AND rpo.partner_id IS NULL
        AND rp.partner_id IS NULL
            """
        query_inject_line += """
WHERE
    rao.report_id = %s
AND ra.report_id = %s """
        if self.hide_account_at_0:
            query_inject_line += """
AND amount_residual != 0.00
"""

        query_inject_line += """
GROUP BY
    rp.id
        """
        query_inject_line_params = (self.date_at,) * 5
        query_inject_line_params += (
            self.env.uid,
            self.open_items_id.id,
            self.id,
        )
        self.env.cr.execute(query_inject_line, query_inject_line_params)

# OriginalAgedPartnerBalanceReportCompute._inject_line_values = AgedPartnerBalanceReportCompute._inject_line_values


