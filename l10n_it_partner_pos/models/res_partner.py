from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_from_ui(self, partner):
        partner_values = dict(partner or {})
        codice_present = "codice_destinatario" in partner_values
        pec_present = "pec_destinatario" in partner_values

        if codice_present or pec_present:
            codice = (partner_values.get("codice_destinatario") or "").strip()
            pec = (partner_values.get("pec_destinatario") or "").strip()
            enabled = bool(codice or pec)
            partner_values["electronic_invoice_subjected"] = enabled
            partner_values["electronic_invoice_obliged_subject"] = enabled

        return super().create_from_ui(partner_values)
