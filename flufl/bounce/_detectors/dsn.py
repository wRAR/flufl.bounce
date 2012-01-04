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

"""Parse RFC 3464 (i.e. DSN) bounce formats.

RFC 3464 obsoletes 1894 which was the old DSN standard.  This module has not
been audited for differences between the two.
"""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'DSN',
    ]


from email.iterators import typed_subpart_iterator
from email.utils import parseaddr
from zope.interface import implementer

from flufl.bounce.interfaces import IBounceDetector



@implementer(IBounceDetector)
class DSN:
    """Parse RFC 3464 (i.e. DSN) bounce formats."""

    def process(self, msg):
        """See `IBounceDetector`."""
        # Iterate over each message/delivery-status subpart.
        failed_addresses = []
        delayed_addresses = []
        for part in typed_subpart_iterator(msg, 'message', 'delivery-status'):
            if not part.is_multipart():
                # Huh?
                continue
            # Each message/delivery-status contains a list of Message objects
            # which are the header blocks.  Iterate over those too.
            for msgblock in part.get_payload():
                address_set = None
                # We try to dig out the Original-Recipient (which is optional)
                # and Final-Recipient (which is mandatory, but may not exactly
                # match an address on our list).  Some MTA's also use
                # X-Actual-Recipient as a synonym for Original-Recipient, but
                # some apparently use that for other purposes :(
                #
                # Also grok out Action so we can do something with that too.
                action = msgblock.get('action', '').lower()
                # Some MTAs have been observed that put comments on the action.
                if action.startswith('delayed'):
                    address_set = delayed_addresses
                elif action.startswith('fail'):
                    address_set = failed_addresses
                else:
                    # Some non-permanent failure, so ignore this block.
                    continue
                params = []
                foundp = False
                for header in ('original-recipient', 'final-recipient'):
                    for k, v in msgblock.get_params([], header):
                        if k.lower() == 'rfc822':
                            foundp = True
                        else:
                            params.append(k)
                    if foundp:
                        # Note that params should already be unquoted.
                        address_set.extend(params)
                        break
                    else:
                        # MAS: This is a kludge, but
                        # SMTP-GATEWAY01.intra.home.dk has a final-recipient
                        # with an angle-addr and no address-type parameter at
                        # all. Non-compliant, but ...
                        for param in params:
                            if param.startswith('<') and param.endswith('>'):
                                address_set.append(param[1:-1])
        # There may be Nones in the current set of failures, so filter those
        # out of both sets.  Also, for Python 3 compatibility, the API
        # requires byte addresses.
        return (
            # First, the delayed, or temporary failures.
            set(parseaddr(address)[1].encode('us-ascii') 
                for address in delayed_addresses
                if address is not None),
            # And now the failed or permanent failures.
            set(parseaddr(address)[1].encode('us-ascii') 
                for address in failed_addresses
                if address is not None)
            )
