from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        fields = result["search_params"]["fields"]

        try:
            fiscalcode_index = fields.index("fiscalcode")
        except ValueError:
            fiscalcode_index = len(fields) - 1

        insert_pos = fiscalcode_index + 1
        for field in [
            "pec_destinatario",
            "codice_destinatario",
            "electronic_invoice_subjected",
            "electronic_invoice_obliged_subject",
        ]:
            if field not in fields:
                fields.insert(insert_pos, field)
                insert_pos += 1

        return result
