Email bounce detectors.

..
    This file is part of flufl.bounce.

    flufl.bounce is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    flufl.bounce is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with flufl.bounce.  If not, see <http://www.gnu.org/licenses/>.


============
flufl.bounce
============

The ``flufl.bounce`` library provides a set of heuristics and an API for
detecting the original bouncing email addresses from a bounce message.  Many
formats found in the wild are supported, as are VERP_ and RFC 3464 (DSN_).


.. _VERP: http://en.wikipedia.org/wiki/Variable_envelope_return_path
.. _DSN: http://www.faqs.org/rfcs/rfc3464.html
