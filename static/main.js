function newStopwatch(displayer) {
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

function newController(stopwatch) {
    const noAnswer = { 'part1': '', 'part2': '' }
    const noop = { category: 'noop', payload: '' }

    const hideError = () => document.getElementById('errorSection').hidden = true

    const updateAnswer = data => {
        document.getElementById('solution1').innerText = data.part1
        document.getElementById('solution2').innerText = data.part2
    }

    const showError = data => {
        document.getElementById('errorSection').hidden = false
        document.getElementById('errorText').innerText = data
    }

    const resetForm = () => document.getElementById('puzzleInput').value = ''

    const solve = async formData => {
        const resp = await fetch('/solve', {
            method: 'POST',
            body: formData
        })
        return await resp.json()
    }

    const actions = {
        solve: async payload => { stopwatch.start(); return await solve(payload); },
        success: payload => { hideError(); updateAnswer(payload); stopwatch.stop(); return noop; },
        timeout: payload => { showError(payload); updateAnswer(noAnswer); stopwatch.stop(); return noop; },
        failure: payload => { showError(payload); updateAnswer(noAnswer); stopwatch.stop(); return noop; },
        reset: _ => { hideError(); updateAnswer(noAnswer); resetForm(); stopwatch.reset(); return noop; },
        unrecognized: category => { console.error(`Unrecognized message category [${category}]!`); return noop; },
    }

    async function process(message) {
        var action = actions[message.category] || function (_) { actions.unrecognized(message.category) }
        var result = await action(message.payload)
        if (result.category != noop.category) {
            process(result)
        }
    }

    return { process: process }

}

function main() {
    const updateCalcTime = ms => document.getElementById('calcTime').innerText = `${ms / 1000}s`

    const controller = newController(newStopwatch(updateCalcTime))

    function addSubmit(ev) {
        ev.preventDefault()
        var message = {
            category: 'solve',
            payload: new FormData(this)
        }
        controller.process(message)
    }

    function addReset(ev) {
        ev.preventDefault()
        message = {
            'category': 'reset',
            'payload': '',
        }
        controller.process(message)
    }

    document.getElementById('solve').addEventListener('submit', addSubmit)

    document.getElementById('clear-button').addEventListener('click', addReset)
}

main()
