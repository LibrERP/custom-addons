# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from openpyxl import Workbook
from openpyxl.styles import Alignment
from io import BytesIO
import base64


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    def download_stock_report(self):
        if self.env.context['active_model'] == 'stock.inventory' and self.env.context['active_id']:
            inventory = self.browse(self.env.context['active_id'])
            filename = f'inventory_report-{inventory.date.date()}.xlsx'

            report = inventory.get_report()

            wizard = self.env['wizard.inventory.report'].create({
                'inventory_id': inventory.id,
                'filename': filename,
                'data_file': base64.encodestring(report)
            })

            return {
                'name': _('Download Inventory Report'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                "view_type": "form",
                'res_model': 'wizard.inventory.report',
                'res_id': wizard.id,
                'target': 'new'
            }

    def get_report(self):
        # Create a new workbook
        workbook = Workbook()

        # Get the active worksheet
        ws = workbook.active

        # Optionally, rename the worksheet
        ws.title = self.name

        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 60
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 60

        ws.append([
            "Codice",
            "Nome",
            "Quantità teorica",
            "Quantità controllata",
            "Prezzo d'Acquisto",
            "Fornitore"
        ])

        for line in self.line_ids:
            if line.product_id.seller_ids:
                info = line.product_id.seller_ids[0]
                cost = info.cost_price
                supplier = info.display_name
            else:
                cost = 0
                supplier = ''

            ws.append([
                line.product_id.default_code,
                line.product_id.name,
                line.theoretical_qty,
                line.product_qty,
                cost,
                supplier
            ])

        output = BytesIO()
        # Save the workbook to a file
        workbook.save(output)
        output.seek(0)

        return output.getvalue()
