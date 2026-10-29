# custom_favicon: File-by-File Technical README

This document explains every source file in this module:
- What the file does (purpose)
- Where the behavior appears in UI (if any)
- How/when it is used
- Whether it is currently active in the module load path

`Active` means loaded by `__manifest__.py` (XML/assets) or imported by Python `__init__.py`.

## Root

### `__init__.py` (`Active`)
- Purpose: Initializes module packages.
- UI location: None directly.
- Use: Imports `controllers` and `models` so Odoo loads Python overrides.

### `__manifest__.py` (`Active`)
- Purpose: Declares module metadata, dependencies, data files, and assets.
- UI location: None directly.
- Use: Controls which XML/QWeb/CSS/JS files are actually loaded at install/upgrade.

## Controllers

### `controllers/__init__.py` (`Active`)
- Purpose: Controller package initializer.
- UI location: None directly.
- Use: Imports `database.py`.

### `controllers/database.py` (`Active`)
- Purpose: Overrides web database manager template rendering with custom branded template pieces.
- UI location: Database manager page (`/web/database/manager` and related DB pages).
- Use: Replaces default visual/content on DB manager, reads custom QWeb HTML and core partials.

## Data

### `data/mail_group_replace.xml` (`Active`)
- Purpose: Renames mail notification group label to Company branding.
- UI location: Settings > Users/Groups where this group label is shown.
- Use: Updates `mail.group_mail_notification_type_inbox`.

## Models

### `models/__init__.py` (`Active`)
- Purpose: Loads model extension files.
- UI location: None directly.
- Use: Imports all active Python overrides. `add_ship_warn.py` is present but intentionally not imported.

### `models/add_ship_warn.py` (`Inactive`)
- Purpose: Adds carrier overweight warning on Sales Order carrier change.
- UI location: Sales Order form when choosing shipping method.
- Use: Not effective currently because it is not imported in `models/__init__.py`.

### `models/auto_reordering_rules.py` (`Active`)
- Purpose: Auto-manages reordering rules for product variants.
- UI location: Indirectly affects Inventory reordering behavior.
- Use: On product template create/write, creates/removes `stock.warehouse.orderpoint` rules per variant.

### `models/hide_odoo_in_chat.py` (`Active`)
- Purpose: Rebrands OdooBot onboarding message text and status label.
- UI location: Discuss chat onboarding for new users.
- Use: Overrides `_init_odoobot()` and `odoobot_state` label.

### `models/ir_http.py` (`Active`)
- Purpose: Adds custom documentation redirect setting into session payload.
- UI location: None directly; consumed by frontend JS.
- Use: Injects `custom_favicon_documentation_redirect_url` in `session_info()` and frontend session info.

### `models/ir_mail_server.py` (`Active`)
- Purpose: Rebrands fallback/test sender logic for outgoing mail server.
- UI location: Technical mail server test flows.
- Use: Overrides `_get_test_email_from()` to prefer branded fallback addresses.

### `models/mail_alias.py` (`Active`)
- Purpose: Rebrands help text of `mail.alias` fields.
- UI location: Technical mail alias forms.
- Use: Overrides field help messages only.

### `models/mail_alias_domain.py` (`Active`)
- Purpose: Rebrands help text for alias domain name field.
- UI location: Technical mail alias domain form.
- Use: Overrides field help message only.

### `models/mail_gateway_allowed.py` (`Active`)
- Purpose: Rebrands empty-list help HTML for allowed mail gateway addresses.
- UI location: Settings area for allowed gateway addresses.
- Use: Overrides `get_empty_list_help()` with custom message and thresholds.

### `models/mail_mail.py` (`Active`)
- Purpose: Rebrands help text for `mail.mail.auto_delete`.
- UI location: Technical email forms.
- Use: Field help text override.

### `models/mail_onboarding_cleanup.py` (`Active`)
- Purpose: Disables OdooBot onboarding and clears initial unread noise.
- UI location: Discuss app initial experience for users.
- Use: Overrides `_init_odoobot()`, removes default welcome message, marks default channel/bot chat as read.

### `models/mail_push_device.py` (`Active`)
- Purpose: Rebrands help for push notification browser keys.
- UI location: Technical push device records.
- Use: Help text override for `keys` field.

### `models/mail_template.py` (`Active`)
- Purpose: Sets default `auto_delete=True` and branded help for mail templates.
- UI location: Technical > Email > Templates.
- Use: Changes default behavior for email record cleanup.

### `models/orderpoint_override.py` (`Active`)
- Purpose: Prevents duplicate reordering rules and prefills values from existing rule.
- UI location: Inventory > Reordering Rules forms.
- Use: Onchange and create override on `stock.warehouse.orderpoint`.

### `models/removed_odoo_handle.py` (`Active`)
- Purpose: Rebrands `res.users` notification labels/help and bot status field labels.
- UI location: User preferences/security/help text contexts.
- Use: Model/field textual rebranding. Contains wide imports and duplicated `Users` class declarations.

