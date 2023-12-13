#!/usr/bin/env python3

import json

import ui24rsc


def test_obj2diff():
    equal, objdiff = ui24rsc.obj2diff({}, {})

    assert equal
    assert isinstance(objdiff, dict)
    assert len(objdiff) == 0

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
    assert json.dumps(objdiff) == \
        '{"foo": "XYZ", "sub01": {"ho": 3}, "sub02": {"2": 10}}'


def test_obj2full():
    objfull = ui24rsc.obj2full({}, {})

    assert isinstance(objfull, dict)
    assert len(objfull) == 0

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

    assert json.dumps(objfull) == \
        '{"baz": 123, "foo": "XYZ", "sub01": {"hey": 1, "ho": 3}, "sub02": [4, 5, 10, 7]}'


def test_obj2tree():
    objtree = ui24rsc.obj2tree({})

    assert isinstance(objtree, dict)
    assert len(objtree) == 0

    objtree = ui24rsc.obj2tree(
        {
            'one.two.three': 3,
            'one.two.six': 6,
            'one.seven': 7,
        }
    )

    assert json.dumps(objtree) == \
        '{"one": {"two": {"three": 3, "six": 6}, "seven": 7}}'


def test_obj2dots():
    objdots = ui24rsc.obj2dots({})

    assert isinstance(objdots, dict)
    assert len(objdots) == 0

    objdots = ui24rsc.obj2dots(
        {
            'one': {
                'two': {'three': 3, 'six': 6},
                'seven': 7,
            },
        }
    )

    assert json.dumps(objdots) == \
        '{"one.two.three": 3, "one.two.six": 6, "one.seven": 7}'


def test_obj2sort():
    obj = ui24rsc.objsort({})

    assert isinstance(obj, dict)
    assert len(obj) == 0

    obj = ui24rsc.objsort(
        {
            'b': 123,
            'a': 456,
            'sub01': {'x': {}, 'f': 'g'},
            'name': 'xyz',
            'sub02': [9, 3, 7],
        }
    )

    assert json.dumps(obj) == \
        '{"name": "xyz", "a": 456, "b": 123, "sub02": [9, 3, 7], "sub01": {"f": "g", "x": {}}}'
