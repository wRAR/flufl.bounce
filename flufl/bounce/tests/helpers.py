# Copyright (C) 2011-2012 by Barry A. Warsaw
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

"""Testing helpers."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'initialize_logging',
    ]


import os
import logging



def initialize_logging():
    """Initialize logging for the test suite.

    Normally, an application would itself initialize the flufl.bounce logger,
    but when the test suite is run, it is the controlling application.
    Sometimes when you run the test suite, you want additional debugging, so
    you can set the logging level via an environment variable $FLUFL_LOGGING.
    This variable can be a set of semi-colon separated key-value pairs,
    themselves separated by an equal sign.  The keys and values can be
    anything accepted by `logging.basicConfig()`.
    """
    kwargs = {}
    envar = os.environ.get('FLUFL_LOGGING')
    if envar is not None:
        for key_value in envar.split(';'):
            key, equals, value = key_value.partition('=')
            kwargs[key] = value
    logging.basicConfig(**kwargs)
