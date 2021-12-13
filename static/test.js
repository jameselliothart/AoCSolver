import { newStopwatch } from "./stopwatch.js";

QUnit.module('stopwatch should', function() {
    QUnit.test('set to 0 with reset', function(assert) {
        var sw = newStopwatch(i => assert.equal(i, 0))
        sw.reset()
    })
});