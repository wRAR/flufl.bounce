# Copyright (C) 2001-2011 by Barry A. Warsaw
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

"""LLNL's custom Sendmail bounce message."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'LLNL',
    ]


import re

from email.iterators import body_line_iterator
from zope.interface import implements

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


acre = re.compile(r',\s*(?P<addr>\S+@[^,]+),', re.IGNORECASE)



class LLNL:
    """LLNL's custom Sendmail bounce message."""

    implements(IBounceDetector)

    def process(self, msg):
        """See `IBounceDetector`."""

        for line in body_line_iterator(msg):
            mo = acre.search(line)
            if mo:
                return NoTemporaryFailures, set([mo.group('addr')])
        return NoFailures
