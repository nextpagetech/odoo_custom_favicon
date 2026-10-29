/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import {
    ErrorDialog,
    ClientErrorDialog,
    NetworkErrorDialog,
    RPCErrorDialog,
    WarningDialog,
    RedirectWarningDialog,
} from "@web/core/errors/error_dialogs";

function stripOdoo(value) {
    if (typeof value !== "string" || !value) {
        return value;
    }
    return value
        .replace(/\bOdoo\b/g, "")
        .replace(/\s{2,}/g, " ")
        .replace(/\s+([,.:;!?])/g, "$1")
        .trim();
}

function sanitizeErrorProps(props) {
    if (!props) {
        return;
    }
    for (const key of ["title", "message", "name", "traceback"]) {
        props[key] = stripOdoo(props[key]);
    }
    if (props.data && typeof props.data === "object") {
        props.data.message = stripOdoo(props.data.message);
        props.data.debug = stripOdoo(props.data.debug);
    }
}

patch(ErrorDialog, {
    title: "Error",
});

patch(ErrorDialog.prototype, {
    setup() {
        super.setup();
        sanitizeErrorProps(this.props);
    },
});

patch(ClientErrorDialog, {
    title: "Client Error",
});

patch(NetworkErrorDialog, {
    title: "Network Error",
});

patch(RPCErrorDialog.prototype, {
    inferTitle() {
        switch (this.props.type) {
            case "server":
                this.title = "Server Error";
                break;
            case "script":
                this.title = "Client Error";
                break;
            case "network":
                this.title = "Network Error";
                break;
            default:
                this.title = "Error";
        }
    },
    setup() {
        super.setup();
        sanitizeErrorProps(this.props);
        this.title = stripOdoo(this.title);
        this.traceback = stripOdoo(this.traceback);
    },
});

patch(WarningDialog.prototype, {
    inferTitle() {
        return stripOdoo(this.props.title || "Warning");
    },
    setup() {
        super.setup();
        this.title = stripOdoo(this.title);
        this.message = stripOdoo(this.message);
    },
});

patch(RedirectWarningDialog.prototype, {
    setup() {
        super.setup();
        this.title = stripOdoo(this.title);
        this.message = stripOdoo(this.message);
    },
});
