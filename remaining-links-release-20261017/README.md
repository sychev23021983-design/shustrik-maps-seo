# Remaining contextual links 17 October 2026

Owner approved L02/L06/L07/L08/L09. Three new links in FBX14596 and C4D/STL15631; label changes on projections20707 and Moon16110. The Moon button link attributes, style, BG and neighboring STL button are retained. No changes to product metadata, prices, downloads, media, SEO, H1, taxonomy or prior three-post release.

prepare.py builds exact guarded edits. Source baseline and manifest specify IDs, post types, hashes, protected fields and previous release fingerprints. release.php uses one InnoDB transaction for four content records and a backup option _shustrik_remaining_links_backup_20261017. Exact pushed source is delivered by deliver.py prepare; preview, apply once, verify and rollback-preview follow.

Guarded rollback: python remaining-links-release-20261017/deliver.py rollback. It restores only this package if content and protected metadata still match; the previous four links/OBJ correction are preserved. No runtime restart or historical orders/events.
