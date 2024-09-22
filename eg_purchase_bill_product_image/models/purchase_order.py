from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    print_product_image = fields.Boolean(string="Print Product Image")