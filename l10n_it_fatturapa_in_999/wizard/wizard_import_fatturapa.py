# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
import re


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def getPartnerBase(self, DatiAnagrafici):
        partner_model = self.env["res.partner"]

        if DatiAnagrafici and DatiAnagrafici.IdFiscaleIVA:
            id_paese = DatiAnagrafici.IdFiscaleIVA.IdPaese.upper()
            id_codice = re.sub(r"\W+", "", DatiAnagrafici.IdFiscaleIVA.IdCodice).upper()

            if not id_paese == "IT" and id_codice[:6] == '999999':
                domain = [("name", '=', DatiAnagrafici.Anagrafica.Denominazione or DatiAnagrafici.Anagrafica.Nome)]
                partners = partner_model.search(domain)
                if len(partners) == 1:
                    return partners[0].commercial_partner_id.id

        return super().getPartnerBase(DatiAnagrafici)
