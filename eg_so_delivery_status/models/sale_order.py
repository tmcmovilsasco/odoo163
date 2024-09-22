from odoo import models, fields, api, _

from datetime import datetime, date, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_status = fields.Char(string="Delivery Status", compute='_delivery_status')

    @api.onchange('picking_ids')
    @api.depends('picking_ids')
    def _delivery_statys(self):
        for order in self:
            if order.picking_ids.mapped('state'):
                status = order.picking_ids.mapped('state')
                res = all(ele == status[0] for ele in status)
                if res:
                    if status[0] == 'draft':
                        order.delivery_status = '🚚 Draft'
                    elif status[0] in ['waiting', 'confirmed']:
                        order.delivery_status = '🚚 Waiting'
                    elif status[0] in 'assigned':
                        order.delivery_status = '🚚 Ready To Ship'
                    elif status[0] in 'done':
                        order.delivery_status = '🚚 Delivered'
                    else:
                        order.delivery_status = '🚚 Cancelled'
                else:
                    if 'done' in status:
                        order.delivery_status = '🚚 Partially Delivered'
                    else:
                        order.delivery_status = '🚚 To Be Delivered'
            else:
                order.delivery_status = '🚚No Delivery Order'
