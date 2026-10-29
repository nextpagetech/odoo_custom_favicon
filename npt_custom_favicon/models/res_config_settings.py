import mimetypes
import time

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Keep these project toggles available even when the merged Settings view
    # is parsed before the project module fields are present in the payload.
    module_hr_timesheet = fields.Boolean(string="Task Logs")
    group_project_rating = fields.Boolean(
        "Customer Ratings",
        implied_group='project.group_project_rating',
    )
    group_project_stages = fields.Boolean(
        "Project Stages",
        implied_group="project.group_project_stages",
    )
    group_project_recurring_tasks = fields.Boolean(
        "Recurring Tasks",
        implied_group="project.group_project_recurring_tasks",
        group='base.group_portal,base.group_user',
    )
    group_project_task_dependencies = fields.Boolean(
        "Task Dependencies",
        implied_group="project.group_project_task_dependencies",
    )
    group_project_milestone = fields.Boolean(
        'Milestones',
        implied_group='project.group_project_milestone',
        group='base.group_portal,base.group_user',
    )

    branding_app_title = fields.Char(
        string='Application Title',
        config_parameter='custom_favicon.branding_app_title',
        help='Brand name shown in browser titles. Used to replace dynamic page titles.',
    )
    branding_favicon = fields.Binary(
        string='Favicon',
        help='Upload a favicon file (.ico, .png, .svg). It will be used in browser tabs.',
    )
    branding_favicon_filename = fields.Char(
        string='Favicon Filename',
        help='Original favicon filename used to detect content type.',
    )
    branding_favicon_url = fields.Char(
        string='Legacy Favicon URL',
        config_parameter='custom_favicon.branding_favicon_url',
        help='Backward-compatible field for older views. Upload field is preferred.',
    )
    pwa_app_icon = fields.Binary(
        string='PWA App Icon',
        help='Icon used for browser install prompt and installed app shortcuts.',
    )
    pwa_app_icon_filename = fields.Char(
        string='PWA App Icon Filename',
        help='Original icon filename used for format detection.',
    )
    brand_promotion_logo = fields.Binary(
        string='Brand Promotion Logo',
        help='Logo shown in footer brand promotion. If empty, company logo is used.',
    )
    brand_promotion_logo_filename = fields.Char(
        string='Brand Promotion Logo Filename',
        help='Original logo filename used to detect content type.',
    )
    documentation_redirect_url = fields.Char(
        string='Documentation Redirect URL',
        config_parameter='custom_favicon.documentation_redirect_url',
        help='When set, documentation links in the backend open this URL.',
    )

    alias_domain_id = fields.Many2one(
        'mail.alias.domain', 
        string='Alias Domain',
        readonly=False, 
        related='company_id.alias_domain_id',
        help="If you have setup a catch-all email domain redirected to the Company server, enter the domain name here."
    )

    def get_values(self):
        values = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        values.update({
            'branding_favicon': params.get_param('custom_favicon.branding_favicon_binary', default=''),
            'branding_favicon_filename': params.get_param('custom_favicon.branding_favicon_filename', default='favicon.ico'),
            'pwa_app_icon': params.get_param('custom_favicon.pwa_app_icon_binary', default=''),
            'pwa_app_icon_filename': params.get_param('custom_favicon.pwa_app_icon_filename', default=''),
            'brand_promotion_logo': params.get_param('custom_favicon.brand_promotion_logo_binary', default=''),
            'brand_promotion_logo_filename': params.get_param('custom_favicon.brand_promotion_logo_filename', default=''),
        })
        return values

    @api.model
    def _get_brand_name(self):
        brand_name = (
            self.env['ir.config_parameter']
            .sudo()
            .get_param('custom_favicon.branding_app_title', default='')
            .strip()
        )
        return brand_name or 'Company ERP'

    @api.model
    def sync_welcome_message_subject(self):
        welcome_message = self.env.ref('mail.module_install_notification', raise_if_not_found=False)
        if not welcome_message or welcome_message._name != 'mail.message':
            return False
        welcome_message.sudo().write({
            'subject': f"Welcome to {self._get_brand_name()}!",
        })
        return True

    def set_values(self):
        super().set_values()
        params = self.env['ir.config_parameter'].sudo()
        old_branding_favicon_binary = params.get_param('custom_favicon.branding_favicon_binary', default='')
        old_branding_favicon_filename = params.get_param('custom_favicon.branding_favicon_filename', default='')
        old_pwa_icon_binary = params.get_param('custom_favicon.pwa_app_icon_binary', default='')
        old_pwa_icon_filename = params.get_param('custom_favicon.pwa_app_icon_filename', default='')

        favicon_binary = (self.branding_favicon or '').strip() or False
        favicon_filename = (self.branding_favicon_filename or '').strip()
        if favicon_binary and not favicon_filename:
            favicon_filename = 'favicon.ico'
        params.set_param('custom_favicon.branding_favicon_binary', favicon_binary)
        params.set_param('custom_favicon.branding_favicon_filename', favicon_filename or False)

        pwa_icon_binary = (self.pwa_app_icon or '').strip() or False
        pwa_icon_filename = (self.pwa_app_icon_filename or '').strip()
        if pwa_icon_binary and not pwa_icon_filename:
            pwa_icon_filename = 'pwa-icon.png'
        params.set_param('custom_favicon.pwa_app_icon_binary', pwa_icon_binary)
        params.set_param('custom_favicon.pwa_app_icon_filename', pwa_icon_filename or False)

        if (
            old_branding_favicon_binary != (favicon_binary or '')
            or old_branding_favicon_filename != (favicon_filename or '')
            or old_pwa_icon_binary != (pwa_icon_binary or '')
            or old_pwa_icon_filename != (pwa_icon_filename or '')
        ):
            params.set_param('custom_favicon.pwa_icon_version', str(int(time.time())))

        brand_logo_binary = (self.brand_promotion_logo or '').strip() or False
        brand_logo_filename = (self.brand_promotion_logo_filename or '').strip()
        brand_logo_mimetype, _ = mimetypes.guess_type(brand_logo_filename or '')
        params.set_param('custom_favicon.brand_promotion_logo_binary', brand_logo_binary)
        params.set_param('custom_favicon.brand_promotion_logo_filename', brand_logo_filename or False)
        params.set_param('custom_favicon.brand_promotion_logo_mimetype', brand_logo_mimetype or 'image/png')
        self.sync_welcome_message_subject()
