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

"""Microsoft's `SMTPSVC' nears I kin tell."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'Microsoft',
    ]


import re

from flufl.enum import Enum
from io import BytesIO
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


scre = re.compile(br'transcript of session follows', re.IGNORECASE)


class ParseState(Enum):
    start = 0
    tag_seen = 1



@implementer(IBounceDetector)
class Microsoft:
    """Microsoft's `SMTPSVC' nears I kin tell."""

    def process(self, msg):
        if msg.get_content_type() != 'multipart/mixed':
            return NoFailures
        # Find the first subpart, which has no MIME type.
        try:
            subpart = msg.get_payload(0)
        except IndexError:
            # The message *looked* like a multipart but wasn't.
            return NoFailures
        data = subpart.get_payload(decode=True)
        if isinstance(data, list):
            # The message is a multi-multipart, so not a matching bounce.
            return NoFailures
        body = BytesIO(data)
        state = ParseState.start
        addresses = set()
        for line in body:
            if state is ParseState.start:
                if scre.search(line):
                    state = ParseState.tag_seen
            elif state is ParseState.tag_seen:
                if '@' in line:
                    addresses.add(line.strip())
        return NoTemporaryFailures, set(addresses)
