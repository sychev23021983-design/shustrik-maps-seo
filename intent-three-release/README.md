# Illinois / Jupiter / Mercury release — 2026-10-04

Owner approved the exact nine fields in proposals.json by replying «да» on 2026-10-04. Scope: SEO title, description and one exact introductory fragment for product IDs 17483, 16047, 15996. H1, all remaining content, excerpt, commerce settings, downloads, taxonomy and canonical/robots overrides are protected.

release.php is run only via CLI in the production WordPress container. Run --preview before --apply; --verify checks all approved fields and protected data. Original content is saved server-side in option _shustrik_intent_three_backup_20261004. --rollback-preview validates recovery without writing; --rollback restores these nine fields only if the current state still exactly matches this release. No payment, order or file-delivery test is performed.

Deploy the pushed source commit using git archive, verify archive SHA256, copy into the container, then apply. Source baseline and public-before evidence are sanitized. public_qa.py compares ordinary and uncached HTML against approved values and preserved links, images, Product offers, H1 and purchase button.

Scientific/compatibility claims elsewhere in the pages and the visual purpose of the second Mercury texture remain separate unresolved work. GA4 05.10 and GSC 10.10 retain priority.
