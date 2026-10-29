/** @odoo-module **/

import { session } from "@web/session";

function getBrandTitle() {
    const value = (session.custom_favicon_branding_app_title || "").trim();
    return value || "ERP BRo";
}

function normalizeUrl(url) {
    const value = (url || "").trim();
    if (!value) {
        return "";
    }
    if (
        value.startsWith("http://") ||
        value.startsWith("https://") ||
        value.startsWith("/")
    ) {
        return value;
    }
    return `https://${value}`;
}

function applyConfiguredFavicon() {
    const faviconDataUri = (session.custom_favicon_branding_favicon_data_uri || "").trim();
    const faviconUrl = normalizeUrl(session.custom_favicon_branding_favicon_url);
    const finalFavicon = faviconDataUri || faviconUrl;
    if (!finalFavicon) {
        return;
    }

    let iconLink = document.querySelector("link[rel='shortcut icon']");
    if (!iconLink) {
        iconLink = document.createElement("link");
        iconLink.setAttribute("rel", "shortcut icon");
        iconLink.setAttribute("type", "image/x-icon");
        document.head.appendChild(iconLink);
    }
    iconLink.setAttribute("href", finalFavicon);
}

function patchTitleWithBrandName() {
    const titleTag = document.querySelector("title");
    if (!titleTag) {
        return;
    }

    const brandTitle = getBrandTitle();
    const updateTitle = () => {
        if (!document.title || !document.title.trim()) {
            document.title = brandTitle;
            return;
        }
        if (document.title.includes("Odoo")) {
            document.title = document.title.replace(/Odoo/g, brandTitle);
        }
    };

    const observer = new MutationObserver(updateTitle);
    observer.observe(titleTag, { childList: true });
    updateTitle();
}

function applyBranding() {
    patchTitleWithBrandName();
    applyConfiguredFavicon();
}

if (document.readyState !== "loading") {
    applyBranding();
} else {
    document.addEventListener("DOMContentLoaded", applyBranding);
}
