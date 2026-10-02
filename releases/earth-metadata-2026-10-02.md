# Earth metadata correction — 2026-10-02

Owner instruction: «делай», following the proposed Earth-only title/description correction. Scope: product 11517, two Yoast fields. This is a correction of unsupported product claims, not a proven traffic recovery treatment.

URL: https://shustrik-maps.com/product/earth-3d-model-terrain-without-water/

## Page brief

Purpose / audience / intent: help buyers of a digital Earth terrain visualization find the C4D/OBJ product and understand its ocean-free relief. Primary query: `earth without water 3d model`. Supporting: Earth terrain, C4D, OBJ. Exclude promises of printing/CNC readiness, STL availability on this card, geographic accuracy and licensing that have not been verified.

Title: `Earth Without Water 3D Model — C4D & OBJ Terrain`

Description: `Explore Earth's terrain beneath the oceans with a 3D model in C4D and OBJ formats. View the file specifications, previews and texture details.`

H1 remains `Earth 3D model Terrain Without Water`; self-canonical and indexability remain. No URL, schema, body, price, file, internal link or CTA changes. Existing product specifications/previews and purchase CTA remain. The existing STL link leads to a separate product; this correction does not promise STL on this card. No new structured-data claims.

## Evidence and limits

GSC web search, exact page, all countries/devices, before 2026-07-29–2026-08-27 vs after 2026-08-31–2026-09-29: clicks 95 → 40, impressions 2840 → 1670, CTR 3.3% → 2.4%, average position 6 → 5.

Visible primary query: clicks 28 → 7, impressions 606 → 262, CTR 4.6% → 2.7%, position 5.2 → 4.4. Broader `earth without water`: impressions 215 → 29 and position 3.2 → 15.3. Neither causality nor aggregate recovery is established; query tables omit anonymized queries.

Device table shows PC 22 → 9 clicks / 665 → 415 impressions; mobile 29 → 6 / 908 → 373; tablet 0 → 0 / 23 → 12. These rows do **not** reconcile with headline page totals (51 → 15 versus 95 → 40). Treat the device breakdown as unvalidated, not as an attributable mobile loss. Country retrieval timed out. No claims about country contribution. GA4 remains unavailable; revenue/conversion effect is unknown.

Public card specification lists C4D and OBJ. Existing metadata incorrectly claims Printing & CNC readiness and “landmass elevation only”; product description/previews show terrain beneath the oceans. No download or file geometry validation was performed.

## Release / acceptance / rollback

Script: `step1-quick-fixes/earth-metadata-2026-10-02.php`. Default read-only. Before applying, validate PHP syntax and preview, commit/push only this release's two files, then copy the exact committed script to the existing WordPress container. Verify SHA256 before execution. Guard post identity, original fields, content SHA256, price, canonical override and noindex value. Save old fields in `_shustrik_earth_metadata_backup_20261002` before updating.

Acceptance: exact public title/description, HTTP 200, same URL/canonical/H1 and indexability; backend content hash and price unchanged; containers healthy. No site-wide cache deletion. Rollback: execute the same script with `--rollback`; it checks expected new values and restores only the two prior fields. Preserve backup.

Measurement: retain the August pilot baseline separately; this correction starts a new exposure window. Earliest 28-day comparison after GSC finalizes 2026-10-03–2026-10-30, using 2026-09-04–2026-10-01 as the preceding 28-day window. Capture that fresh pre-correction window when available. Evaluate query mix, CTR, devices/countries reconciliation and GA4 alongside clicks; no new pilot expansion until timeout/LCP/measurement issues are assessed.
