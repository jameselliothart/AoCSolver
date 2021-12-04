from flask import Flask, request
from flask.json import jsonify
from flask.templating import render_template
from importlib import import_module
import asyncio


app = Flask(__name__)


async def thread_solve(solver, data):
    result = await asyncio.to_thread(solver, data)
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.post('/solve')
async def solve():
    (_, day, puzzle_input) = (
        request.form.get('year', 2021), request.form.get('day', 1), request.form.get('puzzleInput').split())
    solver = import_module(day)
    try:
        part_1 = await asyncio.wait_for(thread_solve(solver.main, puzzle_input), timeout=5)
        part_2 = await asyncio.wait_for(thread_solve(solver.main2, puzzle_input), timeout=5)
        response = jsonify(
            {
                'part1': part_1,
                'part2': part_2,
            }
        )
    except asyncio.TimeoutError:
        response = jsonify(
            {
                'part1': 'took',  # solver.main(puzzle_input),
                'part2': 'too long'  # solver.main2(puzzle_input),
            }
        )

    return response


if __name__ == '__main__':
    app.run()
