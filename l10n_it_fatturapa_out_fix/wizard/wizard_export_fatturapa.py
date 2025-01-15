# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import datetime

# from odoo import _, api, fields, models
from odoo.addons.l10n_it_fatturapa_out.wizard.wizard_export_fatturapa import FatturapaBDS
from odoo.addons.l10n_it_fatturapa.bindings.binding import DataFatturaType
from pyxb.binding.datatypes import decimal as pyxb_decimal
import datetime


def valueAsText(self, value, enable_default_namespace=True):
    if isinstance(value, pyxb_decimal) and hasattr(value, '_CF_pattern'):
        # PyXB changes the text representation of decimals
        # so that it breaks pattern matching.
        # We have to use directly the string value
        # instead of letting PyXB edit it
        return str(value)
    elif isinstance(value, (DataFatturaType, datetime.date)):
        return value.strftime("%Y-%m-%d")
    return super(FatturapaBDS, self).valueAsText(value, enable_default_namespace)


FatturapaBDS.valueAsText = valueAsText
