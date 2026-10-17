# Earth Without Water description — owner-approved release, 2026-10-17

Scope: product 11517, existing `post_content` only. Replace the two existing opening description text bodies with the exact three paragraphs approved in chat. First two paragraphs occupy the existing introductory half-width column beside image 11522; the third replaces the second full-width text body. No new headings or specification repetition.

Preserve all shortcode tokens, media, the complete suffix beginning with the Earth terrain DEM row, related product buttons and styling, short description/specifications, price/download/commerce metadata, title/H1/SEO/canonical/taxonomy. Prior seven link-release posts are fingerprint-protected. Dynamic Woodmart CSS metadata is excluded from fingerprints; rotating related-product listings are excluded from public media comparisons.

Deployment: external WordPress, existing runtime via vpsadmin@10.66.66.1. Commit and push the exact package before `python earth-description-release-20261017/deliver.py prepare`, followed sequentially by `preview`, `apply`, `verify`, `rollback-preview`. Publication is compare-and-swap guarded and backed up in `_shustrik_earth_description_backup_20261017`. Do not repeat apply on an uncertain outcome; inspect CMS/backup first.

Rollback: `python earth-description-release-20261017/deliver.py rollback` restores only the original content if candidate and protected fingerprints still match. No rollback is requested. No orders, payment tests, indexing requests or settings changes.

QA: `python earth-description-release-20261017/public-qa.py verify` compares four public pages against the dated baseline; verify actual desktop/mobile rendering separately. Page-cache TTL may expose the previous copy until its normal background refresh completes; do not interpret a stale response as a failed CMS write.
