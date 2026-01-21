from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_advance_settlement_wizard(self):
        self.ensure_one()

        if self.state != 'posted':
            return

        if self.amount_residual <= 0:
            return

        return {
            'name': 'Settle Advance',
            'type': 'ir.actions.act_window',
            'res_model': 'advance.settlement.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
            }
        }
