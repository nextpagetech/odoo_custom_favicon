import base64
import binascii

from odoo import http
from odoo.addons.web.controllers.webmanifest import WebManifest
from odoo.http import request
from odoo.tools import image_process


class CustomFaviconWebManifest(WebManifest):

    def _get_service_worker_content(self):
        body = super()._get_service_worker_content()
        return body.replace('"odoo-sw-cache"', '"application-sw-cache-v2"')

    def _get_configured_pwa_icon_binary(self, params):
        pwa_icon_binary = params.get_param('custom_favicon.pwa_app_icon_binary', default='')
        if pwa_icon_binary:
            return pwa_icon_binary
        return params.get_param('custom_favicon.branding_favicon_binary', default='')

    def _get_webmanifest(self):
        manifest = super()._get_webmanifest()
        params = request.env['ir.config_parameter'].sudo()
        icon_binary = self._get_configured_pwa_icon_binary(params)
        if not icon_binary:
            return manifest

        version = (params.get_param('custom_favicon.pwa_icon_version', default='') or '').strip()
        suffix = f'?v={version}' if version else ''
        manifest['icons'] = [
            {
                'src': f'/custom_favicon/pwa/icon/{size}.png{suffix}',
                'sizes': f'{size}x{size}',
                'type': 'image/png',
            }
            for size in (192, 512)
        ]
        return manifest

    @http.route('/web/manifest.webmanifest', type='http', auth='public', methods=['GET'], readonly=True)
    def webmanifest(self):
        return request.make_json_response(self._get_webmanifest(), {
            'Content-Type': 'application/manifest+json'
        })

    @http.route('/custom_favicon/pwa/icon/<int:size>.png', type='http', auth='public', methods=['GET'], readonly=True)
    def custom_pwa_icon(self, size=192, **kwargs):
        if size not in (192, 512):
            size = 192

        params = request.env['ir.config_parameter'].sudo()
        icon_binary = self._get_configured_pwa_icon_binary(params)
        if not icon_binary:
            return request.redirect(f'/web/static/img/odoo-icon-{size}x{size}.png')

        try:
            image_data = base64.b64decode(icon_binary, validate=True)
        except (binascii.Error, ValueError):
            return request.redirect(f'/web/static/img/odoo-icon-{size}x{size}.png')

        try:
            resized = image_process(image_data, size=(size, size), expand=True)
        except Exception:
            return request.redirect(f'/web/static/img/odoo-icon-{size}x{size}.png')

        return request.make_response(resized, headers=[('Content-Type', 'image/png')])
