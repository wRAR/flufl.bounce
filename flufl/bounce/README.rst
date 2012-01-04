======================================
flufl.bounce - Email bounce detectors.
======================================

The ``flufl.bounce`` library provides a set of heuristics and an API for
detecting the original bouncing email addresses from a bounce message.  Many
formats found in the wild are supported, as are VERP_ and RFC 3464 (DSN_).


.. _VERP: http://en.wikipedia.org/wiki/Variable_envelope_return_path
.. _DSN: http://www.faqs.org/rfcs/rfc3464.html


Requirements
============

``flufl.bounce`` requires Python 2.6 or newer, and is compatible with
Python 3.


Documentation
=============

A `simple guide`_ to using the library is available within this package, in
the form of doctests.   The manual is also available online in the Cheeseshop
at:

    http://package.python.org/flufl.bounce


Project details
===============

The project home page is:

    http://launchpad.net/flufl.bounce

You should report bugs at:

    http://bugs.launchpad.net/flufl.bounce

You can download the latest version of the package either from the Cheeseshop:

    http://pypi.python.org/pypi/flufl.bounce

or from the Launchpad page above.  Of course you can also just install it with
``pip`` or ``easy_install`` from the command line::

    % sudo pip flufl.bounce
    % sudo easy_install flufl.bounce

You can grab the latest development copy of the code using Bazaar, from the
Launchpad home page above.  See http://bazaar-vcs.org for details on the
Bazaar distributed revision control system.  If you have Bazaar installed, you
can grab your own branch of the code like this::

     bzr branch lp:flufl.bounce

You may contact the author via barry@python.org.


Copyright
=========

Copyright (C) 2004-2012 Barry A. Warsaw

This file is part of flufl.bounce.

flufl.bounce is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

flufl.bounce is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with flufl.bounce.  If not, see <http://www.gnu.org/licenses/>.


Table of Contents
=================

.. toctree::

    docs/using.rst
    NEWS.rst

.. _`simple guide`: docs/using.html
