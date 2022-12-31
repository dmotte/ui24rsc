#!/usr/bin/env python3

import argparse
from functools import reduce
import json
import os
import sys

import yaml


def obj2diff(objfull, objref):
    '''
    Converts a snapshot object from Soundcraft Ui24R full format to custom diff
    format using objref as reference object.
    The first return value is True if objfull is equal to objref and False
    otherwise. The second return value is the object in the diff format
    '''
    if type(objref) is not dict and type(objref) is not list:
        if objfull == objref:
            return True, None
        else:
            return False, objfull

    objdiff = {}

    if type(objref) is dict:
        keys = objref.keys()
    else:
        keys = range(min(len(objfull), len(objref)))

    for k in keys:
        e, d = obj2diff(objfull[k], objref[k])
        if not e:
            objdiff[k] = d

    if objdiff:
        return False, objdiff
    else:
        return True, {}


def obj2full(objdiff, objref):
    '''
    Converts a snapshot object from custom diff format to Soundcraft Ui24R full
    format using objref as reference object.
    The return value is the object in the full format
    '''
    if type(objref) is not dict and type(objref) is not list:
        return objdiff

    if type(objref) is dict:
        objfull = {}
        keys = objref.keys()
    else:
        objfull = [None] * len(objref)  # List with pre-defined size
        keys = range(len(objref))

    for k in keys:
        if k in objdiff.keys():
            objfull[k] = obj2full(objdiff[k], objref[k])
        else:
            objfull[k] = objref[k]

    return objfull


def obj2tree(objdots):
    '''
    Converts a snapshot object from Soundcraft Ui24R dotted format to tree
    format
    '''
    objtree = {}

    for key, val in objdots.items():
        # Avoid problems with "vg.*" keys
        if key.startswith('vg.') and len(key) == 4:
            key = 'vg.' + key[3] + '.content'

        path = key.split('.')

        # Create the structure down to key
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], objtree)

        target[path[-1]] = val

    return objtree


def obj2dots(objtree, path=''):
    '''
    Converts a snapshot object from tree format to Soundcraft Ui24R dotted
    format
    '''
    if path == 'LOCAL':  # The 'LOCAL' root object is preserved as it is
        return {'LOCAL': objtree}

    objdots = {}

    if type(objtree) is dict:
        prefix = '' if path == '' else path + '.'
        for k, v in objtree.items():
            objdots.update(obj2dots(v, prefix + k))
    elif type(objtree) is list:
        prefix = '' if path == '' else path + '.'
        for i, v in enumerate(objtree):
            objdots.update(obj2dots(v, prefix + str(i)))
    else:
        if path.startswith('vg.') and path.endswith('.content') \
                and len(path) == 12:
            path = 'vg.' + path[3]  # Restore "vg.*" keys
        objdots[path] = objtree

    return objdots


def objsort(obj):
    '''
    Recursively sorts an object according to special rules. Returns the sorted
    object
    '''
    if type(obj) is dict:
        if len(obj) == 0:
            return obj
        elif next(iter(obj)) == '0':
            # Numerical sorting
            return {k: objsort(v)
                    for k, v in sorted(obj.items(), key=lambda x: int(x[0]))}
        else:
            tmp = dict(sorted(obj.items()))
            result = {}

            if 'name' in tmp:
                # If present, name should be the first attribute
                result['name'] = tmp.pop('name')

            result.update({k: v for k, v in tmp.items()
                           if type(v) is not dict
                           and type(v) is not list})
            result.update({k: objsort(v) for k, v in tmp.items()
                           if type(v) is list})
            result.update({k: objsort(v) for k, v in tmp.items()
                           if type(v) is dict})

            return result
    elif type(obj) is list:
        return [objsort(x) for x in obj]
    else:
        return obj


DEFAULT_INIT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'default-init.yml')


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Converts a Soundcraft Ui24R snapshot file from/to '
        'different formats'
    )

    parser.add_argument('actions', metavar='ACTIONS', type=str,
                        help='Comma-separated sequence of operations to be '
                        'performed. Examples: "diff,tree" "dots,full" '
                        '"tree,sort"')
    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: -)')
    parser.add_argument('file_out', metavar='FILE_OUT', type=str,
                        nargs='?', default='-',
                        help='Output file. If set to "-" then stdout is used '
                        '(default: -)')

    parser.add_argument('-j', '--json', action='store_true',
                        help='If present, the output format will be forced to '
                        'JSON')
    parser.add_argument('-y', '--yaml', action='store_true',
                        help='If present, the output format will be forced to '
                        'YAML')

    args = vars(parser.parse_args(argv[1:]))

    actions = [x.strip().lower() for x in args['actions'].split(',')]
    file_in = args['file_in']
    file_out = args['file_out']
    force_json = args['json']
    force_yaml = args['yaml']

    if force_json and force_yaml:
        print('Error: both --json and --yaml flags specified', file=sys.stderr)
        return 1

    ############################################################################

    with open(DEFAULT_INIT_PATH, 'r') as f:
        objref = yaml.safe_load(f)
        objref = obj2dots(objref)

    ############################################################################

    if file_in == '-':
        obj = yaml.safe_load(sys.stdin)
    else:
        with open(file_in, 'r') as f:
            obj = yaml.safe_load(f)

    ############################################################################

    format = 'json' if force_json else 'yaml'

    funcs = {
        'diff': lambda x: obj2diff(x, objref)[1],
        'full': lambda x: obj2full(x, objref),
        'tree': obj2tree,
        'dots': obj2dots,
        'sort': objsort,
    }

    for a in actions:
        if a not in funcs:
            print('Unsupported action:', a, file=sys.stderr)
            return 1
        if a in ['diff', 'tree'] and not force_json:
            format = 'yaml'
        if a in ['full', 'dots'] and not force_yaml:
            format = 'json'
        obj = funcs[a](obj)

    ############################################################################

    if format == 'json':
        if file_out == '-':
            json.dump(obj, sys.stdout)
        else:
            with open(file_out, 'w') as f:
                json.dump(obj, f)
    else:
        if file_out == '-':
            yaml.safe_dump(obj, sys.stdout, sort_keys=False)
        else:
            with open(file_out, 'w') as f:
                yaml.safe_dump(obj, f, sort_keys=False)

    return 0
