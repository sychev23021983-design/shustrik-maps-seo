#!/bin/sh
set -eu
release="$1"
case "$release" in ''|*[!0-9a-f]*) exit 2 ;; esac
test "${#release}" -eq 40
root="/tmp/shustrik-world-earth-copy-$release/world-earth-copy-release-20261108"
docker exec shustrik-maps-wordpress-1 php "$root/release.php" --apply
docker exec shustrik-maps-wordpress-1 php "$root/release.php" --verify
