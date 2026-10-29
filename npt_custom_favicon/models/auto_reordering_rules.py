from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template in templates:
            template._sync_reordering_rules()
        return templates

    def write(self, vals):
        res = super().write(vals)
        # Recheck rules when variant structure or purchasable flag changes
        tracked_fields = {'attribute_line_ids', 'product_variant_ids', 'purchase_ok'}
        if tracked_fields.intersection(vals.keys()):
            self._sync_reordering_rules()
        return res

    def _sync_reordering_rules(self):
        """ Ensure each variant has a reordering rule, 
            and remove rules for deleted variants """
        stock_location = self.env.ref('stock.stock_location_stock')
        Orderpoint = self.env['stock.warehouse.orderpoint']

        for template in self:
            # Keep rules only for purchasable variants
            for variant in template.product_variant_ids:
                domain = [
                    ('product_id', '=', variant.id),
                    ('location_id', '=', stock_location.id),
                ]
                existing_rules = Orderpoint.search(domain)
                if variant.purchase_ok:
                    if not existing_rules:
                        Orderpoint.create({
                            'product_id': variant.id,
                            'product_min_qty': 0,
                            'product_max_qty': 0,
                            'location_id': stock_location.id,
                        })
                elif existing_rules:
                    existing_rules.unlink()

            # Remove rules for variants that no longer exist
            all_variant_ids = template.product_variant_ids.ids
            orphan_rules = Orderpoint.search([
                ('location_id', '=', stock_location.id),
                ('product_id.product_tmpl_id', '=', template.id),
                ('product_id', 'not in', all_variant_ids)
            ])
            orphan_rules.unlink()

# from odoo import models, fields, api

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     @api.model_create_multi
#     def create(self, vals_list):
#         templates = super().create(vals_list)

#         stock_location = self.env.ref('stock.stock_location_stock')

#         for template in templates:
#             # Ensure variants are created
#             if not template.product_variant_ids:
#                 template._create_variant_ids()
#             for variant in template.product_variant_ids:
#                 # Avoid duplicate rules if they already exist
#                 if not self.env['stock.warehouse.orderpoint'].search([
#                     ('product_id', '=', variant.id),
#                     ('location_id', '=', stock_location.id)
#                 ], limit=1):
#                     self.env['stock.warehouse.orderpoint'].create({
#                         'product_id': variant.id,
#                         'product_min_qty': 0,
#                         'product_max_qty': 0,
#                         'location_id': stock_location.id,
#                     })
#         return templates




# from odoo import models, fields, api

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     @api.model_create_multi
#     def create(self, vals):
#         product_template = super().create(vals)

#         # Get default internal stock location
#         stock_location = self.env.ref('stock.stock_location_stock')

#         # Loop through all product variants
#         for variant in product_template.product_variant_ids:
#             self.env['stock.warehouse.orderpoint'].create({
#                 'product_id': variant.id,
#                 'product_min_qty': 0,
#                 'product_max_qty': 0,
#                 'location_id': stock_location.id,
#             })

#         return product_template




# from odoo import models, api


# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     @api.model
#     def create(self, vals):
#         product_template = super().create(vals)
#         product_template._create_reordering_rules_for_variants()
#         return product_template

#     def write(self, vals):
#         result = super().write(vals)
#         for template in self:
#             template._create_reordering_rules_for_variants()
#         return result

#     def _create_reordering_rules_for_variants(self):
#         warehouse = self.env['stock.warehouse'].search([], limit=1)
#         Orderpoint = self.env['stock.warehouse.orderpoint']

#         if not warehouse:
#             return  # Prevents crash if no warehouse configured

#         for template in self:
#             if template.type and template.type in ['product', 'consu']:
#                 for variant in template.product_variant_ids:
#                     if not variant:
#                         continue
#                     print("Checking domain type:", type([
#                         ('product_id', '=', variant.id), 
#                         ('warehouse_id', '=', warehouse.id)
#                     ]))     # Should print: <class 'list'>

#                     # *** Always use a list for domain search ***
#                     existing = Orderpoint.search([
#                         ('product_id', '=', variant.id),
#                         ('warehouse_id', '=', warehouse.id)
#                     ], limit=1)
#                     if not existing:
#                         Orderpoint.create({
#                             'product_id': variant.id,
#                             'product_min_qty': 0,
#                             'product_max_qty': 0,
#                             'qty_multiple': 1,
#                             'warehouse_id': warehouse.id,
#                             'location_id': warehouse.lot_stock_id.id,
#                         })


