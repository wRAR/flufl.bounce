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

"""This appears to be the format for Novell GroupWise and NTMail

X-Mailer: Novell GroupWise Internet Agent 5.5.3.1
X-Mailer: NTMail v4.30.0012
X-Mailer: Internet Mail Service (5.5.2653.19)
"""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'GroupWise',
    ]


import re

from email.message import Message
from io import BytesIO
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


acre = re.compile(b'<(?P<addr>[^>]*)>')



def find_textplain(msg):
    if msg.get_content_type() == 'text/plain':
        return msg
    if msg.is_multipart:
        for part in msg.get_payload():
            if not isinstance(part, Message):
                continue
            ret = find_textplain(part)
            if ret:
                return ret
    return None



@implementer(IBounceDetector)
class GroupWise:
    """Parse Novell GroupWise and NTMail bounces."""

    def process(self, msg):
        """See `IBounceDetector`."""
        if msg.get_content_type() != 'multipart/mixed' or not msg['x-mailer']:
            return NoFailures
        addresses = set()
        # Find the first text/plain part in the message.
        text_plain = find_textplain(msg)
        if text_plain is None:
            return NoFailures
        body = BytesIO(text_plain.get_payload(decode=True))
        for line in body:
            mo = acre.search(line)
            if mo:
                addresses.add(mo.group('addr'))
            elif b'@' in line:
                i = line.find(b' ')
                if i == 0:
                    continue
                if i < 0:
                    addresses.add(line)
                else:
                    addresses.add(line[:i])
        return NoTemporaryFailures, set(addresses)
