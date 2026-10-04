# FAQ and PayPal instructions — 2026-10-04

Owner explicitly requested FAQ/PayPal fixes and rejected changing product layout
or separating the existing related STL link. Standard downloads are automatic
after successful payment; special requests are handled separately.

Four text fragments change in three existing records: Support 10438 delivery and
payment answers, FAQ 651 purchase instructions, shared PayPal block 10018 rendered
by How to Buy 608. Existing shortcodes, headings and all other text remain intact.
The old automatic-download/button-replacement/security-warning instruction is
replaced by the current checkout and download-link flow.

`--snapshot` exports only content/protected-field hashes for these three records,
How to Buy and Earth/Authagraph/World. No file addresses, orders or secrets.
`--preview` refuses baseline drift. `--apply` creates non-autoloaded backup option
`_shustrik_help_copy_backup_20261004`, locks scoped posts, changes only content and
modified timestamps in one transaction, and clears the three post caches.
Broad post-save filters are intentionally bypassed because earlier releases
observed unrelated content mutations. No payment settings, metadata or products
change. `--verify` rechecks exact after-content and protected fields.

Deploy a verified Git archive of the pushed source. Keep it persistently at
`/root/shustrik-help-copy-20261004/`, and copy to the container
`/tmp/shustrik-help-copy-20261004/`. Rollback, after inspecting current state:

`sudo docker exec shustrik-maps-wordpress-1 php /tmp/shustrik-help-copy-20261004/release.php --rollback`

Rollback refuses unrelated content/metadata drift, restores the original three
contents and timestamps, and retains the backup. Do not repeat apply. Public QA
must confirm both FAQ pages and How to Buy, ordinary and cache-bypassed output.
Payment or paid delivery is not tested by this text-only release.
