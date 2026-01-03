from odoo import models, fields

class StockPickingExtraCharge(models.Model):
    _name = 'stock.picking.extra.charge'
    _description = 'Delivery Extra Charge'

    picking_id = fields.Many2one(
        'stock.picking',
        string='Picking',
        ondelete='cascade'
    )

    name = fields.Char(string="Description")
    amount = fields.Float(string="Amount")
