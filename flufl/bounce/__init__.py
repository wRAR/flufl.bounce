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

"""Package init."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    '__version__',
    'all_failures',
    'scan_message',
    ]


__version__ = '2.1'


from ._scan import all_failures, scan_message
