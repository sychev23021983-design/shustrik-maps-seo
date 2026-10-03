# Paid purchase guard preview

Disabled by default. No production installation/activation is implied by this folder.

Wraps exactly one existing Site Kit WooCommerce `woocommerce_thankyou` closure in its original WP_Hook slot. Requires `is_paid()` and non-null `get_date_paid()`. Leaves vendor files, original valid-key/marker/WGAI checks, gtag, consent configuration and all other callbacks intact. Does not create an event sender, touch old order metadata, register a payment callback or replay purchases. Zero-value orders are not categorically excluded: WooCommerce must mark them paid with a date.

Guard applies only to guest order-received requests on the canonical site, Site Kit1.184.0/Woo11.1.2 and a classic theme. Closure source hash and exact priority10/arity1 are required. Drift/ambiguity leaves the original hook untouched and reports an in-memory state; this is fail-safe compatibility, not guaranteed unpaid suppression after an upgrade. Revalidate on upgrades. Block theme is deliberately outside scope because its footer purchase path must also be guarded.

Test: CLI `test-installed.php` uses actual WP_Hook and the installed provider's real register_hooks closure/method. All order access and saves are in-memory stubs. Run only from an isolated CLI process; no actual orders, client fields or Google requests. Node test runs installed JS with a local collector. No real-browser/payment-sandbox or Google receipt claim.

Acceptance: unpaid states produce no inline/marker; completed/processing without payment date also produce none; dated paid states retain original payload; pending→paid can emit on a later thankyou render; reload/key/WGAI/dedup paths remain original. Network loss after a paid render still cannot recover due to the original Site Kit marker. This preview fixes paid gating only.

Activation, if separately undertaken, must use an exact pushed source archive, verified runtime versions/source/hook and backup of own file/option. Rollback restores/removes only this MU file and own option; no order metadata rollback/replay. Existing view_item/begin_checkout addon remains separate. No installer or HTTP route is provided by this preview.
