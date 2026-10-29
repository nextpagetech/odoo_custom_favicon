/** @odoo-module **/

/*
 * Hide "Archive" / "Unarchive" from the Action menu ONLY for CRM Leads.
 * - List view: override getStaticActionMenuItems() (the exact spot your core adds them).
 * - Kanban view: sanitize the final action menu items.
 * Odoo 18: patch(target, props) — no patch name arg.
 */

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";

// --- helpers ---
function isCrmLead(ctrl) {
    return ctrl?.model?.root?.resModel === "crm.lead";
}

function stripArchiveArray(items = []) {
    return items.filter((it) => {
        const s = (
            (it.key || "") + " " +
            (it.name || "") + " " +
            (it.label || "") + " " +
            (it.description || "")
        ).toLowerCase();
        return !(s.includes("archive") || s.includes("unarchive"));
    });
}

function stripArchiveBuckets(menu) {
    if (!menu) return menu;
    const out = { ...menu };
    if (Array.isArray(out.action)) out.action = stripArchiveArray(out.action);
    if (Array.isArray(out.other)) out.other = stripArchiveArray(out.other);
    if (Array.isArray(out.more)) out.more = stripArchiveArray(out.more);
    if (Array.isArray(out.print)) out.print = stripArchiveArray(out.print);
    return out;
}

// --- List: remove at source (getStaticActionMenuItems) ---
patch(ListController.prototype, {
    getStaticActionMenuItems() {
        const base = super.getStaticActionMenuItems(...arguments);
        if (!isCrmLead(this)) {
            return base;
        }
        // base is an object keyed by action id (archive, unarchive, export, ...)
        const cleaned = { ...base };
        delete cleaned.archive;
        delete cleaned.unarchive;
        return cleaned;
    },
});

// --- Kanban: sanitize the final combined menu (coverage for kanban) ---
patch(KanbanController.prototype, {
    async getActionMenuItems() {
        const items = await super.getActionMenuItems(...arguments);
        if (!isCrmLead(this)) {
            return items;
        }
        return stripArchiveBuckets(items);
    },
});
