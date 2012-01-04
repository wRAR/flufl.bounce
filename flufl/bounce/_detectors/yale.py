# Copyright (C) 2000-2012 by Barry A. Warsaw
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

"""Yale's mail server is pretty dumb.

Its reports include the end user's name, but not the full domain.  I think we
can usually guess it right anyway.  This is completely based on examination of
the corpse, and is subject to failure whenever Yale even slightly changes
their MTA. :(

"""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Yale',
    ]


import re

from email.utils import getaddresses
from flufl.enum import Enum
from io import BytesIO
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


scre = re.compile(b'Message not delivered to the following', re.IGNORECASE)
ecre = re.compile(b'Error Detail', re.IGNORECASE)
acre = re.compile(b'\\s+(?P<addr>\\S+)\\s+')


class ParseState(Enum):
    start = 0
    intro_found = 1



@implementer(IBounceDetector)
class Yale:
    """Parse Yale's bounces (or what used to be)."""

    def process(self, msg):
        """See `IBounceDetector`."""
        if msg.is_multipart():
            return NoFailures
        try:
            whofrom = getaddresses([msg.get('from', '')])[0][1]
            if not whofrom:
                return NoFailures
            username, domain = whofrom.split('@', 1)
        except (IndexError, ValueError):
            return NoFailures
        if username.lower() != 'mailer-daemon':
            return NoFailures
        parts = domain.split('.')
        parts.reverse()
        for part1, part2 in zip(parts, ('edu', 'yale')):
            if part1 != part2:
                return NoFailures
        # Okay, we've established that the bounce came from the mailer-daemon
        # at yale.edu.  Let's look for a name, and then guess the relevant
        # domains.
        names = set()
        body = BytesIO(msg.get_payload(decode=True))
        state = ParseState.start
        for line in body:
            if state is ParseState.start and scre.search(line):
                state = ParseState.intro_found
            elif state is ParseState.intro_found and ecre.search(line):
                break
            elif state is ParseState.intro_found:
                mo = acre.search(line)
                if mo:
                    names.add(mo.group('addr'))
        # Now we have a bunch of names, these are either @yale.edu or
        # @cs.yale.edu.  Add them both.
        addresses = set()
        for name in names:
            addresses.add(name + b'@yale.edu')
            addresses.add(name + b'@cs.yale.edu')
        return NoTemporaryFailures, addresses
