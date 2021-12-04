function addSubmit(ev) {
    ev.preventDefault()
    fetch('/solve', {
        method: 'POST',
        body: new FormData(this)
    })
        .then(resp => resp.json())
        .then(addShow)
}


function addShow(data) {
    var part1 = document.getElementById('solution1');
    var part2 = document.getElementById('solution2');
    part1.innerText = data['part1']
    part2.innerText = data['part2']
}

function addClear(ev) {
    ev.preventDefault()
    var puzzleInput = document.getElementById('puzzleInput')
    var solutions = document.getElementsByClassName('solution')
    puzzleInput.value = ''
    for (const e of solutions) {
        e.innerHTML = ''
    }
}

var form = document.getElementById('solve')
form.addEventListener('submit', addSubmit)

var clear = document.getElementById('clear-button')
clear.addEventListener('click', addClear)
