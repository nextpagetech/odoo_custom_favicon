from odoo import models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_project(self):
        # Allow project/task creation for goods and combo as well
        lines = self.filtered(lambda l: l.product_id.service_tracking in (
            'task_global_project', 'task_in_project', 'project_only'
        ))
        return super(SaleOrderLine, lines)._timesheet_create_project()

    def _timesheet_create_task(self):
        # Allow task creation for goods and combo as well
        lines = self.filtered(lambda l: l.product_id.service_tracking in (
            'task_global_project', 'task_in_project'
        ))
        return super(SaleOrderLine, lines)._timesheet_create_task()
