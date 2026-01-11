#!/usr/bin/env python3

import json

import ui24rsc

from util import pfmt


def test_obj2diff() -> None:
    equal, objdiff = ui24rsc.obj2diff({}, {})

    assert equal
    assert pfmt(objdiff) == '{}'

    equal, objdiff = ui24rsc.obj2diff(
        {
            'baz': 123,
            'foo': 'XYZ',
            'sub01': {'hey': 1, 'ho': 3},
            'sub02': [4, 5, 10, 7],
        },
        {
            'baz': 123,
            'foo': 'bar',
            'sub01': {'hey': 1, 'ho': 2},
            'sub02': [4, 5, 6, 7],
        },
    )

    assert not equal
    assert pfmt(objdiff) == pfmt({
        'foo': 'XYZ',
        'sub01': {'ho': 3},
        'sub02': {2: 10},
    })


def test_obj2full() -> None:
    objfull = ui24rsc.obj2full({}, {})

    assert pfmt(objfull) == '{}'

    objfull = ui24rsc.obj2full(
        {
            'foo': 'XYZ',
            'sub01': {'ho': 3},
            'sub02': {2: 10},
        },
        {
            'baz': 123,
            'foo': 'bar',
            'sub01': {'hey': 1, 'ho': 2},
            'sub02': [4, 5, 6, 7],
        },
    )

    assert pfmt(objfull) == pfmt({
        'baz': 123,
        'foo': 'XYZ',
        'sub01': {'hey': 1, 'ho': 3},
        'sub02': [4, 5, 10, 7],
    })


def test_obj2tree() -> None:
    objtree = ui24rsc.obj2tree({})

    assert pfmt(objtree) == '{}'

    objtree = ui24rsc.obj2tree(
        {'one.two.three': 3, 'one.two.six': 6, 'one.seven': 7})

    assert pfmt(objtree) == pfmt(
        {'one': {'two': {'three': 3, 'six': 6}, 'seven': 7}})


def test_obj2dots() -> None:
    objdots = ui24rsc.obj2dots({})

    assert pfmt(objdots) == '{}'

    objdots = ui24rsc.obj2dots(
        {'one': {'two': {'three': 3, 'six': 6}, 'seven': 7}})

    assert pfmt(objdots) == pfmt({
        'one.two.three': 3,
        'one.two.six': 6,
        'one.seven': 7,
    })


def test_obj2sort() -> None:
    obj = ui24rsc.objsort({})

    assert pfmt(obj) == '{}'

    obj = ui24rsc.objsort(
        {
            'b': 123,
            'a': 456,
            'sub01': {'x': {}, 'f': 'g'},
            'name': 'xyz',
            'sub02': [9, 3, 7],
        }
    )

    assert pfmt(obj) == pfmt({
        'name': 'xyz',
        'a': 456,
        'b': 123,
        'sub02': [9, 3, 7],
        'sub01': {'f': 'g', 'x': {}},
    })
