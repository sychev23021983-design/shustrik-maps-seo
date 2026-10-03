# Five paired products — approved SEO publication

Owner explicitly approved exact title/meta/H1 and preserving both products in
Portugal, Afghanistan, Africa, Azerbaijan and Australia pairs. All ten existing
product URLs remain published and indexable. Thirty approved fields were changed.
Existing reciprocal links were already present 10/10 and were preserved.

Applied source commit: `04487aac0e9f16379d3e9e3125cb8540c3859164`.
Source archive SHA256: `d60148bf8776fffde5db1db3b8d8ea636861b3bf0623aef269f355e8e26fdc38`.
Target: external `https://shustrik-maps.com`, WordPress on existing VPS through
WireGuard `vpsadmin@10.66.66.1`. No local application runtime was changed.
Successful apply: 2026-10-03 16:21:25 UTC / 19:21:25 Moscow.

Validation: PHP lint and exact preview; DB verification 10/10 at 16:21:59 UTC,
protected content/excerpt hashes, product/file/price/media/category invariants
unchanged. Ordinary public QA eventually 10/10 HIT and uncached QA 10/10 BYPASS:
HTTP200, exact approved title/meta/one H1, original canonical/robots, valid existing
Product identity/offers/price/currency/availability, media and purchase CTA,
reciprocal links10/10 and all ten URLs in the product sitemap. Media HEAD10/10
HTTP200 image/*. Isolated anonymous Portugal product/cart/checkout/removal six
HTTP200/BYPASS requests, checkout/payment forms present, final cart empty.
No order, payment, or customer fields submitted. Browser payment JS was not tested.
Australia desktop rendering observed in Chrome; screenshot in Vault Checks.

The first source `6bedca0` was interrupted by CLI memory exhaustion during the
first wp_update_post. Only the first Portugal product changed; its content hash
also changed. Original content was recovered by exact pre-release SHA256 and all
ten original field/invariant snapshots reverified before the second apply.
The final source bypasses global post-save hooks, updates only the approved title
column plus two Yoast meta fields, invalidates cache and rebuilds only the product's
Yoast indexable. The failed attempt's evidence and backups remain preserved.
The exact hook responsible for the memory exhaustion was not attributed.

First public cache pass served two old STALE responses; final ordinary and uncached
passes passed. No shared cache purge, service restart, payment/tracking/plugin
configuration or vendor-file changes were made.

Backup option: `_shustrik_five_pairs_backup_20261003_v2`, non-autoloaded, original
field existence/values and protected content/excerpts. Backup check 10/10 exact
content/excerpt hashes at 16:24:33 UTC. Raw backup data was not printed or exported.
Persistent source: `/root/shustrik-five-pairs-release-20261003-v2/five-pairs-release/`.
Container CLI source: `/tmp/shustrik-five-pairs-release-20261003-v2/`.

Guarded rollback after checking for unrelated product drift:

```sh
sudo docker exec shustrik-maps-wordpress-1 php /tmp/shustrik-five-pairs-release-20261003-v2/release.php --rollback
```

If the container was recreated, first copy the persistent directory into that
container /tmp path. Repeat normal/uncached HTML and commerce checks after rollback.
Live rollback of the successful release was not run.

Vault evidence: `Checks/five-pairs-public-before-2026-10-03.json`,
`five-pairs-public-first-cache-pass-2026-10-03.json`,
`five-pairs-public-after-2026-10-03.json`, `five-pairs-public-uncached-2026-10-03.json`,
`five-pairs-commerce-qa-2026-10-03.json`, `five-pairs-media-qa-2026-10-03.json`,
`five-pairs-db-verify-v2-2026-10-03.json`, `five-pairs-backup-check-2026-10-03.json`,
`five-pairs-recovery-result-2026-10-03.json`.

Measure this release separately: 2026-10-04–2026-10-31 versus 2026-09-05–2026-10-02,
28 days each, once final data is available. Exclude partial publication day03.10;
other metadata/runtime changes and incomplete purchase tracking remain confounders.
No ranking, CTR, or sales uplift is claimed. Runtime remains degraded because
the existing performance/purchase/consent risks are outside this publication scope.
