from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    notification_type = fields.Selection(
        selection_add=[
            ("email_inbox", "Handle by Emails and Application Inbox"),
            ("whatsapp", "Handle by WhatsApp"),
        ],
        ondelete={
            "email_inbox": "set inbox",
            "whatsapp": "set default",
        },
    )

    odoobot_state = fields.Selection(
        [
            ("not_initialized", "Not initialized"),
            ("onboarding_emoji", "Onboarding emoji"),
            ("onboarding_attachement", "Onboarding attachment"),
            ("onboarding_command", "Onboarding command"),
            ("onboarding_ping", "Onboarding ping"),
            ("onboarding_canned", "Onboarding canned"),
            ("idle", "Idle"),
            ("disabled", "Disabled"),
        ],
        string="Bot Status",
        readonly=True,
        required=False,
    )
