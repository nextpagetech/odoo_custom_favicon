# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomFaviconDocsRedirect(http.Controller):
    @http.route("/custom_favicon/doc_redirect", type="http", auth="user")
    def custom_favicon_doc_redirect(self, **kwargs):
        url = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("custom_favicon.documentation_redirect_url", default="")
            .strip()
        )
        if not url:
            return request.make_response(
                "",
                headers=[("Content-Type", "text/plain; charset=utf-8")],
                status=204,
            )
        if not (url.startswith("http://") or url.startswith("https://")):
            url = f"https://{url}"
        return request.redirect(url, code=302)

