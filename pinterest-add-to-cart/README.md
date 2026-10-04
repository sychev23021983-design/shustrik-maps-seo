# Pinterest AddToCart release 2026-10-04

Owner approved queue fix and channel sales assessment. Extends the existing
own MU wrapper; no vendor, checkout payment or theme changes. Preserves original
prepared event identity/time, encrypted storage, retry/deduplication/fallback.
Checkout/Search stay synchronous. New admission flag defaults off; consumer
accepts add_to_cart irrespective of flag, enabling safe drain. New aggregate
queued_add_to_cart/delivered_add_to_cart counters contain no customer fields.

Deploy exactly the pushed archive to /root/shustrik-pinterest-cart-20261004.
Run deploy.py --preview, then --apply (cart flag remains off), verify consumer,
then --enable. PHP lint/20 synthetic tests and live source-version guards run
before install. Existing views consumer timer/service must already be healthy.
Guest live QA: one cart path to checkout, no order/payment, remove test item;
check cart counters queued/delivered, fallback/terminal/retry and HTTP timing.
The delivered counter means the installed SDK returned non-failed event status;
it does not prove Pinterest advertising attribution or dashboard visibility.

Rollback: sudo python3 /root/shustrik-pinterest-cart-20261004/deploy.py --rollback
Only new cart admission is disabled; views stay queued. Keep the installed
consumer to drain carts. --restore-old refuses until no encrypted payloads and
no pending/in-progress group jobs. Backup is previous-plugin.php + backup.json;
original plugin was 185bdec33fee3c46691d44a766e47f80f90453de4b8b1c586dbb76f70053bb44.
Do not use the older views package rollback for this release. No historical
replay, no orders, no payload/customer IDs exported, no container restart.
