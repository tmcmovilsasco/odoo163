from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_image = fields.Image(string="Product Image", related="product_id.image_128")