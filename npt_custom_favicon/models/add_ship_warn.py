from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('carrier_id')
    def _onchange_carrier_id(self):
        """Show a warning if order weight exceeds carrier max weight, but don't block the process."""
        if self.carrier_id and self.carrier_id.max_weight > 0:
            # calculate order total weight
            order_weight = sum(
                line.product_id.weight * line.product_uom_qty
                for line in self.order_line
                if line.product_id
            )
            # if overweight, show warning
            if order_weight > self.carrier_id.max_weight:
                return {
                    'warning': {
                        'title': "Overweight Warning",
                        'message': (
                            f"The total order weight ({order_weight}) exceeds "
                            f"the maximum allowed weight ({self.carrier_id.max_weight}) "
                            f"for {self.carrier_id.name}."
                        )
                    }
                }
