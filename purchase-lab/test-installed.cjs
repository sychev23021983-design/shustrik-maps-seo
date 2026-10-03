// Executes the captured installed Site Kit JS. No browser, fetch, or real GA4.
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const path = require('node:path');
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'installed-fixture-2026-10-03.json'), 'utf8'));
assert.equal(crypto.createHash('sha256').update(fixture.provider_js).digest('hex'), fixture.source_sha256.provider_js);
const findings = [], checks = [];
function check(name, fn) { fn(); checks.push(name); }
function page(inline, {consent='granted', online=true, execute=true}={}) {
  const attempted=[], received=[], blocked=[], timers=[];
  const context={setTimeout(fn){timers.push(fn);}, jQuery(){return {on(){},each(){}};},
    gtag(command,name,data){
      attempted.push({command,name,data});
      if(consent!=='granted') blocked.push('simulated-consent-gate');
      else if(!online) blocked.push('simulated-network-loss');
      else received.push({name,data});
    }};
  context.window=context; vm.createContext(context);
  vm.runInContext(fixture.gtag_wrapper_js,context);
  context._googlesitekit.wcdata={currency:'USD',products:[],eventsToTrack:['purchase']};
  for(const script of inline) vm.runInContext(script,context);
  if(execute) vm.runInContext(fixture.provider_js,context);
  return {context,attempted,received,blocked,timers,
    rerun(){vm.runInContext(fixture.provider_js,context);},flushTimers(){for(const fn of timers.splice(0))fn();}};
}
for(const row of fixture.cases) {
  const first=page(row.first_inline),second=page(row.second_inline);
  check(row.name+': no real order persisted',()=>assert.equal(row.actual_order_saved,false));
  const suppressed=['invalid-key','already-marked','wgai-owned'].includes(row.name);
  check(row.name+': installed first render behavior',()=>assert.equal(first.attempted.length,suppressed?0:1));
  check(row.name+': installed second render behavior',()=>assert.equal(second.attempted.length,row.name==='block-two-hooks'?1:0));
  if(first.attempted.length) {
    const event=first.attempted[0];
    check(row.name+': real formatter and JS payload',()=>{
      assert.equal(event.name,'purchase');assert.equal(event.data.transaction_id,9000000001);
      assert.equal(event.data.value,15);assert.equal(event.data.currency,'USD');
      assert.equal(event.data.items.length,1);assert.equal(event.data.items[0].item_name,'Synthetic lab item');
      assert.equal(event.data.items[0].price,15);assert.equal(event.data.items[0].quantity,1);
      assert.equal(event.data.event_source,'site-kit');assert.equal(event.data.user_data,undefined);
    });
  }
  findings.push({scenario:row.name,initial_status:row.initial_status,final_status:row.final_status,
    first_purchase_attempts:first.attempted.length,second_purchase_attempts:second.attempted.length,
    marker_before_js:row.first_marker,actual_order_saved:false});
}
const paid=fixture.cases.find(row=>row.name==='completed');
for(const [name,options] of [['consent-granted',{consent:'granted'}],['consent-denied',{consent:'denied'}],['consent-unknown',{consent:'unknown'}],['network-lost',{online:false}],['javascript-disabled',{execute:false}]]) {
  const first=page(paid.first_inline,options),reload=page(paid.second_inline);
  check(name+': provider attempts',()=>assert.equal(first.attempted.length,options.execute===false?0:1));
  check(name+': isolated sink receipt',()=>assert.equal(first.received.length,name==='consent-granted'?1:0));
  check(name+': later allowed reload cannot recover',()=>assert.equal(reload.received.length,0));
  findings.push({scenario:name,marker_before_js:paid.first_marker,
    provider_attempts:first.attempted.length,local_sink_receipts:first.received.length,
    allowed_reload_receipts:reload.received.length,gate_is_simulated:true,production_consent_verified:false});
}
const replay=page(paid.first_inline);
replay.rerun();check('wrapper suppresses same payload within 5ms',()=>assert.equal(replay.attempted.length,1));
replay.flushTimers();replay.rerun();check('wrapper is not durable deduplication',()=>assert.equal(replay.attempted.length,2));
findings.push({scenario:'same-inline-executed-again-after-wrapper-timer',provider_attempts:2,real_ga4_deduplication_verified:false});
const report={utc:new Date().toISOString(),fixture_utc:fixture.utc,source_sha256:fixture.source_sha256,
  harness_checks_passed:checks.length,assertion_failures:0,actual_orders_saved:0,real_ga4_requests:0,
  scope:'installed PHP method/formatter + installed JS in Node VM; synthetic objects, DOM and downstream collector stubs',
  limitations:['No real browser or Google collector receipt','Consent gating is a simulated sink, not a production CMP test','No actual payment gateway callback','No GA4 report deduplication test','PHP method invocation does not prove every order status reaches WooCommerce thankyou'],
  acceptance:{paid_only_gate_in_tested_method:false,network_loss_recovery:false,
    production_consent_policy_verified:false,paid_synthetic_payload_correct:true,
    classic_php_reload_suppressed:true,production_purchase_completeness_fixed:false},findings,checks};
fs.writeFileSync(path.join(__dirname,'results-2026-10-03.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({checks_passed:checks.length,assertion_failures:0,acceptance:report.acceptance,real_ga4_requests:0,actual_orders_saved:0},null,2));
