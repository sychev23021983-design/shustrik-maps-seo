const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(__dirname + '/shustrik-ecommerce-funnel.js', 'utf8');
function fixture(event = 'view_item', loading = false) {
    const calls = [], timers = [], listeners = [];
    const window = {
        shustrikEcommerceFunnel: {event, data: {currency: 'USD', value: 32, items: [{item_id: '11517', price: 32, quantity: 1}]}},
        _googlesitekit: {gtagEvent: (...args) => calls.push(args)},
        setTimeout: fn => timers.push(fn),
        gtag: () => { throw Error('Must not bypass Site Kit'); },
    };
    const document = {readyState: loading ? 'loading' : 'complete', addEventListener: (event, fn, options) => {
        assert.equal(event, 'DOMContentLoaded'); assert.equal(options.once, true); listeners.push(fn);
    }};
    const context = vm.createContext({window, document});
    return {window, calls, timers, listeners, run: () => vm.runInContext(source, context)};
}
let count = 0;
function test(name, fn) { fn(); count++; console.log('PASS ' + name); }
for (const event of ['view_item', 'begin_checkout']) test(event + ' once per document', () => {
    const f = fixture(event); f.run(); f.run(); assert.equal(f.calls.length, 1); assert.equal(f.calls[0][0], event);
});
for (const event of ['add_to_cart', 'purchase', 'page_view']) test('reject ' + event, () => {
    const f = fixture(event); f.run(); assert.equal(f.calls.length, 0);
});
test('Site Kit opt-out', () => { const f = fixture(); f.window['ga-disable-G-TEST'] = true; f.run(); assert.equal(f.calls.length, 0); });
test('missing wrapper fails closed after bounded wait', () => {
    const f = fixture(); delete f.window._googlesitekit; f.run(); let retries = 0;
    while (f.timers.length) { f.timers.shift()(); retries++; assert.ok(retries <= 19); }
    assert.equal(retries, 19); assert.equal(f.calls.length, 0);
});
test('late wrapper sends once', () => {
    const f = fixture(); const kit = f.window._googlesitekit; delete f.window._googlesitekit; f.run();
    f.window._googlesitekit = kit; f.timers.shift()(); f.run(); assert.equal(f.calls.length, 1);
});
test('opt-out during wait', () => {
    const f = fixture(); delete f.window._googlesitekit; f.run(); f.window['ga-disable-G-TEST'] = true;
    f.timers.shift()(); assert.equal(f.timers.length, 0); assert.equal(f.calls.length, 0);
});
test('DOMContentLoaded waits and deduplicates script execution', () => {
    const f = fixture('begin_checkout', true); f.run(); f.run(); assert.equal(f.calls.length, 0);
    assert.equal(f.listeners.length, 1); f.listeners[0](); assert.equal(f.calls.length, 1);
});
test('empty cart does not send', () => { const f = fixture(); f.window.shustrikEcommerceFunnel.data.items = []; f.run(); assert.equal(f.calls.length, 0); });
console.log(count + ' checks passed');
