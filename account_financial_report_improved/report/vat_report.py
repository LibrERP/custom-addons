# Copyright  2023 Didotech s.r.l.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class VATReportCompute(models.TransientModel):
    """ Here, we just define methods.
    For class fields, go more top at this file.
    """

    _inherit = 'report_vat_report'

    def _inject_taxtags_values(self):
        """Inject report values for report_vat_report_taxtags."""
        query_inject_taxtags = """
WITH
    taxtags AS
        (SELECT coalesce(regexp_replace(tag.name,
                '[^0-9\\.]+', '', 'g'), ' ') AS code,
                tag.name, tag.id,
                coalesce(sum(
                case 
                    when move.move_type = 'receivable_refund' then -movetax.tax_base_amount 
                    else movetax.tax_base_amount
                end
                ), 0.00) AS net,
                coalesce(sum(movetax.balance), 0.00) AS tax
            FROM
                account_account_tag AS tag
                INNER JOIN account_tax_account_tag AS taxtag
                    ON tag.id = taxtag.account_account_tag_id
                INNER JOIN account_tax AS tax
                    ON tax.id = taxtag.account_tax_id
                INNER JOIN account_move_line AS movetax
                    ON movetax.tax_line_id = tax.id
                INNER JOIN account_move AS move
                    ON move.id = movetax.move_id
            WHERE tag.id is not null AND movetax.tax_exigible
                AND move.company_id = %s AND move.date >= %s
                    AND move.date <= %s AND move.state = 'posted'
            GROUP BY tag.id
            ORDER BY code, tag.name
        )
INSERT INTO
    report_vat_report_taxtag
    (
    report_id,
    create_uid,
    create_date,
    taxtag_id,
    code,
    name,
    net, tax
    )
SELECT
    %s AS report_id,
    %s AS create_uid,
    NOW() AS create_date,
    tag.id,
    tag.code,
    tag.name,
    abs(tag.net),
    abs(tag.tax)
FROM
    taxtags tag
        """
        query_inject_taxtags_params = (self.company_id.id, self.date_from,
                                       self.date_to, self.id, self.env.uid)
        self.env.cr.execute(query_inject_taxtags, query_inject_taxtags_params)

    def _inject_taxgroups_values(self):
        """Inject report values for report_vat_report_taxtags."""
        query_inject_taxgroups = """
WITH
    taxgroups AS
        (SELECT coalesce(taxgroup.sequence, 0) AS code,
                taxgroup.name, taxgroup.id,
                 coalesce(sum(
                case 
                    when move.move_type = 'receivable_refund' then -movetax.tax_base_amount 
                    else movetax.tax_base_amount
                end
                ), 0.00) AS net,
                coalesce(sum(movetax.balance), 0.00) AS tax
            FROM
                account_tax_group AS taxgroup
                INNER JOIN account_tax AS tax
                    ON tax.tax_group_id = taxgroup.id
                INNER JOIN account_move_line AS movetax
                    ON movetax.tax_line_id = tax.id
                INNER JOIN account_move AS move
                    ON move.id = movetax.move_id
            WHERE taxgroup.id is not null AND movetax.tax_exigible
                AND move.company_id = %s AND move.date >= %s
                    AND move.date <= %s AND move.state = 'posted'
            GROUP BY taxgroup.id
            ORDER BY code, taxgroup.name
        )
INSERT INTO
    report_vat_report_taxtag
    (
    report_id,
    create_uid,
    create_date,
    taxgroup_id,
    code,
    name,
    net, tax
    )
SELECT
    %s AS report_id,
    %s AS create_uid,
    NOW() AS create_date,
    groups.id,
    groups.code,
    groups.name,
    abs(groups.net),
    abs(groups.tax)
FROM
    taxgroups groups
        """
        query_inject_taxgroups_params = (self.company_id.id, self.date_from,
                                         self.date_to, self.id, self.env.uid)
        self.env.cr.execute(query_inject_taxgroups,
                            query_inject_taxgroups_params)

    def _inject_tax_taxtags_values(self):
        """ Inject report values for report_vat_report_tax. """
        # pylint: disable=sql-injection
        query_inject_tax = """
WITH
    taxtags_tax AS
        (
            SELECT
                tag.id AS report_tax_id, ' ' AS code,
                tax.name, tax.id,
                 coalesce(sum(
                case 
                    when move.move_type = 'receivable_refund' then -movetax.tax_base_amount 
                    else movetax.tax_base_amount
                end
                ), 0.00) AS net,
                coalesce(sum(movetax.balance), 0.00) AS tax
            FROM
                report_vat_report_taxtag AS tag
                INNER JOIN account_tax_account_tag AS taxtag
                    ON tag.taxtag_id = taxtag.account_account_tag_id
                INNER JOIN account_tax AS tax
                    ON tax.id = taxtag.account_tax_id
                INNER JOIN account_move_line AS movetax
                    ON movetax.tax_line_id = tax.id
                INNER JOIN account_move AS move
                    ON move.id = movetax.move_id
            WHERE tag.id is not null AND movetax.tax_exigible
                AND tag.report_id = %s AND move.company_id = %s
                AND move.date >= %s AND move.date <= %s
                AND move.state = 'posted'
            GROUP BY tag.id, tax.id
            ORDER BY tax.name
        )
INSERT INTO
    report_vat_report_tax
    (
    report_tax_id,
    create_uid,
    create_date,
    tax_id,
    name,
    net,
    tax
    )
SELECT
    tt.report_tax_id,
    %s AS create_uid,
    NOW() AS create_date,
    tt.id,
    tt.name,
    abs(tt.net),
    abs(tt.tax)
FROM
    taxtags_tax tt
        """
        query_inject_tax_params = (self.id, self.company_id.id, self.date_from,
                                   self.date_to, self.env.uid)
        self.env.cr.execute(query_inject_tax, query_inject_tax_params)

    def _inject_tax_taxgroups_values(self):
        """ Inject report values for report_vat_report_tax. """
        # pylint: disable=sql-injection
        query_inject_tax = """
WITH
    taxtags_tax AS
        (
            SELECT
                taxtag.id AS report_tax_id, ' ' AS code,
                tax.name, tax.id,
                 coalesce(sum(
                case 
                    when move.move_type = 'receivable_refund' then -movetax.tax_base_amount 
                    else movetax.tax_base_amount
                end
                ), 0.00) AS net,
                coalesce(sum(movetax.balance), 0.00) AS tax
            FROM
                report_vat_report_taxtag AS taxtag
                INNER JOIN account_tax AS tax
                    ON tax.tax_group_id = taxtag.taxgroup_id
                INNER JOIN account_move_line AS movetax
                    ON movetax.tax_line_id = tax.id
                INNER JOIN account_move AS move
                    ON move.id = movetax.move_id
            WHERE taxtag.id is not null AND movetax.tax_exigible
                AND taxtag.report_id = %s AND move.company_id = %s
                AND move.date >= %s AND move.date <= %s
                AND move.state = 'posted'
            GROUP BY taxtag.id, tax.id
            ORDER BY tax.name
        )
INSERT INTO
    report_vat_report_tax
    (
    report_tax_id,
    create_uid,
    create_date,
    tax_id,
    name,
    net,
    tax
    )
SELECT
    tt.report_tax_id,
    %s AS create_uid,
    NOW() AS create_date,
    tt.id,
    tt.name,
    abs(tt.net),
    abs(tt.tax)
FROM
    taxtags_tax tt
        """
        query_inject_tax_params = (self.id, self.company_id.id, self.date_from,
                                   self.date_to, self.env.uid)
        self.env.cr.execute(query_inject_tax, query_inject_tax_params)
