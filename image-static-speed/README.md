# Responsive thumbnails and browser cache

Native responsive HTML for WooCommerce loop/gallery thumbnails after Woodmart filters. Preserve main product image, alt text, full-size lightbox links and all payment settings. Public CSS/JS/font assets and upload images receive 30-day browser cache; PDF lifetime and dynamic routes unchanged.

Deploy exact committed files on VPS with sudo python3 deploy.py. Deployment verifies existing Nginx SHA256, MU absence and PHP syntax; backs up exact config and rolls back on failure. Rollback: sudo python3 deploy.py --rollback. Existing page cache can contain old HTML temporarily; verify a cache-busted public request and natural expiry separately. No payment or order operations.
