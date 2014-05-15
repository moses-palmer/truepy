# coding=utf-8
'''
truepy
Copyright (C) 2014 Moses Palmér

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
'''

def main(**args):
    # TODO: Implement
    return 0


import argparse
import sys

parser = argparse.ArgumentParser(prog = 'truepy', description =
    'Creates and verifies TrueLicense version 1 licenses')

try:
    sys.exit(main(**vars(parser.parse_args())))
except Exception as e:
    try:
        sys.stderr.write('%s\n' % e.args[0] % e.args[1:])
    except:
        sys.stderr.write('%s\n' % str(e))
    sys.exit(1)