### `models/res_config_settings.py` (`Active`)
- Purpose: Adds/extends settings fields.
- UI location: Settings app (General Settings sections).
- Use: Adds `documentation_redirect_url` (`ir.config_parameter`) and reuses alias domain related field.

### `models/res_users.py` (`Active`)
- Purpose: Rebrands OdooBot onboarding chat message and state label.
- UI location: Discuss onboarding chat and user status labels.
- Use: Overrides `_init_odoobot()` similarly to `hide_odoo_in_chat.py`.

### `models/sale_order_line.py` (`Active`)
- Purpose: Allows timesheet project/task creation for lines based on service tracking flags.
- UI location: Sales orders linked to project/task generation.
- Use: Overrides `_timesheet_create_project()` and `_timesheet_create_task()`.

## Security

### `security/ir.model.access.csv` (`Inactive`)
- Purpose: Access rules declaration file.
- UI location: None directly.
- Use: Not currently loaded because manifest data list comments out security CSV.

## Static Assets

### `static/src/css/hide_sale_preview.css` (`Active`)
- Purpose: Hides sales no-content preview/sample quotation links.
- UI location: Sales screens showing empty-state helper cards.
- Use: Backend CSS in `web.assets_backend`.

### `static/src/image/pictures/favicon.ico` (`Active`)
- Purpose: Brand favicon.
- UI location: Browser tab icon (backend and frontend).
- Use: Referenced in web layout template and frontend asset bundle.

### `static/src/image/pictures/nextpage_logo.png` (`Passive`)
- Purpose: Logo used in custom DB manager page.
- UI location: Database manager page.
- Use: Referenced by `static/src/public/database_manager.qweb.html`.

### `static/src/import_data_content/import_data_content.xml` (`Active`)
- Purpose: Rebrands import screen header text.
- UI location: Import data wizard/list header area.
- Use: QWeb inheritance of `ImportDataContent`.

### `static/src/js/dialog_patch.js` (`Active`)
- Purpose: Rebrands dialog titles by replacing "Odoo" with "Company".
- UI location: Generic backend dialogs.
- Use: OWL patch on `Dialog` component.

### `static/src/js/documentation_link_patch.js` (`Active`)
- Purpose: Global documentation link redirect based on settings URL.
- UI location: Any backend location using `documentation_link` widget.
- Use: Patches `DocumentationLink.url` getter and redirects to configured URL when set.

### `static/src/js/error_dialog_patch.js` (`Active`)
- Purpose: Rebrands error dialog titles/messages.
- UI location: Error popups (RPC/client/network/warning).
- Use: Patches multiple error dialog classes and title inference.

### `static/src/js/hide_archive_actions.js` (`Inactive`)
- Purpose: Removes Archive/Unarchive actions for CRM leads in list/kanban.
- UI location: CRM Leads action menu.
- Use: Not loaded because it is not included in `web.assets_backend`.

### `static/src/js/web_title_patch.js` (`Active`)
- Purpose: Rebrands browser page title by replacing "Odoo".
- UI location: Browser tab title throughout backend.
- Use: Mutation observer on `<title>`.

### `static/src/public/database_manager.qweb.html` (`Active via controller`)
- Purpose: Full branded database manager HTML template.
- UI location: `/web/database/manager`, DB create/restore/backup/duplicate/delete modals.
- Use: Loaded by `controllers/database.py` as custom template source.

### `static/src/xml/import_action.xml` (`Active`)
- Purpose: Removes import action documentation link/help snippets.
- UI location: Import action/no-content panel.
- Use: QWeb extension of `ImportAction`.

### `static/src/xml/import_sidepanel_no_docs.xml` (`Active`)
- Purpose: Removes import sidepanel documentation link.
- UI location: Import side panel.
- Use: QWeb extension of `ImportDataSidepanel`.

## Views

### `views/brand_promotion_message.xml` (`Active`)
- Purpose: Replaces bottom brand promotion block with custom brand link/logo.
- UI location: Webclient branding area.
- Use: Inherits `web.brand_promotion_message`.

### `views/discuss_channel_demo_replace.xml` (`Inactive`)
- Purpose: Replaces demo discuss channel message body text with branded wording.
- UI location: Demo discuss content.
- Use: Not loaded by manifest currently.

### `views/go_to_apps.xml` (`Active`)
- Purpose: Renames tooltip/title of website frontend "go to backend apps" button.
- UI location: Website frontend top bar.
- Use: Inherits `website.layout`.

### `views/hide_odoo_meeting.xml` (`Active`)
- Purpose: Hides "Odoo meeting/video call location" button in calendar event forms.
- UI location: Calendar event form and quick-create modal.
- Use: Sets button invisible in inherited calendar views.

### `views/hide_sms_crm.xml` (`Inactive`)
- Purpose: Hides specific SMS action button in CRM lead form.
- UI location: CRM lead form.
- Use: Not loaded by manifest currently.

### `views/ir_module_override.xml` (`Active`)
- Purpose: Rebrands app/module marketplace links and buy/upgrade link targets.
- UI location: Apps module form and kanban cards.
- Use: Replaces/rewires links to custom website.

