# -*- coding: utf-8 -*-
{
    'name': "custom_favicon",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,
    'license': 'LGPL-3',
    'author': "NPT",
    'website': "https://www.npt.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web','base', 'base_setup', 'auth_totp', 'website','hr_attendance', 'sale_timesheet', 'stock', 'product', 'crm','purchase','sale','maintenance','mail', 'mail_plugin','contacts', 'base_import', 'mrp', 'l10n_in','website_links',], #'point_of_sale','sms',

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
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
        # 'views/web_tour_replace.xml',
        # 'views/discuss_channel_demo_replace.xml',
        # 'views/mail_template_override.xml',
        'views/mail_compose_message_views.xml',
        'views/mail_plugin_login.xml',
        'views/remove_odoo_placeholder.xml',
        'views/res_users_views.xml',
        # 'views/mail_template_odoo.xml',
        # 'views/hide_sms_crm.xml',
        
    ],
    # only loaded in demonstration mode
    'assets':{
        'web.assets_backend': [
            'custom_favicon/static/src/css/hide_sale_preview.css',
            'custom_favicon/static/src/js/web_title_patch.js',
            'custom_favicon/static/src/js/dialog_patch.js',
            'custom_favicon/static/src/js/documentation_link_patch.js',
             "custom_favicon/static/src/import_data_content/import_data_content.xml",
             "custom_favicon/static/src/js/error_dialog_patch.js",
             "custom_favicon/static/src/xml/import_sidepanel_no_docs.xml",
             "custom_favicon/static/src/xml/import_action.xml",
        ],
        'web.assets_frontend': [
            'custom_favicon/static/src/image/pictures/favicon.ico',
            
        ],
    },
}
