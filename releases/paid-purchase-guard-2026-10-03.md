# Paid purchase guard — activated 2026-10-03

Owner approved activation: «согласен делай». Applied17:20:30UTC/20:20:30Moscow to external https://shustrik-maps.com, WordPress VPS through WireGuard vpsadmin@10.66.66.1. Source dcae6512aa6ac8107969cfe09a1d63f03eadc85c, original guard logic760b38f unchanged. GitHub-first/main/upstream0:0; original dirty files preserved.

Exact source archive SHA25608672f2e113397e15e0d1d9c71e270e1431de5511c436f23a5b306768edd28fb matchedPC/VPS. Installed only `shustrik-purchase-paid-guard.php`, SHA256666940e505df36627c2c556f680f0a0e3e71a7515c68e994b3f8c6a460b2fbe6, own enabled option=true. No vendor/order/history/consent/payment configuration changes. Earlier apply refused before any writes because Windows Git archive used CRLF; folder attributes now pinLF and final archive revalidated. Working/archive logic was identical; runtime byte hash now matches the original tested LF file.

Preflight92PHP and deployed-file92PHP passed. Prior JS57 passed, unchanged JS path. Fresh CLI WP bootstrap on nonexistent order-received/0 route20:21:27: environment ready, state wrapped, one guard closure, existing funnel addon enabled. Did not invoke order callbacks. This confirms fresh hook wiring, not a real paid visitor/Google receipt.

Isolated guest cart/add/checkout/remove/empty sixHTTP200BYPASS passed20:22:29; no order/payment/customer data. Product20:22:32HTTP200BYPASS, approved title/meta/H1/canonical/CTA/peer links preserved, one gtag loader. WP/DB running/restart0; bindingWP127.0.0.1:8083/DBnohostbinding verified. Runtime degraded retained.

Persistent backup `/root/shustrik-paid-guard-20261003/` stores own source/admin/deploy and before/after states; original own file/option absent. Rollback `sudo python3 /root/shustrik-paid-guard-20261003/deploy.py --rollback`: checks exact own file hash and original absent state, deletes own option then only own file. Does not replay or modify order markers. Live rollback not executed.

Remaining: original paid marker-before-JS still loses events after network/JS failure; no automatic event without a later receipt visit, no repair of already marked pending orders; actual consent/payment sandbox/Google receipt not verified. Pinned SiteKit1.184.0/Woo11.1.2/classic theme/provider source hash; revalidate upgrades. Historical four missing orders not attributed. Storj/ExpressCheckout decisions unchanged.
