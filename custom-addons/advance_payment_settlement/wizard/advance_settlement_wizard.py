from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AdvanceSettlementWizard(models.TransientModel):
    _name = 'advance.settlement.wizard'
    _description = 'Advance Settlement Wizard'

    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice / Bill',
        required=True,
        readonly=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        related='invoice_id.partner_id',
        readonly=True
    )

    line_ids = fields.One2many(
        'advance.settlement.wizard.line',
        'wizard_id',
        string='Available Advances'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        invoice = self.env['account.move'].browse(
            self.env.context.get('active_id')
        )

        if not invoice or invoice.state != 'posted':
            raise UserError(_("Invoice must be posted."))

        res['invoice_id'] = invoice.id

        advances = self.env['advance.payment'].search([
            ('partner_id', '=', invoice.partner_id.id),
            ('state', '=', 'posted'),
        ])

        lines = []
        for adv in advances:
            balance = adv.amount  # temporary, will improve later

            if balance > 0:
                lines.append((0, 0, {
                    'advance_id': adv.id,
                    'available_balance': balance,
                    'settle_amount': 0.0,
                }))

        res['line_ids'] = lines
        return res


class AdvanceSettlementWizardLine(models.TransientModel):
    _name = 'advance.settlement.wizard.line'
    _description = 'Advance Settlement Wizard Line'

    wizard_id = fields.Many2one(
        'advance.settlement.wizard',
        required=True,
        ondelete='cascade'
    )

    advance_id = fields.Many2one(
        'advance.payment',
        string='Advance',
        required=True,
        readonly=True
    )

    available_balance = fields.Float(
        string='Available Balance',
        readonly=True
    )

    settle_amount = fields.Float(
        string='Settle Amount'
    )
