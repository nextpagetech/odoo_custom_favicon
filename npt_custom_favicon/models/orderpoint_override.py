from odoo import api, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.onchange("product_id", "location_id")
    def _onchange_product_location_prefill(self):
        """When selecting a product/location, prefill values from the existing rule."""
        if self.product_id and self.location_id:
            existing = self.search(
                [
                    ("product_id", "=", self.product_id.id),
                    ("location_id", "=", self.location_id.id),
                    ("company_id", "=", self.company_id.id),
                ],
                limit=1,
            )
            if existing:
                self.product_min_qty = existing.product_min_qty
                self.product_max_qty = existing.product_max_qty
                self.qty_multiple = existing.qty_multiple
                self.warehouse_id = existing.warehouse_id.id

    @api.model_create_multi
    def create(self, vals_list):
        """Prevent duplicate rules per product/location by updating the existing one."""
        records = self.env[self._name]
        to_create = []

        for vals in vals_list:
            product_id = vals.get("product_id")
            location_id = vals.get("location_id")
            company_id = vals.get("company_id") or self.env.company.id
            if product_id and location_id:
                existing = self.search(
                    [
                        ("product_id", "=", product_id),
                        ("location_id", "=", location_id),
                        ("company_id", "=", company_id),
                    ],
                    limit=1,
                )
                if existing:
                    existing.write(vals)
                    records |= existing
                    continue
            to_create.append(vals)

        if to_create:
            records |= super().create(to_create)

        return records
