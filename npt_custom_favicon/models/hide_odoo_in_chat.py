from odoo import models, fields, _
from markupsafe import Markup


class Users(models.Model):
    _inherit = 'res.users'

    odoobot_state = fields.Selection(
        [
            ('not_initialized', 'Not initialized'),
            ('onboarding_emoji', 'Onboarding emoji'),
            ('onboarding_attachement', 'Onboarding attachment'),
            ('onboarding_command', 'Onboarding command'),
            ('onboarding_ping', 'Onboarding ping'),
            ('onboarding_canned', 'Onboarding canned'),
            ('idle', 'Idle'),
            ('disabled', 'Disabled'),
        ],
        string="Bot Status",
        readonly=True
    )

    def _get_chat_brand_name(self):
        brand_name = (
            self.env['ir.config_parameter']
            .sudo()
            .get_param('custom_favicon.branding_app_title', default='')
            .strip()
        )
        return brand_name or 'ERP BRo'

    def _init_odoobot(self):
        self.ensure_one()
        odoobot_id = self.env['ir.model.data']._xmlid_to_res_id("base.partner_root")
        channel = self.env['discuss.channel'].channel_get([odoobot_id, self.partner_id.id])
        brand_name = self._get_chat_brand_name()

        message = Markup("%s<br/>%s<br/><b>%s</b> <span class=\"o_odoobot_command\">:)</span>") % (
            _("Hello,"),
            _(
                "The %s chat helps employees collaborate efficiently. "
                "I'm here to help you discover its features."
            ) % brand_name,
            _("Try to send me an emoji")
        )

        channel.sudo().message_post(
            author_id=odoobot_id,
            body=message,
            message_type="comment",
            silent=True,
            subtype_xmlid="mail.mt_comment",
        )
        self.sudo().odoobot_state = 'onboarding_emoji'
        return channel
