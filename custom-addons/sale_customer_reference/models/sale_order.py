from odoo import fields, models

class Sale_Order(models.Model):
    _inherit = 'sale.order'

    customer_reference = fields.Char(string='Customer Ref.')

    approver_id = fields.Many2one(
        string='Approver',
        comodel_name='res.users',
    )

    approvers = fields.Many2many(
        string='Backup Approvers',
        comodel_name='res.users'
    )

    extra_charge_ids = fields.One2many(
        'sale.order.extra.charge',
        'sale_order_id',
        string='Extra Charges'
    )

    def _prepare_invoice(self):
        invoice_vals = super(Sale_Order, self)._prepare_invoice()

        invoice_vals['customer_reference'] = self.customer_reference
        invoice_vals['approver_id'] = self.approver_id.id
        invoice_vals['approvers'] = [(6, 0, self.approvers.ids)]

        extra_charge_vals = []
        for line in self.extra_charge_ids:
            extra_charge_vals.append((0, 0, {
                'name': line.name,
                'amount': line.amount,
            }))

        invoice_vals['extra_charge_ids'] = extra_charge_vals
        return invoice_vals

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            for picking in order.picking_ids:
                picking.extra_charge_ids = [
                    (0, 0, {
                        'name': line.name,
                        'amount': line.amount,
                    }) for line in order.extra_charge_ids
                ]

        return res