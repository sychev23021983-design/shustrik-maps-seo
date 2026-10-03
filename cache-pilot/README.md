# Shustrik anonymous cache coalescing pilot — 2026-10-03

Owner authorized stepwise stability work. Initial instrumentation window: 175 requests/54 samples, maxrt2.85s, noBusy4/no unavailable probes. One cron499 at0.961s does not prove visitor outage. Historical579 upstream-header timeouts remain unexplained.

This narrow mitigation coalesces requests to the same new anonymous cache key and serves stale content while an expired entry refreshes in background. Four directives only in Shustrik location /; shared WordPress cache definitions, TTL60s, worker limit4, query/session/cart/checkout bypass, security protections and timing logs remain unchanged. This does not fix unique query/BYPASS workload or prove the historical root cause. Metadata changes must account for the existing60sTTL/background refresh.

Default deploy read-only with expected vhost hash; --apply backs up then validates/reloads Nginx, automatic restoration on failure. Commit/push exact script before VPS execution. Rollback /root/shustrik-cache-pilot-20261003/deploy.py --rollback checks installed hash and restores instrumentation vhost. Observability rollback must follow cache-pilot rollback; its drift guard intentionally refuses the changed vhost while this pilot is active.

Acceptance: bounded two simultaneous anonymous Earth requests to a cold exact cache key yield one MISS and one HIT, identical public metadata; afterTTL expired request usesSTALE/background update and next requestHIT. Cart/checkout/query/session remainBYPASS, no orders/payment/PII. Containers/bindings unchanged. Retain timing comparison and rollback. Do not stress-test production or clear shared cache; at most evict the validated Earth anonymous key for the acceptance probe. Evaluate against subsequent instrumented traffic, not only a synthetic pair.

Primary documentation: https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_lock and https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_background_update
