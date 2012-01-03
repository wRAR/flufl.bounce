# Copyright (C) 2001-2012 by Barry A. Warsaw
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

"""Recognizes simple heuristically delimited warnings."""

__metaclass__ = type
__all__ = [
    'SimpleWarning',
    ]


from flufl.bounce._detectors.simplematch import SimpleMatch
from flufl.bounce._detectors.simplematch import _c
from flufl.bounce.interfaces import NoPermanentFailures



# This is a list of tuples of the form
#
#     (start cre, end cre, address cre)
#
# where 'cre' means compiled regular expression, start is the line just before
# the bouncing address block, end is the line just after the bouncing address
# block, and address cre is the regexp that will recognize the addresses.  It
# must have a group called 'addr' which will contain exactly and only the
# address that bounced.
PATTERNS = [
    # pop3.pta.lia.net
    (_c('The address to which the message has not yet been delivered is'),
     _c('No action is required on your part'),
     _c(r'\s*(?P<addr>\S+@\S+)\s*')),
    # MessageSwitch
    (_c('Your message to:'),
     _c('This is just a warning, you do not need to take any action'),
     _c(r'\s*(?P<addr>\S+@\S+)\s*')),
    # Symantec_AntiVirus_for_SMTP_Gateways
    (_c('Your message with Subject:'),
     _c('Delivery attempts will continue to be made'),
     _c(r'\s*(?P<addr>\S+@\S+)\s*')),
    # googlemail.com warning
    (_c('Delivery to the following recipient has been delayed'),
     _c('Message will be retried'),
     _c(r'\s*(?P<addr>\S+@\S+)\s*')),
    # Exchange warning message.
    (_c('This is an advisory-only email'),
     _c('has been postponed'),
     _c('"(?P<addr>[^"]+)"')),
    # Next one goes here...
    ]



class SimpleWarning(SimpleMatch):
    """Recognizes simple heuristically delimited warnings."""

    PATTERNS = PATTERNS

    def process(self, msg):
        """See `SimpleMatch`."""
        # Since these are warnings, they're classified as temporary failures.
        # There are no permanent failures.
        (temporary,
         permanent_really_temporary) = super(SimpleWarning, self).process(msg)
        return permanent_really_temporary, NoPermanentFailures
