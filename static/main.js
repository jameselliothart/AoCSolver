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

    var sw = { stop: stop, start: start }

    return sw
}

function newController(stopwatch) {
    const NO_ANSWER = { 'part1': '', 'part2': '' }
    const NOOP = {category: 'noop', payload: ''}

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
        'solve': async payload => { stopwatch.start(); return await solve(payload); },
        'success': payload => { hideError(); updateAnswer(payload); stopwatch.stop(); return NOOP; },
        'timeout': payload => { showError(payload); updateAnswer(NO_ANSWER); stopwatch.stop(); return NOOP; },
        'failure': payload => { showError(payload); updateAnswer(NO_ANSWER); stopwatch.stop(); return NOOP; },
        'reset': _ => { hideError(); updateAnswer(NO_ANSWER); resetForm(); updateCalcTime(0); return NOOP; },
        'unrecognized': category => {console.error(`Unrecognized message category [${category}]!`); return NOOP; },
    }

    async function process(message) {
        var action = actions[message.category] || function (_) { actions.unrecognized(message.category) }
        var result = await action(message.payload)
        if (result.category != NOOP.category) {
            process(result)
        }
    }

    return { process: process }

}

const updateCalcTime = ms => document.getElementById('calcTime').innerText = `${ms / 1000}s`

const CONTROLLER = newController(newStopwatch(updateCalcTime))

function addSubmit(ev) {
    ev.preventDefault()
    var message = {
        category: 'solve',
        payload: new FormData(this)
    }
    CONTROLLER.process(message)
}

function addReset(ev) {
    ev.preventDefault()
    message = {
        'category': 'reset',
        'payload': '',
    }
    CONTROLLER.process(message)
}

function main() {
    var form = document.getElementById('solve')
    form.addEventListener('submit', addSubmit)

    var clear = document.getElementById('clear-button')
    clear.addEventListener('click', addReset)
}

main()
