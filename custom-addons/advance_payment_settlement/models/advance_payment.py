from odoo import api, fields, models
from odoo.exceptions import UserError


class AdvancePayment(models.Model):
    _name = 'advance.payment'
    _description = 'Advance Payment (Customer / Vendor)'
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Advance Number',
        required=True,
        copy=False,
        readonly=True,
        default= 'New'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True
    )

    partner_type = fields.Selection(
        [
            ('customer', 'Customer'),
            ('vendor', 'Vendor'),
        ],
        string='Type',
        required=True,
    )

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        required=True
    )

    amount = fields.Float(
        string='Advance Amount',
        required=True,
    )

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        domain="[('type', 'in', ('bank', 'cash'))]",
        required=True
    )

    payment_method_id = fields.Many2one(
        'account.payment.method.line',
        string='Payment Method',
        required=True
    )

    move_id = fields.Many2one(
        'account.move',
        string='Accounting Entry',
        readonly=True,
        copy=False
    )

    # settled_amount = fields.Float(
    #     string='Settled Amount',
    #     compute='_compute_settlement',
    #     store=True
    # )
    #
    # balance_amount = fields.Float(
    #     string='Remaining Balance',
    #     compute='_compute_settlement',
    #     store=True
    # )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('settled', 'Settled'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
    )

    reference = fields.Char(string='Reference / Notes')

    # @api.depends('amount', 'move_id.line_ids.matched_debit_ids', 'move_id.line_ids.matched_credit_ids')
    # def _compute_settlement(self):
    #     for record in self:
    #         settled = 0.0
    #
    #         if record.move_id:
    #             for line in record.move_id.line_ids:
    #                 for partial in line.matched_debit_ids:
    #                     settled += partial.amount
    #                 for partial in line.matched_credit_ids:
    #                     settled += partial.amount
    #
    #         record.settled_amount = settled
    #         record.balance_amount = record.amount - settled
    #
    #         if record.state == 'posted' and record.balance_amount == 0:
    #             record.state = 'settled'

    def action_post(self):
        for record in self:
            if record.amount <= 0:
                raise UserError('Advance amount must be greater than zero.')

            if record.move_id:
                raise UserError('This advance is already posted.')

            move = record._create_account_move()
            move.action_post()

            record.move_id = move.id
            record.state = 'posted'

            if record.name == 'New':
                record.name = self.env['ir.sequence'].next_by_code(
                    'advance.payment'
                )

    def action_cancel(self):
        for record in self:
            if record.state == 'settled':
                raise UserError('You cannot cancel a settled advance.')

            if record.move_id and record.move_id.state == 'posted':
                record.move_id.button_cancel()

            record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            if record.move_id:
                raise UserError('Remove accounting entry before resetting to draft.')

            record.state = 'draft'


    def _create_account_move(self):
        self.ensure_one()

        company = self.env.company

        if self.partner_type == 'customer':
            advance_account = company.customer_advance_account_id
            counterpart_account = self.partner_id.property_account_receivable_id
        else:
            advance_account = company.vendor_advance_account_id
            counterpart_account = self.partner_id.property_account_payable_id

        if not advance_account:
            raise UserError('Advance account is not configured in company settings.')

        move_vals = {
            'move_type': 'entry',
            'date': self.date,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'ref': self.reference or self.name,
            'line_ids': [
                (0, 0, {
                    'name': 'Advance Payment',
                    'account_id': advance_account.id,
                    'debit': self.amount if self.partner_type == 'vendor' else 0.0,
                    'credit': self.amount if self.partner_type == 'customer' else 0.0,
                    'partner_id': self.partner_id.id,
                }),
                (0, 0, {
                    'name': 'Advance Payment',
                    'account_id': counterpart_account.id,
                    'credit': self.amount if self.partner_type == 'vendor' else 0.0,
                    'debit': self.amount if self.partner_type == 'customer' else 0.0,
                    'partner_id': self.partner_id.id,
                }),
            ],
        }

        return self.env['account.move'].create(move_vals)
