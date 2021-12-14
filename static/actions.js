import { newStopwatch } from "./stopwatch.js";

const updateCalcTime = ms => document.getElementById('calcTime').innerText = `${ms / 1000}s`
const sw = newStopwatch(updateCalcTime)

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

const noAnswer = { part1: '', part2: '' }
export const noop = { category: 'noop', payload: '' }
export function newTerminatingAction(fn) {
    const action = payload => {
        fn(payload)
        return noop
    }
    return action
}

export const defaultActions = {
    solve: async payload => { sw.start(); return await solve(payload); },
    success: newTerminatingAction(payload => { hideError(); updateAnswer(payload); sw.stop(); }),
    timeout: newTerminatingAction(payload => { showError(payload); updateAnswer(noAnswer); sw.stop(); }),
    failure: newTerminatingAction(payload => { showError(payload); updateAnswer(noAnswer); sw.stop(); }),
    reset: newTerminatingAction(_ => { hideError(); updateAnswer(noAnswer); resetForm(); sw.reset(); }),
}