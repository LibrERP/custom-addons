# © 2021 Fabio Giovannelli <fabio.giovannelli@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardImportFatturapa(models.TransientModel):
    _inherit = 'wizard.import.fatturapa'

    def get_account_taxes(self, AliquotaIVA, Natura):
        """
        Override the original method because of not raising errors
        """
        account_tax_model = self.env['account.tax']
        # check if a default tax exists and generate def_purchase_tax object
        ir_values = self.env['ir.default']
        company_id = self.env['res.company']._company_default_get(
            'account.invoice.line').id
        supplier_taxes_ids = ir_values.get(
            'product.product', 'supplier_taxes_id', company_id=company_id)
        def_purchase_tax = False
        if supplier_taxes_ids:
            def_purchase_tax = account_tax_model.browse(supplier_taxes_ids)[0]
        if float(AliquotaIVA) == 0.0 and Natura:
            account_taxes = account_tax_model.search(
                [
                    ('type_tax_use', '=', 'purchase'),
                    ('kind_id.code', '=', Natura),
                    ('amount', '=', 0.0),
                ], order='sequence')
            if not account_taxes:
                msg = _('No tax with percentage %s and nature %s found. '
                        'Please configure this tax.') % (AliquotaIVA, Natura)
                self.log_inconsistency(msg)
                raise UserError(msg)
            if len(account_taxes) > 1:
                msg = _('Too many taxes with percentage %s and nature %s found.'
                        ' Tax %s with lower priority has been set on invoice '
                        'lines.') % (AliquotaIVA, Natura,
                                     account_taxes[0].description)
                self.log_inconsistency(msg)
                # raise UserError(msg)
        else:
            account_taxes = account_tax_model.search(
                [
                    ('type_tax_use', '=', 'purchase'),
                    ('amount', '=', float(AliquotaIVA)),
                    ('price_include', '=', False),
                    # partially deductible VAT must be set by user
                    ('children_tax_ids', '=', False),
                ], order='sequence')
            if not account_taxes:
                msg = _("XML contains tax with percentage '%s' but it does not "
                        "exist in your system") % AliquotaIVA
                self.log_inconsistency(msg)
                raise UserError(msg)
            # check if there are multiple taxes with
            # same percentage
            if len(account_taxes) > 1:
                # just logging because this is an usual case: see split payment
                _logger.warning(_(
                    "Too many taxes with percentage equals "
                    "to '%s'.\nFix it if required"
                ) % AliquotaIVA)
                # if there are multiple taxes with same percentage
                # and there is a default tax with this percentage,
                # set taxes list equal to supplier_taxes_id, loaded before
                if (
                    def_purchase_tax and
                    def_purchase_tax.amount == (float(AliquotaIVA))
                ):
                    account_taxes = def_purchase_tax
        return account_taxes
