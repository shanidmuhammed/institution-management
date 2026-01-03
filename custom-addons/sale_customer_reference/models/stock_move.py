from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):

        vals = super(StockMove, self)._get_new_picking_values()

        if self.sale_line_id and self.sale_line_id.order_id:
            order = self.sale_line_id.order_id

            vals['customer_reference'] = order.customer_reference
            vals['approver_id'] = order.approver_id.id
            approver_ids_list = order.approvers.ids

            vals['approvers'] = [(6, 0, approver_ids_list)]
        return vals