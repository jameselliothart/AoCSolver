const NO_ANSWER = { 'part1': '', 'part2': '' }

const hideError = () => document.getElementById('errorSection').hidden = true

const updateAnswer = data => {
    var part1 = document.getElementById('solution1');
    var part2 = document.getElementById('solution2');
    part1.innerText = data.part1
    part2.innerText = data.part2
}

const showError = data => {
    var errorSection = document.getElementById('errorSection')
    var errorText = document.getElementById('errorText')
    errorSection.hidden = false
    errorText.innerText = data
}

const resetForm = () => document.getElementById('puzzleInput').value = ''

function processMessage(message) {
    var actions = {
        'success': payload => { hideError(); updateAnswer(payload); },
        'timeout': payload => { showError(payload); updateAnswer(NO_ANSWER); },
        'failure': payload => { showError(payload); updateAnswer(NO_ANSWER); },
        'reset': _ => { hideError(); updateAnswer(NO_ANSWER); resetForm() },
        'unrecognized': category => console.error(`Unrecognized message category [${category}]!`),
    }
    var action = actions[message.category] || function (_) { actions.unrecognized(message.category) }
    action(message.payload)
}

function addSubmit(ev) {
    ev.preventDefault()
    fetch('/solve', {
        method: 'POST',
        body: new FormData(this)
    })
        .then(resp => resp.json())
        .then(processMessage)
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
