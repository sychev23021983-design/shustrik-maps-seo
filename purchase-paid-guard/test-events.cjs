const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto'),path=require('node:path');
const root=__dirname, input=JSON.parse(fs.readFileSync(path.join(root,'php-results-2026-10-03.json'),'utf8'));
let checks=0;
function check(fn){fn();checks++;}
check(()=>assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'shustrik-purchase-paid-guard.php'))).digest('hex'),input.guard_sha256));
check(()=>assert.equal(crypto.createHash('sha256').update(input.provider_js).digest('hex'),input.source_sha256.provider_js));
function run(scripts,online=true){
 const attempts=[],received=[];
 const context={setTimeout(){},jQuery(){return {on(){},each(){}};},gtag(type,name,data){attempts.push({name,data});if(online)received.push({name,data});}};
 context.window=context;vm.createContext(context);vm.runInContext(input.gtag_wrapper_js,context);
 context._googlesitekit.wcdata={currency:'USD',products:[],eventsToTrack:['purchase']};
 for(const script of scripts)vm.runInContext(script,context);
 vm.runInContext(input.provider_js,context);return {attempts,received};
}
const findings=[];
for(const row of input.cases){
 const first=run(row.first_inline),second=run(row.second_inline);
 const paid=['completed','processing','free-paid'].includes(row.name);
 check(()=>assert.equal(first.attempts.length,paid?1:0));
 check(()=>assert.equal(second.attempts.length,row.name==='late-payment'?1:0));
 for(const event of [...first.attempts,...second.attempts]){
  check(()=>assert.equal(event.name,'purchase'));
  check(()=>assert.equal(event.data.transaction_id,9000000001));
  check(()=>assert.equal(event.data.currency,'USD'));
  check(()=>assert.equal(event.data.value,row.name==='free-paid'?0:15));
  check(()=>assert.equal(event.data.items.length,1));
  check(()=>assert.equal(event.data.user_data,undefined));
 }
 findings.push({name:row.name,first_purchase_attempts:first.attempts.length,second_purchase_attempts:second.attempts.length});
}
const completed=input.cases.find(row=>row.name==='completed');
const loss=run(completed.first_inline,false),reload=run(completed.second_inline,true);
check(()=>assert.equal(loss.attempts.length,1));check(()=>assert.equal(loss.received.length,0));check(()=>assert.equal(reload.received.length,0));
const output={utc:new Date().toISOString(),php_checks_passed:input.checks_passed,js_checks_passed:checks,assertion_failures:0,
 scope:'installed Site Kit JS in Node VM with local sink; preview is not installed in production',
 paid_gate_passed:true,late_payment_next_render_passed:true,original_marker_network_loss_recovery:false,
 real_browser_consent_verified:false,real_google_receipt_verified:false,actual_orders_saved:0,real_ga4_requests:0,
 guard_sha256:input.guard_sha256,findings};
fs.writeFileSync(path.join(root,'js-results-2026-10-03.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify(output,null,2));
