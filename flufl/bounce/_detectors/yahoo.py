# Copyright (C) 1998-2012 by Barry A. Warsaw
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

"""Yahoo! has its own weird format for bounces."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Yahoo',
    ]


import re

from email.iterators import body_line_iterator
from email.utils import parseaddr
from flufl.enum import Enum
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


tcre = re.compile(r'message\s+from\s+yahoo\.\S+', re.IGNORECASE)
acre = re.compile(r'<(?P<addr>[^>]*)>:')
ecre = re.compile(r'--- Original message follows')


class ParseState(Enum):
    start = 0
    tag_seen = 1



@implementer(IBounceDetector)
class Yahoo:
    """Yahoo! bounce detection."""

    def process(self, msg):
        """See `IBounceDetector`."""
        # Yahoo! bounces seem to have a known subject value and something
        # called an x-uidl: header, the value of which seems unimportant.
        sender = parseaddr(msg.get('from', '').lower())[1] or ''
        if not sender.startswith('mailer-daemon@yahoo'):
            return NoFailures
        addresses = set()
        state = ParseState.start
        for line in body_line_iterator(msg):
            line = line.strip()
            if state is ParseState.start and tcre.match(line):
                state = ParseState.tag_seen
            elif state is ParseState.tag_seen:
                mo = acre.match(line)
                if mo:
                    addresses.add(mo.group('addr').encode('us-ascii'))
                    continue
                mo = ecre.match(line)
                if mo:
                    # We're at the end of the error response.
                    break
        return NoTemporaryFailures, addresses
