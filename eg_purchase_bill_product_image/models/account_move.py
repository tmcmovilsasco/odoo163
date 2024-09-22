from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    print_bill_product_image = fields.Boolean(string="Print Product Image")