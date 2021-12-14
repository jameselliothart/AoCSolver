import { defaultController } from "./controller.js";

function main(controller) {
    const _controller = controller

    function addSubmit(ev) {
        ev.preventDefault()
        var message = {
            category: 'solve',
            payload: new FormData(this)
        }
        _controller.process(message)
    }

    function addReset(ev) {
        ev.preventDefault()
        var message = {
            category: 'reset',
            payload: '',
        }
        _controller.process(message)
    }

    document.getElementById('solve').addEventListener('submit', addSubmit)

    document.getElementById('clear-button').addEventListener('click', addReset)
}

main(defaultController())
