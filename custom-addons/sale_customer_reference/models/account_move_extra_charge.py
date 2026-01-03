from odoo import models, fields

class AccountMoveExtraCharge(models.Model):
    _name = 'account.move.extra.charge'
    _description = 'Invoice Extra Charge'

    move_id = fields.Many2one(
        'account.move',
        string='Invoice',
        ondelete='cascade'
    )

    name = fields.Char(string="Description")
    amount = fields.Float(string="Amount")
