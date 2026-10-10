# Paid guard compatibility release 2026-10-10

Approved by owner after review of the isolated candidate. Source changes only the WooCommerce gate11.1.2→11.2.1 and plugin patch version0.1.0→0.1.1. Recovery stays uninstalled. The existing option remains unchanged; no order metadata, payment settings or historical events are touched.

Candidate hash:6a9cfc06e1a93060777df0f8baef7aa54c13908486695a4b6ed5cf8d817b978d. Expected previous hash:666940e505df36627c2c556f680f0a0e3e71a7515c68e994b3f8c6a460b2fbe6. Site Kit1.184.0/provider hash82da28caecda75acca747963336c170ddf6399999a91f7ecb7588db0b6182c85 and Woo11.2.1/classic theme required.

On VPS root, from the exact pushed source archive: `python3 deploy.py --apply --source-commit <exact-40-character-commit>`. Destination is only `/opt/vps/shustrik-maps/wordpress/wp-content/mu-plugins/shustrik-purchase-paid-guard.php`; source/old hash, option, versions and canonical home are checked before change. PHP lint precedes backup and atomic replacement. Existing file ownership/mode are retained. No container restart required.

Persistent backup: `/root/shustrik-paid-guard-compat-20261010-backup/before.php` plus manifest and after inspection. Rollback from the same saved source folder: `python3 deploy.py --rollback`. It refuses runtime/source drift, restores only the old file and leaves the enabled option intact. Rollback restores the old incompatible Woo11.1.2 gate; it does not resolve tracking.

Acceptance: run installed-file synthetic PHP checks and simulated guest receipt installation in an independent CLI request; verify unchanged provider/option, exact new MU hash, one callback wrapper and unchanged other slots. Check public home/cart/checkout and running containers. No actual order/payment or production purchase event for testing. Reported completeness must await natural paid orders and processed GA4.
