# Missing ecommerce events — prepared preview, not deployed

Adds `view_item` on public product documents and `begin_checkout` on nonempty standard checkout documents. Uses the existing Site Kit `_googlesitekit.gtagEvent` wrapper; no new Google Tag, measurement ID, raw gtag fallback, consent command, cookies, storage, order hooks or purchase sender.

## Activation and compatibility

Both runtime files must be siblings directly in `wp-content/mu-plugins/`. PHP is inert unless the WordPress option `shustrik_ecommerce_funnel_enabled` is the boolean `true` (not the string `yes` or `1`). Nothing has been installed in that directory during preview.

Pinned to WooCommerce 11.1.2 / Site Kit 1.184.0. Other versions stop emission pending a new compatibility review. Also stops if the Site Kit provider begins supplying either missing event, conversion tracking is disabled, Analytics has no active/enqueued tag, or this is another hostname. Excludes admin, AJAX, REST, cron, feeds, all logged-in visitors, category/cart, order-pay and order-received endpoints. This logged-in exclusion is deliberately stricter than configurations that allow logged-in customers.

Site Kit's opt-out flags block the JavaScript. Existing Google consent behavior is inherited through the original tag pipeline; no grant is forced. Consent denial/acceptance in a real browser remains a release check. No promise of zero consent-mode cookieless pings is made.

One event per eligible document; no resend on Woo `updated_checkout`, repeated script execution or bfcache restoration. A full reload/new checkout document is a new entry. Missing wrapper stops after 20 attempts over at most 4.75 seconds. Third-party consent tools that remove the wrapper until late acceptance require fresh-page verification; this extension will not invent a consent API.

## Values and identifiers

Product: published catalogue ID/title/currency, quantity one, catalogue price when exact. Variable parents omit price/value until checkout rather than presenting a minimum as a selected price. Variations use the parent ID plus public `item_variant`, matching Site Kit. Checkout: catalogue data re-read by product ID, positive quantities, unit price from discounted Woo `line_total / quantity`; value excludes tax/shipping. Only public item fields are exported, never customer information, order IDs/keys, arbitrary cart fields or custom item names. More than 100 items or invalid values stop emission.

This does not change `add_to_cart`/`purchase` or repair purchase payment semantics. Existing purchase counts still need separate completeness validation.

## Checked 2026-10-03

- `node ecommerce-funnel/test-events.cjs`: 11 JavaScript checks passed, including once-only, opt-out, forbidden events and missing/delayed wrapper.
- PHP 8.3 in the existing WordPress container: lint passed; `test-gates.php` 17 request-eligibility checks passed.
- `preview.php` in a separate `/tmp/shustrik-ecommerce-preview-20261003/` directory: 12 checks passed; real public Earth ID 11517 / USD 32, synthetic discounted two-item quantity USD 60; custom fields excluded. No session/order/options/GA mutation. Preview evidence is in the canonical project Checks directory.
- Server/browser dispatch and Google collector receipt are NOT verified by these tests.

## Concrete release sequence (next step)

1. Fetch this exact commit on the release workspace. Recheck Site Kit/Woo versions, public emitters/loader count, enabled conversion tracking and original provider events. Confirm no other plugin emits these events. Do not change authentication, DNS, cookie configuration or Stripe.
2. Verify the exact target `/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/` and both destination files. Abort if either already exists. Save baseline public HTML, current option existence/type and hashes under a dated root-only release directory. Copy only the two runtime files, verify source/destination SHA256 and PHP lint; leave the option absent/disabled.
3. In a WordPress CLI helper guarded by exact host and expected source hashes, set only `shustrik_ecommerce_funnel_enabled` to boolean true. Invalidate eligible product HTML using the existing targeted cache procedure; checkout should already bypass cache. No broad restart or unrelated cache/configuration change.
4. Check Earth then category/empty cart/nonempty checkout with an isolated guest session, no order/payment. Verify one existing loader and provider, one `view_item` per product document, one `begin_checkout` per nonempty checkout document, no duplicate on Woo update. Check opt-out and existing consent states. Verify calls reaching GA4 through an available browser/collector observation method; mocked JavaScript alone does not close this check. Remove the test cart item.
5. If collector/consent behavior or duplicates fail, disable immediately; record the failure. If live QA passes, save exact commit/hashes/time and start a new measurement window. After GA processing, use the recovered read-only Data API to check that the two event rows appear; this aggregate is supplementary and does not prove every browser delivery.

## Rollback

Set only `shustrik_ecommerce_funnel_enabled` to boolean false (or delete it if it did not exist before release). Invalidate the same product cache scope: cached inline payloads may outlive the option switch. Remove only the two own runtime files after verifying their exact hashes and absence of a pre-existing version; retain backup/evidence. A stale HTML page may retain an old event until cache invalidation, so verify public HTML again. Do not touch Site Kit, Pinterest, payment tracking, tag IDs or unrelated options.

No production activation or rollback was executed in the preview step.
