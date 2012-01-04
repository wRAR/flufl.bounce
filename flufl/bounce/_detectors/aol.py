# Copyright (C) 2009-2012 by Barry A. Warsaw
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

"""Recognizes a class of messages from AOL that report only Screen Name."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'AOL',
    ]


import re

from email.utils import parseaddr
from zope.interface import implementer

from flufl.bounce.interfaces import (
    IBounceDetector, NoFailures, NoTemporaryFailures)


scre = re.compile(b'mail to the following recipients could not be delivered')



@implementer(IBounceDetector)
class AOL:
    """Recognizes a class of messages from AOL that report only Screen Name."""

    def process(self, msg):
        if msg.get_content_type() != 'text/plain':
            return NoFailures
        if not parseaddr(msg.get('from', ''))[1].lower().endswith('@aol.com'):
            return NoFailures
        addresses = set()
        found = False
        for line in msg.get_payload(decode=True).splitlines():
            if scre.search(line):
                found = True
                continue
            if found:
                local = line.strip()
                if local:
                    if re.search(b'\\s', local):
                        break
                    if b'@' in local:
                        addresses.add(local)
                    else:
                        addresses.add(local + b'@aol.com')
        return NoTemporaryFailures, addresses
