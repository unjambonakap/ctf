#!/usr/bin/env python

from chdrft.utils.misc import cwdpath, failsafe, JsonUtils, path_from_script
from chdrft.utils.cache import cache_argparse, CacheDB
from chdrft.utils.string import str_dist
from uc.uc import uc, get_level_dumpname
import argparse
import logging
import os
import re



def do_get_snapshot(x, level, outdir):
    print('getting level ', level)
    outfile = os.path.join(outdir, get_level_dumpname(level))
    if os.path.isfile(outfile):
        print('{} already exists, skipping'.format(level))
        return
    x.set_level(level)
    x.load()
    x.reset()

    y = JsonUtils()
    res = y.encode(x.get_snapshot())
    with open(outfile, 'w') as f:
        f.write(res)


def get_snapshot(args, x):
    levels = [x.value for x in list(uc.Levels)]
    if args.all:
        for level in levels:
            do_get_snapshot(x, level, args.out)
    else:
        choice = args.level
        tb = []
        for level in levels:
            tb.append((str_dist(level, choice, case=False), level))
        tb.sort()
        best = tb[0][0]
        if best == tb[1][0] and best >= len(choice)//2:
            print('could not decide between {} and {}'.format(
                tb[0][1],
                tb[1][1]))
            assert False
        do_get_snapshot(x, tb[0][1], args.out)


def get_levels(args, x):
    levels = x.get_levels()
    tmp = [x['name'] for x in levels]
    print('\n'.join(tmp))
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', type=str, default='jambonkappa')
    parser.add_argument('--cookiejar', type=cwdpath,
                        default=cwdpath('cookie.txt'))
    parser.add_argument('-v', '--verbose', action='store_true')

    default_outdir = path_from_script(__file__, '../data')
    subp = parser.add_subparsers()
    x = subp.add_parser('get_levels')
    x.set_defaults(func=get_levels)

    x = subp.add_parser('get_snapshot')
    x.add_argument('--level', type=str)
    x.add_argument('--all', action='store_true')
    x.add_argument('--out', type=cwdpath, default=default_outdir)
    x.set_defaults(func=get_snapshot)

    cache_argparse(parser)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    with CacheDB.load_from_argparse(args) as cache:
        x = uc(args.login, args.cookiejar, cache=cache)
        x.root()
        failsafe(lambda: x.kill())
        args.func(args, x)
