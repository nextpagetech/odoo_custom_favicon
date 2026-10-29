/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { DocumentationLink } from "@web/views/widgets/documentation_link/documentation_link";

function normalizeUrl(url) {
    const value = (url || "").trim();
    if (!value) {
        return "";
    }
    if (value.startsWith("http://") || value.startsWith("https://")) {
        return value;
    }
    return `https://${value}`;
}

function getRedirectUrl() {
    return normalizeUrl(session.custom_favicon_documentation_redirect_url);
}

function getRedirectHost() {
    const redirectUrl = getRedirectUrl();
    if (!redirectUrl) {
        return "";
    }
    try {
        return (new URL(redirectUrl, window.location.origin).hostname || "").toLowerCase();
    } catch {
        return "";
    }
}

function isManagedDocumentationAnchor(anchor) {
    if (!anchor) {
        return false;
    }
    if (anchor.classList.contains("o_doc_link")) {
        return true;
    }
    const href = (anchor.getAttribute("href") || "").trim();
    if (!href || href.startsWith("#") || href.startsWith("javascript:")) {
        return false;
    }
    let parsed;
    try {
        parsed = new URL(href, window.location.origin);
    } catch {
        return false;
    }
    const host = (parsed.hostname || "").toLowerCase();
    const path = (parsed.pathname || "").toLowerCase();
    if (path.startsWith("/custom_favicon/doc_redirect")) {
        return true;
    }
    const redirectHost = getRedirectHost();
    if (redirectHost && (host === redirectHost || host.endsWith(`.${redirectHost}`))) {
        return true;
    }
    if (host.includes("odoo.com")) {
        return path.includes("/documentation") || path.includes("/page/tour");
    }
    return false;
}

function applyRedirectOrBlock(anchor, ev) {
    if (!isManagedDocumentationAnchor(anchor)) {
        return;
    }
    const redirectUrl = getRedirectUrl();
    if (!redirectUrl) {
        ev.preventDefault();
        ev.stopPropagation();
        return;
    }
    anchor.setAttribute("href", redirectUrl);
    anchor.setAttribute("target", "_blank");
    anchor.setAttribute("rel", "noopener noreferrer");
}

document.addEventListener(
    "click",
    (ev) => {
        const anchor = ev.target.closest("a");
        applyRedirectOrBlock(anchor, ev);
    },
    true
);

patch(DocumentationLink.prototype, {
    get url() {
        const redirectUrl = getRedirectUrl();
        if (redirectUrl) {
            return redirectUrl;
        }
        return "";
    },
});
