# -*- coding: utf-8 -*-
{
    'name': 'Custom Favicon & Branding',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Customize browser title, favicon, PWA icon and key Odoo branding touchpoints.',
    'description': """
Custom Favicon & Branding lets administrators configure the browser-facing identity
of Odoo 18, including the application title, favicon, PWA icon, brand promotion
logo and documentation redirect URL.

This package also contains broader active UI/debranding, mail/onboarding, settings,
inventory reordering and sales-timesheet customizations. Review the complete scope
before production deployment.
    """,
    'author': 'Next Page Technologies Pvt Ltd',
    'website': 'https://nextpagetechnologies.com',
    'license': 'LGPL-3',
    'price': 10.0,
    'currency': 'USD',

    'depends': [
        'web',
        'base',
        'base_setup',
        'auth_totp',
        'website',
        'hr_attendance',
        'sale_timesheet',
        'stock',
        'product',
        'crm',
        'purchase',
        'sale',
        'maintenance',
        'mail',
        'mail_plugin',
        'contacts',
        'base_import',
        'mrp',
        'l10n_in',
        'website_links',
    ],

    'data': [
        'data/module_branding.xml',
        'data/mail_group_replace.xml',
        'views/title_bar_favicon.xml',
        'views/offline_page_branding.xml',
        'views/brand_promotion_message.xml',
        'views/res_config_settings_view_inherit.xml',
        'views/remove_upgrade_widget.xml',
        'views/remove_documentation_link.xml',
        'views/reorder.xml',
        'views/ir_module_override.xml',
        'views/go_to_apps.xml',
        'views/hide_odoo_meeting.xml',
        'views/res_users_password_view.xml',
        'views/product_template_inherit.xml',
        'views/remove_odoo_in_mail.xml',
        'views/welcome_message_replace.xml',
        'views/mail_plugin_login_inherit.xml',
        'views/odoobot_replace.xml',
        'views/mail_compose_message_views.xml',
        'views/mail_plugin_login.xml',
        'views/remove_odoo_placeholder.xml',
        'views/res_users_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'npt_custom_favicon/static/src/css/hide_sale_preview.css',
            'npt_custom_favicon/static/src/js/web_title_patch.js',
            'npt_custom_favicon/static/src/js/dialog_patch.js',
            'npt_custom_favicon/static/src/js/documentation_link_patch.js',
            'npt_custom_favicon/static/src/import_data_content/import_data_content.xml',
            'npt_custom_favicon/static/src/js/error_dialog_patch.js',
            'npt_custom_favicon/static/src/xml/import_sidepanel_no_docs.xml',
            'npt_custom_favicon/static/src/xml/import_action.xml',
        ],
    },

    'images': [
        'static/description/banner.png',
    ],

    'application': False,
    'installable': True,
    'auto_install': False,
}
