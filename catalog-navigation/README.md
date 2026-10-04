# Catalog navigation — owner-authorized 2026-10-04

Hide menu links to empty Fantasy (term84) and Elevation Maps (term206), without
deleting any menus or categories. The menu filter applies only to the exact two
URLs and leaves them visible once published products exist (including children).
Other links, including related STL product links, are unaffected.

Add one H1 `3D Models` through Woodmart's existing before-shop hook only on the
3d-models category and its pagination. No term descriptions/metadata, products,
prices, files, payment behavior, theme code or database settings are modified.

`admin.php --snapshot` emits hashes only. `--verify` guards all raw menu records,
three taxonomy records, three selected product records and the archive template.
Deploy the exact pushed Git archive to `/root/shustrik-catalog-navigation-20261004/`.
`sudo python3 .../deploy.py --preview` requires the new own MU file to be absent.
`--apply` retains the absence/hash backup then installs only the own MU file.

Rollback: `sudo python3 /root/shustrik-catalog-navigation-20261004/deploy.py --rollback`.
This removes only the own file if its hash still matches, after verifying data.
Backup is retained. No global menu settings or cached pages are deleted.
Verify ordinary and query URLs after anonymous cache refresh; retain publication
as pending until ordinary output has both changes. Check H1 position, navigation,
pagination, an unrelated category and selected products. Do not submit an order.
