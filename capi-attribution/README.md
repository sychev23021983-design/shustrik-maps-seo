# Temporary callback attribution, owner continuation 2026-10-04

The prior profiler expired at00:00UTC and retained five slow synchronous Pinterest
calls after the PageVisit/ViewCategory queue release. Static vendor source maps
AddToCart to woocommerce_add_to_cart and Checkout to woocommerce_before_thankyou;
the route /checkout alone cannot distinguish a receipt from ordinary checkout.

This bounded diagnostic observes WP HTTP callbacks without changing them.
It derives the event class from an IGNORE_ARGS backtrace and a fixed five-name
allowlist, not request payload/body, cookies, credentials or order data. It logs
only UTC, generic route, total time, callback, blocking flag, milliseconds/error
boolean and incomplete-call count. No URL/path/query values, IP, user/order/event
IDs, response text or payload is read/exported. A transient URL hash pairs hooks,
never persisted. Consumer CLI is excluded. Unknown callback remains `other`.

Auto-cutoff 2026-10-04 12:00UTC/15:00Moscow; approximately256KiB protected private
log cap. /tmp/shustrik-capi-attribution is0700 and log0600. No network request is
created by the instrument; completion hooks do not see libraries bypassing WP
HTTP APIs. First validate source lint, exact archive hash, synthetic privacy
shape if needed, live guest cart/checkout without submitting orders, cleanup.

Deploy exact pushed Git archive to /root/shustrik-capi-attribution-20261004/.
--preview requires absent own target/backup; --apply installs only own MU file,
retaining absence/hash backup. No database settings, scheduler or payment behavior
changes, no service restart. Existing expired profiler and logs retained.

Rollback: sudo python3 /root/shustrik-capi-attribution-20261004/deploy.py --rollback
It archives only its own file after hash guard, retains logs and source. Auto
cutoff stops instrumentation even if file remains; do not extend without a new
scope/review. Do not infer historical event identity solely from timing.
