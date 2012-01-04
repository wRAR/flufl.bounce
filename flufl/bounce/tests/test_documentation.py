# Copyright (C) 2004-2012 by Barry A. Warsaw
#
# This file is part of flufl.bounce.
#
# flufl.bounce is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# flufl.bounce is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.bounce.  If not, see <http://www.gnu.org/licenses/>.

"""Test harness for doctests."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    'additional_tests',
    ]


import os
import atexit
import doctest
import unittest

try:
    # Python 3
    from email import message_from_bytes as parse
except ImportError:
    # Python 2
    from email import message_from_string as parse

from pkg_resources import (
    resource_filename, resource_exists, resource_listdir, cleanup_resources)

from flufl.bounce.tests.helpers import initialize_logging


COMMASPACE = ', '
DOT = '.'
DOCTEST_FLAGS = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_NDIFF)



def stop():
    """Call into pdb.set_trace()"""
    # Do the import here so that you get the wacky special hacked pdb instead
    # of Python's normal pdb.
    import pdb
    pdb.set_trace()



def setup(testobj):
    """Test setup."""
    # Make sure future statements in our doctests match the Python code.  When
    # run with 2to3, the future import gets removed and these names are not
    # defined.
    try:
        testobj.globs['absolute_import'] = absolute_import
        testobj.globs['print_function'] = print_function
        testobj.globs['unicode_literals'] = unicode_literals
    except NameError:
        pass
    testobj.globs['stop'] = stop
    testobj.globs['parse'] = parse



def additional_tests():
    "Run the doc tests (README.rst and docs/*, if any exist)"
    initialize_logging()
    doctest_files = [
        os.path.abspath(resource_filename('flufl.bounce', 'README.rst'))]
    if resource_exists('flufl.bounce', 'docs'):
        for name in resource_listdir('flufl.bounce', 'docs'):
            if os.path.splitext(name)[1] in ('.txt', '.rst'):
                doctest_files.append(
                    os.path.abspath(
                        resource_filename('flufl.bounce', 'docs/%s' % name)))
    kwargs = dict(module_relative=False,
                  optionflags=DOCTEST_FLAGS,
                  setUp=setup,
                  )
    atexit.register(cleanup_resources)
    return unittest.TestSuite((
        doctest.DocFileSuite(*doctest_files, **kwargs)))
