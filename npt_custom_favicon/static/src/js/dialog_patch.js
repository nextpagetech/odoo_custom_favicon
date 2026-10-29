/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Dialog } from "@web/core/dialog/dialog";
import { session } from "@web/session";

function getBrandTitle() {
    const value = (session.custom_favicon_branding_app_title || "").trim();
    return value || "ERP BRo";
}

function stripOdooWord(value) {
    if (typeof value !== "string") {
        return value;
    }
    return value
        .replace(/\bOdoo\b/g, "")
        .replace(/\s{2,}/g, " ")
        .replace(/\s+([,.:;!?])/g, "$1")
        .trim();
}

patch(Dialog.prototype, {
    setup() {
        const brandTitle = getBrandTitle();
        if (typeof this.props.title === "string" && this.props.title.includes("Odoo")) {
            const isErrorDialog =
                typeof this.props.contentClass === "string" &&
                this.props.contentClass.includes("o_error_dialog");
            this.props.title = isErrorDialog
                ? stripOdooWord(this.props.title)
                : this.props.title.replace(/Odoo/g, brandTitle);
        }
        super.setup?.();
    },
});
