# -*- coding: utf-8 -*-
from odoo import http
from odoo import sql_db
from odoo.addons.web.controllers.database import Database as WebDatabase
from odoo.tools.misc import file_open
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.tools import config
from odoo.service import db as db_service
import re
from lxml import html


class NPTDatabase(WebDatabase):

    def _get_database_manager_brand_title(self, databases):
        default_title = (config.get("custom_favicon_default_brand_title") or "Company ERP").strip()
        dbname = http.request.db or (databases[0] if len(databases) == 1 else None)
        if not dbname:
            return default_title
        try:
            with sql_db.db_connect(dbname).cursor() as cr:
                cr.execute(
                    "SELECT value FROM ir_config_parameter WHERE key = %s",
                    ("custom_favicon.branding_app_title",),
                )
                row = cr.fetchone()
            brand_title = (row[0] if row and row[0] else "").strip()
            return brand_title or default_title
        except Exception:
            return default_title

    def _render_template(self, **d):
        d.setdefault('manage', True)
        d['insecure'] = config.verify_admin_password('admin')
        d['list_db'] = config['list_db']
        d['langs'] = db_service.exp_list_lang()
        d['countries'] = db_service.exp_list_countries()
        d['pattern'] = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = db_service.list_db_incompatible(d['databases'])
        except Exception:
            d['databases'] = [http.request.db] if http.request.db else []
        d['brand_title'] = self._get_database_manager_brand_title(d['databases'])

        templates = {}

        # Load custom and original QWeb HTML files
        templates['database_manager'] = self._read_file('npt_custom_favicon/static/src/public/database_manager.qweb.html')
        templates['master_input'] = self._read_file('web/static/src/public/database_manager.master_input.qweb.html')
        templates['create_form'] = self._read_file('web/static/src/public/database_manager.create_form.qweb.html')

        def load(template_name):
            fromstring = html.document_fromstring if template_name == 'database_manager' else html.fragment_fromstring
            return (fromstring(templates[template_name]), template_name)

        return qweb_render('database_manager', d, load)

    def _read_file(self, path):
        with file_open(path, 'r') as f:
            return f.read()
