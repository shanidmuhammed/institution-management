from odoo import models, fields

class SaleOrderExtraCharge(models.Model):
    _name = 'sale.order.extra.charge'
    _description = 'Sale Order Extra Charge'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        ondelete='cascade'
    )

    move_id = fields.Many2one(
        'account.move',
        string='Invoice',
        ondelete='cascade'
    )

    name = fields.Char(string="Description", required=True)
    amount = fields.Float(string="Amount")
