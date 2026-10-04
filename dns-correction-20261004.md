# Shustrik Maps DNS correction — 2026-10-04

Owner authorized correction with «делай» and «продолжай». Applied in Hostinger hPanel around 08:22 MSK to external target https://shustrik-maps.com.

Removed only apex A 88.223.84.50 and apex AAAA 2a02:4780:2b:1722:0:2066:40ab:2, both TTL1800. Kept apex A147.45.42.169. Full before/after exports compared as normalized DNS records: exactly these two deletions; all mail, DKIM, NS and subdomain records unchanged. SOA2026100402→2026100404.

Before change: forced HTTPS on147.45.42.169 returned200/TLSverify0;88.223.84.50 reproducedTLSalert80/EPROTO in curl and Node inside uptime-kuma. SSH/WireGuard/sudoDocker available, WP/DBrunning/restart0/OOMfalse and nginx-tpassed.

As of08:26MSK, provider UI/export confirms correction; DNS publication still inconsistent across authoritative/recursive responses, and Kuma can still hit cached old address/EPROTO. Complete propagation and a green monitor series are not confirmed. Runtime remains degraded; do not treat this ledger as outage resolved. No application code, container, server configuration, certificate or monitor changes.

Rollback: recreate only the two removed apex records at TTL1800 if required. Full zone exports and screenshot preserved in Vault project Checks/dns-zone-before-2026-10-04.txt, dns-zone-after-2026-10-04.txt and dns-fixed-2026-10-04.png. Do not import the whole zone without comparing unrelated changes.

Source baseline main4176ec6c72a0dd3628700e236d6fbb0d9631b404/upstream0:0. Original dirty/untracked work preserved. This commit records an external DNS change; it is not a WordPress image/source deployment.
