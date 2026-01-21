from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    customer_advance_account_id = fields.Many2one(
        'account.account',
        string='Customer Advance Account'
    )

    vendor_advance_account_id = fields.Many2one(
        'account.account',
        string='Vendor Advance Account'
    )
