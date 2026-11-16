# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import models
from odoo.tools import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)

# DatiRiepilogo monetary amounts (ImponibileImporto, Imposta, Arrotondamento)
# are Amount2DecimalType in the FatturaPA schema: exactly 2 decimals.
FPA_RIEPILOGO_PRECISION = 2


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def getAllTaxes(self, invoice):
        """Add <Arrotondamento> to each VAT summary line whose tax breaks the
        SdI 00421 constraint `Imposta == round(ImponibileImporto * aliquota / 100)`.

        With price-included taxes, Odoo rounds VAT per line, so the booked tax
        (sum of per-line rounded VAT) can differ by a cent or two from
        `round(taxable_base * rate)`. The base OCA module copies the booked base
        and tax verbatim and never emits <Arrotondamento>, so SdI rejects the
        file. We mirror core `l10n_it_edi` here: pin the taxable base to
        `Imposta * 100 / aliquota` and record the delta vs the per-line base in
        <Arrotondamento>. Booked VAT and the document total are left untouched.
        """
        all_taxes = super().getAllTaxes(invoice)
        prec = FPA_RIEPILOGO_PRECISION
        for key, tax_data in all_taxes.items():
            tax = self.env["account.tax"].browse(key)
            if tax.exists() and tax.amount_type == "percent" and tax.price_include:
                rate = tax.amount
                if rate:
                    base = tax_data.get("ImponibileImporto") or 0.0
                    imposta = tax_data.get("Imposta") or 0.0

                    if float_is_zero(imposta, precision_digits=prec):
                        continue

                    sign = -1.0 if base < 0 else 1.0
                    abase = abs(base)
                    aimposta = abs(imposta)

                    # Already consistent? Leave it exactly as the base module produced it.
                    if float_compare(
                        float_round(abase * rate / 100.0, precision_digits=prec),
                        aimposta,
                        precision_digits=prec,
                    ) == 0:
                        continue

                    target_base = float_round(aimposta * 100.0 / rate, precision_digits=prec)
                    arrotondamento = float_round(target_base - abase, precision_digits=prec)

                    if float_is_zero(arrotondamento, precision_digits=prec):
                        continue

                    tax_data["ImponibileImporto"] = sign * target_base
                    tax_data["Arrotondamento"] = sign * arrotondamento
                    _logger.info(
                        "FatturaPA %s: tax %s (%.2f%%) price-included rounding fixed: "
                        "ImponibileImporto %.2f -> %.2f, Arrotondamento %.2f, Imposta %.2f",
                        invoice.name or invoice.id,
                        tax.name,
                        rate,
                        abase,
                        target_base,
                        arrotondamento,
                        aimposta,
                    )
        return all_taxes
