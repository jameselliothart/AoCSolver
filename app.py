from collections import namedtuple
from functools import singledispatch
from flask import Flask, request
from flask.json import jsonify
from flask.templating import render_template
from flask.logging import create_logger
from importlib import import_module
import asyncio

from werkzeug.wrappers.request import Request


app = Flask(__name__)
LOG = create_logger(app)


Ok = namedtuple('Ok', 'data')
Failure = namedtuple('Failure', 'message')


async def thread_solve(solver, data):
    result = await asyncio.to_thread(solver, data)
    return result


def get_form_data(form):
    (year, day, puzzle_input) = (int(form.get('year')),
                                 int(form.get('day')), form.get('puzzleInput').splitlines())
    if year in [2021] and day in range(26):
        return Ok((year, day, puzzle_input))
    return Failure(f'Year/day {year}/{day} outside of accepted range 2021/1-25')


@singledispatch
def solve_puzzle(form_result):
    raise NotImplementedError(f'Unrecognized form result {form_result=}')


@solve_puzzle.register
def _(form_result: Failure):
    return jsonify(
        category='failure',
        payload=f'Error: {form_result.message}',
    )


@solve_puzzle.register
async def _(form_result: Ok):
    (_, day, puzzle_input) = form_result.data
    solver = import_module(f'{day}')
    part_1 = await asyncio.wait_for(thread_solve(solver.part_one, puzzle_input), timeout=5)
    part_2 = await asyncio.wait_for(thread_solve(solver.part_two, puzzle_input), timeout=5)
    return jsonify(
        category='success',
        payload={
            'part1': part_1,
            'part2': part_2,
        }
    )


async def get_response(req: Request):
    try:
        form_data = get_form_data(req.form)
        response = await solve_puzzle(form_data)
    except asyncio.TimeoutError:
        LOG.warning('Puzzle took too long to solve!', exc_info=1)
        response = jsonify(
            category='timeout',
            payload='Uh oh! It took too long to solve this puzzle...',
        )
    except Exception as e:
        app.log_exception(e)
        response = jsonify(
            category='failure',
            payload='Oops! An error occurred while solving the puzzle.'
        )

    return response


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/test')
def test():
    return render_template('test.html')


@app.post('/solve')
async def solve():
    return await get_response(request)


if __name__ == '__main__':
    app.run()
