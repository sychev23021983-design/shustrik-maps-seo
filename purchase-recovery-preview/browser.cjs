'use strict';
// Dependency-injected browser boundary; no network, cookies or gtag call built in.
async function attempt({readConsent, online, tagReady, claim, authorize, send}) {
  if (readConsent() !== 'granted' || !online() || !tagReady()) return 'waiting';
  const ticket = await claim();
  if (!ticket) return 'not-claimed';
  if (readConsent() !== 'granted' || !online() || !tagReady()) return 'waiting-after-claim';
  const payload = await authorize(ticket);
  if (!payload) return 'not-authorized';
  // Consent can change while authorization is in flight. Never rely on earlier consent.
  if (readConsent() !== 'granted' || !online() || !tagReady()) return 'suppressed-after-authorization';
  try { send(payload); } catch (_) { return 'ambiguous'; }
  return 'attempted'; // callback/HTTP success do not assert processed GA4 receipt.
}
module.exports={attempt};
