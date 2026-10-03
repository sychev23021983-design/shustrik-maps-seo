# Scoped asynchronous Pinterest view events

Owner requested the next concrete performance fix after confirmed synchronous CAPI latency. Only PageVisit/ViewCategory move to Action Scheduler; original Tag/events IDs/timestamps, crawler exclusion and synchronous AddToCart/Checkout/Search remain. No vendor edits, cache bypass changes or fake HTTP success response. Tracker wrapper uses public get/add/remove methods, composition around the original Conversions preparation, and version1.4.27 guard.

Prepared payload is sodium-secretbox encrypted in nonautoload WordPress options using a runtime-derived wp_salt key (never printed, no new credential or auth change). It may contain existing IP/UA/hashed email already required by CAPI. No payload/credential in AS args or our logs: only opaque job ID. Account fingerprint guards reconnect drift. Success/permanent failure deletes payload immediately;5 transient attempts (60/300/900/1800seconds), expiry6hours, cleanup every consumer run,2000-record soft capacity then original sync fallback. Original plugin's existing logging settings are retained. ID/time persist through retries for Pinterest deduplication; exactly-once network delivery is not claimed after a lost acknowledgement.

Action Scheduler4.0.0 group-specific claim of at most2 due actions per isolated CLI run. Systemd5s after run, one consumer service, no Apache worker needed; existing WP scheduler remains unchanged. Default runners may also claim these jobs; AS claims plus a120s payload lease prevent concurrent duplicate dispatch. Aggregated counters only. Worker timer is application runtime, not Codex automation.

GitHub-first; preview/lint/synthetic tests/preflight source hashes; commit/push exact archive and compare hashes before --apply. Deploy starts consumer with admission disabled, then enables admission only after consumer success. Existing dirty work preserved. Commerce/SEO/queue delivery/before-after phase QA required.

Rollback `sudo python3 /root/shustrik-pinterest-async-20261003/deploy.py --rollback` disables only new asynchronous admission, restoring original sync tracker while keeping consumer and encrypted payloads until drained. Do not remove consumer with queued data; guarded full removal can follow payloads0. No API credentials, salts or event payloads should be output/read by diagnostics.

API references: https://actionscheduler.org/api/ and https://developer.wordpress.org/reference/hooks/pre_http_request/ (HTTP short-circuit considered and rejected in favor of tracker-level queue).
