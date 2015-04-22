#!/usr/bin/env python
# -*- coding: utf-8 -*-
# grabber: grabs the mac screen at regular intervals
# https://github.com/bnomis/grabber
# (c) Simon Blanchard
from __future__ import print_function
import argparse
import os
import sys


def seq(options):
    for odir in options.directories:
        try:
            ls = os.listdir(odir)
        except Exception as e:
            print('Exception listing directory %s: %s' % (odir, e))
            return

        num_files = len(ls)
        if num_files > 1:
            ls.sort()
            count = 1
            for f in ls:
                root, ext = os.path.splitext(f)
                if ext == '.png':
                    name = '%s%04d.png' % (options.base, count)
                    if f != name:
                        frmname = os.path.join(odir, f)
                        toname = os.path.join(odir, name)
                        try:
                            os.rename(frmname, toname)
                        except Exception as e:
                            print('Exception renaming %s -> %s: %s' % (frmname, toname, e))
                    count += 1


def main():
    program_name = 'seq'
    usage_string = '%(prog)s [options] <directory>'
    __version__ = '0.1.0'
    version_string = '%(prog)s %(version)s' % {'prog': program_name, 'version': __version__}
    description_string = 'rename files in sequential ascending order'

    parser = argparse.ArgumentParser(
        prog=program_name,
        usage=usage_string,
        description=description_string,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version=version_string
    )

    parser.add_argument(
        '-b',
        '--base',
        default='grab',
        help='Base file name. Default: %(default)s.',
    )

    parser.add_argument(
        'directories',
        metavar='Directory',
        nargs='+',
        help='Directories to process'
    )

    options = parser.parse_args(sys.argv[1:])

    seq(options)


if __name__ == '__main__':
    main()
