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

"""Parse bounce messages generated by Postfix.

This also matches something called 'Keftamail' which looks just like Postfix
bounces with the word Postfix scratched out and the word 'Keftamail' written
in in crayon.

It also matches something claiming to be 'The BNS Postfix program', and
'SMTP_Gateway'.  Everybody's gotta be different, huh?
"""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Postfix',
    ]


import re

from flufl.enum import Enum
from io import BytesIO
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


# Are these heuristics correct or guaranteed?
pcre = re.compile(
    b'[ \\t]*the\\s*(bns)?\\s*(postfix|keftamail|smtp_gateway)',
    re.IGNORECASE)
rcre = re.compile(b'failure reason:$', re.IGNORECASE)
acre = re.compile(b'<(?P<addr>[^>]*)>:')

REPORT_TYPES = ('multipart/mixed', 'multipart/report')


class ParseState(Enum):
    start = 0
    salutation_found = 1



def flatten(msg, leaves):
    # Give us all the leaf (non-multipart) subparts.
    if msg.is_multipart():
        for part in msg.get_payload():
            flatten(part, leaves)
    else:
        leaves.append(msg)



def findaddr(msg):
    addresses = set()
    body = BytesIO(msg.get_payload(decode=True))
    state = ParseState.start
    for line in body:
        # Preserve leading whitespace.
        line = line.rstrip()
        # Yes, use match() to match at beginning of string.
        if state is ParseState.start and (
            pcre.match(line) or rcre.match(line)):
            # Then...
            state = ParseState.salutation_found
        elif state is ParseState.salutation_found and line:
            mo = acre.search(line)
            if mo:
                addresses.add(mo.group('addr'))
            # Probably a continuation line.
    return addresses



@implementer(IBounceDetector)
class Postfix:
    """Parse bounce messages generated by Postfix."""

    def process(self, msg):
        """See `IBounceDetector`."""
        if msg.get_content_type() not in REPORT_TYPES:
            return NoFailures
        # We're looking for the plain/text subpart with a Content-Description:
        # of 'notification'.
        leaves = []
        flatten(msg, leaves)
        for subpart in leaves:
            content_type = subpart.get_content_type()
            content_desc = subpart.get('content-description', '').lower()
            if content_type == 'text/plain' and content_desc == 'notification':
                return NoTemporaryFailures, set(findaddr(subpart))
        return NoFailures
