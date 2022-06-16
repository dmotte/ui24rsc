#!/usr/bin/env python3

import ui24rsc


def test_obj2diff():
    equal, objdiff = ui24rsc.obj2diff({}, {})

    assert equal

    assert type(objdiff) is dict
    assert len(objdiff) == 0  # TODO
