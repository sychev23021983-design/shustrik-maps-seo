'use strict';
const assert=require('node:assert/strict');const {attempt}=require('./browser.cjs');
(async()=>{
  let checks=0;const eq=(a,b)=>{assert.equal(a,b);checks++;};
  for (const initial of ['unknown','denied']) {
    let calls=0;
    eq(await attempt({readConsent:()=>initial,online:()=>true,tagReady:()=>true,
      claim:async()=>{calls++;},authorize:async()=>{calls++;},send:()=>calls++}),'waiting');eq(calls,0);
  }
  let consent='granted',calls=0;
  const base={readConsent:()=>consent,online:()=>true,tagReady:()=>true,
    claim:async()=>({id:'SYNTHETIC',generation:1}),authorize:async()=>({transaction_id:'SYNTHETIC'}),send:()=>calls++};
  eq(await attempt({...base,claim:async()=>{consent='denied';return {id:'SYNTHETIC'};}}),'waiting-after-claim');eq(calls,0);
  consent='granted';
  eq(await attempt({...base,authorize:async()=>{consent='denied';return {transaction_id:'SYNTHETIC'};}}),'suppressed-after-authorization');eq(calls,0);
  consent='granted';eq(await attempt(base),'attempted');eq(calls,1);
  eq(await attempt({...base,send:()=>{throw Error('ambiguous');}}),'ambiguous');
  eq(await attempt({...base,authorize:async()=>null}),'not-authorized');
  eq(await attempt({...base,tagReady:()=>false}),'waiting');eq(calls,1);
  console.log(JSON.stringify({checks,passed:true,real_browser:false,google_requests:0},null,2));
})().catch(e=>{console.error(e);process.exit(1);});
