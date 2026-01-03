from odoo import fields, models

class Account_Move(models.Model):
    _inherit = 'account.move'

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
        'account.move.extra.charge',
        'move_id',
        string='Extra Charges'
    )