# Moon description — owner-approved release 2026-10-17

Product16110, existing Description text only: exact three paragraphs approved by owner in chat. First paragraph replaces the existing introduction; second and third replace the existing text beside image16121. Remove three old headings with unsupported research/VR/texture-segmentation claims. No new headings, no repeated specifications.

Preserve every shortcode token, images, full lower content from the Color Texture row, short description/specifications, H1/title/meta/canonical/taxonomy/commerce and related buttons including BG/styles/links. Seven prior published posts (six article/link pages plus Earth11517) are fingerprint protected. Term ordering is deterministic by name/termID in both snapshot and verifier, following the diagnosed Earth verifier issue.

External deployment target https://shustrik-maps.com via existing WireGuard SSH and sudoDocker. Commit/push before prepare; deploy the exact archive and verify its SHA256. Run `python moon-description-release-20261017/deliver.py prepare`, then preview/apply/verify/rollback-preview sequentially. Apply once; inspect before retry on uncertainty. Conditional content writes in one InnoDB transaction; backup option `_shustrik_moon_description_backup_20261017`.

Rollback, only if needed: `python moon-description-release-20261017/deliver.py rollback`. Guard checks content, protected metadata and prior releases before restoring only original Description. No orders/payment/indexing/settings changes or build/restart.

Public QA compares Moon and its two related product targets, excludes the rotating related grid, and preserves authored media/metadata/specifications/links. Review actual desktop/mobile rendering separately. Old page-cache responses can persist until the existing background refresh completes; never repeat apply because of stale public HTML.
