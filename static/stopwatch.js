export function newStopwatch(displayer) {
    var running = false

    function inc(val) {
        setTimeout(function () {
            if (running) {
                displayer(val++)
                inc(val)
            }
        }, 1)
    }
    function start() { running = true; inc(0) }
    function stop() { running = false }
    function reset() { displayer(0) }

    var sw = { stop: stop, start: start, reset: reset }

    return sw
}
