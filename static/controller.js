import { actions } from "./actions.js";

export function newController(actions) {
    const _actions = actions

    const invalidAction = category => { console.warn(`Unrecognized message category [${category}]!`); return _actions.noop; }

    async function process(message) {
        var action = _actions[message.category] || function (_) { return invalidAction(message.category) }
        var result = await action(message.payload)
        if (result.category != _actions.noop.category) {
            process(result)
        }
    }

    return { process: process }

}

export function defaultController() { return newController(actions) }