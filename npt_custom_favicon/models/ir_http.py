import mimetypes

from odoo import models


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def _get_branding_favicon_data_uri(self, params):
        favicon_binary = params.get_param('custom_favicon.branding_favicon_binary', default='')
        if not favicon_binary:
            return ''
        favicon_filename = params.get_param('custom_favicon.branding_favicon_filename', default='favicon.ico')
        mimetype, _ = mimetypes.guess_type(favicon_filename or '')
        return f"data:{mimetype or 'image/x-icon'};base64,{favicon_binary}"

    def session_info(self):
        info = super().session_info()
        params = self.env['ir.config_parameter'].sudo()
        info['custom_favicon_documentation_redirect_url'] = (
            params.get_param('custom_favicon.documentation_redirect_url', default='')
        )
        info['custom_favicon_branding_app_title'] = (
            params.get_param('custom_favicon.branding_app_title', default='')
        )
        info['custom_favicon_branding_favicon_data_uri'] = self._get_branding_favicon_data_uri(params)
        info['custom_favicon_branding_favicon_url'] = (
            params.get_param('custom_favicon.branding_favicon_url', default='')
        )
        return info

    def get_frontend_session_info(self):
        info = super().get_frontend_session_info()
        params = self.env['ir.config_parameter'].sudo()
        info['custom_favicon_documentation_redirect_url'] = (
            params.get_param('custom_favicon.documentation_redirect_url', default='')
        )
        info['custom_favicon_branding_app_title'] = (
            params.get_param('custom_favicon.branding_app_title', default='')
        )
        info['custom_favicon_branding_favicon_data_uri'] = self._get_branding_favicon_data_uri(params)
        info['custom_favicon_branding_favicon_url'] = (
            params.get_param('custom_favicon.branding_favicon_url', default='')
        )
        return info
