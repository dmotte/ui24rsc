#!/usr/bin/env python3

from pprint import pformat


# Src: https://github.com/dmotte/misc/tree/main/snippets
def pfmt(x: object) -> str:
    '''
    Like pprint.pformat but preserves the order of dict keys.
    Useful for strict deep comparison of objects
    '''
    return pformat(x, sort_dicts=False)
