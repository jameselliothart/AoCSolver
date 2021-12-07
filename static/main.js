const NO_ANSWER = { 'part1': '', 'part2': '' }

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

const updateCalcTime = ms => document.getElementById('calcTime').innerText = `${ms / 1000}s`

function newStopwatch(displayer) {
    var running = false

    function inc(val) {
        setTimeout(function () {
            if (running) {
                displayer(val++)
                console.log(val)
                inc(val)
            }
        }, 1)
    }
    function start() { running = true; inc(0) }
    function stop() { running = false }

    var sw = { stop: stop, start: start }

    return sw
}

const solve = formData => {
    fetch('/solve', {
        method: 'POST',
        body: formData
    })
        .then(resp => resp.json())
        .then(processMessage)
}

function newMessageProcessor() {
    sw = newStopwatch(updateCalcTime)
    var actions = {
        'solve': payload => {sw.start(); solve(payload); },
        'success': payload => { hideError(); updateAnswer(payload); sw.stop(); },
        'timeout': payload => { showError(payload); updateAnswer(NO_ANSWER); sw.stop(); },
        'failure': payload => { showError(payload); updateAnswer(NO_ANSWER); sw.stop(); },
        'reset': _ => { hideError(); updateAnswer(NO_ANSWER); resetForm(); updateCalcTime(0); },
        'unrecognized': category => console.error(`Unrecognized message category [${category}]!`),
    }

    function process(message) {
        var action = actions[message.category] || function (_) { actions.unrecognized(message.category) }
        action(message.payload)
    }

    return {process: process}

}

const PROCESSOR = newMessageProcessor()

function processMessage(message) {
    PROCESSOR.process(message)
}

function addSubmit(ev) {
    ev.preventDefault()
    var message = {
        category: 'solve',
        payload: new FormData(this)
    }
    processMessage(message)
}

function addReset(ev) {
    ev.preventDefault()
    message = {
        'category': 'reset',
        'payload': '',
    }
    processMessage(message)
}

function main() {
    var form = document.getElementById('solve')
    form.addEventListener('submit', addSubmit)

    var clear = document.getElementById('clear-button')
    clear.addEventListener('click', addReset)
}

main()
