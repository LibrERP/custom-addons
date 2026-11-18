# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import models
from odoo.tools import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)

# DatiRiepilogo monetary amounts (ImponibileImporto, Imposta, Arrotondamento)
# are Amount2DecimalType in the FatturaPA schema: exactly 2 decimals.
FPA_RIEPILOGO_PRECISION = 2

# SdI applies a rounding tolerance to control 00421
# (Imposta == round(ImponibileImporto * aliquota / 100)). As long as the booked
# VAT stays within this tolerance of the recomputed value, SdI accepts it, so we
# keep Odoo's booked Imposta (which matches the registro IVA) untouched. We only
# override it when the gap would actually trigger a scarto.
SDI_00421_TOLERANCE = 0.01


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def getAllTaxes(self, invoice):
        """Fix VAT summary lines that would break SdI 00421
        `Imposta == round(ImponibileImporto * aliquota / 100)`.

        With price-included taxes Odoo rounds VAT per line, so the booked tax
        (sum of per-line rounded VAT) can differ from `round(taxable_base * rate)`.
        The base OCA module copies the booked base and tax verbatim.

        Tolerance-aware behaviour: SdI accepts a small rounding gap on 00421, so
        whenever the booked Imposta is within SDI_00421_TOLERANCE of the recomputed
        value we leave it exactly as Odoo booked it - this keeps the e-invoice in
        sync with the registro IVA (the common one-cent price-included case, e.g.
        booked 20.40 vs recomputed 20.39). Only when the gap exceeds the tolerance
        (where SdI would actually reject, e.g. a 0.02 delta) do we pin <Imposta>
        to `round(ImponibileImporto * aliquota / 100)`.

        We keep the real taxable base (which equals the sum of the lines'
        PrezzoTotale, so 00423 stays satisfied) and never emit <Arrotondamento>
        nor inflate the base (the earlier `Imposta * 100 / aliquota` approach),
        because that pushed ImponibileImporto above the real line total
        (e.g. 92.68 -> 92.73) and broke the
        Imponibile + Imposta = ImportoTotaleDocumento reconciliation.
        """
        all_taxes = super().getAllTaxes(invoice)
        prec = FPA_RIEPILOGO_PRECISION
        for key, tax_data in all_taxes.items():
            tax = self.env["account.tax"].browse(key)
            # Margin-scheme taxes (l10n_it_second_hand_tax) are collapsed to
            # AliquotaIVA 0 / Natura N5 / Imposta 0, with the whole gross folded
            # back into ImponibileImporto. The SdI 00421 constraint does not apply
            # to them, so the correction below must not touch them.
            # getattr keeps this safe when that module is not installed.
            if (
                tax.exists()
                and tax.amount_type == "percent"
                and tax.price_include
                and not getattr(tax, "is_margin_tax", False)
            ):
                rate = tax.amount
                if rate:
                    base = tax_data.get("ImponibileImporto") or 0.0
                    imposta = tax_data.get("Imposta") or 0.0

                    if float_is_zero(imposta, precision_digits=prec):
                        continue

                    sign = -1.0 if imposta < 0 else 1.0
                    expected_imposta = sign * float_round(
                        abs(base) * rate / 100.0, precision_digits=prec
                    )

                    # Within the SdI tolerance (includes the already-consistent
                    # case)? Keep Odoo's booked Imposta so the XML matches the books.
                    gap = float_round(
                        abs(imposta - expected_imposta), precision_digits=prec
                    )
                    if float_compare(
                        gap, SDI_00421_TOLERANCE, precision_digits=prec
                    ) <= 0:
                        continue

                    tax_data["Imposta"] = expected_imposta
                    _logger.info(
                        "FatturaPA %s: tax %s (%.2f%%) price-included VAT gap %.2f "
                        "exceeds SdI tolerance %.2f: Imposta %.2f -> %.2f on "
                        "ImponibileImporto %.2f (Arrotondamento omitted)",
                        invoice.name or invoice.id,
                        tax.name,
                        rate,
                        gap,
                        SDI_00421_TOLERANCE,
                        imposta,
                        expected_imposta,
                        base,
                    )
        return all_taxes
