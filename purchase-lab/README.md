# Isolated installed Site Kit purchase lab — 2026-10-03

Read-only CLI capture and local Node VM test, requested by the owner. Not an application release or a replacement tracking implementation. Does not create WooCommerce orders or call the Google collector.

`capture-installed.php` runs only under CLI on the guarded site. Namespace overrides intercept order lookup and inline registration. The order and persistence method are memory stubs. Actual installed `maybe_add_purchase_inline_script`, `get_formatted_order`, price/product formatters, conversion wrapper and WooCommerce JS are exercised. The synthetic product/item are unsaved; no customer getters, secrets or actual order IDs are used. `9000000001` is a synthetic transaction ID. WGAI ownership is overridden for a specific fixture; block hook sequencing is simulated, not a rendered block checkout test.

Captured Google Site Kit JS is Apache-2.0 third-party source, copyright Google LLC. Source: installed google-site-kit plugin, WooCommerce events provider and Conversion_Tracking.php. Exact runtime SHA256 values and capture time are in the fixture; nothing is loaded from the network by the test.

Run `node purchase-lab/test-installed.cjs`. Results distinguish passing harness assertions from unmet purchase acceptance criteria. The stubbed downstream collector models grant/denial/unknown and network loss; this is not evidence that the production site has such consent enforcement. Timers and jQuery are minimal stubs. No browser rendering, real payment callback, Google receipt or GA4 report-level deduplication is claimed.

Findings: the exercised method emits pending/failed/cancelled/on-hold synthetic payloads without a paid check; marker-before-JS prevents recovery after simulated denial, network loss or disabled JS. Correct paid synthetic USD15/items payload is observed. Classic reload is suppressed; wrapper throttling lasts 5ms, not durable transaction deduplication. No historical markers are reset and no purchase events replayed.

Production correction requires a paid-only trigger, a documented consent policy, one purchase owner, a retry/deduplication design and an isolated real-browser/payment-sandbox acceptance check. This lab installs no MU plugin, changes no options and adds no HTTP route. Rollback/deployment are not applicable to a QA-only commit; deployed source commits remain unchanged.
