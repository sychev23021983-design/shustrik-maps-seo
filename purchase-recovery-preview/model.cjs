'use strict';
// Isolated architecture model. No WordPress hooks, HTTP, gtag or order writes.
const terminal = new Set(['observed', 'suppressed', 'expired']);
class Recovery {
  constructor(store, releaseAt, { ttl = 72 * 3600000, lease = 30000 } = {}) {
    this.store = store; this.releaseAt = releaseAt; this.ttl = ttl; this.lease = lease;
  }
  // Adapter must read authoritative WooCommerce data and authenticate receipt access.
  prepare(order, access, now) {
    if (!access || !order.paid || !Number.isFinite(order.paidAt) || !Number.isFinite(order.createdAt)
        || order.createdAt < this.releaseAt || order.paidAt < this.releaseAt
        || order.createdAt > now || order.paidAt > now) return false;
    const p = order.payload;
    if (!p || typeof p.transaction_id !== 'string' || !p.transaction_id.trim()
        || p.currency !== 'USD' || !Number.isFinite(p.value) || p.value < 0
        || !Array.isArray(p.items) || !p.items.length) return false;
    const clean = { transaction_id: p.transaction_id, currency: p.currency, value: p.value,
      items: p.items.map(i => ({ item_id: i.item_id, price: i.price, quantity: i.quantity })) };
    if (clean.items.some(i => typeof i.item_id !== 'string' || !i.item_id
        || !Number.isFinite(i.price) || i.price < 0 || !Number.isInteger(i.quantity) || i.quantity < 1)) return false;
    // Unique key; never reset an existing attempt, suppression or observation on reload.
    if (!this.store.has(p.transaction_id)) this.store.set(p.transaction_id, {
      state: 'ready', payload: clean, expires: order.paidAt + this.ttl, attempts: 0, generation: 0
    });
    return true;
  }
  claim(id, { access, paid, consent, online, tagReady }, now) {
    const r = this.store.get(id);
    if (!r || !access || !paid || terminal.has(r.state)) return null;
    if (consent === 'denied') { r.state = 'suppressed'; delete r.payload; return null; }
    if (now >= r.expires) { r.state = 'expired'; delete r.payload; return null; }
    if (r.state === 'inflight') {
      if (now >= r.leaseUntil) r.state = 'await_reconciliation';
      return null; // An expired lease is ambiguous, not permission to resend.
    }
    if (r.state === 'await_reconciliation' || consent !== 'granted' || !online || !tagReady) return null;
    r.state = 'inflight'; r.attempts++; r.generation++; r.leaseUntil = now + this.lease;
    return { id, generation: r.generation, payload: structuredClone(r.payload) };
  }
  // Consent/access must be freshly checked immediately before the actual browser call.
  dispatch(ticket, context, send, now) {
    const r = this.store.get(ticket?.id);
    if (!r || r.state !== 'inflight' || ticket.generation !== r.generation) return false;
    if (!context.access || !context.paid || context.consent !== 'granted') {
      r.state = context.consent === 'denied' ? 'suppressed' : 'ready';
      if (r.state === 'suppressed') delete r.payload;
      r.generation++; return false;
    }
    if (now >= r.expires) { r.state = 'expired'; delete r.payload; return false; }
    if (now >= r.leaseUntil) { r.state = 'await_reconciliation'; return false; }
    if (!context.online || !context.tagReady) {
      r.state = 'ready'; r.generation++; return false; // Known no-call path can safely retry.
    }
    // Record uncertainty before crossing the boundary. Exceptions may occur AFTER send.
    r.state = 'await_reconciliation';
    try { send(structuredClone(r.payload)); } catch (_) { /* still ambiguous */ }
    return true;
  }
  callback(ticket) {
    const r = this.store.get(ticket?.id);
    if (r && ticket.generation === r.generation && r.state === 'await_reconciliation') r.callbackSeen = true;
    // A gtag callback is not evidence of a processed GA4 purchase.
  }
  reconcile(id, observation) {
    const r = this.store.get(id);
    if (!r || r.state !== 'await_reconciliation') return false;
    if (observation.property !== '501927425' || observation.transaction_id !== id
        || observation.currency !== r.payload.currency || observation.value !== r.payload.value
        || observation.processed !== true) return false;
    r.state = 'observed'; delete r.payload; return true;
    // Missing rows never authorize replay; processing lag/filtering may explain them.
  }
}
module.exports = { Recovery };
