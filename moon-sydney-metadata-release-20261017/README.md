# Moon/Sydney SEO metadata, owner-authorized 2026-10-17

Only Yoast title and description for products16110/18062, plus derived product indexables rebuilt via installed Yoast Indexable_Builder. Preserve all post fields (including content/modified dates/H1/summary), every other metadata key except dynamic wd_page_css_files, taxonomy, seven prior released posts. Stable taxonomy ordering and metadata-key ordering. Current before/after are exact in manifest; no archive, compatibility or print-ready promises.

GitHub-first source commit/push followed by deliver.py prepare/preview/apply/verify/rollback-preview, sequentially. Exact archive SHA256 checked; transactional postmeta/Yoast indexable/options tables verified InnoDB. Original values saved in _shustrik_moon_sydney_metadata_backup_20261017 before transaction. Apply once, do not retry an uncertain outcome. Existing WordPress external target, no build/restart/order/payment/indexing actions. Public response may need normal cache refresh.

Guarded rollback: python moon-sydney-metadata-release-20261017/deliver.py rollback. Restores only four previous SEO values and corresponding derived indexables if all content/metadata/prior-post invariants match. Does not restore an older product description. Browser checks confirm titles/H1/new descriptions; Google search snippets are not immediately verifiable and may be rewritten by Google.
