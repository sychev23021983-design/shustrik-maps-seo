# Arizona visual and copy release — 2026-10-05

Owner explicitly requested uploading three generated images including one commercial scenario, assigning image title/alt, checking the semantic core and implementing relevant improvements on the product page. Scope: product 9520 only. Existing owner changes are excluded from staging.

Assets: three WebP conversions of the existing AI concepts, unchanged pixel dimensions/content. Titles, alt, captions and exact copy are in manifest.json. Baseline contains public product content and hashes of protected commerce fields; no download URLs or credentials.

SEO decision: existing core has Arizona elevation-map mixed intent deferred for format/assortment. It is not assigned to this STL SKU. Existing product-specific title/H1 preserved; body emphasizes Arizona topographic map STL, printable relief and CNC preparation, removes unsupported universal compatibility/accuracy/laser claims, separates STL from standalone DEM data. No new primary-keyword measurement or SERP demand is claimed. Technical excerpt remains unchanged pending resolution of inconsistent dimensions/projection; no guessed replacement.

Media: append three attachments to existing product gallery, preserve featured image and existing gallery order; add labeled figures in Description. Commercial image explicitly requires separately agreed permission; no change to personal-use licence, price, slug, canonical, robots, downloads, technical excerpt, payment flow or related-product links.

Apply only after exact preview and source/asset hash verification. CLI modes: release.php --preview / --apply / --verify / --rollback-preview / --rollback. Backup option: _shustrik_arizona_visual_backup_20261005. Rollback restores original product content, gallery and meta description while retaining uploaded media. Recheck public cache and product after rollback. Unattached imports after any failed partial apply require inspection; do not blindly rerun.

Preparation: prepare.py converts PNG to WebP and creates manifest from baseline. It does not change generated content.
