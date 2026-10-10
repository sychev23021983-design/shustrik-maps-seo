'use strict';
const assert = require('node:assert/strict');
const { Recovery } = require('./model.cjs');
let checks = 0;
function eq(a, b) { assert.deepEqual(a, b); checks++; }
const start = 1000000;
const order = () => ({ createdAt: start, paidAt: start + 100, paid: true,
  payload: { transaction_id: 'SYNTHETIC-1', currency: 'USD', value: 15,
    email: 'removed@example.invalid', items: [{ item_id: 'LAB', price: 15, quantity: 1 }] } });
const ctx = () => ({ access: true, paid: true, consent: 'granted', online: true, tagReady: true });
const fresh = () => { const store = new Map(); return [new Recovery(store, start), store]; };
const now = start + 1000;
for (const bad of [ {paid:false}, {paidAt:null}, {createdAt:NaN}, {createdAt:start-1}, {paidAt:start-1}, {paidAt:now+1} ]) {
  const [m,s] = fresh(); eq(m.prepare({...order(),...bad}, true, now), false); eq(s.size, 0);
}
{ const [m,s]=fresh(); eq(m.prepare(order(),false,now),false); eq(s.size,0); }
for (const patch of [{transaction_id:''},{currency:'EUR'},{value:NaN},{value:-1},{items:[]},
  {items:[{item_id:'LAB',price:15,quantity:0}]}]) {
  const [m,s]=fresh(); const o=order(); Object.assign(o.payload,patch);
  eq(m.prepare(o,true,now),false); eq(s.size,0);
}
{ const [m,s]=fresh(); const o=order(); o.payload.value=0; o.payload.items[0].price=0;
  eq(m.prepare(o,true,now),true); eq(s.get('SYNTHETIC-1').payload.value,0); }
for (const patch of [{access:false},{paid:false},{consent:'unknown'},{online:false},{tagReady:false}]) {
  const [m,s]=fresh(); m.prepare(order(),true,now);
  eq(m.claim('SYNTHETIC-1',{...ctx(),...patch},now),null); eq(s.get('SYNTHETIC-1').attempts,0);
}
{ const [m,s]=fresh(); const o=order(); o.paid=false;
  eq(m.prepare(o,true,now),false); o.paid=true;
  eq(m.prepare(o,true,now),true); // delayed payment alone sends nothing
  eq(s.get('SYNTHETIC-1').attempts,0);
  const t=m.claim('SYNTHETIC-1',ctx(),now); let calls=0;
  eq(m.dispatch(t,ctx(),()=>calls++,now),true); eq(calls,1);
  m.callback(t); eq(s.get(t.id).state,'await_reconciliation');
  eq(m.claim(t.id,ctx(),now+100000),null); // no resend on callback/reload
  eq(m.prepare(o,true,now+100000),true); eq(s.get(t.id).attempts,1);
  eq('email' in s.get(t.id).payload,false);
  for (const bad of [{property:'wrong'}, {transaction_id:'wrong'}, {value:99}, {processed:false}]) {
    eq(m.reconcile(t.id,{property:'501927425',transaction_id:t.id,currency:'USD',value:15,processed:true,...bad}),false);
  }
  eq(m.reconcile(t.id,{property:'501927425',transaction_id:t.id,currency:'USD',value:15,processed:true}),true);
  eq(m.claim(t.id,ctx(),now+100001),null); eq(s.get(t.id).payload,undefined);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now); const t=m.claim('SYNTHETIC-1',ctx(),now);
  eq(m.claim(t.id,ctx(),now),null); // concurrent tab
  let calls=0; eq(m.dispatch(t,{...ctx(),online:false},()=>calls++,now),false);
  const t2=m.claim(t.id,ctx(),now+1);
  eq(m.dispatch(t,ctx(),()=>calls++,now+1),false); // stale lease
  eq(m.dispatch(t2,ctx(),p=>{eq(p.transaction_id,t.id);calls++;},now+1),true); eq(calls,1);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now); const t=m.claim('SYNTHETIC-1',ctx(),now);
  eq(m.dispatch(t,{...ctx(),consent:'denied'},()=>assert.fail('denied send'),now),false);
  eq(s.get(t.id).state,'suppressed'); eq(s.get(t.id).payload,undefined);
  m.prepare(order(),true,now); eq(m.claim(t.id,ctx(),now+1),null);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now); const t=m.claim('SYNTHETIC-1',ctx(),now);
  m.dispatch(t,ctx(),()=>{throw new Error('network ambiguous');},now);
  eq(s.get(t.id).state,'await_reconciliation'); eq(m.claim(t.id,ctx(),now+50000),null);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now); const t=m.claim('SYNTHETIC-1',ctx(),now);
  // No JS ran after lease acquisition; crash and real send cannot be distinguished.
  eq(m.claim(t.id,ctx(),now+30001),null); eq(s.get(t.id).state,'await_reconciliation');
  // Rehydrate the model with simulated persisted rows, not a real durable adapter.
  const restarted=new Recovery(new Map(JSON.parse(JSON.stringify([...s]))),start);
  eq(restarted.claim(t.id,ctx(),now+60000),null);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now);
  eq(m.claim('SYNTHETIC-1',ctx(),start+100+72*3600000),null);
  eq(s.get('SYNTHETIC-1').state,'expired'); eq(s.get('SYNTHETIC-1').payload,undefined);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now);
  // JS never executes on initial receipt: stored intent survives until a later render.
  const reloaded=new Recovery(new Map(JSON.parse(JSON.stringify([...s]))),start);
  eq(reloaded.claim('SYNTHETIC-1',{...ctx(),consent:'unknown'},now+1),null);
  const t=reloaded.claim('SYNTHETIC-1',ctx(),now+2); eq(t.payload.value,15);
  let calls=0; reloaded.dispatch(t,ctx(),()=>calls++,now+2); eq(calls,1);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now);
  eq(m.claim('SYNTHETIC-1',{...ctx(),consent:'denied'},now),null);
  eq(s.get('SYNTHETIC-1').state,'suppressed');
  eq(m.claim('SYNTHETIC-1',ctx(),now+1),null);
}
{ const [m,s]=fresh(); m.prepare(order(),true,now); const t=m.claim('SYNTHETIC-1',ctx(),now);
  eq(m.dispatch(t,{...ctx(),paid:false},()=>assert.fail('unpaid send'),now),false);
  eq(s.get(t.id).state,'ready');
  const t2=m.claim(t.id,ctx(),now+1); let calls=0;
  eq(m.dispatch(t2,ctx(),()=>calls++,now+1),true);
  eq(m.dispatch(t2,ctx(),()=>calls++,now+2),false); eq(calls,1);
}
console.log(JSON.stringify({scope:'isolated synthetic model',checks,passed:true,
  google_requests:0,real_orders:0,production_installed:false},null,2));
