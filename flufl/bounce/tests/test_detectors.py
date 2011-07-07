# Copyright (C) 2011 by Barry A. Warsaw
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

"""Test the bounce detection modules."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'load_tests',
    ]


import unittest

from contextlib import closing
from email import message_from_file, message_from_string
from pkg_resources import resource_stream

from flufl.bounce._detectors.caiwireless import Caiwireless
from flufl.bounce._detectors.microsoft import Microsoft
from flufl.bounce._detectors.smtp32 import SMTP32
from flufl.bounce._detectors.tests.detectors import make_test_cases
from flufl.bounce.tests.helpers import initialize_logging



class OtherBounceTests(unittest.TestCase):
    def test_SMTP32_failure(self):
        # This file has no X-Mailer: header
        with closing(resource_stream('flufl.bounce.tests.data',
                                     'postfix_01.txt')) as fp:
            msg = message_from_file(fp)
        self.failIf(msg['x-mailer'] is not None)
        temporary, permanent = SMTP32().process(msg)
        self.failIf(temporary)
        self.failIf(permanent)

    def test_caiwireless(self):
        # BAW: this is a mostly bogus test; I lost the samples. :(
        msg = message_from_string("""\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

""")
        temporary, permanent = Caiwireless().process(msg)
        self.failIf(temporary)
        self.failIf(permanent)

    def test_microsoft(self):
        # BAW: similarly as above, I lost the samples. :(
        msg = message_from_string("""\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

""")
        temporary, permanent = Microsoft().process(msg)
        self.failIf(temporary)
        self.failIf(permanent)



def load_tests(loader, tests, pattern):
    """Interface to setuptools.py test runner."""
    initialize_logging()
    suite = unittest.TestSuite()
    for test_case in make_test_cases():
        suite.addTest(test_case)
    suite.addTest(unittest.makeSuite(OtherBounceTests))
    return suite
