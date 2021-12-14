import { newStopwatch } from "./stopwatch.js";
import { newController } from "./controller.js";
import { noop } from "./actions.js";


QUnit.module('stopwatch should', () => {
    QUnit.test('set to 0 with reset', assert => {
        var sw = newStopwatch(i => assert.strictEqual(i, 0))
        sw.reset()
    })
    QUnit.test('update continuously once started', assert => {
        const done = assert.async()
        assert.timeout(500)
        var counter = { count: 0 }
        var sw = newStopwatch(i => { counter.count++; console.log(`stopwatch ticker: ${i}`) })
        sw.start()
        setTimeout(() => { sw.stop(); assert.ok(counter.count > 5); done(); }, 100)
    })
})

QUnit.module('controller should', () => {
    QUnit.test('gracefully ignore unrecognized message categories', async assert => {
        var controller = newController({ noop: noop })
        try {
            await controller.process({ category: 'nonsense', payload: '' })
            assert.ok(true)
        } catch (e) {
            assert.ok(false, `Exception was thrown: ${e}`)
        }
    })
    QUnit.test('dispatch actions based on message category', async assert => {
        var counter = { count: 0 }
        var actions = { noop: noop, updateCounter: payload => { counter.count = payload; return noop; } }
        var message = { category: 'updateCounter', payload: 10 }
        var controller = newController(actions)
        await controller.process(message)
        assert.strictEqual(counter.count, message.payload, 'Check message processing')
    })
})