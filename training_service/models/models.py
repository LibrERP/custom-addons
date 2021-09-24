from odoo import api, fields, models  # noqa: F401


class TrainingService(models.Model):
    _name = 'training.service'
    _description = 'Main Training Service model'

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Client", required=True
    )
    description = fields.Text(string="Description", required=True)
    training_date = fields.Datetime(string="Date Start", required=True)
    training_date_end = fields.Datetime(string="Date End", required=False)

    meeting_type = fields.Selection(
        string="Meeting Type",
        selection=[
            ('on_site', 'On-site'),
            ('on_line', 'On-line'),
            ('by_phone', 'By Phone'),
            ('other', 'Other'),
        ],
        required=True,
    )
    contract = fields.Many2one(
        comodel_name="sale.order", string="Contract/Agreement", required=False
    )
    student_ids = fields.Many2many(comodel_name="res.partner", string="Students")
