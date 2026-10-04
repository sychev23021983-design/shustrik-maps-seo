# AddToCart queue proposal — 2026-10-04

Status: tested proposal, NOT deployed; admission flag defaults to false.

Live attribution at 06:19:39 UTC confirmed blocking AddToCart: 1068.29 ms of
1388.07 ms total PHP request. The guest Earth purchase path reached checkout;
no order/payment was submitted and the cart was emptied afterwards.

Only two changes to the existing queue wrapper: the consumer also accepts
add_to_cart, and the producer admits AddToCart only when the new option
_shu_pin_add_to_cart_async_enabled is true. PageVisit/ViewCategory retain their
existing behavior; Checkout (thank-you receipt) and Search remain synchronous.
Original prepared event ID/time/data remain intact. No vendor files are edited.

PHP lint and 20 isolated checks passed on the target PHP runtime. These use
synthetic SDK/WordPress stubs and perform no outbound requests or DB writes.
They cover default-off, flag-on admission, deduplication, ID/time preservation,
drain with flag off, scheduling fallback, encrypted payloads, retry limits,
TTL cleanup, crawler guard and unchanged Checkout/Search. Actual API delivery
of queued AddToCart is not yet verified.

Release prerequisites: fresh GitHub-first/runtime checks; guard live own plugin
SHA256 185bdec33fee3c46691d44a766e47f80f90453de4b8b1c586dbb76f70053bb44,
Pinterest 1.4.27 and installed vendor source hashes; guarded backup of own file
and previous option state; verify shustrik-pinterest-views.timer and consumer
before enabling admission. The correctly named timer was active and service
Result=success / ExecMainStatus=0 during this diagnosis. Aggregate queue probe:
queued4611/delivered4608/retry0/expired0/terminal0/fallback0; two payloads,
oldest19s, one running/one pending. These are changing counters, not a promise.

Deployment implementation/activation is still required. After installing the
consumer-capable code with the new flag OFF, verify it, enable only this flag,
then check a guest AddToCart path, encrypted queue drainage and API delivery
aggregates without orders, payment, customer exports or historical replay.

Rollback first disables only the new AddToCart flag, returning new events to
original synchronous delivery. Keep the new consumer alive to drain existing
AddToCart payloads. Restore the old plugin only after payload count is zero and
there are no pending/in-progress actions in the isolated group. Restoring the
old consumer early would reject queued add_to_cart. Existing view queue stays
operational. Do not remove workers or inspect/export encrypted payloads.
