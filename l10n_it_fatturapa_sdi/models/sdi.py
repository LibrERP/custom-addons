# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
import platform


class SdiChannel(models.Model):
    _inherit = "sdi.channel"

    def _get_node(self):
        self.node = platform.node()

    channel_type = fields.Selection(
        selection_add=[("sdi", "SDI")],
        ondelete={"sdi": "cascade"}
    )
    channel_subtype = fields.Selection(
        string="SDI provider",
        selection=[],
        required=True,
    )

    sdi_username = fields.Char(string='Username', size=255)
    sdi_password = fields.Char('Password', size=50)
    sdi_storage_format = fields.Selection(
        [('xml', 'XML'), ('p7m', 'P7M')],
        'Invoice format', default='xml'
    )
    sdi_node = fields.Char(
        'SW Node', size=64, required=True, default='some_node',
        help="Protection against accidentally sending invoice during the tests." 
             "To be able to send XML invoices to SDI this value should be "
             "equal to the name of the local host")
    node = fields.Char(compute=_get_node, string='Server Node', method=True)
    # use_local_storage = fields.Boolean(string="Open documents from local storage", default=True)

    active_invoice_host = fields.Char(
        string='Server for Active Invoices'
    )
    passive_invoice_host = fields.Char(
        string='Server for Passive Invoices'
    )
