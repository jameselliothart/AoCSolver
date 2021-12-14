import { defaultActions, noop, newTerminatingAction } from "./actions.js";

export function newController(actions) {
    const _actions = actions

    const invalidAction = newTerminatingAction(category => console.warn(`Unrecognized message category [${category}]!`))

    async function process(message) {
        var action = _actions[message.category] || function (_) { return invalidAction(message.category) }
        var result = await action(message.payload)
        if (result.category != noop.category) {
            process(result)
        }
    }

    return { process: process }

}

export function defaultController() { return newController(defaultActions) }