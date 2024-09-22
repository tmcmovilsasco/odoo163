from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    bill_product_image = fields.Image(string="Product Image", related="product_id.image_128")