### `views/mail_compose_message_views.xml` (`Active`)
- Purpose: Rebrands placeholder for `reply_to` in compose mail wizard.
- UI location: Email composer dialog.
- Use: Inherits `mail.email_compose_message_wizard_form`.

### `views/mail_plugin_login.xml` (`Active`)
- Purpose: Rebrands mail plugin OAuth/app-auth confirmation sentence.
- UI location: Mail plugin auth screen.
- Use: Inherits `mail_plugin.app_auth`.

### `views/mail_plugin_login_inherit.xml` (`Active`)
- Purpose: Same rebranding as `mail_plugin_login.xml` with alternate xpath.
- UI location: Mail plugin auth screen.
- Use: Also inherits `mail_plugin.app_auth`; potential overlap/duplication.

### `views/mail_template_odoo.xml` (`Inactive`)
- Purpose: Large HTML override of invite/set-password email with branding changes.
- UI location: Outgoing invitation email content.
- Use: Not loaded by manifest currently.

### `views/mail_template_override.xml` (`Active`)
- Purpose: Overrides `mail_template_test` body.
- UI location: Technical email template test output.
- Use: Sets a simple branded HTML body.

### `views/odoobot_replace.xml` (`Active`)
- Purpose: Renames base OdooBot partner record and image label semantics.
- UI location: Discuss bot identity/name.
- Use: Updates `base.partner_root` record values.

### `views/privacy_lookup_wizard_view.xml` (`Inactive`)
- Purpose: Defines a custom form view for `privacy.lookup.wizard`.
- UI location: Privacy lookup wizard popup/form.
- Use: Exists but not loaded by manifest.

### `views/product_template_inherit.xml` (`Active`)
- Purpose: Makes `service_tracking` visible on product template form.
- UI location: Product form.
- Use: Inherits `product.product_template_only_form_view`.

### `views/remove_documentation_link.xml` (`Active`)
- Purpose: Large set of settings view overrides replacing/removing documentation links and some help blocks.
- UI location: Settings across Base/Mail/Calendar/Website/Inventory/Sales/CRM/Purchase/MRP/Accounting/L10N/Timesheets.
- Use: Many `res.config.settings` inherited views with `documentation` attribute rewrites and content replacements.

### `views/remove_odoo_in_mail.xml` (`Inactive`)
- Purpose: Removes or changes "Powered by ErpBro" footer in mail notification layouts.
- UI location: Outgoing notification emails.
- Use: Not loaded by manifest currently.

### `views/remove_odoo_placeholder.xml` (`Active`)
- Purpose: Clears website placeholder text in company/partner/crm forms and website short-link input.
- UI location: Contacts, Companies, CRM lead forms, website short URL UI.
- Use: Multiple inherited form/template edits. Contains commented legacy duplicate block.

### `views/remove_upgrade_widget.xml` (`Active`)
- Purpose: Removes upgrade/install widget behavior from many settings module fields.
- UI location: Settings pages across multiple apps.
- Use: Clears `widget` attribute or replaces fields to suppress upgrade widget affordances.

### `views/reorder.xml` (`Active`)
- Purpose: Defines custom Reordering Rules tree/form views and action.
- UI location: Inventory > Reordering Rules action.
- Use: Custom list/form layout and domain for visible rules.

### `views/res_config_settings_view_inherit.xml` (`Active`)
- Purpose: Branded help/title text changes in multiple settings areas; adds documentation redirect setting; removes About section.
- UI location: General Settings, CRM, Accounting, Attendance settings.
- Use: Inherited settings views with text overrides and inserted `documentation_redirect_url` setting.

### `views/res_users_password_view.xml` (`Active`)
- Purpose: Shows plain text in change password wizard field by removing password masking attribute.
- UI location: Change password wizard user lines.
- Use: Inherited `change.password.user` tree view.

### `views/res_users_views.xml` (`Active`)
- Purpose: Removes 2FA documentation widgets and rebrands API key helper text.
- UI location: Users form > Account Security.
- Use: Inherited `auth_totp` and base users views.

### `views/title_bar_favicon.xml` (`Active`)
- Purpose: Replaces favicon and default page title expression.
- UI location: All backend pages rendered through `web.layout`.
- Use: Template inheritance of `web.layout`.

### `views/web_tour_replace.xml` (`Inactive`)
- Purpose: Changes discuss web tour URL to branded path.
- UI location: Web tour runtime.
- Use: Not loaded by manifest currently.

### `views/welcome_message_replace.xml` (`Active`)
- Purpose: Changes default install welcome message subject.
- UI location: Discuss `#general` welcome system message.
- Use: Overrides `mail.module_install_notification` message record.

## Notes and Maintenance Tips

- Several files are intentionally present but not loaded (`Inactive` above). Keep or remove based on roadmap.
- Some behaviors are duplicated across files (for example bot/message and plugin login branding) and may conflict depending on load order.
- `views/remove_documentation_link.xml` is broad and high-risk during upgrades because it inherits many cross-module settings nodes.
- `views/brand_promotion_message.xml` references `/custom_favicon/static/src/img/pictures/npt_logo.png`; verify that image path exists (current module tree uses `static/src/image/pictures/...`).
