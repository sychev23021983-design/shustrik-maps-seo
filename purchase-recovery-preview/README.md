# Purchase recovery architecture preview

Executable isolated model, not an installable plugin. Run `node purchase-recovery-preview/test.cjs`. No network, WordPress hooks, payment callbacks, real orders, credentials or browser tracking are present. It does not change the active paid guard.

## Proposed ownership and boundaries

A future adapter would replace only Site Kit's purchase path for newly created orders after a release watermark. It must not run alongside the original purchase sender. Preserve Site Kit's other events and the existing gtag destination. Existing markers stay untouched; exclude all orders created before the release even if paid later. This intentionally sacrifices recovery of old orders to avoid historical replay. The release timestamp in this model is synthetic, not an activation date.

Authoritative paid eligibility is WooCommerce is_paid plus a non-null date_paid. Receipt access requires WooCommerce's valid order-key/ownership checks, guest scope and exact canonical target. Never expose an outbox by transaction ID alone. The model's access/paid booleans stand for these trusted adapter checks, not client claims.

The proposed database row contains a unique transaction ID, an allowlisted payload, expiry, attempt generation and status. Preparation is idempotent. Payload must be regenerated/validated against current authoritative payment data before dispatch; refunds/cancellations invalidate eligibility. No customer data, email, address, user_data, order keys, analytics cookies or client IDs are stored in this model. Product payload is intentionally minimal; production must preserve the validated Site Kit value/tax/shipping/discount format and destination without inventing values.

## State behavior

| Condition | Behavior |
|---|---|
| Unpaid, invalid access, old order or malformed payload | No row or event |
| Paid and eligible | Ready; no send until an authenticated browser is present |
| Unknown analytics consent, offline or missing tag | Wait without calling sender |
| Consent denied | Suppress permanently for this order, remove payload; later grant does not replay it |
| Granted consent and ready browser | Acquire one lease and recheck consent/access/payment just before dispatch |
| Offline/tag missing before dispatch | Release lease; future browser visit may retry |
| Sender called, throws, callback fires or lease times out | Await reconciliation; do not automatically resend |
| Matching processed GA4 transaction, property, currency and value | Observed; remove payload and block future sends |
| No processed report row | Remains unresolved; absence is not evidence of nondelivery |
| Ready row reaches proposed 72-hour retention | Expire and remove payload |

Thirty-second leases and 72-hour retention are proposed preview defaults, not an approved policy. Awaiting rows also need a production expiry/cleanup worker; this model has no scheduler. A future implementation needs database atomic insert/compare-and-swap locking across PHP requests. The Map guarantees only synchronous single-process model behavior; JSON rehydration tests state semantics, not durability or distributed concurrency.

## Recovery limits

Loss of JS before claiming leaves the row ready and allows an eligible receipt revisit. Loss after claiming is indistinguishable from a dispatched event, so it requires reconciliation. Delayed payment prepares eligibility without sending; if the browser never returns, browser-only recovery cannot deliver. A background Measurement Protocol sender would require a separate design for durable consent and attribution and is outside this preview.

Stable nonempty transaction_id is retained. Google documents web-stream purchase deduplication for repeated IDs, but this model does not prove Google processing or cross-user behavior. It uses conservative suppression of ambiguous retries rather than assuming exactly-once delivery. Callback means event command processing finished, not that processed revenue is present.

References checked 2026-10-10:

- [Google transaction ID deduplication](https://support.google.com/analytics/answer/12313109?hl=en).
- [Google tag callback and timeout parameters](https://developers.google.com/tag-platform/gtagjs/reference/parameters?hl=en).

## What must pass before any installation

1. Implement a disabled WordPress adapter using verified provider hash/version and preserving a single purchase owner. Drift must disable recovery; it must not produce a second sender.
2. Prove authenticated access, database atomicity, current order/payload validation, expiry cleanup, no historical replay and rollback in an isolated WordPress fixture. No public endpoint or durable browser storage before consent is approved.
3. Connect consent to the actual site's mechanism. Unknown defaults to no send. The conservative denied policy above is proposed, not inferred from the live site.
4. Verify browser behavior with a local collector or a dedicated non-production analytics property. No real orders or production purchase events for testing.
5. Only then consider an exact pushed production release with a new watermark, own-file/option backups and rollback. Leave existing order markers intact. Observe subsequent natural payments after GA4 processing.

Rollback for this preview: none required in production because nothing is installed. No deploy or activate command is included.
