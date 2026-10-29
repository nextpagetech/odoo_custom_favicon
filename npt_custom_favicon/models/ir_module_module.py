import re

from odoo import fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    branded_summary = fields.Char(
        string="Branded Summary",
        compute="_compute_branded_module_metadata",
    )
    branded_author = fields.Char(
        string="Branded Author",
        compute="_compute_branded_module_metadata",
    )

    def _replace_odoo_branding(self, value, *, default=""):
        text = (value or "").strip()
        if not text:
            return default
        return re.sub(r"\bOdoo\b", "ERPBRO", text, flags=re.IGNORECASE)

    def _compute_branded_module_metadata(self):
        for module in self:
            module.branded_summary = module._replace_odoo_branding(module.summary)
            module.branded_author = module._replace_odoo_branding(
                module.author,
                default="ERPBRO",
            )

    def action_open_custom_learn_more_url(self):
        self.ensure_one()
        url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("custom_favicon.documentation_redirect_url", default="")
            .strip()
        )
        if not url:
            return False
        if not (url.startswith("http://") or url.startswith("https://")):
            url = f"https://{url}"
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }
