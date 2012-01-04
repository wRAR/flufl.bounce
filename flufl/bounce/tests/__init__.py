# Copyright (C) 2012 by Barry A. Warsaw
#
# This file is part of flufl.bounce
#
# flufl.bounce is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# flufl.bounce is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.bounce.  If not, see <http://www.gnu.org/licenses/>.

"""Python 2.7 and 3.2+ unittest discover support."""

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type
__all__ = [
    #'load_tests',
    ]


# XXX This is *supposed* to support `python -m unittest discover`,
# specifically to find the doctests and dynamically created tests that
# discovery normally wouldn't find.  Unfortunately, this function (when named
# `load_tests()`) doesn't seem to get called when using unittest discovery.
#
# It *does* seem to be called by distribute's `python setup.py test` support,
# which makes no sense (it's undocumented AFAICT).  And in that case, it
# messes with the tests by running the setup.py's discovered tests twice.
# This is because `additional_tests()` is added twice, once automatically by
# distribute and then explicitly here.
#
# SIGH.
#
# For now, disable unittest discovery.



def XXX_load_tests(loader, standard_tests, pattern):
    # For `python -m unittest discover` support, this must return *all* tests
    # that the suite wants to run, including doctests.
    print('loader:', loader)
    print('standard tests:', standard_tests)
    print('pattern:', pattern)
    from . import test_detectors
    suite = test_detectors.additional_tests()
    # Add all the standard tests because discovery will stop when it finds
    # load_tests(), so the standard tests won't be run automatically.
    suite.addTests(standard_tests)
    # Add the doctests.
    from .test_documentation import additional_tests
    suite.addTests(additional_tests())
    return suite
