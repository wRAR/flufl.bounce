# Copyright (C) 2011 by Barry A. Warsaw
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

"""Top-level bounce detector API."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'scan_message',
    ]


import os
import sys
import logging

from flufl.bounce._interfaces import IBounceDetector, Stop
from pkg_resources import resource_listdir


log = logging.getLogger('flufl.bounce')



def _find_detectors(package):
    # See Mailman 3's scan_module() and find_components()
    missing = object()
    for filename in resource_listdir(package, ''):
        basename, extension = os.path.splitext(filename)
        if extension != '.py':
            continue
        module_name = '{0}.{1}'.format(package, basename)
        __import__(module_name, fromlist='*')
        module = sys.modules[module_name]
        for name in getattr(module, '__all__', []):
            component = getattr(module, name, missing)
            if component is missing:
                log.error('skipping missing __all__ entry: {0}'.format(name))
            if IBounceDetector.implementedBy(component):
                yield component



def scan_message(msg):
    """Detect the set of bouncing original recipients.

    :param msg: The bounce message.
    :type msg: `email.message.Message`
    :return: The set of detected original recipients.
    :rtype: set of strings
    """
    fatal_addresses = set()
    package = 'flufl.bounce._detectors'
    for detector_class in _find_detectors(package):
        addresses = detector_class().process(msg)
        if addresses is Stop:
            return Stop
        fatal_addresses.update(addresses)
    return fatal_addresses
