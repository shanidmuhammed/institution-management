from odoo import fields, models

class Stock_Picking(models.Model):
    _inherit = 'stock.picking'

    customer_reference = fields.Char(string='Customer Reference')

    approver_id = fields.Many2one(
        string='Approver',
        comodel_name='res.users',
        readonly=True
    )

    approvers = fields.Many2many(
        string='Backup Approvers',
        comodel_name='res.users',
        readonly=True
    )

    extra_charge_ids = fields.One2many(
        'stock.picking.extra.charge',
        'picking_id',
        string='Extra Charges'
    )