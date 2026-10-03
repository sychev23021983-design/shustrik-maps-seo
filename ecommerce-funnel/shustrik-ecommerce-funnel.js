(function (window, document) {
    'use strict';
    // A second execution, Woo AJAX update or bfcache restoration cannot emit twice.
    if (window.shustrikEcommerceFunnelStarted) return;
    window.shustrikEcommerceFunnelStarted = true;
    const config = window.shustrikEcommerceFunnel;
    if (!config || !['view_item', 'begin_checkout'].includes(config.event)
        || !config.data || !Array.isArray(config.data.items) || !config.data.items.length) return;
    let attempts = 0;
    function send() {
        // Site Kit's own opt-out flags take precedence. No alternate gtag/loader.
        if (Object.keys(window).some(key => key.startsWith('ga-disable-') && window[key] === true)) return;
        const kit = window._googlesitekit;
        if (kit && typeof kit.gtagEvent === 'function') {
            kit.gtagEvent(config.event, config.data);
            return;
        }
        if (++attempts < 20) window.setTimeout(send, 250);
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', send, {once: true});
    else send();
})(window, document);
