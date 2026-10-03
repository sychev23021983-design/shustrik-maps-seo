# Approved five-pair SEO release — 2026-10-03

Owner explicitly approved exact title, meta description and H1 for ten existing
Portugal/Afghanistan/Africa/Azerbaijan/Australia products, preserving both URLs
of each pair. Text is copied exactly from the approved Vault Page Brief.

Only Yoast title/description and the native WooCommerce product title (H1) change.
Existing product links, content, descriptions, slugs, prices, file definitions,
media, categories, robots and canonical overrides are guarded against drift.
Public baseline found all ten reciprocal peer links already present.

`proposals.json`: approved exact fields and scope.
`baseline.json`: current fields, field existence, IDs and protected hashes.
No credentials, downloadable file addresses or customer records are included.

`release.php`: CLI-only, exact site guard. Default `--preview` is read-only.
`--apply` saves the entire scoped old-field backup as a non-autoloaded WordPress
option `_shustrik_five_pairs_backup_20261003` before any product writes, validates
each product immediately before mutation, verifies protected invariants, and
restores attempted fields on failure unless unrelated field drift is detected.
`--verify` confirms exact published fields and protected invariants.
`--rollback` validates backup and before/after values, then restores field values
or their original absence. Backups are retained. Unrelated concurrent edits cause
a refusal rather than being overwritten.

Deployment uses a Git archive of this directory from the pushed source commit,
verified by SHA256 locally/on VPS. Persistent source is retained under
`/root/shustrik-five-pairs-release-20261003/`. Only the CLI helper is copied to
the WordPress container `/tmp/shustrik-five-pairs-release-20261003/`; no plugin
files, services, network policies, payment settings or commerce event hooks change.

After apply: `--verify`, public ordinary and uncached HTML checks, media HEADs,
product sitemap presence, and an isolated product/cart/checkout/cleanup scenario.
Schema product identity and offers/prices remain identical; the product name can
follow the newly approved native product title. No new schema claims are added.
No order or payment is submitted during QA.

Recovery after container recreation: copy this directory from the persistent
source into the same `/tmp` path, then run the guarded `--rollback` through
`sudo docker exec shustrik-maps-wordpress-1 php .../release.php --rollback`.
Recheck ordinary and uncached public output after rollback. Nginx anonymous page
cache can briefly serve the old HTML while background refresh runs; do not treat
STALE responses as successful verification.
