from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    def _init_odoobot(self):
        """Skip onboarding bot and clear default chat unread counters."""
        self.ensure_one()
        self.sudo().odoobot_state = "disabled"
        self._remove_general_welcome_message()
        self._clear_default_discuss_unreads()
        return self.env["discuss.channel"]

    def _clear_default_discuss_unreads(self):
        self = self.sudo()
        general_channel = self.env.ref("mail.channel_all_employees", raise_if_not_found=False)
        odoobot_partner = self.env.ref("base.partner_root", raise_if_not_found=False)
        Message = self.env["mail.message"]
        Member = self.env["discuss.channel.member"]
        Channel = self.env["discuss.channel"]

        for user in self:
            if general_channel:
                member = Member.search([
                    ("channel_id", "=", general_channel.id),
                    ("partner_id", "=", user.partner_id.id),
                ], limit=1)
                if member and member.new_message_separator == 0:
                    last_general_message = Message.search([
                        ("model", "=", "discuss.channel"),
                        ("res_id", "=", general_channel.id),
                    ], order="id desc", limit=1)
                    if last_general_message:
                        member._mark_as_read(last_general_message.id, sync=False)

            if odoobot_partner:
                bot_chat = Channel.search([
                    ("channel_type", "=", "chat"),
                    ("channel_member_ids.partner_id", "in", [odoobot_partner.id]),
                    ("channel_member_ids.partner_id", "in", [user.partner_id.id]),
                ], limit=1)
                if bot_chat:
                    bot_member = Member.search([
                        ("channel_id", "=", bot_chat.id),
                        ("partner_id", "=", user.partner_id.id),
                    ], limit=1)
                    if bot_member and bot_member.new_message_separator == 0:
                        last_bot_message = Message.search([
                            ("model", "=", "discuss.channel"),
                            ("res_id", "=", bot_chat.id),
                        ], order="id desc", limit=1)
                    if last_bot_message:
                        bot_member._mark_as_read(last_bot_message.id, sync=False)

    def _remove_general_welcome_message(self):
        """Delete the default general channel welcome message so it never shows."""
        self = self.sudo()
        general_channel = self.env.ref("mail.channel_all_employees", raise_if_not_found=False)
        if not general_channel:
            return

        # Prefer the exact XML id, fallback on matching content.
        welcome_message = self.env.ref("mail.module_install_notification", raise_if_not_found=False)
        messages = self.env["mail.message"]
        if welcome_message and welcome_message.res_id == general_channel.id:
            messages |= welcome_message
        else:
            messages |= self.env["mail.message"].search([
                ("model", "=", "discuss.channel"),
                ("res_id", "=", general_channel.id),
                ("body", "ilike", "Welcome to the #general channel%"),
            ])

        if messages:
            messages.unlink()
